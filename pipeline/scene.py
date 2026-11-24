"""The Impossible Lab #19 - a balloon on Mars (E17 cascade middle, reel 2).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(19)
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


import bmesh
FNT = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def label(body, loc, size, m, align="CENTER", rot=TR):
    o = text(body, loc, rot, size, m, align); o.data.font = FNT; noshadow(o); o.visible_glossy = False; return o
def cyl(loc, r, d, m, name="cyl", rot=(0, 0, 0), verts=32, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def open_cyl(loc, r, d, m, name, thick=0.006, verts=40):
    o = cyl(loc, r, d, m, name, verts=verts)
    bpy.ops.object.mode_set(mode="EDIT"); bm = bmesh.from_edit_mesh(o.data)
    bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if fc.normal.z > 0.9], context="FACES"); bmesh.update_edit_mesh(o.data)
    bpy.ops.object.mode_set(mode="OBJECT")
    if thick > 0.0045:
        sol = o.modifiers.new("shell", "SOLIDIFY"); sol.thickness = thick
    return o


# ================= episode 19: a balloon on Mars (E17 cascade middle, reel 2) =================
# Hook (x = 0): EARTH balloon (left, calm) vs MARS balloon (right, butterscotch sky wall): from 0.08 s the Mars balloon
# swells and pops at ~1.0 s (latex shreds). Line 2: Mars surface set (x = 30), a fresh tied balloon on a table beside
# a plate of marshmallows, a sealed snack bag and a rubber glove. Line 3: air dots vanish, the balloon starts to swell.
# Line 4 (cascade): marshmallows puff -> snack bag bulges -> glove fingers inflate. Line 5: balloon keeps swelling,
# "VOLUME xN" climbs while "NEEDS x100+" is shown, latex thins (lighter colour). Line 6: tear lines race across it.
# Line 7: pop, shreds fly; RIP vs SOUND speed bars race. Last ~1.4 s: hook framing (loop).
M_TABLE = noise_mat("table", (0.55, 0.36, 0.22), (0.66, 0.45, 0.28), 7.0, 0.45)
M_WALLE = tiles("wallE", (0.20, 0.30, 0.40), (0.12, 0.16, 0.20), 4.0)
M_WALLM = mat("wallM", (0.55, 0.28, 0.14), 0.9)
M_GLASS = liquid("glass", (0.97, 0.99, 1.0), (0.92, 0.96, 1.0), 0.02)
def latex(name, col):
    m = mat(name, col, 0.22); return m
M_BALE = latex("balE", (0.80, 0.04, 0.05))
M_BALM = latex("balM", (0.80, 0.04, 0.05))
M_BALS = latex("balS", (0.80, 0.04, 0.05))
M_SHRED = latex("shred", (0.80, 0.04, 0.05))
M_STRING = mat("string", (0.95, 0.95, 0.92), 0.6)
M_WEIGHT = mat("weight", (0.15, 0.15, 0.17), 0.3, 0.8)
M_MALLOW = mat("mallow", (0.97, 0.95, 0.92), 0.85)
M_PLATE = mat("plate", (0.35, 0.55, 0.80), 0.3)
M_BAG = mat("bag", (0.95, 0.70, 0.10), 0.25, 0.6)
M_BAGB = mat("bagb", (0.85, 0.15, 0.10), 0.3, 0.5)
M_GLOVE = mat("glove", (0.15, 0.55, 0.85), 0.35)
M_GROUND = noise_mat("marsground", (0.45, 0.20, 0.09), (0.70, 0.38, 0.18), 2.5, 0.95)
M_ROCK = noise_mat("rock", (0.30, 0.13, 0.06), (0.50, 0.26, 0.12), 6.0, 0.9)
M_DARK = mat("dark", (0.04, 0.04, 0.05), 0.5)
M_AIR = mat("air", (0.6, 0.85, 1.0), 0.4, 0, (0.55, 0.85, 1.0), 3.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_AMB = mat("lbla", (1.0, 0.65, 0.15), 0.4, 0, (1.0, 0.6, 0.12), 4.0)
M_RIP = mat("rip", (1.0, 0.95, 0.8), 0.4, 0, (1.0, 0.95, 0.75), 6.0)
M_REDL = mat("redl", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 3.0)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.5
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.55, 0.32, 0.18, 1); WBG.inputs[1].default_value = 0.3

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_HS = 0.08                  # hook: Mars balloon starts swelling
T_HP = 1.00                  # hook: pop
T_SET = t2 + 0.6             # Mars balloon lands on the table
T_THIN = t3 + 0.45           # air dots vanish
T_SW = t3 + 0.75             # Mars balloon starts to swell
T_MAL = t4 + 0.25            # cascade 1: marshmallows puff
T_BAG = t4 + 0.95            # cascade 2: snack bag bulges
T_GLV = t4 + 1.65            # cascade 3: glove inflates
T_RIP = t6 + 0.05            # tear lines start
T_POP = t7 + 0.10            # pop
T_BARS = t7 + 0.35           # speed bars race
VMAX = 20.0                  # volume factor reached before it tears (shown), needs x100+

def balloon(x, y, zk, R0, m, name):
    """balloon = sphere scaled z 1.15 + knot; zk = knot height. returns dict"""
    b = sphere((x, y, zk + R0 * 1.15), 1.0, m, name, None, 40)
    k = noshadow(sphere((x, y, zk), 0.012, m, name + "knot", None, 10)); k.scale = (1, 1, 1.4)
    return dict(o=b, k=k, x=x, y=y, zk=zk, R0=R0)
def set_bal(d, s, f, hide=False):
    R = d["R0"] * s
    o = d["o"]
    if hide: o.scale = (0.0001,) * 3
    else: o.scale = (R, R, R * 1.15)
    o.location = (d["x"], d["y"], d["zk"] + R * 1.15 - 0.004)
    o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)
    vis(d["k"], not hide, f, (1, 1, 1.4))

def shreds(cx, cy, cz, R, n, seed, mm):
    rs = random.Random(seed); out = []
    for k in range(n):
        u = rs.uniform(-1, 1); a = rs.uniform(0, math.tau); dirv = V((math.sqrt(1 - u * u) * math.cos(a), math.sqrt(1 - u * u) * math.sin(a), u))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(cx, cy, cz)); o = bpy.context.object
        link(o, mm); noshadow(o)
        out.append(dict(o=o, d=dirv, sp=rs.uniform(0.6, 1.4), sz=rs.uniform(0.018, 0.034), spin=V((rs.uniform(-9, 9), rs.uniform(-9, 9), rs.uniform(-9, 9)))))
    return out
def anim_shreds(SH, c, R, tp, t, f, g=3.71, until=99):
    for s in SH:
        o = s["o"]
        if tp <= t < until:
            dt = t - tp
            p = V(c) + s["d"] * (R + s["sp"] * 1.2 * dt) + V((0, 0, -0.5 * g * dt * dt))
            o.location = p; sz = s["sz"]; o.scale = (sz, sz * 0.5, sz * 0.18)
            o.rotation_euler = s["spin"] * dt
        else:
            o.location = c; o.scale = (0.0001,) * 3; o.rotation_euler = (0, 0, 0)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f); o.keyframe_insert("rotation_euler", frame=f)

# ================= HOOK set (x = 0) =================
TOP = 0.90
LX, RX = -0.20, 0.20
box((0, 0, TOP / 2), (2.6, 1.0, TOP), M_TABLE, "counter")
box((-1.0, 0.6, 1.8), (2.0, 0.1, 3.6), M_WALLE, "wallE")
box((1.0, 0.6, 1.8), (2.0, 0.1, 3.6), M_WALLM, "wallM")
ZK = TOP + 0.08
for xx in (LX, RX):
    box((xx, 0, TOP + 0.015), (0.04, 0.04, 0.03), M_WEIGHT, "hweight")
    cyl_between((xx, 0, TOP + 0.03), (xx, 0, ZK), 0.0018, M_STRING, None, "hstring", caps=False, verts=6)
HB_E = balloon(LX, 0, ZK, 0.09, M_BALE, "hbalE")
HB_M = balloon(RX, 0, ZK, 0.09, M_BALM, "hbalM")
HSH = shreds(RX, 0, ZK + 0.2, 0.17, 26, 5, M_SHRED)
label("EARTH", (LX, 0.5, 1.36), 0.10, M_LBLB); label("AIR: 1 BAR", (LX, 0.5, 1.27), 0.06, M_WHITE)
label("MARS", (RX, 0.5, 1.36), 0.10, M_WHITE); label("AIR: 0.006 BAR", (RX, 0.5, 1.27), 0.05, M_WHITE)
kl = bpy.data.objects.new("kitchen", bpy.data.lights.new("kitchen", "AREA")); kl.data.energy = 260; kl.data.size = 3
kl.data.color = (1.0, 0.92, 0.8); kl.location = (-1.0, -2.8, 3.0); kl.rotation_euler = (math.radians(45), 0, math.radians(-20)); S.collection.objects.link(kl)
kl2 = bpy.data.objects.new("kitchen2", bpy.data.lights.new("kitchen2", "AREA")); kl2.data.energy = 160; kl2.data.size = 2.5
kl2.data.color = (0.95, 0.95, 1.0); kl2.location = (1.4, -2.6, 2.4); kl2.rotation_euler = (math.radians(50), 0, math.radians(25)); S.collection.objects.link(kl2)

# ================= MARS surface set (x = 30) =================
MX = 30.0; MT = 0.55
bpy.ops.mesh.primitive_plane_add(size=160, location=(MX, 40, 0)); link(bpy.context.object, M_GROUND)
rr = random.Random(9)
for k in range(40):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rr.uniform(0.05, 0.35), location=(MX + rr.uniform(-6, 6), rr.uniform(0.8, 14), 0))
    o = bpy.context.object; o.scale = (1, rr.uniform(0.7, 1.2), rr.uniform(0.3, 0.7)); link(o, M_ROCK)
for (dx, dy, h, r) in ((-9, 40, 4.0, 9.0), (8, 50, 5.0, 12.0), (0, 70, 7, 16)):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=r, depth=h, location=(MX + dx, dy, h / 2)); link(bpy.context.object, M_ROCK)
box((MX, 0, MT - 0.02), (1.05, 0.42, 0.04), M_TABLE, "mtable_top")
for (dx, dy) in ((-0.47, -0.16), (0.47, -0.16), (-0.47, 0.16), (0.47, 0.16)):
    box((MX + dx, dy, (MT - 0.04) / 2), (0.03, 0.03, MT - 0.04), M_DARK, "leg")
# balloon (right of centre), knot just above the table
BX = MX + 0.24; BZK = MT + 0.06
box((BX, 0.02, MT + 0.015), (0.04, 0.04, 0.03), M_WEIGHT, "mweight")
cyl_between((BX, 0.02, MT + 0.03), (BX, 0.02, BZK), 0.0018, M_STRING, None, "mstring", caps=False, verts=6)
MB = balloon(BX, 0.02, BZK, 0.08, M_BALS, "mbal")
MB_GROUP = [MB["o"], MB["k"]] + [o for o in bpy.data.objects if o.name.startswith(("mweight", "mstring"))]
SH = shreds(BX, 0.02, BZK + 0.25, 0.217, 44, 11, M_SHRED)
# plate of marshmallows (left)
PX = MX - 0.36
cyl((PX, 0.0, MT + 0.006), 0.085, 0.012, M_PLATE, "plate")
MAL = []
for (dx, dy) in ((-0.035, -0.02), (0.0, 0.025), (0.035, -0.02), (0.0, -0.035), (-0.04, 0.03), (0.04, 0.03)):
    o = cyl((PX + dx, dy, MT + 0.012 + 0.014), 0.016, 0.028, M_MALLOW, "mallow", verts=16)
    MAL.append(o)
# snack bag (left of centre): pillow
GX = MX - 0.12
bpy.ops.mesh.primitive_cube_add(size=1, location=(GX, 0.02, MT + 0.115)); BAG = link(bpy.context.object, M_BAG); BAG.name = "bag"
BAG.modifiers.new("ss", "SUBSURF").levels = 3; bpy.ops.object.shade_smooth()
BAGC = box((GX, 0.02, MT + 0.235), (0.17, 0.035, 0.018), M_BAGB, "bagcrimp"); BAGC2 = box((GX, 0.02, MT + 0.008), (0.17, 0.035, 0.014), M_BAGB, "bagcrimp2")
BAGS = label("SNACKS", (GX, -0.09, MT + 0.12), 0.034, M_REDL); BAGS.visible_shadow = False
# rubber glove (centre), lying on the table, fingers up the screen
VX = MX + 0.03
GLV = empty("glove", (VX, -0.02, MT + 0.012))
palm = sphere((0, 0, 0), 1.0, M_GLOVE, "palm", GLV, 24)
FING = []
for k, (dx, ln, ang) in enumerate(((-0.03, 0.050, 18), (-0.012, 0.062, 6), (0.008, 0.066, -2), (0.026, 0.058, -10), (0.044, 0.040, -48))):
    e = empty(f"fing{k}", (dx, 0, 0.05 if k < 4 else 0.005), GLV); e.rotation_euler = (0, math.radians(ang), 0)
    o = sphere((0, 0, ln / 2), 1.0, M_GLOVE, "finger", e, 16); FING.append((o, ln))
cuff = cyl((0.0, 0, -0.07), 0.035, 0.035, M_GLOVE, "cuff", rot=(0, 0, 0), parent=GLV)
GLV.rotation_euler = (0, 0, 0)   # standing glove, palm facing the camera
GLV.location = (VX, 0.03, MT + 0.085)
AIR = []
rnd = random.Random(21)
for k in range(40):
    o = noshadow(sphere((MX + rnd.uniform(-0.5, 0.5), -0.10 + rnd.uniform(-0.1, 0.1), MT + 0.12 + rnd.uniform(0, 0.33)), 0.012, M_AIR, "air", None, 8))
    AIR.append((o, V(o.location), rnd.uniform(0, math.tau), k != 13))
AIR_T = label("", (MX, -0.15, MT + 0.50), 0.045, M_LBLB)
VOL_T = label("", (MX - 0.14, -0.14, MT + 0.36), 0.05, M_AMB)
NEED_T = label("NEEDS ×100+", (MX - 0.14, -0.14, MT + 0.44), 0.05, M_WHITE)
# speed bars (after the pop), in front of the table, under where the balloon was
BAR_Y = -0.12
RIPB = empty("ripb", (MX - 0.42, BAR_Y, MT + 0.47)); box((0.5, 0, 0), (1.0, 0.01, 0.04), M_RIP, "ripbar", RIPB)
SNDB = empty("sndb", (MX - 0.42, BAR_Y, MT + 0.33)); box((0.5, 0, 0), (1.0, 0.01, 0.04), M_LBLB, "sndbar", SNDB)
RIP_T = label("BALLOON RIP ≈ 570 m/s", (MX - 0.42, BAR_Y, MT + 0.54), 0.05, M_RIP, align="LEFT")
SND_T = label("MARS SOUND ≈ 240 m/s", (MX - 0.42, BAR_Y, MT + 0.40), 0.05, M_LBLB, align="LEFT")
sun = bpy.data.objects.new("msun", bpy.data.lights.new("msun", "SUN")); sun.data.energy = 3.5
sun.data.color = (1.0, 0.93, 0.85); sun.rotation_euler = (math.radians(50), 0, math.radians(-35)); S.collection.objects.link(sun)
# tear lines on the swollen balloon (sphere surface points), revealed progressively
RIPS = []
RB = 0.08 * VMAX ** (1 / 3); CB = V((BX, 0.02, BZK + RB * 1.15 - 0.004))
rt = random.Random(4)
def surf_pt(pol, phi):
    return CB + V((RB * 1.01 * math.sin(pol) * math.sin(phi), -RB * 1.01 * math.sin(pol) * math.cos(phi), RB * 1.16 * math.cos(pol)))
for br in range(5):
    pol, phi = math.radians(70), math.radians(-10)
    dp, dq = rt.uniform(-1, 1), rt.uniform(-1, 1)
    nrm = math.hypot(dp, dq); dp, dq = dp / nrm * 0.16, dq / nrm * 0.16
    for s in range(6):
        p1 = surf_pt(pol, phi); pol2 = pol + dp + rt.uniform(-0.06, 0.06); phi2 = phi + dq + rt.uniform(-0.06, 0.06)
        p2 = surf_pt(pol2, phi2)
        o = cyl_between(p1, p2, 0.0035, M_RIP, None, "rip", caps=False, verts=6); noshadow(o)
        RIPS.append((o, T_RIP + s * 0.11 + br * 0.03)); pol, phi = pol2, phi2

# ---------- text handler ----------
def vol_at(t):
    if t < T_SW: return 1.0
    if t < t5: return 1.0 + 1.0 * smooth((t - T_SW) / (t5 - T_SW))          # x2 by line 5
    return 2.0 + (VMAX - 2.0) * smooth((t - t5) / (T_RIP - t5 - 0.1))      # x20 when it tears
def handler(scene, *a):
    t = scene.frame_current / FPS
    AIR_T.data.body = "AIR: EARTH" if t < T_THIN else "AIR: MARS (0.6 %)"
    VOL_T.data.body = f"VOLUME ×{vol_at(t):.0f}"
bpy.app.handlers.frame_change_pre.append(handler)

# ---------- animation ----------
for f in range(0, N + 1):
    t = f / FPS
    # hook balloons (replay after T_LOOP)
    tt = t - T_LOOP if t >= T_LOOP else t
    set_bal(HB_E, 1.0, f)
    hs = 1.0 + 0.9 * smooth((tt - T_HS) / (T_HP - T_HS)) ** 0.8 if tt >= T_HS else 1.0
    set_bal(HB_M, hs, f, hide=(T_HP <= tt < (t2 if t < T_LOOP else 99)) or (t >= t2 and t < T_LOOP))
    anim_shreds(HSH, (RX, 0, ZK + 0.09 * 1.9 * 1.15), 0.09 * 1.9, T_HP + (T_LOOP if t >= T_LOOP else 0), t, f, 9.81, t2 if t < T_LOOP else 99)
    # Mars balloon: lands, swells, tears, pops
    DZ = 0.30 * (1 - smooth((t - t2) / 0.6)) if t < T_SET else 0.0
    s = vol_at(t) ** (1 / 3)
    gone = t >= T_POP
    MB["zk"] = BZK + DZ; set_bal(MB, s, f, hide=gone)
    for o in MB_GROUP[2:]:
        if "z0" not in o: o["z0"] = o.location.z
        o.location.z = o["z0"] + DZ; o.keyframe_insert("location", frame=f)
    # latex thins: colour lightens as it stretches
    lt = smooth((vol_at(t) - 1) / (VMAX - 1))
    bsdf(M_BALS).inputs["Base Color"].default_value = (0.80 + 0.15 * lt, 0.04 + 0.30 * lt, 0.05 + 0.28 * lt, 1)
    bsdf(M_BALS).inputs["Base Color"].keyframe_insert("default_value", frame=f)
    anim_shreds(SH, CB, RB, T_POP, t, f, 3.71)
    for (o, tr) in RIPS: vis(o, tr <= t < T_POP, f)
    # cascade
    m = smooth((t - T_MAL) / 0.4)
    for o in MAL: o.scale = (1 + 0.55 * m, 1 + 0.55 * m, 1 + 0.75 * m); o.keyframe_insert("scale", frame=f)
    b = smooth((t - T_BAG) / 0.45)
    BAG.scale = (0.18 + 0.07 * b, 0.03 + 0.11 * b, 0.20 + 0.07 * b); BAG.keyframe_insert("scale", frame=f)
    hz = 0.40 * BAG.scale[2]; BAG.location.z = MT + 0.012 + hz; BAG.keyframe_insert("location", frame=f)
    for o, zz in ((BAGC, MT + 0.012 + 2 * hz), (BAGC2, MT + 0.012)):
        o.location.z = zz; o.scale = (0.75 + 0.35 * b, 1, 1); o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    BAGS.location.z = MT + 0.012 + hz; BAGS.keyframe_insert("location", frame=f)
    g = smooth((t - T_GLV) / 0.45)
    palm.scale = (0.038 + 0.024 * g, 0.010 + 0.035 * g, 0.048 + 0.022 * g); palm.keyframe_insert("scale", frame=f)
    for (o, ln) in FING:
        rr_ = 0.006 + 0.012 * g; o.scale = (rr_, rr_, ln / 2 * (0.85 + 0.45 * g)); o.location.z = ln / 2 * (0.85 + 0.45 * g)
        o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)
    # air dots
    for (o, p0, ph, goes) in AIR:
        o.location = p0 + V((0.02 * math.sin(t * 7 + ph), 0, 0.02 * math.cos(t * 6 + ph * 2))); o.keyframe_insert("location", frame=f)
        sc = 1.0 if not (goes and t >= T_THIN) else max(0.0001, 1 - (t - T_THIN) / 0.25)
        if t < t3 - 0.05 or t >= t4: sc = 0.0001
        o.scale = (sc, sc, sc); o.keyframe_insert("scale", frame=f)
    vis(AIR_T, t3 - 0.05 <= t < t4, f)
    vis(VOL_T, t5 - 0.05 <= t < t6 - 0.05, f); vis(NEED_T, t5 + 0.5 <= t < t6 - 0.05, f)   # hidden in the close-up (edge crop)
    vis(BAGS, t4 - 0.05 <= t < t5, f)
    # speed bars race (rip bar 570 vs sound 240 -> lengths 0.84 / 0.354 m)
    u = smooth((t - T_BARS) / 0.9)
    RIPB.scale = (max(0.0001, 0.84 * u), 1, 1) if t >= T_BARS and t < T_LOOP else (0.0001,) * 3
    SNDB.scale = (max(0.0001, 0.354 * u), 1, 1) if t >= T_BARS and t < T_LOOP else (0.0001,) * 3
    RIPB.keyframe_insert("scale", frame=f); SNDB.keyframe_insert("scale", frame=f)
    vis(RIP_T, T_BARS <= t < tc, f); vis(SND_T, T_BARS + 0.2 <= t < tc, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -1.10, 1.30), (0.0, -0.02, 1.08), (0.0, -1.04, 1.29), (0.0, -0.02, 1.08))
SEG = [
    (0.0, t2 - 0.05, HOOK, 20, 20),
    (t2 - 0.05, t3 - 0.05, fixed((MX + 0.3, -2.6, 1.15), (MX + 0.05, 0, 0.80), (MX + 0.1, -1.9, 1.0), (MX + 0.0, 0, 0.76)), 22, 24),
    (t3 - 0.05, t5 - 0.05, fixed((MX - 0.05, -1.75, 1.02), (MX - 0.05, 0, 0.72), (MX - 0.05, -1.62, 1.0), (MX - 0.05, 0, 0.72)), 24, 24),
    (t5 - 0.05, t6 - 0.05, fixed((MX + 0.08, -1.85, 1.10), (MX + 0.1, 0, 0.82), (MX + 0.12, -1.95, 1.12), (MX + 0.12, 0, 0.85)), 24, 24),
    (t6 - 0.05, t7 - 0.05, fixed((BX, -1.25, 1.0), (BX, 0, 0.90), (BX, -1.15, 1.0), (BX, 0, 0.90)), 26, 26),
    (t7 - 0.05, T_LOOP, fixed((MX, -1.9, 1.05), (MX, 0, 0.80), (MX, -1.8, 1.04), (MX, 0, 0.80)), 24, 24),
    (T_LOOP, DUR + 0.01, HOOK, 20, 20),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "hs": T_HS, "hp": T_HP, "set": T_SET,
           "thin": T_THIN, "sw": T_SW, "mal": T_MAL, "bag": T_BAG, "glv": T_GLV, "rip": T_RIP, "pop": T_POP, "bars": T_BARS},
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
