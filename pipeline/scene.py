"""The Impossible Lab #08 - shrunk to 1 cm tall.
Units: the mannequin is 1.75 units tall = 1 cm real, so 1 unit = 5.71 mm (scale factor 175).
Shots: (hook) lab balance on a patio stone: a 5 mm raindrop (65 mg) outweighs the 1 cm person (13 mg);
shrink on a ruler; gentle fall from a garden wall (terminal speed ~4 m/s); heat rings radiate away
(heat loss per kg x175); rain from below; a drop engulfs the figure; balance again, level:
13 mg of water (the clinging film, ~1.1x body mass, Haldane) vs the figure. Last second returns to the hook.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(8)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 6; S.cycles.glossy_bounces = 2; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 4; S.cycles.transparent_max_bounces = 2
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"

from timeline import LINES, CARD_START
L = {l["i"]: l for l in LINES}
V = Vector

def mat(name, base=(0.5, 0.5, 0.5), rough=0.5, metal=0.0, emit=None, estr=0.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Transmission Weight"].default_value = trans
    b.inputs["IOR"].default_value = ior
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    return m
def noise_mat(name, c1, c2, scale, bump_scale=None, bstr=0.4, rough=0.95):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 6
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*c1, 1); rp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    if bump_scale:
        nz2 = nt.nodes.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = bump_scale
        bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = bstr
        nt.links.new(nz2.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs[0], b.inputs["Normal"])
    return m

M_STONE = noise_mat("stone", (0.33, 0.31, 0.29), (0.55, 0.52, 0.48), 0.6, 9, 0.35)
M_GROUT = mat("grout", (0.18, 0.17, 0.16), 0.95)
M_GRASS = noise_mat("grass", (0.10, 0.28, 0.06), (0.25, 0.50, 0.12), 2.0, None, rough=0.7)
M_SOIL = noise_mat("soil", (0.12, 0.08, 0.05), (0.24, 0.17, 0.11), 1.5, 6, 0.4)
M_WALL = noise_mat("wall", (0.55, 0.30, 0.20), (0.70, 0.42, 0.30), 0.2, 3, 0.5, 0.9)
M_BRASS = mat("brass", (0.85, 0.62, 0.25), 0.25, 1.0)
M_STEEL = mat("steel", (0.75, 0.76, 0.78), 0.2, 1.0)
M_BASEBLK = mat("baseblk", (0.05, 0.05, 0.06), 0.4)
M_WATER = mat("water", (0.85, 0.93, 1.0), 0.02, 0, None, 0, 1.0, 1.33)
M_RULER = mat("ruler", (0.93, 0.88, 0.62), 0.5)
M_TICK = mat("tick", (0.05, 0.05, 0.05), 0.5)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_SHIRT = mat("shirt", (0.95, 0.55, 0.06), 0.6)
M_PANTS = mat("pants", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_HEAT = mat("heat", (1.0, 0.35, 0.05), 0.5, 0, (1.0, 0.35, 0.05), 8.0)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 5.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.7, 1.0), 5.0)
M_GLOW = mat("glow", (0.4, 0.75, 1.0), 0.5, 0, (0.4, 0.75, 1.0), 3.0)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tcw = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tcw.outputs["Generated"], sep.inputs[0])
rpw = nt.nodes.new("ShaderNodeValToRGB"); e = rpw.color_ramp.elements
e[0].position = 0.45; e[0].color = (0.55, 0.60, 0.66, 1); e[1].position = 0.85; e[1].color = (0.30, 0.42, 0.58, 1)
nt.links.new(sep.outputs["Z"], rpw.inputs[0]); nt.links.new(rpw.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.2
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.2; sun.data.angle = math.radians(8); sun.data.color = (1.0, 0.96, 0.90)
sun.rotation_euler = (math.radians(50), 0, math.radians(-35)); S.collection.objects.link(sun)

def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box", parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; bpy.ops.object.transform_apply(scale=True); return link(o, m, parent)
def cyl_between(a, b, r, m, parent=None, name="limb", caps=True, verts=18):
    a, b = V(a), V(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.name = name
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    bpy.ops.object.shade_smooth(); link(o, m, parent)
    if caps:
        for p in (a, b):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=7, radius=r, location=p)
            e = bpy.context.object; bpy.ops.object.shade_smooth(); link(e, m, parent)
    return o
def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); e.location = loc; S.collection.objects.link(e)
    if parent: e.parent = parent
    return e
def text(body, loc, rot, size, m, align="CENTER", parent=None):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object
    t.data.body = body; t.data.size = size; t.data.extrude = 0.01; t.data.align_x = align; t.data.align_y = "CENTER"
    return link(t, m, parent)
def sphere(loc, r, m, name="sph", parent=None, seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def vis(o, on, f, base=(1, 1, 1)):
    o.scale = base if on else (0.0001,) * 3; o.keyframe_insert("scale", frame=f)

# ---------- patio: stone slabs + grass border ----------
for i in range(-3, 4):
    for j in range(-3, 4):
        box((i * 16.2, j * 16.2, -0.5), (16, 16, 1.0), M_STONE, "slab")
box((0, 0, -0.62), (120, 120, 0.2), M_GROUT, "grout")
bpy.ops.mesh.primitive_plane_add(size=1500, location=(0, 0, -0.7)); link(bpy.context.object, M_SOIL)
for k in range(260):
    a = random.uniform(0, 2 * math.pi); d = random.uniform(60, 140)
    x, y = d * math.cos(a), d * math.sin(a)
    if y < -40 and abs(x) < 60: continue
    h = random.uniform(30, 75)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=random.uniform(1.0, 2.0), depth=h, location=(x, y, h / 2 - 0.7))
    o = bpy.context.object; o.scale = (1, 0.18, 1)
    o.rotation_euler = (random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), random.uniform(0, math.pi)); link(o, M_GRASS)

# ---------- lab balance (centre at origin) ----------
FUL_H = 4.2; ARM = 2.7; HANG = 2.2; PAN_R = 1.05
box((0, 0, 0.15), (3.0, 1.6, 0.3), M_BASEBLK, "base")
cyl_between((0, 0, 0.3), (0, 0, FUL_H - 0.15), 0.16, M_BRASS, caps=False)
sphere((0, 0, FUL_H), 0.22, M_BRASS)
beam = empty("beam", (0, 0, FUL_H)); beam.rotation_mode = "XYZ"
cyl_between((-ARM, 0, 0), (ARM, 0, 0), 0.09, M_BRASS, beam, "beambar")
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.25, depth=0.8, location=(0, 0, 0.35), rotation=(math.pi, 0, 0))
link(bpy.context.object, M_BRASS, beam)
pans = []
for s in (-1, 1):
    pe = empty(f"pan{s}")
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=PAN_R, depth=0.08, location=(0, 0, 0)); link(bpy.context.object, M_STEEL, pe)
    for k in range(3):
        a = k * 2 * math.pi / 3 + 0.5
        cyl_between((PAN_R * 0.9 * math.cos(a), PAN_R * 0.9 * math.sin(a), 0.04), (0, 0, HANG), 0.018, M_STEEL, pe, "string", caps=False, verts=6)
    pans.append(pe)
DROP_R = 2.5 / 5.71                                          # 5 mm raindrop -> radius 0.438 units
BLOB_R = ((3 * 13.06 / (4 * math.pi)) ** (1 / 3)) / 5.71     # 13 mg of water (= your mass) -> radius 0.256 units
drop_on_pan = sphere((0, 0, 0), DROP_R, M_WATER, "paddrop")
blob_on_pan = sphere((0, 0, 0), BLOB_R, M_WATER, "padblob")
TR = (math.radians(90), 0, 0)
LBL_YOU = text("YOU 13 mg", (0, 0, 0), TR, 0.48, M_LBLB)
LBL_DROP = text("DROP 65 mg", (0, 0, 0), TR, 0.48, M_LBL)
LBL_WATER = text("WATER 13 mg", (0, 0, 0), TR, 0.48, M_LBL)

# ---------- ruler (shrink shot) at x = 40 ----------
RX = 40.0; R0 = RX - 5.25; UNIT_CM = 1.75
box((RX, 0, 0.12), (12.5, 3.2, 0.24), M_RULER, "ruler")
for k in range(0, 61):
    xx = R0 + k * UNIT_CM / 10
    ln = 1.2 if k % 10 == 0 else (0.8 if k % 5 == 0 else 0.45)
    box((xx, 1.6 - ln / 2, 0.245), (0.03, ln, 0.01), M_TICK, "tick")
    if k % 10 == 0:
        text(str(k // 10), (xx, 0.35, 0.55), (math.radians(80), 0, 0), 0.6, M_TICK)
FX = R0 + UNIT_CM * 0.5                                       # figure stands between the 0 and 1 cm marks
CMBAR = [box((FX + 0.75, -0.4, 0.24 + UNIT_CM / 2), (0.05, 0.05, UNIT_CM), M_LBL, "cmbar"),
         box((FX + 0.75, -0.4, 0.26), (0.35, 0.05, 0.05), M_LBL, "cmt"),
         box((FX + 0.75, -0.4, 0.24 + UNIT_CM), (0.35, 0.05, 0.05), M_LBL, "cmt"),
         text("1 cm", (FX + 1.55, -0.4, 0.24 + UNIT_CM / 2), TR, 0.45, M_LBL)]
sphere((RX + 2.0, -1.0, 0.9), 0.75, M_STONE).scale = (1.4, 1.0, 0.8)

# ---------- garden wall (fall shot) at x = -60 ----------
WX = -60.0; WALL_H = 26.0
box((WX - 6, 0, WALL_H / 2 - 0.5), (12, 30, WALL_H), M_WALL, "wall")
for zz in range(1, 9):
    box((WX, 0, zz * 3.0), (0.05, 30.2, 0.12), M_GROUT, "mortar")
box((WX + 6, 0, -0.45), (16, 30, 0.6), M_SOIL, "bed")
for k in range(40):
    x = WX + random.uniform(4, 13); y = random.uniform(-12, 12); h = random.uniform(4, 11)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=random.uniform(0.4, 0.8), depth=h, location=(x, y, h / 2 - 0.3))
    o = bpy.context.object; o.scale = (1, 0.2, 1); o.rotation_euler = (random.uniform(-.3, .3), random.uniform(-.3, .3), random.uniform(0, 3)); link(o, M_GRASS)

# ---------- person mannequin (pelvis at origin, faces -y, shoulders along x) ----------
body = empty("body")
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.30))
o = bpy.context.object; o.scale = (0.20, 0.12, 0.32); bpy.ops.object.shade_smooth(); link(o, M_SHIRT, body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.02))
o = bpy.context.object; o.scale = (0.18, 0.13, 0.13); bpy.ops.object.shade_smooth(); link(o, M_PANTS, body)
cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
sphere((0, 0, 0.76), 0.105, M_SKIN, "head", body, 22)
arms, legs = [], []
for side in (-1, 1):
    sh = empty(f"shoulder{side}", (side * 0.21, 0, 0.5), body)
    cyl_between((0, 0, 0), (side * 0.03, 0, -0.30), 0.045, M_SKIN, sh, "upperarm")
    cyl_between((side * 0.03, 0, -0.30), (side * 0.04, 0, -0.58), 0.04, M_SKIN, sh, "forearm")
    sh.rotation_mode = "XYZ"; arms.append(sh)
for side in (-1, 1):
    hp = empty(f"hip{side}", (side * 0.09, 0, 0), body)
    cyl_between((0, 0, 0), (side * 0.01, 0, -0.45), 0.068, M_PANTS, hp, "thigh")
    cyl_between((side * 0.01, 0, -0.45), (side * 0.01, 0, -0.86), 0.05, M_SKIN, hp, "shin")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(side * 0.01, -0.05, -0.88))
    ft = bpy.context.object; ft.scale = (0.05, 0.12, 0.04); link(ft, M_SHOE, hp)
    hp.rotation_mode = "XYZ"; legs.append(hp)
body.rotation_mode = "XYZ"
STAND = 0.915
shell = sphere((0, 0, 0), 1.0, M_WATER, "shell", None, 40)
heat_rings = []
for k in range(4):
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.03, major_segments=48, minor_segments=6)
    o = bpy.context.object; link(o, M_HEAT); o.rotation_euler = (math.radians(90), 0, 0); heat_rings.append(o)
glow = sphere((0, 0, 0), 1.0, M_GLOW, "coldglow")
RAIN = []
for k in range(14):
    d = sphere((0, 0, 0), DROP_R * random.uniform(0.6, 1.05), M_WATER, "rain", None, 20)
    RAIN.append((d, random.uniform(-4, 4), random.uniform(-1.0, 4.0), random.uniform(0, 1)))
SPLASH = [sphere((0, 0, 0), random.uniform(0.05, 0.12), M_WATER, "spl", None, 12) for _ in range(16)]
SPL_DIR = [V((math.cos(a), math.sin(a) * 0.6, 0)) for a in [k * 2 * math.pi / 16 for k in range(16)]]
BIGDROP = sphere((0, 0, 0), DROP_R * 1.15, M_WATER, "bigdrop", None, 28)

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_STEP = t3 + 0.25
T_FALL = 1.45
T_LANDF = T_STEP + T_FALL
T_HIT = t6 + 0.20
HX = 26.0; HY = -22.0                                                    # heat / rain spot

def beam_angle(t, mode):
    if mode == "hook":
        tau = t if t < t2 else t - (tc + 0.9)
        return math.radians(6 + 8 * smooth(tau / 0.6)) if t < t2 else math.radians(14)
    if mode == "level": return math.radians(-7) * (1 - smooth((t - (t7 + 0.15)) / 1.1))
    return math.radians(14)

def place_balance(t, f, mode):
    a = beam_angle(t, mode); beam.rotation_euler = (0, a, 0); beam.keyframe_insert("rotation_euler", frame=f)
    for s, pe in zip((-1, 1), pans):
        tip = V((s * ARM * math.cos(a), 0, FUL_H - s * ARM * math.sin(a)))
        pe.location = tip - V((0, 0, HANG)); pe.keyframe_insert("location", frame=f)
    lp, rp = pans[0].location.copy(), pans[1].location.copy()
    drop_on_pan.location = rp + V((0, 0, 0.04 + DROP_R * 0.82)); drop_on_pan.keyframe_insert("location", frame=f)
    blob_on_pan.location = rp + V((0, 0, 0.04 + BLOB_R * 0.8)); blob_on_pan.keyframe_insert("location", frame=f)
    vis(drop_on_pan, mode == "hook", f, (1, 1, 0.82)); vis(blob_on_pan, mode == "level", f, (1, 1, 0.8))
    for o, pp in ((LBL_YOU, lp), (LBL_DROP, rp), (LBL_WATER, rp)):
        o.location = pp + V((0, -1.2, -0.75)); o.keyframe_insert("location", frame=f)
    vis(LBL_YOU, mode in ("hook", "level"), f); vis(LBL_DROP, mode == "hook", f)
    vis(LBL_WATER, mode == "level", f)
    return lp + V((0, 0, 0.04 + STAND))

def mode_of(t):
    if t < t2: return "hook"
    if t >= tc: return "level" if t < tc + 0.9 else "hook"
    if t < t3: return "ruler"
    if t < t4: return "fall"
    if t < t5: return "heat"
    if t < t7 - 0.05: return "rain"
    return "level"

POS = {}
for f in range(0, N + 1):
    t = f / FPS; m = mode_of(t)
    pelvis = place_balance(t, f, m)
    scl = 1.0; rot = (0, 0, 0); arm = math.radians(8); leg = 0.0
    if m in ("hook", "level"):
        p = pelvis; arm = math.radians(25 + 10 * math.sin(t * 3))
    elif m == "ruler":
        u = smooth((t - t2) / 0.9); scl = 3.2 - 2.2 * u
        p = V((FX, -0.4, 0.24 + STAND * scl)); arm = math.radians(10)
    elif m == "fall":
        x0 = WX + 0.6
        if t < T_STEP: p = V((x0 - 0.3, 0, WALL_H + STAND)); arm = math.radians(20)
        elif t < T_LANDF:
            u = (t - T_STEP) / T_FALL
            p = V((x0 + 1.6 * u, 0, WALL_H + STAND - WALL_H * (u ** 1.15)))
            arm = math.radians(120 + 25 * math.sin(t * 9)); leg = 0.3 * math.sin(t * 7)
            rot = (0.25 * math.sin(t * 4), 0, 0)
        else:
            k = min((t - T_LANDF) / 0.3, 1.0)
            p = V((x0 + 1.6, 0, STAND - 0.15 - 0.3 * math.sin(math.pi * k)))
            arm = math.radians(120 - 100 * smooth(k * 1.5)); leg = 0.4 * math.sin(math.pi * k)
    elif m == "heat":
        p = V((HX, HY, STAND)); arm = math.radians(10 + 6 * math.sin(t * 20))
    else:
        p = V((HX, HY, STAND)); arm = math.radians(15)
        if t > T_HIT: arm = math.radians(70); leg = 0.25
    body.location = p; body.scale = (scl,) * 3; body.rotation_euler = rot
    body.keyframe_insert("location", frame=f); body.keyframe_insert("scale", frame=f); body.keyframe_insert("rotation_euler", frame=f)
    for k, sh in enumerate(arms):
        side = -1 if k == 0 else 1
        sh.rotation_euler = (0, -side * arm, 0); sh.keyframe_insert("rotation_euler", frame=f)
    for k, hp in enumerate(legs):
        hp.rotation_euler = (leg * (1 if k == 0 else -1), 0, 0); hp.keyframe_insert("rotation_euler", frame=f)
    POS[f] = p.copy()
    for o in CMBAR: vis(o, m == "ruler" and t > t2 + 0.9, f)
    for k, o in enumerate(heat_rings):
        on = m == "heat"; ph = ((t - t4) * 0.9 + k / 4) % 1.0
        o.location = p + V((0, 0, -0.1)); o.keyframe_insert("location", frame=f)
        vis(o, on, f, (0.6 + 2.4 * ph,) * 3)
    g = smooth((t - t4) / (t5 - t4)) if m == "heat" else 0.0
    glow.location = p + V((0, 0, -0.05)); glow.keyframe_insert("location", frame=f)
    vis(glow, False, f, (0.30 * g + 0.0001, 0.22 * g + 0.0001, 0.98 * g + 0.0001))
    for d, dx, dy, ph in RAIN:
        z = 14 - ((t * 9 + ph * 14) % 14)
        d.location = V((HX + dx, HY + dy, z)); d.keyframe_insert("location", frame=f)
        vis(d, m == "rain", f, (1, 1, 1.25))
    if m == "rain" and t < T_HIT:
        BIGDROP.location = V((HX, HY, 2.0 + (T_HIT - t) * 14)); vis(BIGDROP, True, f, (1, 1, 1.2))
    else:
        BIGDROP.location = V((0, HY, 40)); vis(BIGDROP, False, f)
    BIGDROP.keyframe_insert("location", frame=f)
    wet = m == "rain" and t >= T_HIT; k = smooth((t - T_HIT) / 0.15)
    shell.location = p + V((0, 0, -0.05)); shell.keyframe_insert("location", frame=f)
    vis(shell, wet, f, (0.55 * k + 0.0001, 0.45 * k + 0.0001, 1.12 * k + 0.0001))
    for o, dvec in zip(SPLASH, SPL_DIR):
        u = t - T_HIT; on = m == "rain" and 0 <= u < 0.5
        o.location = (p + V((0, 0, -0.6)) + dvec * (u * 6) + V((0, 0, 4 * u - 9 * u * u))) if on else V((0, 0, -50))
        o.keyframe_insert("location", frame=f); vis(o, on, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((2.2, -17.5, 3.4), (0.0, 0, 2.0), (2.0, -16.6, 3.3), (0.0, 0, 2.0))
LEVEL = fixed((0.2, -17.6, 3.3), (0.2, 0, 2.0), (0.2, -17.0, 3.2), (0.2, 0, 2.0))
SEG = [
    (0.0, t2 - 0.05, HOOK, 26, 27),
    (t2 - 0.05, t3 - 0.05, fixed((FX + 0.4, -8.8, 3.0), (FX + 0.6, 0, 1.5), (FX + 0.4, -9.4, 3.2), (FX + 0.6, 0, 1.4)), 26, 26),
    (t3 - 0.05, T_STEP + 0.35, fixed((WX + 7.5, -9.5, WALL_H + 4.0), (WX + 0.8, 0, WALL_H - 0.3)), 28, 28),
    (T_STEP + 0.35, t4 - 0.05, ("follow", (5.0, -14.0, 1.2), (0.5, 0, 0.3)), 30, 30),
    (t4 - 0.05, t5 - 0.05, fixed((HX + 0.6, HY - 5.8, 1.6), (HX, HY, 0.85), (HX + 0.4, HY - 5.0, 1.5), (HX, HY, 0.85)), 30, 33),
    (t5 - 0.05, T_HIT - 0.05, fixed((HX + 1.2, HY - 9.0, 0.6), (HX, HY, 1.35), (HX + 1.0, HY - 8.2, 0.6), (HX, HY, 1.25)), 24, 24),
    (T_HIT - 0.05, t7 - 0.05, fixed((HX + 0.9, HY - 4.6, 0.8), (HX, HY, 0.9), (HX + 0.8, HY - 4.3, 0.85), (HX, HY, 0.9)), 30, 31),
    (t7 - 0.05, tc + 0.9, LEVEL, 25, 26),
    (tc + 0.9, DUR + 0.01, HOOK, 27, 26),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0])); spec = seg[2]
    if spec[0] == "follow":
        bp = POS[f]; p = bp + V(spec[1]); q = bp + V(spec[2]); p.z = max(p.z, 1.5)
    else:
        _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_step": T_STEP, "t_land": T_LANDF, "t_hit": T_HIT, "t_card": tc,
           "cuts": [s[0] for s in SEG[1:]], "drop_r_units": DROP_R, "blob_r_units": BLOB_R},
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
