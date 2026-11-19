"""The Impossible Lab #14 - a scoop of ice cream on Mercury's night side (E13 reel 1: consequence in motion at t = 0).
Units: arbitrary (scoop radius 0.42). Hook set (origin): EARTH kitchen scoop (x = -0.9, spoon sinks in, lifts a ball) vs
MERCURY NIGHT scoop on regolith (x = +0.9, spoon strikes at t = 0.12 s, cracks + glassy shards fly). Line 2 Mercury
night landscape (x = 36, -180 °C), line 3 open freezer (x = 12, -18 °C, spoon scoops), line 4 macro (x = 24): ice
crystals drifting in amber syrup; temperature counts -18 -> -30 °C, syrup turns to blue glass, cracks appear.
Line 5: close-up on the Mercury scoop, two more strikes ("It chips."). Lines 6-7: landscape, day counter 1 -> 88,
sunrise, scoop melts and scorches. Last ~1 s: back to the hook framing (loop).
Text objects updated by a frame_change_pre handler.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(13)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 6; S.cycles.glossy_bounces = 2; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 2; S.cycles.transparent_max_bounces = 8
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"

from timeline import LINES, CARD_START
L = {l["i"]: l for l in LINES}
V = Vector

def mat(name, base=(0.5, 0.5, 0.5), rough=0.5, metal=0.0, emit=None, estr=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    return m
def liquid(name, tint, gloss_col, mixf=0.22):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (*tint, 1)
    gl = nt.nodes.new("ShaderNodeBsdfPrincipled"); gl.inputs["Base Color"].default_value = (*gloss_col, 1)
    gl.inputs["Roughness"].default_value = 0.08
    fr = nt.nodes.new("ShaderNodeLayerWeight"); fr.inputs["Blend"].default_value = 0.35
    mx = nt.nodes.new("ShaderNodeMixShader")
    mth = nt.nodes.new("ShaderNodeMath"); mth.operation = "ADD"; mth.inputs[1].default_value = mixf
    nt.links.new(fr.outputs["Facing"], mth.inputs[0])
    clamp = nt.nodes.new("ShaderNodeClamp"); nt.links.new(mth.outputs[0], clamp.inputs[0])
    nt.links.new(clamp.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs[0])
    return m
def tiles(name, c_tile, c_grout, scale):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.25
    br = nt.nodes.new("ShaderNodeTexBrick"); br.offset = 0.0
    br.inputs["Color1"].default_value = (*c_tile, 1); br.inputs["Color2"].default_value = (*[c * 0.93 for c in c_tile], 1)
    br.inputs["Mortar"].default_value = (*c_grout, 1); br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = 0.02; br.inputs["Brick Width"].default_value = 0.5; br.inputs["Row Height"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return m
def noise_mat(name, c1, c2, scale, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 5
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*c1, 1); rp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    return m

def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box", parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; bpy.ops.object.transform_apply(scale=True); return link(o, m, parent)
def cyl_between(a, b, r, m, parent=None, name="limb", caps=True, verts=16):
    a, b = V(a), V(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.name = name
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    bpy.ops.object.shade_smooth(); link(o, m, parent)
    if caps:
        for p in (a, b):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=r, location=p)
            e = bpy.context.object; bpy.ops.object.shade_smooth(); link(e, m, parent)
    return o
def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); e.location = loc; S.collection.objects.link(e)
    if parent: e.parent = parent
    return e
def text(body, loc, rot, size, m, align="CENTER", parent=None):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object
    t.data.body = body; t.data.size = size; t.data.extrude = 0.005; t.data.align_x = align; t.data.align_y = "CENTER"
    return link(t, m, parent)
def sphere(loc, r, m, name="sph", parent=None, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def vis(o, on, f, base=(1, 1, 1)):
    o.scale = base if on else (0.0001,) * 3; o.keyframe_insert("scale", frame=f)
def noshadow(o):
    o.visible_shadow = False
    return o
TR = (math.radians(90), 0, 0)

def wave_mat(name, cols, scale, rough=0.7, distort=4.0, estr=0.0):
    """Banded planet: wave texture along z -> colour ramp."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = scale; wv.inputs["Distortion"].default_value = distort
    wv.inputs["Detail"].default_value = 3
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*cols[0], 1); el[1].position = 1.0; el[1].color = (*cols[-1], 1)
    for i, c in enumerate(cols[1:-1], 1):
        e = el.new(i / (len(cols) - 1)); e.color = (*c, 1)
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
    nt.links.new(wv.outputs["Color"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    if estr:
        nt.links.new(rp.outputs[0], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = estr
    return m


# ================= episode 14: ice cream on Mercury's night side =================
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def kf_color(m, f, col):
    i = bsdf(m).inputs["Base Color"]; i.default_value = (*col, 1); i.keyframe_insert("default_value", frame=f)
def kf_input(m, name, f, v):
    i = bsdf(m).inputs[name]; i.default_value = v; i.keyframe_insert("default_value", frame=f)
def lerp3(a, b, u): return tuple(x + (y - x) * u for x, y in zip(a, b))

M_WOOD = noise_mat("wood", (0.42, 0.24, 0.12), (0.58, 0.36, 0.18), 6.0, 0.5)
M_WALL = mat("wall", (0.85, 0.62, 0.42), 0.8)
M_REG = noise_mat("reg", (0.22, 0.22, 0.24), (0.48, 0.47, 0.46), 5.0)
M_REG2 = noise_mat("reg2", (0.16, 0.16, 0.18), (0.38, 0.37, 0.36), 3.0)
M_BOWL = mat("bowl", (0.92, 0.92, 0.95), 0.25)
M_BOWLM = mat("bowlm", (0.20, 0.42, 0.85), 0.25)
M_STEEL = mat("steel", (0.80, 0.82, 0.85), 0.22, 1.0)
CREAM = (0.96, 0.86, 0.66)
M_CREAM = mat("cream", CREAM, 0.65)                       # soft Earth scoop
M_GLASSY = mat("glassy", (0.78, 0.86, 0.95), 0.08, 0.0)   # Mercury scoop: frosty, glossy
bsdf(M_GLASSY).inputs["Coat Weight"].default_value = 0.8
M_SHARD = mat("shard", (0.82, 0.90, 1.0), 0.05)
bsdf(M_SHARD).inputs["Coat Weight"].default_value = 1.0
M_CRACK = mat("crack", (0.02, 0.03, 0.06), 0.6)
M_MELT = mat("melt", CREAM, 0.3)                          # landscape scoop: frost -> melt -> scorch
M_SYRUP = mat("syrup", (0.50, 0.20, 0.03), 0.05)
M_XTAL = mat("xtal", (0.92, 0.96, 1.0), 0.15, 0, (0.8, 0.9, 1.0), 0.6)
M_FRZ = mat("frz", (0.90, 0.94, 0.98), 0.45)
M_FRZIN = mat("frzin", (0.75, 0.86, 0.98), 0.5, 0, (0.55, 0.75, 1.0), 0.35)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.62, 0.15), 5.0)
M_RED = mat("red", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 3.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_DIV = mat("div", (1, 1, 1), 0.4, 0, (1, 1, 1), 2.0)
M_STAR = mat("star", (1, 1, 1), 0.5, 0, (1, 1, 1), 6.0)
M_SUN = mat("sunm", (1, 0.9, 0.7), 0.5, 0, (1.0, 0.85, 0.55), 0.0)
M_CRATER = mat("crater", (0.10, 0.10, 0.11), 0.95)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.004, 0.005, 0.012, 1); WBG.inputs[1].default_value = 1.0

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_SUN = t7 + 0.95           # "Then it bakes."
def ramp(t, a, b, v0, v1):
    return v0 + (v1 - v0) * (1 - (1 - max(0.0, min(1.0, (t - a) / (b - a)))) ** 3)

# ---------- reusable props ----------
BOWL_H = 0.32; SC_R = 0.42
def bowl_scoop(name, x, y, z, scoop_m, bowl_m=M_BOWL):
    root = empty(name, (x, y, z))
    bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=0.30, radius2=0.52, depth=BOWL_H, location=(0, 0, BOWL_H / 2))
    b = bpy.context.object; bpy.ops.object.shade_smooth(); link(b, bowl_m, root)
    sc = sphere((0, 0, BOWL_H + SC_R * 0.72), SC_R, scoop_m, "scoop", root, 32)
    # lumpy top: a few small blobs
    rnd = random.Random(hash(name) % 1000)
    for k in range(5):
        a = rnd.uniform(0, 6.28); r = SC_R * 0.85
        sphere((r * 0.55 * math.cos(a), r * 0.55 * math.sin(a), BOWL_H + SC_R * 0.72 + r * 0.55), SC_R * 0.32, scoop_m, "lump", root, 14)
    return root, sc
