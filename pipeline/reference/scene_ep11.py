"""The Impossible Lab #11 - your breath on Everest's summit.
Units: metres. Mannequin 1.75 m (pelvis origin, standing pelvis height 0.915).
Set (origin): SEA LEVEL plinth (x = -1.3, sand) vs EVEREST 8,849 m rock-and-snow peak (x = +1.3). Above each figure a
glass "breath" bubble: 30 molecules at sea level vs 10 on the summit, 1 in 5 red (O2) in both (air is still ~21 % O2,
pressure ~1/3). Line 3 shows the 20 missing molecules as ghosts; line 4 a BRAIN O2 gauge drains with a 0:00 -> 2:00
timer (frame_change_pre handler) and the lights dim on "lights out". Line 5: base camp (x = 40) with tents and a
climber; line 6: the climber stands on the summit with an orange oxygen bottle + mask, arms up. Last ~1.3 s: hook.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(11)
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

# ---------- person mannequin (pelvis at origin, faces -y, shoulders along x) ----------
STAND = 0.915
def person(name, shirt):
    body = empty(name)
    torso = sphere((0, 0, 0.30), 1.0, shirt, "torso", body, 22); torso.scale = (0.20, 0.12, 0.32)
    o = sphere((0, 0, 0.02), 1.0, M_PANTS, "hips", body, 22); o.scale = (0.18, 0.13, 0.13)
    cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
    sphere((0, 0, 0.76), 0.105, M_SKIN, "head", body, 20)
    arms, legs = [], []
    for side in (-1, 1):
        sh = empty(f"{name}sh{side}", (side * 0.21, 0, 0.5), body)
        cyl_between((0, 0, 0), (side * 0.03, 0, -0.30), 0.045, M_SKIN, sh, "upperarm")
        cyl_between((side * 0.03, 0, -0.30), (side * 0.04, 0, -0.58), 0.04, M_SKIN, sh, "forearm")
        sh.rotation_mode = "XYZ"; arms.append(sh)
    for side in (-1, 1):
        hp = empty(f"{name}hp{side}", (side * 0.09, 0, 0), body)
        cyl_between((0, 0, 0), (side * 0.01, 0, -0.45), 0.068, M_PANTS, hp, "thigh")
        cyl_between((side * 0.01, 0, -0.45), (side * 0.01, 0, -0.86), 0.05, M_SKIN, hp, "shin")
        ft = sphere((side * 0.01, -0.05, -0.88), 1.0, M_SHOE, "foot", hp, 12); ft.scale = (0.05, 0.12, 0.04)
        hp.rotation_mode = "XYZ"; legs.append(hp)
    body.rotation_mode = "XYZ"
    return {"body": body, "torso": torso, "arms": arms, "legs": legs}
def pose(P, f, loc, rot=(0, 0, 0), arm=0.15, leg=(0.0, 0.0), chest=1.0, arm_fwd=0.0):
    b = P["body"]; b.location = loc; b.rotation_euler = rot
    b.keyframe_insert("location", frame=f); b.keyframe_insert("rotation_euler", frame=f)
    P["torso"].scale = (0.20 * chest, 0.12 * chest ** 1.6, 0.32); P["torso"].keyframe_insert("scale", frame=f)
    for k, sh in enumerate(P["arms"]):
        side = -1 if k == 0 else 1
        sh.rotation_euler = (arm_fwd, -side * arm, 0); sh.keyframe_insert("rotation_euler", frame=f)
    for k, hp in enumerate(P["legs"]):
        hp.rotation_euler = (leg[k], 0, 0); hp.keyframe_insert("rotation_euler", frame=f)

M_SAND = noise_mat("sand", (0.78, 0.66, 0.45), (0.88, 0.78, 0.58), 6.0)
M_SNOW = noise_mat("snow", (0.86, 0.90, 0.97), (0.98, 0.99, 1.0), 3.0, 0.7)
M_ROCK = noise_mat("rock", (0.08, 0.08, 0.10), (0.22, 0.21, 0.24), 2.5)
M_CSNOW = noise_mat("csnow", (0.55, 0.60, 0.70), (0.74, 0.78, 0.86), 3.0, 0.8)
M_SEA = mat("sea", (0.05, 0.32, 0.55), 0.15)
M_PLINTH = mat("plinth", (0.10, 0.11, 0.13), 0.5)
M_GLASS = liquid("glass", (0.92, 0.97, 1.0), (0.85, 0.92, 1.0), 0.06)
M_N2 = mat("n2", (0.72, 0.76, 0.82), 0.4)
M_GHOST = mat("ghost", (1, 1, 1), 0.4, 0, (1, 1, 1), 1.5)
M_O2 = mat("o2", (1.0, 0.18, 0.10), 0.35, 0, (1.0, 0.18, 0.08), 2.5)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_SHIRT = mat("shirt", (0.95, 0.18, 0.08), 0.6)
M_JACKET = mat("jacket", (0.08, 0.55, 0.65), 0.6)
M_PANTS = mat("pants", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 5.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.7, 1.0), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_RED = mat("red", (1.0, 0.25, 0.15), 0.4, 0, (1.0, 0.25, 0.12), 3.0)
M_GAUGE = mat("gauge", (0.05, 0.05, 0.06), 0.5)
M_TENT = mat("tent", (1.0, 0.45, 0.05), 0.6)
M_TENT2 = mat("tent2", (0.95, 0.85, 0.10), 0.6)
M_TANK = mat("tank", (0.95, 0.42, 0.05), 0.3, 0.6)
M_MASK = mat("mask", (0.15, 0.15, 0.17), 0.4)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tcw = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tcw.outputs["Generated"], sep.inputs[0])
rpw = nt.nodes.new("ShaderNodeValToRGB"); e = rpw.color_ramp.elements
e[0].position = 0.45; e[0].color = (0.70, 0.78, 0.90, 1); e[1].position = 0.85; e[1].color = (0.12, 0.28, 0.62, 1)
nt.links.new(sep.outputs["Z"], rpw.inputs[0]); nt.links.new(rpw.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.6; sun.data.angle = math.radians(6); sun.data.color = (1.0, 0.96, 0.90)
sun.rotation_euler = (math.radians(40), 0, math.radians(-30)); S.collection.objects.link(sun)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA"))
fill.data.energy = 1200; fill.data.size = 10; fill.location = (0, -10, 6); fill.rotation_euler = (math.radians(60), 0, 0)
S.collection.objects.link(fill)
fill2 = bpy.data.objects.new("fill2", bpy.data.lights.new("fill2", "AREA"))
fill2.data.energy = 450; fill2.data.size = 8; fill2.location = (40, -10, 5); fill2.rotation_euler = (math.radians(65), 0, 0)
S.collection.objects.link(fill2)

# ---------- hook / story set (origin): SEA LEVEL (x = -1.3) vs EVEREST SUMMIT (x = +1.3) ----------
LX, RX = -1.4, 1.4
LTOP, RTOP = 0.9, 1.7
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0)); link(bpy.context.object, M_PLINTH)
box((LX, 0, LTOP / 2), (2.0, 1.8, LTOP), M_PLINTH, "lplinth")
box((LX, 0, LTOP + 0.06), (2.0, 1.8, 0.12), M_SAND, "sand")
box((LX, 0.75, LTOP + 0.08), (2.0, 0.3, 0.1), M_SEA, "sea")
bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=1.15, radius2=0.42, depth=RTOP, location=(RX, 0.05, RTOP / 2))
cone = bpy.context.object; link(cone, M_ROCK); cone.rotation_euler = (0, 0, 0.3)
bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=0.72, radius2=0.40, depth=0.7, location=(RX, 0.05, RTOP - 0.33))
cap = bpy.context.object; link(cap, M_SNOW); cap.rotation_euler = (0, 0, 0.3)
text("SEA LEVEL", (LX, -0.92, 0.6), TR, 0.27, M_LBLB)
text("EVEREST 8,849 m", (RX, -1.25, 0.6), TR, 0.24, M_LBL)
sign = box((RX, -1.2, 0.6), (1.95, 0.04, 0.42), M_GAUGE, "sign")

# breath bubbles: same 1/5 oxygen, summit holds a third of the molecules
BZ = 3.35; BR = 0.42
def bubble(cx, n, seed):
    rnd = random.Random(seed)
    g = sphere((cx, 0, BZ), BR, M_GLASS, "bubble", None, 32); noshadow(g)
    mols = []
    for i in range(n):
        while True:
            p = V((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))
            if p.length < 1: break
        m = M_O2 if i % 5 == 0 else M_N2
        o = sphere(V((cx, 0, BZ)) + p * (BR - 0.08), 0.06, m, "mol", None, 10)
        mols.append((o, V((cx, 0, BZ)) + p * (BR - 0.07), rnd.uniform(0, 6.28)))
    return g, mols
BL, MOL_L = bubble(LX, 30, 1)
BRt, MOL_R = bubble(RX, 10, 2)
# ghost molecules: the two thirds missing on the summit (appear on line 3)
rnd = random.Random(5); GHOST = []
for i in range(20):
    while True:
        p = V((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))
        if p.length < 1: break
    o = sphere(V((RX, 0, BZ)) + p * (BR - 0.08), 0.06, M_GHOST, "ghost", None, 10); noshadow(o); GHOST.append(o)
    wm = o.modifiers.new("wf", "WIREFRAME"); wm.thickness = 0.008
PCT_L = text("21% O₂", (LX, -0.05, BZ - BR - 0.17), TR, 0.16, M_WHITE)
PCT_R = text("21% O₂", (RX, -0.05, BZ - BR - 0.17), TR, 0.16, M_WHITE)
THIRD = text("⅓ THE AIR", (RX, -0.05, BZ - BR - 0.17), TR, 0.16, M_LBL)
FULL = text("FULL", (LX, -0.05, BZ - BR - 0.17), TR, 0.16, M_LBLB)

# brain-oxygen gauge next to the summit figure (line 4)
GX = RX + 0.95; GZ0 = RTOP + 0.05; GH = 0.7
gauge = empty("gauge")
box((GX, -0.2, GZ0 + GH / 2), (0.24, 0.06, GH + 0.08), M_GAUGE, "gframe", gauge)
gfill = box((0, 0, 0.5), (0.17, 0.05, 1.0), M_O2, "gfill")
bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
gfill.location = (GX, -0.24, GZ0)
gtxt = text("BRAIN O₂", (GX, -0.24, GZ0 + GH + 0.16), TR, 0.12, M_WHITE, parent=gauge)
timer = text("0:00", (GX, -0.24, GZ0 - 0.16), TR, 0.14, M_LBL, parent=gauge)

# ---------- base camp set (x = 40) ----------
CX = 40.0
bpy.ops.mesh.primitive_plane_add(size=80, location=(CX, 8, 0.01)); link(bpy.context.object, M_CSNOW)
for (dx, dy, m) in ((-1.6, 0.6, M_TENT), (0.2, 1.4, M_TENT2), (1.7, 0.4, M_TENT), (-0.4, 3.2, M_TENT2)):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.75, radius2=0, depth=0.9, location=(CX + dx, dy, 0.45))
    t_ = bpy.context.object; t_.rotation_euler = (0, 0, math.radians(45)); link(t_, m)
for i in range(5):
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=6 + 2 * i, radius2=0.5, depth=7 + 3 * (i % 3), location=(CX - 16 + 8 * i, 30 + 4 * (i % 2), 3.5 + 1.5 * (i % 3)))
    link(bpy.context.object, M_CSNOW)
box((CX, -1.22, 2.2), (3.6, 0.04, 0.85), M_GAUGE, "campsign")
CAMP_LBL = text("BASE CAMP", (CX, -1.3, 2.35), TR, 0.30, M_LBL)
WEEKS_LBL = text("WEEKS OF ADAPTING", (CX, -1.3, 2.0), TR, 0.20, M_WHITE)
for o in (CAMP_LBL, WEEKS_LBL): o.visible_shadow = False

FIG_L = person("figL", M_SHIRT)
FIG_R = person("figR", M_SHIRT)
FIG_C = person("figC", M_JACKET)      # climber (camp, then summit with oxygen)
tankset = empty("tankset", (0, 0, 0), FIG_C["body"])
cyl_between((0, 0.17, 0.05), (0, 0.17, 0.55), 0.09, M_TANK, tankset, "o2tank")
mask = box((0, -0.10, 0.73), (0.12, 0.06, 0.09), M_MASK, "mask", tankset)
cyl_between((0, 0.17, 0.55), (0.0, -0.08, 0.70), 0.015, M_MASK, tankset, "hose", caps=False)

O2LBL = text("BOTTLED O\u2082", (RX + 0.85, -0.35, RTOP + 1.1), TR, 0.14, M_LBL)

# ---------- timing ----------
t2, t3, t4, t5, t6 = (L[i]["start"] for i in range(2, 7))
tc = CARD_START
W4 = {w["w"]: w["t"] for w in L[4]["words"]}
T_OUT = W4["lights"]                         # lights out
T_SUMMIT2 = t6 + 0.80                        # cut to the summit with oxygen
T_LOOP = tc + 0.25                           # back to the hook framing

def mode_of(t):
    if t < t2: return "hook"
    if t < t3: return "bubbles"
    if t < t4: return "third"
    if t < t5: return "faint"
    if t < T_SUMMIT2: return "camp"
    if t < T_LOOP: return "oxygen"
    return "hook"

def timer_txt(scene, *a):
    t = scene.frame_current / FPS
    if t < t4: s = 0
    else: s = min(120, int(120 * min((t - t4 - 0.2) / (T_OUT - t4 - 0.1), 1.0))) if t > t4 + 0.2 else 0
    timer.data.body = f"{s // 60}:{s % 60:02d}"
bpy.app.handlers.frame_change_pre.append(timer_txt)

SIT = 0.14   # pelvis height above the surface when sitting slumped
for f in range(0, N + 1):
    t = f / FPS; m = mode_of(t)
    # sea-level figure: standing, breathing easy
    pose(FIG_L, f, V((LX, 0.05, LTOP + 0.12 + STAND)), arm=math.radians(12 + 3 * math.sin(t * 2)), chest=1.0 + 0.04 * math.sin(t * 2.2))
    # summit figure: sitting, slumping forward; lies down at lights out
    if m in ("hook",):
        u = t if t < t2 else t - DUR
        k = smooth((u + 1.0) / 2.2)                        # slumps during the hook; looped
        pose(FIG_R, f, V((RX, 0.05, RTOP + SIT)), rot=(0.15 + 0.55 * k, 0, 0), arm=math.radians(10), leg=(-1.45, -1.35),
             chest=1.0 + 0.08 * math.sin(t * 7))
    elif m in ("bubbles", "third"):
        pose(FIG_R, f, V((RX, 0.05, RTOP + SIT)), rot=(0.7, 0, 0), arm=math.radians(10), leg=(-1.45, -1.35), chest=1.0 + 0.08 * math.sin(t * 7))
    elif m == "faint":
        k = smooth((t - T_OUT + 0.15) / 0.5)
        pose(FIG_R, f, V((RX - 0.0, 0.05 - 0.25 * k, RTOP + SIT - 0.02 * k)), rot=(0.7 + 0.85 * k, 0, 0), arm=math.radians(10 + 40 * k),
             leg=(-1.45 + 0.3 * k, -1.35 + 0.3 * k), chest=1.0 + 0.08 * math.sin(t * 7) * (1 - k))
    else:
        pose(FIG_R, f, V((RX, 0.05, -30)))
    # climber: camp, then summit with oxygen
    if m == "camp":
        pose(FIG_C, f, V((CX + 0.3, -0.4, STAND)), rot=(0, 0, math.radians(-15)), arm=math.radians(15 + 4 * math.sin(t * 2)),
             chest=1.0 + 0.04 * math.sin(t * 2))
    elif m == "oxygen":
        k = smooth((t - T_SUMMIT2) / 0.6)
        pose(FIG_C, f, V((RX, 0.05, RTOP + STAND - 0.05)), rot=(0, 0, math.radians(30)), arm=math.radians(20 + 140 * k), chest=1.0 + 0.04 * math.sin(t * 2))
    else:
        pose(FIG_C, f, V((CX, 0, -30)))
    vis(tankset, m == "oxygen", f); vis(O2LBL, m == "oxygen" and t > T_SUMMIT2 + 0.3, f)
    vis(BRt, m != "oxygen", f)
    for (o, p0, ph) in MOL_R: vis(o, m != "oxygen", f)
    # bubble molecules jitter; on the oxygen shot the summit bubble refills with red O2
    for (o, p0, ph) in MOL_L + MOL_R:
        o.location = p0 + V((0.02 * math.sin(t * 5 + ph), 0.02 * math.cos(t * 4 + ph), 0.02 * math.sin(t * 6 + 2 * ph)))
        o.keyframe_insert("location", frame=f)
    for i, g in enumerate(GHOST):
        vis(g, m == "third" and t > t3 + 0.6 + 0.03 * i, f)
    vis(PCT_L, m in ("bubbles",), f); vis(PCT_R, m in ("bubbles",), f)
    vis(THIRD, m == "third", f); vis(FULL, m == "third", f)
    vis(gauge, m == "faint", f)
    lvl = 1.0 if t < t4 + 0.2 else max(0.06, 1.0 - 0.94 * (t - t4 - 0.2) / (T_OUT - t4 - 0.1))
    gfill.scale = (1, 1, GH * lvl) if m == "faint" else (0.0001, 0.0001, 0.0001); gfill.keyframe_insert("scale", frame=f)
    # lights out: dim the sun/fills/world after "lights"
    dim = 1.0
    if m == "faint" and t > T_OUT: dim = 1.0 - 0.85 * smooth((t - T_OUT) / 0.35)
    sun.data.energy = 3.6 * dim; sun.data.keyframe_insert("energy", frame=f)
    fill.data.energy = 1200 * dim; fill.data.keyframe_insert("energy", frame=f)
    bg.inputs[1].default_value = 1.0 * (0.25 + 0.75 * dim); bg.inputs[1].keyframe_insert("default_value", frame=f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.15, -11.0, 2.1), (0.0, 0, 1.75), (0.1, -10.5, 2.05), (0.0, 0, 1.75))
SEG = [
    (0.0, t2 - 0.05, HOOK, 27, 28),
    (t2 - 0.05, t3 - 0.05, fixed((0.0, -9.6, BZ - 0.4), (0.0, 0, BZ - 0.74), (0.0, -9.0, BZ - 0.4), (0.0, 0, BZ - 0.74)), 30, 30),
    (t3 - 0.05, t4 - 0.05, fixed((RX + 0.15, -5.8, BZ - 0.2), (RX, 0, BZ - 0.45), (RX + 0.05, -5.3, BZ - 0.2), (RX, 0, BZ - 0.45)), 30, 31),
    (t4 - 0.05, t5 - 0.05, fixed((RX + 0.6, -5.4, RTOP + 0.95), (RX + 0.35, 0, RTOP + 0.42), (RX + 0.5, -4.9, RTOP + 0.85), (RX + 0.35, 0, RTOP + 0.4)), 30, 30),
    (t5 - 0.05, T_SUMMIT2, fixed((CX + 0.2, -7.6, 1.9), (CX, 0, 1.25), (CX + 0.1, -7.0, 1.85), (CX, 0, 1.25)), 28, 28),
    (T_SUMMIT2, T_LOOP, fixed((RX + 0.35, -6.0, RTOP + 1.3), (RX + 0.25, 0, RTOP + 1.0), (RX + 0.3, -5.6, RTOP + 1.3), (RX + 0.25, 0, RTOP + 1.0)), 30, 30),
    (T_LOOP, DUR + 0.01, HOOK, 27, 26),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0])); spec = seg[2]
    _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_out": T_OUT, "t_summit2": T_SUMMIT2, "t_loop": T_LOOP, "t_card": tc,
           "cuts": [s[0] for s in SEG[1:]], "molecules_sea": 30, "molecules_summit": 10, "o2_share": "1 in 5 both"},
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
