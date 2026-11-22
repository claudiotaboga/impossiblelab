"""The Impossible Lab #17 - popcorn on Mars (E13 opening: EARTH vs MARS pans pop at 0.08 s, Mars flakes 2x volume).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(17)
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



# ================= episode 17: popcorn on Mars =================
# Hook (x = 0): EARTH pan (left) vs MARS pan (right) on one counter; kernels start popping at 0.08 s and the Mars
# flakes come out visibly bigger (1.26x linear = 2x volume). Line 2: Mars surface set (x = 30), pan on a stove on red
# ground, camera pulls back. Line 3: close-up (x = 60): air dots over the pan, all but one vanish. Line 4: pressure
# gauge climbs 0 -> 9 ATM while the big kernel swells and shakes; it bursts at ~8.0 s. Line 5: an EARTH-size flake
# appears for comparison, then the Mars flake puffs to 2x volume. Lines 6-7: back to the hook pans: Earth duds ringed
# (5) vs Mars (1). Last ~1 s: hook framing (loop).
import bmesh
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def kf_input(m, name, f, v):
    i = bsdf(m).inputs[name]; i.default_value = v; i.keyframe_insert("default_value", frame=f)
def label(body, loc, size, m, align="CENTER", rot=TR):
    o = text(body, loc, rot, size, m, align); noshadow(o); o.visible_glossy = False; return o
def cyl(loc, r, d, m, name="cyl", rot=(0, 0, 0), verts=32, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def ramp(t, a, b, v0, v1):
    return v0 + (v1 - v0) * smooth((t - a) / (b - a))

M_COUNTER = noise_mat("counter", (0.78, 0.76, 0.72), (0.88, 0.86, 0.82), 9.0, 0.35)
M_WALLE = tiles("wallE", (0.20, 0.30, 0.40), (0.12, 0.16, 0.20), 4.0)
M_WALLM = tiles("wallM", (0.45, 0.20, 0.10), (0.22, 0.10, 0.06), 4.0)
M_DARK = mat("dark", (0.04, 0.04, 0.05), 0.5)
M_STEEL = mat("steel", (0.75, 0.76, 0.78), 0.22, 1.0)
M_FLAME = mat("flame", (0.2, 0.4, 1.0), 0.5, 0, (0.25, 0.5, 1.0), 6.0)
M_POP = mat("pop", (0.97, 0.93, 0.80), 0.85)
M_HULL = mat("hull", (0.80, 0.45, 0.10), 0.3)
M_KERN = mat("kern", (0.92, 0.58, 0.12), 0.22)
M_DUD = mat("dud", (0.55, 0.30, 0.08), 0.3)
M_GROUND = noise_mat("ground", (0.42, 0.16, 0.07), (0.70, 0.36, 0.17), 3.0, 0.95)
M_ROCK = noise_mat("rock", (0.22, 0.10, 0.06), (0.40, 0.20, 0.12), 6.0, 0.9)
M_SKY = mat("sky", (0.8, 0.55, 0.4), 0.5, 0, (0.85, 0.58, 0.42), 1.0)
M_AIR = mat("air", (0.6, 0.85, 1.0), 0.4, 0, (0.55, 0.85, 1.0), 3.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_LBL = mat("lbl", (1.0, 0.45, 0.2), 0.4, 0, (1.0, 0.42, 0.15), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_RED = mat("red", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 4.0)
M_GREEN = mat("grn", (0.3, 1.0, 0.5), 0.4, 0, (0.3, 1.0, 0.5), 3.0)
M_FACE = mat("face", (0.95, 0.95, 0.92), 0.4)
M_GHOST = mat("ghost", (0.6, 0.8, 1.0), 0.6, 0, (0.45, 0.7, 1.0), 0.6)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.6
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.02, 0.025, 0.04, 1); WBG.inputs[1].default_value = 1.0

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_POP0 = 0.08
T_THIN = t3 + 0.75                 # all but one air dot vanish
T_G0, T_G1 = t4 + 0.25, t4 + 2.0   # gauge climbs 0 -> 9 atm
T_BURST = t4 + 2.15                # kernel bursts
T_EARTH = t5 + 0.25                # Earth-size flake appears for comparison
T_PUFF = t5 + 1.15                 # Mars flake puffs to 2x volume
T_DUDS = t7 + 0.05                 # duds ringed
MARS_S = 2 ** (1 / 3)              # 2x volume -> 1.26x linear

# ---------- props ----------
def stove_pan(x, y, top, pr=0.17, ph=0.06, seed=1):
    box((x, y, top + 0.04), (0.42, 0.38, 0.08), M_DARK, "stove")
    fl = []
    for k in range(10):
        a = k / 10 * math.tau
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.02, radius2=0, depth=0.06, location=(x + math.cos(a) * 0.08, y + math.sin(a) * 0.08, top + 0.11))
        o = bpy.context.object; link(o, M_FLAME); fl.append(o)
    pb = top + 0.12
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=pr, depth=ph, location=(x, y, pb + ph / 2))
    pan = bpy.context.object; bpy.ops.object.shade_smooth(); link(pan, M_STEEL)
    sol = pan.modifiers.new("shell", "SOLIDIFY"); sol.thickness = 0.008
    bpy.ops.object.mode_set(mode="EDIT"); bm = bmesh.from_edit_mesh(pan.data)
    bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if fc.normal.z > 0.9], context="FACES"); bmesh.update_edit_mesh(pan.data)
    bpy.ops.object.mode_set(mode="OBJECT")
    cyl_between((x, y + pr, pb + ph - 0.01), (x + 0.02, y + pr + 0.2, pb + ph + 0.01), 0.012, M_DARK, None, "handle")
    return pb + 0.008, fl
def flake(name, base, seed):
    """popcorn flake: cluster of puffy lobes + a hull fleck, root empty at its centre; base = radius"""
    rnd = random.Random(seed); e = empty(name)
    for k in range(6):
        d = V((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.7, 1))).normalized() * base * 0.55
        o = sphere(d, base * rnd.uniform(0.55, 0.8), M_POP, name + "_l", e, 12)
        o.scale = (1, 1, rnd.uniform(0.75, 1.0))
    sphere(V((0, 0, -base * 0.45)), base * 0.28, M_HULL, name + "_h", e, 10)
    e.scale = (0.0001,) * 3
    return e
def kernel(loc, r, m, name):
    o = sphere(loc, 1, m, name, None, 14); o.scale = (r * 0.8, r * 0.65, r); o.rotation_euler = (0.3, 0.2, random.uniform(0, 3))
    return o

# ================= HOOK set (x = 0) =================
TOP = 0.90
LX, RX = -0.215, 0.215
box((0, 0, TOP / 2), (2.6, 1.0, TOP), M_COUNTER, "counter")
box((-1.0, 0.6, 1.8), (2.0, 0.1, 3.6), M_WALLE, "wallE")
box((1.0, 0.6, 1.8), (2.0, 0.1, 3.6), M_WALLM, "wallM")
PANS = {}
rnd = random.Random(5)
KERN = {"E": [], "M": []}
for side, x, sd in (("E", LX, 3), ("M", RX, 4)):
    pz, fl = stove_pan(x, 0.0, TOP, seed=sd)
    PANS[side] = (pz, fl)
    n_dud = 5 if side == "E" else 1
    for k in range(20):
        a = k * 2.39996 + (0.3 if side == "M" else 0); r = 0.13 * math.sqrt((k + 0.5) / 20)
        p = V((x + math.cos(a) * r, math.sin(a) * r, pz + 0.008))
        dud = k in ((3, 7, 11, 15, 18) if side == "E" else (11,))
        kn = kernel(p, 0.011, M_DUD if False else M_KERN, f"k{side}{k}")
        # pop times: 4 inside the first 0.45 s, rest spread to ~1.8 s
        tp = T_POP0 + (k * 0.1 if k < 4 else 0.45 + (k - 4) * 0.085) + rnd.uniform(0, 0.04)
        fk = None if dud else flake(f"f{side}{k}", 0.026 * (MARS_S if side == "M" else 1.0), sd * 100 + k)
        land = V((x + math.cos(a) * r * 0.9, math.sin(a) * r * 0.9, pz + 0.02 + 0.025 * (k % 3)))
        KERN[side].append(dict(k=kn, f=fk, p=p, land=land, tp=tp, dud=dud, h=rnd.uniform(0.10, 0.2), spin=rnd.uniform(4, 9)))
HL = [label("EARTH", (LX, 0.5, 1.30), 0.075, M_LBLB), label("AIR: 1 ATM", (LX, 0.5, 1.225), 0.045, M_WHITE)]
HR = [label("MARS", (RX, 0.5, 1.30), 0.075, M_LBL), label("AIR: ≈0.006 ATM", (RX, 0.5, 1.225), 0.045, M_WHITE)]
DUD_E = label("DUDS: 5", (LX, -0.12, TOP + 0.33), 0.06, M_RED)
DUD_M = label("DUDS: 1", (RX, -0.12, TOP + 0.33), 0.06, M_GREEN)
RINGS = []
for side in ("E", "M"):
    for d in KERN[side]:
        if d["dud"]:
            bpy.ops.mesh.primitive_torus_add(major_radius=0.024, minor_radius=0.005, location=d["p"] + V((0, 0, 0.004)))
            o = bpy.context.object; link(o, M_RED); noshadow(o); RINGS.append(o)
kl = bpy.data.objects.new("kitchen", bpy.data.lights.new("kitchen", "AREA")); kl.data.energy = 420; kl.data.size = 3
kl.data.color = (1.0, 0.9, 0.75); kl.location = (-1.0, -2.8, 3.0); kl.rotation_euler = (math.radians(45), 0, math.radians(-20)); S.collection.objects.link(kl)
kl2 = bpy.data.objects.new("kitchen2", bpy.data.lights.new("kitchen2", "AREA")); kl2.data.energy = 260; kl2.data.size = 2.5
kl2.data.color = (0.95, 0.9, 1.0); kl2.location = (1.4, -2.6, 2.4); kl2.rotation_euler = (math.radians(50), 0, math.radians(25)); S.collection.objects.link(kl2)

# ================= MARS surface set (x = 30) =================
MX = 30.0
bpy.ops.mesh.primitive_plane_add(size=80, location=(MX, 20, 0)); link(bpy.context.object, M_GROUND)
rr = random.Random(9)
for k in range(26):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rr.uniform(0.05, 0.35), location=(MX + rr.uniform(-4, 4), rr.uniform(0.6, 9), 0))
    o = bpy.context.object; o.scale = (1, rr.uniform(0.7, 1.2), rr.uniform(0.4, 0.8)); link(o, M_ROCK)
for (dx, dy, r, h) in ((-9, 28, 8, 3.0), (6, 32, 10, 2.4), (14, 25, 6, 2.0)):
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=r, radius2=r * 0.3, depth=h, location=(MX + dx, dy, h / 2)); link(bpy.context.object, M_GROUND)
box((MX, 45, 10), (120, 0.1, 40), M_SKY, "sky")
PZ_M, FL_M = stove_pan(MX, 0, 0.0, seed=7)
KM = [kernel((MX + math.cos(k * 2.4) * 0.12 * math.sqrt((k + .5) / 14), math.sin(k * 2.4) * 0.12 * math.sqrt((k + .5) / 14), PZ_M + 0.008), 0.011, M_KERN, "km") for k in range(14)]
SUM_T1 = label("MARS SURFACE", (MX, -0.25, 0.55), 0.07, M_LBL)
sun = bpy.data.objects.new("msun", bpy.data.lights.new("msun", "SUN")); sun.data.energy = 3.0
sun.data.color = (1.0, 0.88, 0.75); sun.rotation_euler = (math.radians(50), 0, math.radians(-35)); S.collection.objects.link(sun)

# ================= close-up set (x = 60) =================
CX = 60.0; CT = 0.6; PCX = CX - 0.12
box((CX, 0, CT / 2), (2.4, 1.2, CT), M_COUNTER, "counter2")
box((CX, 0.7, 1.6), (4, 0.1, 3.2), M_WALLM, "wall2")
PZ_C, FL_C = stove_pan(PCX, 0, CT, pr=0.2, seed=11)
BIG = kernel((PCX, 0, PZ_C + 0.045), 0.05, M_KERN, "bigk")
BIGF = flake("bigf", 0.075, 77)
BIGF.location = (PCX, 0, PZ_C + 0.11)
EF = flake("earthf", 0.075, 78)     # Earth-size comparison flake on a small plate, left of the pan
EF.location = (PCX - 0.40, -0.05, CT + 0.10)
cyl((PCX - 0.40, -0.05, CT + 0.008), 0.11, 0.016, M_FACE, "plate")
LBL_E = label("EARTH SIZE", (PCX - 0.40, -0.12, CT + 0.255), 0.032, M_LBLB)
LBL_M = label("MARS: 2× VOLUME", (PCX, -0.12, CT + 0.34), 0.03, M_LBL)
AIR = []
rnd = random.Random(21)
for k in range(36):
    o = noshadow(sphere((PCX + rnd.uniform(-0.26, 0.26), -0.05 + rnd.uniform(-0.1, 0.1), CT + 0.33 + rnd.uniform(0, 0.22)), 0.014, M_AIR, "air", None, 8))
    AIR.append((o, V(o.location), rnd.uniform(0, math.tau), k != 17))
AIR_T = label("", (PCX, -0.15, CT + 0.60), 0.045, M_LBLB)
# pressure gauge right of the pan (face toward camera)
GX, GZ = PCX + 0.54, CT + 0.40
cyl((GX, 0.02, GZ), 0.13, 0.03, M_DARK, "gbody", rot=(math.radians(90), 0, 0))
cyl((GX, 0.0, GZ), 0.115, 0.012, M_FACE, "gface", rot=(math.radians(90), 0, 0))
cyl_between((GX, 0.04, GZ - 0.13), (GX - 0.06, 0.04, CT + 0.12), 0.012, M_STEEL, None, "gpipe")
for k in range(10):   # ticks 0..9 atm over 270 degrees (from -135 to +135, clockwise)
    ang = math.radians(-135 + 270 * k / 9)
    p = V((GX + math.sin(ang) * 0.095, -0.012, GZ + math.cos(ang) * 0.095))
    box(p, (0.006, 0.004, 0.018), M_RED if k == 9 else M_DARK, "tick").rotation_euler = (0, ang, 0)
label("9", (GX + math.sin(math.radians(135)) * 0.07, -0.014, GZ + math.cos(math.radians(135)) * 0.07), 0.026, M_RED)
label("0", (GX + math.sin(math.radians(-135)) * 0.07, -0.014, GZ + math.cos(math.radians(-135)) * 0.07), 0.026, M_DARK)
NEEDLE = empty("needle", (GX, -0.014, GZ))
box((0, 0, 0.042), (0.008, 0.004, 0.085), M_RED, "ndl", NEEDLE)
GT = label("", (GX - 0.255, -0.03, GZ + 0.02), 0.05, M_WHITE)
GT2 = label("INSIDE THE KERNEL", (GX, -0.03, GZ + 0.175), 0.028, M_WHITE)
cl = bpy.data.objects.new("cl", bpy.data.lights.new("cl", "AREA")); cl.data.energy = 300; cl.data.size = 2.5
cl.data.color = (1.0, 0.92, 0.8); cl.location = (CX - 1.0, -2.4, 2.4); cl.rotation_euler = (math.radians(50), 0, math.radians(-25)); S.collection.objects.link(cl)
cl2 = bpy.data.objects.new("cl2", bpy.data.lights.new("cl2", "AREA")); cl2.data.energy = 160; cl2.data.size = 2
cl2.data.color = (0.9, 0.88, 1.0); cl2.location = (CX + 1.3, -2.2, 1.8); cl2.rotation_euler = (math.radians(55), 0, math.radians(30)); S.collection.objects.link(cl2)

# ---------- text handler ----------
def atm_at(t): return 9.0 * smooth((t - T_G0) / (T_G1 - T_G0)) if t >= T_G0 else 0.0
def handler(scene, *a):
    t = scene.frame_current / FPS
    AIR_T.data.body = "AIR: EARTH" if t < T_THIN else "AIR: MARS (<1 %)"
    GT.data.body = f"{atm_at(t):.0f} ATM" if t < T_BURST else "POP!"
bpy.app.handlers.frame_change_pre.append(handler)

# ---------- animation ----------
for f in range(0, N + 1):
    t = f / FPS
    for fl in PANS["E"][1] + PANS["M"][1] + FL_M + FL_C:
        fl.scale = (1, 1, 0.8 + 0.4 * abs(math.sin(t * 17 + fl.location.x * 13 + fl.location.y * 7))); fl.keyframe_insert("scale", frame=f)
    for side in ("E", "M"):
        for d in KERN[side]:
            kn, fk = d["k"], d["f"]
            jig = 0.002 * math.sin(t * 40 + d["spin"] * 5)
            popped = (not d["dud"]) and t >= d["tp"]
            kn.location = d["p"] + V((jig, 0, abs(jig))); kn.keyframe_insert("location", frame=f)
            vis(kn, not popped, f, (0.0088, 0.00715, 0.011))
            if fk:
                if not popped: fk.scale = (0.0001,) * 3; fk.location = d["p"]
                else:
                    u = min(1.0, (t - d["tp"]) / 0.45)
                    g = min(1.0, (t - d["tp"]) / 0.08)
                    fk.scale = (0.3 + 0.7 * g + 0.15 * math.sin(min(u, 1) * math.pi),) * 3
                    fk.location = d["p"].lerp(d["land"], u) + V((0, 0, d["h"] * math.sin(u * math.pi)))
                    fk.rotation_euler = (d["spin"] * min(t - d["tp"], 0.45), 0.5 * d["spin"] * min(t - d["tp"], 0.45), 0)
                    fk.keyframe_insert("rotation_euler", frame=f)
                fk.keyframe_insert("scale", frame=f); fk.keyframe_insert("location", frame=f)
    on = T_DUDS <= t < T_LOOP
    vis(DUD_E, on, f); vis(DUD_M, on, f)
    for o in RINGS: vis(o, on, f, (1 + 0.15 * math.sin(t * 10),) * 3 if on else (1, 1, 1))
    for o in HL + HR: vis(o, True, f)
    # Mars surface kernels sizzle
    for k, o in enumerate(KM):
        o.location.z = PZ_M + 0.008 + abs(0.004 * math.sin(t * 30 + k)); o.keyframe_insert("location", frame=f)
    # close-up: air dots; all but one vanish at T_THIN
    for (o, p0, ph, goes) in AIR:
        o.location = p0 + V((0.02 * math.sin(t * 7 + ph), 0, 0.02 * math.cos(t * 6 + ph * 2))); o.keyframe_insert("location", frame=f)
        s = 1.0 if not (goes and t >= T_THIN) else max(0.0001, 1 - (t - T_THIN) / 0.25)
        if t >= t4 - 0.05: s = 0.0001
        o.scale = (s, s, s); o.keyframe_insert("scale", frame=f)
    vis(AIR_T, t < t4 - 0.05, f)
    # gauge needle + big kernel swells, shakes, bursts
    NEEDLE.rotation_euler = (0, math.radians(-135 + 270 * atm_at(t) / 9.0 + (2 * math.sin(t * 50) if T_G1 <= t < T_BURST else 0)), 0)
    NEEDLE.keyframe_insert("rotation_euler", frame=f)
    sw = 1 + 0.12 * smooth((t - T_G0) / (T_G1 - T_G0)) if t >= T_G0 else 1
    shk = 0.004 * math.sin(t * 60) * smooth((t - T_G0) / (T_G1 - T_G0)) if t >= T_G0 else 0
    BIG.location = (PCX + shk, 0, PZ_C + 0.045); BIG.keyframe_insert("location", frame=f)
    vis(BIG, t < T_BURST, f, (0.04 * sw, 0.0325 * sw, 0.05 * sw))
    if t < T_BURST: s = 0.0001; z = PZ_C + 0.08
    else:
        u = (t - T_BURST); g = min(1.0, u / 0.1)
        s = 0.3 + 0.7 * g + 0.2 * math.exp(-u * 6) * math.sin(u * 25) * g
        if t >= T_PUFF: s *= 1 + (MARS_S - 1) * smooth((t - T_PUFF) / 0.4)
        z = PZ_C + 0.075 + 0.12 * math.sin(min(u / 0.5, 1) * math.pi) + 0.04 * (s - 1)
    BIGF.scale = (s, s, s); BIGF.location = (PCX, 0, z)
    BIGF.rotation_euler = (0.4 * min(max(t - T_BURST, 0), 0.5) * 6, 0, 0.3 * t)
    BIGF.keyframe_insert("scale", frame=f); BIGF.keyframe_insert("location", frame=f); BIGF.keyframe_insert("rotation_euler", frame=f)
    ge = smooth((t - T_EARTH) / 0.25) if t >= T_EARTH else 0.0
    EF.scale = (max(ge, 0.0001),) * 3; EF.rotation_euler = (0.4, 0, 0.3 * t); EF.keyframe_insert("scale", frame=f); EF.keyframe_insert("rotation_euler", frame=f)
    vis(LBL_E, t >= T_EARTH + 0.1, f); vis(LBL_M, t >= T_PUFF + 0.2, f)
    vis(GT, t4 - 0.05 <= t < t5 + 0.1, f); vis(GT2, t4 - 0.05 <= t < t5 + 0.1, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -1.02, 1.42), (0.0, -0.02, 1.04), (0.0, -0.97, 1.40), (0.0, -0.02, 1.04))
SEG = [
    (0.0, t2 - 0.05, HOOK, 16, 16),
    (t2 - 0.05, t3 - 0.05, fixed((MX, -1.0, 0.55), (MX, 0, 0.30), (MX, -2.6, 0.9), (MX, 0, 0.42)), 24, 24),
    (t3 - 0.05, t4 - 0.05, fixed((PCX, -1.9, 1.25), (PCX, 0, 0.94), (PCX + 0.02, -1.8, 1.25), (PCX + 0.02, 0, 0.94)), 30, 30),
    (t4 - 0.05, t5 - 0.05, fixed((PCX + 0.27, -2.0, 1.12), (PCX + 0.27, 0, 0.88), (PCX + 0.27, -1.9, 1.1), (PCX + 0.27, 0, 0.88)), 26, 26),
    (t5 - 0.05, t6 - 0.05, fixed((PCX - 0.20, -1.75, 1.10), (PCX - 0.20, 0, 0.80), (PCX - 0.20, -1.65, 1.08), (PCX - 0.20, 0, 0.80)), 30, 30),
    (t6 - 0.05, T_LOOP, fixed((0.0, -0.95, 1.45), (0.0, -0.02, 1.05), (0.0, -0.9, 1.43), (0.0, -0.02, 1.05)), 16, 16),
    (T_LOOP, DUR + 0.01, HOOK, 16, 16),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    shk = 0.0
    if 0 <= t - T_BURST < 0.4: shk += 0.01 * math.exp(-(t - T_BURST) * 9) * math.sin((t - T_BURST) * 70)
    cam.location = p + V((shk, 0, shk * 0.6)); cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "pop0": T_POP0,
           "pops": sorted(d["tp"] for s in ("E", "M") for d in KERN[s] if not d["dud"]),
           "thin": T_THIN, "g0": T_G0, "g1": T_G1, "burst": T_BURST, "earth": T_EARTH, "puff": T_PUFF, "duds": T_DUDS},
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