def spoon(name):
    e = empty(name)
    bw = sphere((0, 0, 0.15), 1.0, M_STEEL, "spbowl", e, 18); bw.scale = (0.11, 0.035, 0.16)
    cyl_between((0, 0, 0.27), (0, 0, 1.25), 0.022, M_STEEL, e, "sphandle", caps=True, verts=10)
    e.rotation_mode = "QUATERNION"
    return e
def aim(sp, tip, d, f):
    sp.location = V(tip); sp.rotation_quaternion = V(d).normalized().to_track_quat("Z", "Y")
    sp.keyframe_insert("location", frame=f); sp.keyframe_insert("rotation_quaternion", frame=f)
def label(body, loc, size, m):
    o = text(body, loc, TR, size, m); noshadow(o); o.visible_glossy = False; return o
def stars(x0, x1, y, z0, z1, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        sphere((rnd.uniform(x0, x1), y + rnd.uniform(0, 4), rnd.uniform(z0, z1)), rnd.uniform(0.02, 0.05), M_STAR, "star", None, 6)

# ---------- HOOK set: EARTH (left, kitchen) vs MERCURY NIGHT (right, regolith + stars) ----------
LX, RX = -0.9, 0.9
box((-1.6, 0.6, -0.25), (3.2, 3.0, 0.5), M_WOOD, "counter")
box((-1.6, 2.2, 1.6), (3.2, 0.1, 4.2), M_WALL, "wall")
box((1.8, 3.0, -0.25), (3.6, 8.0, 0.5), M_REG, "regpad")
for k in range(6):
    sphere((0.6 + k * 0.6, 4 + (k % 3) * 1.5, -0.5), 0.9 + 0.3 * (k % 2), M_REG2, "hill", None, 16).scale = (1.6, 1.0, 0.5)
stars(0.1, 4.0, 7.0, 0.4, 6.5, 120, 3)
box((0.0, 0.7, 1.6), (0.025, 3.0, 4.2), M_DIV, "divider")
E_ROOT, E_SC = bowl_scoop("bowlE", LX, 0, 0, M_CREAM)
M_ROOT, M_SC = bowl_scoop("bowlM", RX, 0, 0, M_GLASSY, M_BOWLM)
label("EARTH", (LX, 0.3, 1.95), 0.17, M_LBLB); label("-18 °C", (LX, 0.3, 1.62), 0.25, M_LBLB)
LBL_MN = label("MERCURY NIGHT", (RX, 0.3, 1.95), 0.13, M_LBL); label("-180 °C", (RX, 0.3, 1.62), 0.25, M_RED)
SP_E = spoon("spE"); SP_M = spoon("spM")
TOP_E = V((LX, 0, BOWL_H + SC_R * 1.45)); TOP_M = V((RX, 0, BOWL_H + SC_R * 1.45))
# little scooped ball that rides out on the Earth spoon
BALL_E = sphere((0, 0, 0.12), 0.11, M_CREAM, "ballE", SP_E, 14)
# cracks on the Mercury scoop: zigzag lines on its front surface, parented to the bowl
CRACKS = []
rnd = random.Random(21)
C0 = V((0, 0, BOWL_H + SC_R * 0.72)); RR = SC_R * 1.01
def sp(pol, phi): return C0 + RR * V((math.sin(pol) * math.sin(phi), -math.sin(pol) * math.cos(phi), math.cos(pol)))
for phi0 in (-0.55, 0.05, 0.6):
    pts = []; phi = phi0
    for k in range(6):
        pol = 0.30 + k * 0.22; phi += rnd.uniform(-0.18, 0.18); pts.append(sp(pol, phi))
    for p, q in zip(pts, pts[1:]):
        CRACKS.append(cyl_between(p, q, 0.011, M_CRACK, M_ROOT, "crack", caps=False, verts=6))
    for p in pts: CRACKS.append(sphere(p, 0.011, M_CRACK, "cj", M_ROOT, 6))
# shards
SHARDS = []
for k in range(16):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rnd.uniform(0.035, 0.075), location=(0, 0, 0))
    o = bpy.context.object; link(o, M_SHARD); o.scale = (rnd.uniform(0.6, 1.4), rnd.uniform(0.5, 1.0), rnd.uniform(0.4, 1.2))
    bpy.ops.object.transform_apply(scale=True)
    v = V((rnd.uniform(-1.6, 1.9), rnd.uniform(-1.6, -0.2), rnd.uniform(1.4, 3.2)))
    SHARDS.append((o, v, V((rnd.uniform(-9, 9), rnd.uniform(-9, 9), rnd.uniform(-9, 9)))))

