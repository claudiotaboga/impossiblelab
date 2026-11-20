"""The Impossible Lab #15 - a scoop of ice cream on Mercury's night side (E13 reel 1: consequence in motion at t = 0).
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


# ================= episode 15: Earth stops spinning for one second =================
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def kf_input(m, name, f, v):
    i = bsdf(m).inputs[name]; i.default_value = v; i.keyframe_insert("default_value", frame=f)
def globe_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.55
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 6
    rp = nt.nodes.new("ShaderNodeValToRGB"); el = rp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (0.03, 0.14, 0.45, 1); el[1].position = 1.0; el[1].color = (0.55, 0.45, 0.25, 1)
    e = el.new(0.52); e.color = (0.05, 0.20, 0.55, 1)
    e = el.new(0.545); e.color = (0.18, 0.42, 0.14, 1)
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    return m

M_WOOD = noise_mat("wood", (0.42, 0.24, 0.12), (0.58, 0.36, 0.18), 6.0, 0.5)
M_WALL = mat("wall", (0.07, 0.09, 0.13), 0.8)
M_FLOOR = tiles("floor", (0.80, 0.78, 0.74), (0.45, 0.42, 0.40), 3.0)
M_MUG = mat("mug", (0.85, 0.18, 0.12), 0.3)
M_COFFEE = mat("coffee", (0.16, 0.07, 0.03), 0.08)
M_PLATE = mat("plate", (0.94, 0.94, 0.96), 0.25)
M_APPLE = mat("apple", (0.75, 0.08, 0.06), 0.35)
M_BOOK = mat("book", (0.12, 0.35, 0.75), 0.6)
M_STEAM = mat("steam", (1, 1, 1), 0.5, 0, (1, 1, 1), 0.6)
M_STREAK = mat("streak", (1, 1, 1), 0.5, 0, (1, 1, 1), 2.5)
M_GLOBE = globe_mat("globe")
M_RING = mat("ring", (1.0, 0.45, 0.05), 0.4, 0, (1.0, 0.42, 0.04), 2.2)
M_RING45 = mat("ring45", (0.3, 1.0, 0.5), 0.4, 0, (0.3, 1.0, 0.5), 4.0)
M_SOUND = mat("soundbar", (0.85, 0.88, 0.95), 0.4, 0, (0.8, 0.85, 1.0), 1.2)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.62, 0.15), 5.0)
M_RED = mat("red", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 3.0)
M_GREEN = mat("grn", (0.3, 1.0, 0.5), 0.4, 0, (0.3, 1.0, 0.5), 3.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_DIV = mat("div", (1, 1, 1), 0.4, 0, (1, 1, 1), 2.0)
M_STAR = mat("star", (1, 1, 1), 0.5, 0, (1, 1, 1), 6.0)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.004, 0.006, 0.016, 1); WBG.inputs[1].default_value = 1.0

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_STOP = t2 + 1.05            # "...for one second." -> globe halts
LAUNCH = [0.08, t3 + 0.95]    # hook launch, line-3 launch ("Your mug doesn't.")
T_MINI = t4 + 0.55            # small mug leaves the equator tangentially
T_BARS1 = t4 + 1.35           # cut to the speed bars (equator 465 vs sound 343)
T_BARS2 = t5 + 1.15           # cut to the bars again: 465 -> 329 at 45 deg
def ramp(t, a, b, v0, v1):
    return v0 + (v1 - v0) * (1 - (1 - max(0.0, min(1.0, (t - a) / (b - a)))) ** 3)
def label(body, loc, size, m, align="CENTER", rot=TR):
    o = text(body, loc, rot, size, m, align); noshadow(o); o.visible_glossy = False; return o
def stars(x0, x1, y, z0, z1, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        sphere((rnd.uniform(x0, x1), y + rnd.uniform(0, 4), rnd.uniform(z0, z1)), rnd.uniform(0.02, 0.05), M_STAR, "star", None, 6)

# ---------- props ----------
TOP = 0.75
def table(x):
    box((x, 0, TOP - 0.03), (0.9, 0.6, 0.06), M_WOOD, "tabletop")
    for dx in (-0.38, 0.38):
        for dy in (-0.24, 0.24):
            box((x + dx, dy, (TOP - 0.06) / 2), (0.06, 0.06, TOP - 0.06), M_WOOD, "leg")
def mug(name, loc, scale=1.0):
    e = empty(name, loc)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.085, depth=0.2, location=(0, 0, 0.1))
    o = bpy.context.object; bpy.ops.object.shade_smooth(); link(o, M_MUG, e)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.075, depth=0.01, location=(0, 0, 0.185))
    link(bpy.context.object, M_COFFEE, e)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.055, minor_radius=0.014, location=(0.095, 0, 0.1), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; bpy.ops.object.shade_smooth(); link(o, M_MUG, e)
    e.scale = (scale,) * 3
    return e
def tableset(x, tag):
    """mug + plate with an apple + a book on one table; returns movable roots with rest positions"""
    items = []
    items.append((mug(tag + "mug", (x - 0.2, -0.05, TOP), 1.25), V((x - 0.2, -0.05, TOP))))
    pe = empty(tag + "plate", (x + 0.17, -0.1, TOP))
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.15, depth=0.02, location=(0, 0, 0.01)); link(bpy.context.object, M_PLATE, pe)
    sphere((0, 0, 0.085), 0.07, M_APPLE, "apple", pe, 16)
    items.append((pe, V((x + 0.17, -0.1, TOP))))
    be = empty(tag + "book", (x + 0.02, 0.16, TOP))
    box((0, 0, 0.03), (0.34, 0.24, 0.06), M_BOOK, "book", be)
    items.append((be, V((x + 0.02, 0.16, TOP))))
    return items

# ---------- HOOK set: NORMAL EARTH (left) vs STOPPED EARTH (right) ----------
LX, RX = -0.52, 0.52
box((0, -1.5, -0.05), (6, 9, 0.1), M_FLOOR, "floor")
box((0, 0.9, 1.8), (6, 0.1, 3.8), M_WALL, "wall")
box((0, 0.1, 1.4), (0.02, 1.6, 3.0), M_DIV, "divider")
table(LX); table(RX)
ITEMS_L = tableset(LX, "L"); ITEMS_R = tableset(RX, "R")
HL = [label("NORMAL EARTH", (LX, 0.5, 1.66), 0.10, M_LBLB), label("MUG STAYS PUT", (LX, 0.5, 1.47), 0.075, M_WHITE)]
HL += [label("STOPPED EARTH", (RX, 0.5, 1.66), 0.10, M_LBL), label("MUG: 465 m/s →", (RX, 0.5, 1.46), 0.085, M_RED)]
LBL_G = label("GROUND: STOPPED", (RX, 0.5, 1.22), 0.075, M_WHITE)
STEAM = [sphere((0, 0, 0), 0.025, M_STEAM, "steam", None, 8) for k in range(7)]
for o in STEAM: noshadow(o)
STREAKS = []
rnd = random.Random(5)
for k in range(9):
    o = box((0, 0, 0), (1.0, 0.012, 0.012), M_STREAK, "streak"); noshadow(o)
    STREAKS.append((o, V((RX + rnd.uniform(-0.3, 0.3), -0.15 + rnd.uniform(-0.1, 0.2), TOP + rnd.uniform(0.05, 0.35)))))
DROPS = []
for k in range(7):
    o = sphere((RX - 0.2 + k * 0.09, -0.05 + rnd.uniform(-0.03, 0.03), TOP + 0.002), 0.022 + 0.008 * (k % 2), M_COFFEE, "drop", None, 10)
    o.scale = (1.6, 1.0, 0.18); bpy.ops.object.transform_apply(scale=True); DROPS.append(o)
kl = bpy.data.objects.new("kitchen", bpy.data.lights.new("kitchen", "AREA")); kl.data.energy = 520; kl.data.size = 4
kl.data.color = (1.0, 0.88, 0.7); kl.location = (-1.2, -3.2, 3.4); kl.rotation_euler = (math.radians(50), 0, math.radians(-20)); S.collection.objects.link(kl)
kl2 = bpy.data.objects.new("kitchen2", bpy.data.lights.new("kitchen2", "AREA")); kl2.data.energy = 300; kl2.data.size = 3
kl2.data.color = (0.85, 0.9, 1.0); kl2.location = (1.6, -3.0, 2.6); kl2.rotation_euler = (math.radians(55), 0, math.radians(25)); S.collection.objects.link(kl2)

# ---------- GLOBE set ----------
GX, GZ, GR = 30.0, 1.3, 1.0
GROOT = empty("groot", (GX, 0, GZ))
GLOBE = sphere((0, 0, 0), GR, M_GLOBE, "globe", GROOT, 64)
bpy.ops.mesh.primitive_torus_add(major_radius=GR * 1.005, minor_radius=0.013, location=(GX, 0, GZ)); RING_EQ = bpy.context.object
link(RING_EQ, M_RING); noshadow(RING_EQ)
la = math.radians(45)
bpy.ops.mesh.primitive_torus_add(major_radius=GR * math.cos(la) * 1.007, minor_radius=0.013, location=(GX, 0, GZ + GR * math.sin(la))); RING_45 = bpy.context.object
link(RING_45, M_RING45); noshadow(RING_45)
MINI = mug("minimug", (GX, -GR - 0.02, GZ - 0.06), 0.8); MINI.rotation_euler = (math.radians(90), 0, 0)
POLE_MUG = mug("polemug", (GX, 0, GZ + GR - 0.005), 0.9)
PSTEAM = [sphere((0, 0, 0), 0.02, M_STEAM, "psteam", None, 8) for k in range(6)]
for o in PSTEAM: noshadow(o)
G_T1 = label("", (GX, -1.15, GZ - 0.12), 0.15, M_WHITE)
G_T2 = label("", (GX, -1.15, GZ - 0.36), 0.13, M_LBL)
P_T1 = label("NORTH POLE", (GX - 0.2, -0.1, GZ + GR + 0.36), 0.085, M_LBLB, "RIGHT")
P_T2 = label("≈ 0 m/s", (GX - 0.2, -0.1, GZ + GR + 0.2), 0.11, M_GREEN, "RIGHT")
L45 = label("45° N", (GX, -0.78, GZ + 0.98), 0.13, M_GREEN)
stars(GX - 8, GX + 8, 9.0, -4, 7, 200, 7)
sl = bpy.data.objects.new("sunl", bpy.data.lights.new("sunl", "AREA")); sl.data.energy = 900; sl.data.size = 2.5
sl.data.color = (1.0, 0.95, 0.88); sl.location = (GX - 3.0, -4.5, 3.0); sl.rotation_euler = (math.radians(60), 0, math.radians(-35)); S.collection.objects.link(sl)
fil = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA")); fil.data.energy = 140; fil.data.size = 4
fil.data.color = (0.6, 0.7, 1.0); fil.location = (GX + 3.5, -4.0, 2.5); fil.rotation_euler = (math.radians(60), 0, math.radians(40)); S.collection.objects.link(fil)

# ---------- BARS set ----------
BX = 60.0; X0 = BX - 1.05; SCL = 2.2 / 465
box((BX, 2.0, 1.3), (8, 0.1, 6), mat("bbg", (0.02, 0.03, 0.06), 0.9), "barbg")
BAR_S = box((0, 0, 0), (1, 0.2, 0.22), M_SOUND, "barS")
BAR_M = box((0, 0, 0), (1, 0.2, 0.22), M_RING, "barM")
B_S = label("SOUND · 343 m/s", (X0, -0.1, 2.23), 0.12, M_WHITE, "LEFT")
B_M = label("", (X0, -0.1, 1.43), 0.12, M_LBL, "LEFT")
B_V = label("", (X0, -0.1, 0.80), 0.11, M_RED, "LEFT")
for zz in (1.95, 1.15): noshadow(box((X0 + 343 * SCL, -0.12, zz), (0.018, 0.02, 0.4), M_DIV, "soundline"))
bl = bpy.data.objects.new("barl", bpy.data.lights.new("barl", "AREA")); bl.data.energy = 300; bl.data.size = 5
bl.location = (BX, -5, 3); bl.rotation_euler = (math.radians(60), 0, 0); S.collection.objects.link(bl)

# ---------- text handler ----------
def mug_speed(t):
    if t < T_BARS2: return 465
    return int(round(ramp(t, T_BARS2 + 0.15, T_BARS2 + 0.75, 465, 329)))
def handler(scene, *a):
    t = scene.frame_current / FPS
    if t < T_STOP:
        G_T1.data.body = "EARTH: SPINNING"; G_T2.data.body = ""
    elif t < t4 - 0.05:
        G_T1.data.body = "EARTH: STOPPED"; G_T2.data.body = "FOR 1 SECOND"
    elif t < t5:
        G_T1.data.body = "EQUATOR"; G_T2.data.body = "≈465 m/s"
    else:
        G_T1.data.body = ""; G_T2.data.body = ""
    v = mug_speed(t)
    B_M.data.body = f"{'EQUATOR' if v == 465 and t < T_BARS2 + 0.15 else '45° N'} MUG · {v} m/s"
    B_V.data.body = "FASTER THAN SOUND" if t < T_BARS2 + 0.2 else "JUST UNDER SOUND SPEED"
    G_T1.data.align_x = G_T2.data.align_x = "CENTER"
bpy.app.handlers.frame_change_pre.append(handler)

def last_launch(t):
    if t >= T_LOOP: return None
    # objects are reset (back on the table) during line 2 and until the line-3 launch
    if t3 - 0.05 <= t < LAUNCH[1]: return None
    if LAUNCH[0] <= t < t3 - 0.05: return LAUNCH[0]
    if t >= LAUNCH[1]: return LAUNCH[1]
    return None

for f in range(0, N + 1):
    t = f / FPS
    li = last_launch(t)
    s = (t - li) if li is not None else -1
    # right-table items: launch east (+x) with motion stretch
    for k, (o, p0) in enumerate(ITEMS_R):
        if s < 0:
            o.location = p0; o.scale = (1, 1, 1)
        else:
            dx = 3.0 * s + 12 * s * s
            o.location = p0 + V((dx, 0, 0.02 * k * min(s * 8, 1)))
            st = 1 + 5 * min(s / 0.08, 1)
            o.scale = (st, 1, 1) if dx < 3.0 else (0.0001,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    for k, (o, p0) in enumerate(STREAKS):
        on = 0 <= s < 0.7
        if on:
            u = s / 0.7; o.location = p0 + V((0.25 + 0.6 * u + 0.05 * k, 0, 0)); o.scale = (0.25 + 0.5 * (k % 3) / 2, 1, 1)
        else:
            o.scale = (0.0001,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    for k, o in enumerate(DROPS):
        vis(o, s >= 0.03 * k, f)
    # hook steam (left mug) + pole steam
    for k, o in enumerate(STEAM):
        ph = (t * 0.35 + k / len(STEAM)) % 1.0
        o.location = (LX - 0.22 + 0.03 * math.sin(6 * ph + k), -0.05, TOP + 0.24 + 0.45 * ph)
        o.scale = ((1 - ph) * 1.2,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    for k, o in enumerate(PSTEAM):
        ph = (t * 0.3 + k / len(PSTEAM)) % 1.0
        o.location = (GX + 0.025 * math.sin(6 * ph + k), 0, GZ + GR + 0.2 + 0.35 * ph)
        o.scale = ((1 - ph) * 1.1,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    # globe spin: steady until T_STOP, then dead stop with a small shudder
    ang = 1.7 * min(t, T_STOP)
    sh = 0.03 * math.exp(-(t - T_STOP) * 10) * math.sin((t - T_STOP) * 60) if t >= T_STOP else 0
    GROOT.rotation_euler = (0, 0, ang + sh); GROOT.keyframe_insert("rotation_euler", frame=f)
    vis(RING_EQ, t < T_STOP or (t4 - 0.05 <= t < t5 + 1.0), f)
    vis(RING_45, t5 - 0.05 <= t < t6 - 0.05, f)
    vis(L45, t5 - 0.05 <= t < t6 - 0.05, f)
    vis(P_T1, t >= t7 - 0.1, f); vis(P_T2, t >= t7 - 0.1, f)
    # mini mug on the equator: leaves tangentially (east) at T_MINI
    sm = t - T_MINI
    MINI.location = (GX + (0 if sm < 0 else 1.6 * sm + 6 * sm * sm), -GR - 0.02, GZ - 0.06)
    MINI.scale = (0.8,) * 3 if (t4 - 0.05 <= t < T_BARS1) and (sm < 0 or 1.6 * sm + 6 * sm * sm < 2.0) else (0.0001,) * 3
    MINI.keyframe_insert("location", frame=f); MINI.keyframe_insert("scale", frame=f)
    # pole mug: barely moves (a slow quarter-turn wobble over the whole shot)
    POLE_MUG.rotation_euler = (0, 0, 0.25 * smooth((t - t7) / 1.2)); POLE_MUG.keyframe_insert("rotation_euler", frame=f)
    vis(POLE_MUG, t >= t6 - 0.05, f, (0.9,) * 3)
    for o in PSTEAM:
        if t < t6 - 0.05: o.scale = (0.0001,) * 3; o.keyframe_insert("scale", frame=f)
    # bars grow at each bar cut
    for (o, v_fn, z) in ((BAR_S, lambda tt: 343, 1.95), (BAR_M, mug_speed, 1.15)):
        tb = T_BARS1 if t < T_BARS2 - 0.05 else T_BARS2
        g = smooth((t - tb) / 0.45) if tb == T_BARS1 else 1.0
        ln = max(0.001, v_fn(t) * SCL * g)
        o.location = (X0 + ln / 2, 0, z); o.scale = (ln, 1, 1)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    # table jolt on "The ground stops."
    vis(LBL_G, t >= t3 + 0.15 and t < T_LOOP, f)
    for o in HL: vis(o, t < t3 - 0.05, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -4.9, 1.15), (0.0, 0, 1.0), (0.0, -4.6, 1.13), (0.0, 0, 1.0))
GLOBE_F = fixed((GX, -7.0, 1.45), (GX, 0, 1.25), (GX, -6.6, 1.42), (GX, 0, 1.25))
SEG = [
    (0.0, t2 - 0.05, HOOK, 30, 30),
    (t2 - 0.05, t3 - 0.05, GLOBE_F, 30, 30),
    (t3 - 0.05, t4 - 0.05, fixed((RX, -3.0, 1.05), (RX, 0, 1.0), (RX + 0.04, -2.8, 1.04), (RX + 0.04, 0, 1.0)), 30, 30),
    (t4 - 0.05, T_BARS1, fixed((GX, -6.2, 1.45), (GX, 0, 1.2), (GX, -5.9, 1.42), (GX, 0, 1.2)), 30, 30),
    (T_BARS1, t5 - 0.05, fixed((BX, -6.2, 1.35), (BX, 0, 1.3), (BX, -6.0, 1.35), (BX, 0, 1.3)), 30, 30),
    (t5 - 0.05, T_BARS2, fixed((GX, -5.6, 3.9), (GX, 0, 1.6), (GX, -5.4, 3.7), (GX, 0, 1.6)), 30, 30),
    (T_BARS2, t6 - 0.05, fixed((BX, -6.0, 1.35), (BX, 0, 1.3), (BX, -5.8, 1.35), (BX, 0, 1.3)), 30, 30),
    (t6 - 0.05, T_LOOP, fixed((GX, -3.6, 3.7), (GX, 0, 2.35), (GX, -3.45, 3.62), (GX, 0, 2.35)), 30, 30),
    (T_LOOP, DUR + 0.01, HOOK, 30, 30),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    # camera shake at the globe stop and at each launch
    shk = 0.0
    for te in [T_STOP] + LAUNCH:
        if 0 <= t - te < 0.4: shk += 0.03 * math.exp(-(t - te) * 9) * math.sin((t - te) * 70)
    cam.location = p + V((shk, 0, shk * 0.6)); cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "launch": LAUNCH, "stop": T_STOP,
           "mini": T_MINI, "bars1": T_BARS1, "bars2": T_BARS2, "pole": t6},
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