# ---------- FREEZER set (line 3) ----------
FX = 12.0
FZ = 0.5
box((FX, 0.9, FZ - 0.08), (2.4, 1.8, 0.16), M_FRZ, "frzbot")
box((FX, 0.9, FZ + 2.0), (2.4, 1.8, 0.16), M_FRZ, "frztop")
box((FX - 1.15, 0.9, FZ + 0.96), (0.1, 1.8, 2.1), M_FRZ, "frzl"); box((FX + 1.15, 0.9, FZ + 0.96), (0.1, 1.8, 2.1), M_FRZ, "frzr")
box((FX, 1.75, FZ + 0.96), (2.3, 0.1, 2.1), M_FRZIN, "frzback")
box((FX, 0.9, -0.3), (6, 6, 0.6), M_WOOD, "frzfloor")
box((FX, 4.0, 2.0), (8, 0.1, 6), M_WALL, "frzwall")
F_ROOT, F_SC = bowl_scoop("bowlF", FX, 0.6, FZ, M_CREAM)
SP_F = spoon("spF"); BALL_F = sphere((0, 0, 0.12), 0.11, M_CREAM, "ballF", SP_F, 14)
TOP_F = V((FX, 0.6, FZ + BOWL_H + SC_R * 1.45))
fl = bpy.data.objects.new("frzlight", bpy.data.lights.new("frzlight", "AREA")); fl.data.energy = 260; fl.data.size = 1.6
fl.data.color = (0.75, 0.88, 1.0); fl.location = (FX, 0.9, FZ + 1.85); S.collection.objects.link(fl)

# ---------- MACRO set (line 4): ice crystals in syrup -> glass ----------
GX = 24.0
SLAB = box((GX, 0.2, 1.3), (2.6, 0.4, 2.2), M_SYRUP, "slab")
XT = []
for k in range(34):
    s = rnd.uniform(0.10, 0.22)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=s, location=(GX + rnd.uniform(-1.2, 1.2), -0.02, 1.3 + rnd.uniform(-0.95, 0.95)))
    o = bpy.context.object; link(o, M_XTAL); o.scale = (1, 0.5, rnd.uniform(0.7, 1.3)); o.rotation_euler = (0, rnd.uniform(0, 3), 0)
    XT.append((o, V(o.location), rnd.uniform(0, 6.28)))
GCRACK = []
for k in range(7):
    o = box((GX + rnd.uniform(-1.0, 1.0), -0.03, 1.3 + rnd.uniform(-0.75, 0.75)), (0.04, 0.08, rnd.uniform(0.5, 1.0)), M_CRACK, "gcrack")
    o.rotation_euler = (0, rnd.uniform(-1.2, 1.2), 0); GCRACK.append(o)
label("INSIDE THE SCOOP: ICE + SUGAR SYRUP", (GX, -0.2, 3.05), 0.12, M_WHITE)
MAC_T = label("-18 °C", (GX, -0.2, 2.72), 0.30, M_LBLB)
ml = bpy.data.objects.new("macl", bpy.data.lights.new("macl", "AREA")); ml.data.energy = 900; ml.data.size = 5
ml.location = (GX, -5, 3.5); ml.rotation_euler = (math.radians(60), 0, 0); S.collection.objects.link(ml)

# ---------- MERCURY landscape (lines 2, 6, 7) ----------
WX = 36.0
box((WX, 20, -0.3), (60, 60, 0.6), M_REG, "plain")
for (cx, cy, r) in [(WX - 2.2, 3.0, 0.9), (WX + 2.6, 6.0, 1.4), (WX - 4.0, 10, 2.0), (WX + 1.0, 14, 2.6), (WX + 6, 9, 1.0)]:
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.16, location=(cx, cy, 0.0)); o = bpy.context.object
    o.scale = (1, 1, 0.35); link(o, M_REG2)
    bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.9, depth=0.02, location=(cx, cy, 0.005)); link(bpy.context.object, M_CRATER)
for k in range(9):
    sphere((WX - 16 + k * 4, 34 + (k % 3) * 3, -1.0), 3.0 + (k % 3), M_REG2, "ridge", None, 16).scale = (1.8, 1.0, 0.45)
stars(WX - 14, WX + 14, 42, 1.0, 16, 220, 7)
W_ROOT, W_SC = bowl_scoop("bowlW", WX, 0, 0, M_MELT, M_BOWLM)
SUN = sphere((WX + 8.0, 60, -9.0), 4.5, M_SUN, "sunball", None, 32)
W_T1 = label("MERCURY · NIGHT SIDE", (WX, 0.3, 2.2), 0.15, M_LBL)
W_T2 = label("-180 °C", (WX, 0.3, 1.85), 0.27, M_RED)
nl = bpy.data.objects.new("nightl", bpy.data.lights.new("nightl", "AREA")); nl.data.energy = 500; nl.data.size = 8
nl.data.color = (0.55, 0.65, 1.0); nl.location = (WX - 2, -6, 5); nl.rotation_euler = (math.radians(55), 0, math.radians(-15)); S.collection.objects.link(nl)
sunl = bpy.data.objects.new("sunl", bpy.data.lights.new("sunl", "SUN")); sunl.data.color = (1.0, 0.85, 0.6); sunl.data.angle = math.radians(4)
sunl.rotation_euler = (math.radians(100), 0, math.radians(175)); S.collection.objects.link(sunl)

# ---------- hook lighting ----------
kl = bpy.data.objects.new("kitchen", bpy.data.lights.new("kitchen", "AREA")); kl.data.energy = 380; kl.data.size = 3
kl.data.color = (1.0, 0.85, 0.65); kl.location = (LX - 0.8, -3.0, 3.2); kl.rotation_euler = (math.radians(50), 0, math.radians(-15)); S.collection.objects.link(kl)
ml2 = bpy.data.objects.new("mercl", bpy.data.lights.new("mercl", "AREA")); ml2.data.energy = 330; ml2.data.size = 3
ml2.data.color = (0.6, 0.72, 1.0); ml2.location = (RX + 0.9, -3.0, 3.2); ml2.rotation_euler = (math.radians(50), 0, math.radians(15)); S.collection.objects.link(ml2)

# ---------- text handler ----------
def macro_temp(t):
    return round(ramp(t, t4 + 0.1, t4 + 1.0, -18, -30)) if t < t4 + 1.25 else -30
def handler(scene, *a):
    t = scene.frame_current / FPS
    MAC_T.data.body = f"{macro_temp(t)} °C" if t < t4 + 1.15 else "-30 °C: GLASS"
    if t < t6:
        W_T1.data.body = ""; W_T2.data.body = ""
    elif t < T_SUN:
        day = int(round(ramp(t, t6 + 0.1, T_SUN - 0.1, 1, 88)))
        W_T1.data.body = "NIGHT LASTS ≈88 EARTH DAYS"; W_T2.data.body = f"DAY {day}"
    else:
        W_T1.data.body = "SUNRISE"; W_T2.data.body = "430 °C"
bpy.app.handlers.frame_change_pre.append(handler)

# ---------- impacts on the Mercury hook scoop ----------
IMPACTS = [0.12, t5 + 0.25, t5 + 1.15]
G = 9.0
def last_impact(t):
    if t >= T_LOOP: return None
    p = [i for i in IMPACTS if i <= t]
    return p[-1] if p else None

E_DIR = V((-1.0, -0.35, 0.75)); M_DIR = V((1.0, -0.35, 0.75))
for f in range(0, N + 1):
    t = f / FPS
    # --- Earth spoon: sinks in (0-0.6), lifts out with a ball (1.1-1.8); repeated in the loop ---
    tl = t - T_LOOP if t >= T_LOOP else t
    dip = smooth(tl / 0.55) - smooth((tl - 1.05) / 0.6)
    tip = TOP_E + V((0.02, 0, 0.22 - 0.50 * dip))
    lift = smooth((tl - 1.05) / 0.6)
    aim(SP_E, tip + V((0, 0, 0.10 * lift)), E_DIR, f)
    BALL_E.scale = (1, 1, 1) if (tl > 1.0 and t < t2 + 0.2) or (t >= T_LOOP and tl > 1.0) else (0.0001,) * 3
    BALL_E.keyframe_insert("scale", frame=f)
    E_SC.scale = (1 + 0.04 * dip, 1 + 0.04 * dip, 1 - 0.07 * dip); E_SC.keyframe_insert("scale", frame=f)
    # --- Mercury spoon: strikes and bounces back ---
    li = last_impact(t)
    if t >= T_LOOP:
        h = 0.28 - 0.20 * smooth((t - T_LOOP) / 0.6); jolt = 0.0
    elif li is None:
        h = 0.10 * (1 - t / 0.12)
        jolt = 0.0
    else:
        s = t - li
        nxt = [i for i in IMPACTS if i > t]
        h = 0.36 * math.sin(min(math.pi / 2, s * 5.5)) if s < 0.29 else 0.36
        if s >= 0.57:
            # rest high, then wind up before the next strike
            if nxt and nxt[0] - t < 0.3: h = 0.36 * (nxt[0] - t) / 0.3
            else: h = 0.36
        jolt = 0.04 * math.exp(-s * 12) * math.sin(s * 70)
    aim(SP_M, TOP_M + V((-0.02, 0, h)), M_DIR, f)
    M_ROOT.location = (RX + jolt, 0, 0); M_ROOT.keyframe_insert("location", frame=f)
    for o in CRACKS:
        vis(o, li is not None, f)
    # shards fly from the latest impact (one burst per impact; the 2nd impact is a smaller 'tink')
    for k, (o, v, w) in enumerate(SHARDS):
        on = li is not None and not (li == IMPACTS[1] and k % 3)
        if on:
            s = t - li; p0 = TOP_M + V((0.05, -0.12, -0.05))
            p = p0 + v * s * 0.55 + V((0, 0, -0.5 * G * 0.3 * s * s))
            if p.z < 0.03 + 0.0: p.z = 0.03
            o.location = p; o.rotation_euler = tuple(x * min(s, 0.8) for x in w)
            o.scale = (1, 1, 1)
        else:
            o.scale = (0.0001,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f); o.keyframe_insert("scale", frame=f)
    # --- freezer spoon (line 3) ---
    s3 = t - t3
    dip = smooth((s3 - 0.1) / 0.5) - smooth((s3 - 0.95) / 0.5)
    lift = smooth((s3 - 0.95) / 0.5)
    aim(SP_F, TOP_F + V((0.02, 0, 0.30 - 0.42 * dip + 0.35 * lift)), E_DIR, f)
    BALL_F.scale = (1, 1, 1) if s3 > 0.9 else (0.0001,) * 3; BALL_F.keyframe_insert("scale", frame=f)
    F_SC.scale = (1 + 0.04 * dip, 1 + 0.04 * dip, 1 - 0.07 * dip); F_SC.keyframe_insert("scale", frame=f)
    # --- macro: crystals drift in liquid syrup, freeze in glass ---
    g = smooth((t - (t4 + 1.15)) / 0.8)
    for (o, p0, ph) in XT:
        amp = 0.06 * (1 - g)
        o.location = p0 + V((amp * math.sin(t * 2.3 + ph), 0, amp * math.cos(t * 1.9 + ph)))
        o.keyframe_insert("location", frame=f)
    for o in GCRACK:
        vis(o, t >= t4 + 1.9, f)
    # --- landscape scoop: melts and scorches after sunrise ---
    m = smooth((t - T_SUN - 0.15) / 0.75) if t < T_LOOP else 0.0
    W_SC.scale = (1 + 0.35 * m, 1 + 0.35 * m, 1 - 0.62 * m); W_SC.keyframe_insert("scale", frame=f)
    W_SC.location = (0, 0, BOWL_H + SC_R * 0.72 - 0.20 * m); W_SC.keyframe_insert("location", frame=f)
# lumps on the landscape scoop sink with it
for o in W_ROOT.children:
    if o.name.startswith("lump"):
        z0 = o.location.z
        for f in range(0, N + 1):
            t = f / FPS; m = smooth((t - T_SUN - 0.15) / 0.75) if t < T_LOOP else 0.0
            o.location.z = z0 - 0.42 * m; o.scale = (1 - 0.6 * m,) * 3
            o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)

# keyframed materials (sparse keys are enough)
def mkeys(fn, times):
    for tt in times: fn(int(round(tt * FPS)), tt)
def syrup_at(f, tt):
    g = smooth((tt - (t4 + 1.15)) / 0.8)
    kf_color(M_SYRUP, f, lerp3((0.50, 0.20, 0.03), (0.45, 0.62, 0.85), g)); kf_input(M_SYRUP, "Roughness", f, 0.05)
mkeys(syrup_at, [0, t4 + 1.15, t4 + 1.55, t4 + 1.95])
def melt_at(f, tt):
    m = smooth((tt - T_SUN - 0.15) / 0.75) if tt < T_LOOP else 0.0
    sc = smooth((tt - T_SUN - 0.6) / 0.6) if tt < T_LOOP else 0.0
    col = lerp3(lerp3((0.80, 0.88, 0.98), CREAM, m), (0.25, 0.12, 0.05), sc)
    kf_color(M_MELT, f, col); kf_input(M_MELT, "Roughness", f, 0.12 + 0.1 * m)
mkeys(melt_at, [0, T_SUN, T_SUN + 0.3, T_SUN + 0.6, T_SUN + 0.9, T_SUN + 1.2, T_LOOP - 0.05, T_LOOP])
def sun_at(f, tt):
    u = smooth((tt - T_SUN + 0.15) / 0.7) if tt < T_LOOP else 0.0
    SUN.location = (WX + 8.0, 60, -9.0 + 10.0 * u); SUN.keyframe_insert("location", frame=f)
    kf_input(M_SUN, "Emission Strength", f, 18.0 * u)
    sunl.data.energy = 9.0 * u; sunl.data.keyframe_insert("energy", frame=f)
    nl.data.energy = 500 * (1 - 0.6 * u); nl.data.keyframe_insert("energy", frame=f)
mkeys(sun_at, [0, T_SUN - 0.2, T_SUN, T_SUN + 0.2, T_SUN + 0.4, T_SUN + 0.6, T_LOOP - 0.05, T_LOOP])
for fc in [M_SUN.node_tree.animation_data, sunl.data.animation_data, nl.data.animation_data]:
    pass

for f in range(0, N + 1):
    t = f / FPS; vis(LBL_MN, not (t5 - 0.05 <= t < t6 - 0.05), f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -7.6, 1.55), (0.0, 0, 1.0), (0.0, -7.2, 1.5), (0.0, 0, 1.0))
LAND = fixed((WX + 0.2, -6.6, 1.9), (WX, 0, 1.25), (WX + 0.1, -5.8, 1.7), (WX, 0, 1.15))
SEG = [
    (0.0, t2 - 0.05, HOOK, 30, 31),
    (t2 - 0.05, t3 - 0.05, LAND, 30, 31),
    (t3 - 0.05, t4 - 0.05, fixed((FX, -6.8, 1.75), (FX, 0.6, 1.65), (FX, -6.2, 1.75), (FX, 0.6, 1.62)), 30, 31),
    (t4 - 0.05, t5 - 0.05, fixed((GX, -9.0, 1.75), (GX, 0, 1.64), (GX, -8.5, 1.75), (GX, 0, 1.64)), 30, 31),
    (t5 - 0.05, t6 - 0.05, fixed((RX - 0.1, -5.2, 1.15), (RX, 0, 0.95), (RX - 0.1, -4.8, 1.1), (RX, 0, 0.95)), 30, 31),
    (t6 - 0.05, T_LOOP, fixed((WX + 0.2, -7.4, 1.75), (WX, 0, 1.05), (WX + 0.1, -6.4, 1.6), (WX, 0, 0.95)), 30, 31),
    (T_LOOP, DUR + 0.01, HOOK, 30, 31),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "impacts": IMPACTS,
           "earth_dip": 0.0, "freezer_dip": t3 + 0.1, "glass": t4 + 1.15, "cracks": t4 + 1.9, "sunrise": T_SUN},
          open("/home/claude/reel/beats.json", "w"), indent=1)

args = [a for a in (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]) if a != "--force"]
if args and ("," in args[0] or len(args) == 1): frames = [int(x) for x in args[0].split(",") if x]
else:
    f_a, f_b = (int(args[0]), int(args[1])) if len(args) >= 2 else (0, N - 1)
    step = int(args[2]) if len(args) >= 3 else 1
    frames = range(f_a, f_b + 1, step)
for f in frames:
    out = f"/home/claude/reel/frames/{f:04d}.png"
    if os.path.exists(out) and "--force" not in sys.argv: continue
    S.frame_set(f); S.render.filepath = out
    t0 = time.time(); bpy.ops.render.render(write_still=True)
    print(f"frame {f} {time.time() - t0:.1f}s", flush=True)
