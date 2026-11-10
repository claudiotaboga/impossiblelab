"""The Impossible Lab #04 - gravity reversed for one second.
Sunny city plaza with a red/white 10 m scale tower. A primitive mannequin (and every loose
object around it) falls UP ~4.9 m during the flipped second, coasts to ~9.8 m, falls back
(hard cut before landing). Twist: indoors, the ceiling stops the rise after <1 m.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(4)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 3; S.cycles.glossy_bounces = 1; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 0; S.cycles.transparent_max_bounces = 2
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"

from timeline import LINES, CARD_START
def sec(t): return t * FPS
L = {l["i"]: l for l in LINES}

# ---------- materials ----------
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
def brick_mat(name, c1, c2, mortar, scale, bw=0.5, rh=0.5, ms=0.015, rough=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    br = nt.nodes.new("ShaderNodeTexBrick"); br.offset = 0.5
    br.inputs["Color1"].default_value = (*c1, 1); br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (*mortar, 1); br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = ms
    br.inputs["Brick Width"].default_value = bw; br.inputs["Row Height"].default_value = rh
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return m

M_SKIN = mat("dummy", (0.78, 0.74, 0.70), 0.55)
M_SUIT = mat("suit", (0.05, 0.12, 0.30), 0.6)
M_GOGG = mat("goggles", (1.0, 0.45, 0.05), 0.3, 0, (1.0, 0.45, 0.05), 0.6)
M_PAVE = brick_mat("pave", (0.62, 0.60, 0.56), (0.55, 0.53, 0.50), (0.38, 0.36, 0.34), 0.9)
M_RED = mat("towerred", (0.75, 0.06, 0.04), 0.45)
M_WHT = mat("towerwhite", (0.88, 0.88, 0.86), 0.45)
M_MARK = mat("mark", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 3.0)
M_ARROW = mat("arrow", (1.0, 0.68, 0.18), 0.4, 0, (1.0, 0.62, 0.12), 6.0)
M_TRUNK = mat("trunk", (0.25, 0.16, 0.09), 0.8)
M_LEAF = mat("leaf", (0.10, 0.35, 0.08), 0.7)
BALLC = [(0.9, 0.15, 0.1), (0.1, 0.4, 0.9), (0.95, 0.75, 0.1), (0.15, 0.7, 0.3), (0.9, 0.9, 0.9), (0.8, 0.3, 0.7)]
M_BALL = [mat(f"ball{k}", c, 0.35) for k, c in enumerate(BALLC)]
M_CONE = mat("cone", (1.0, 0.35, 0.02), 0.5)
M_CRATE = mat("crate", (0.55, 0.38, 0.2), 0.8)
M_BLD = [brick_mat(f"bld{k}", (0.10, 0.14, 0.2), (0.12, 0.16, 0.22), c, 0.35, 0.35, 0.45, 0.3)
         for k, c in enumerate([(0.85, 0.80, 0.70), (0.70, 0.75, 0.80), (0.86, 0.62, 0.48), (0.78, 0.78, 0.74)])]
# interior
M_FLOOR = brick_mat("floor", (0.45, 0.28, 0.14), (0.40, 0.25, 0.12), (0.3, 0.18, 0.09), 1.2, 0.9, 0.12, 0.004, 0.4)
M_IWALL = mat("iwall", (0.80, 0.72, 0.60), 0.8)
M_ICEIL = mat("iceil", (0.92, 0.92, 0.90), 0.8)
M_SOFA = mat("sofa", (0.10, 0.35, 0.42), 0.8)
M_LAMP = mat("lamp", (1, 1, 1), 0.5, 0, (1.0, 0.9, 0.75), 12.0)
M_IWIN = mat("iwin", (1, 1, 1), 0.5, 0, (0.75, 0.88, 1.0), 3.0)
M_FRAME = mat("frame", (0.9, 0.55, 0.15), 0.5)

# ---------- world: clear midday sky ----------
world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.75, 0.85, 0.95, 1)
ramp.color_ramp.elements[1].position = 0.45; ramp.color_ramp.elements[1].color = (0.12, 0.35, 0.85, 1)
nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
nt.links.new(ramp.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 4.5; sun.data.angle = math.radians(2.0); sun.data.color = (1.0, 0.95, 0.85)
sun.rotation_euler = (math.radians(40), math.radians(10), math.radians(-35)); S.collection.objects.link(sun)

# ---------- helpers ----------
def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box", parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; return link(o, m, parent)
def cyl_between(a, b, r, m, parent, name="limb", caps=True):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=r, depth=d.length, location=(a + b) / 2)
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
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

# ---------- plaza ----------
box((0, 0, -0.05), (240, 240, 0.1), M_PAVE, "ground")
TX, TY = 1.3, 0.7                      # scale tower (10 x 1 m, red/white)
for k in range(10):
    box((TX, TY, k + 0.5), (0.32, 0.32, 1.0), M_RED if k % 2 == 0 else M_WHT, "tower")
for h in (5, 10):
    box((TX, TY, h), (0.62, 0.62, 0.05), M_MARK, f"mark{h}")
    bpy.ops.object.text_add(location=(TX + 0.36, TY - 0.17, h + 0.12), rotation=(math.radians(90), 0, 0))
    tx = bpy.context.object; tx.data.body = f"{h} m"; tx.data.size = 0.42; tx.data.extrude = 0.02
    tx.data.align_x = "LEFT"; link(tx, M_MARK)
# city blocks behind the plaza
for k in range(16):
    x = -60 + k * 8 + random.uniform(-1.5, 1.5); h = random.uniform(9, 32)
    box((x, 32 + random.uniform(0, 10), h / 2), (random.uniform(5, 7.5), 6, h), M_BLD[k % 4], "bld")
for k in range(10):
    x = -50 + k * 11 + random.uniform(-2, 2); h = random.uniform(8, 22)
    box((x, -40 - random.uniform(0, 8), h / 2), (7, 6, h), M_BLD[(k + 1) % 4], "bld")
for k in range(12):  # trees (anchored: they do not move)
    x, y = random.choice([-1, 1]) * random.uniform(5, 22), random.uniform(5, 22)
    h = random.uniform(2.5, 4.5)
    cyl_between((x, y, 0), (x, y, h), 0.12, M_TRUNK, None, "trunk", caps=False)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=random.uniform(1.2, 1.9), location=(x, y, h + 0.6))
    link(bpy.context.object, M_LEAF)

# ---------- mannequin (pelvis at origin, head +z, shoulders along y) ----------
body = empty("body")
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.30))
o = bpy.context.object; o.scale = (0.12, 0.19, 0.32); bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.02))
o = bpy.context.object; o.scale = (0.125, 0.17, 0.12); bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, radius=0.105, location=(0, 0, 0.76))
o = bpy.context.object; bpy.ops.object.shade_smooth(); link(o, M_SKIN, body)
bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.018, location=(0, 0, 0.78))
link(bpy.context.object, M_GOGG, body)
arms, legs = [], []
for side in (-1, 1):
    sh = empty(f"shoulder{side}", (0, side * 0.21, 0.5), body)
    cyl_between((0, 0, 0), (0, side * 0.03, -0.30), 0.045, M_SKIN, sh, "upperarm")
    cyl_between((0, side * 0.03, -0.30), (0, side * 0.04, -0.58), 0.04, M_SKIN, sh, "forearm")
    arms.append(sh)
for side in (-1, 1):
    hp = empty(f"hip{side}", (0, side * 0.09, 0), body)
    cyl_between((0, 0, 0), (0, side * 0.01, -0.45), 0.065, M_SUIT, hp, "thigh")
    cyl_between((0, side * 0.01, -0.45), (0, side * 0.01, -0.86), 0.05, M_SKIN, hp, "shin")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(-0.05, side * 0.01, -0.88))
    ft = bpy.context.object; ft.scale = (0.11, 0.045, 0.035); link(ft, M_SKIN, hp)
    legs.append(hp)
STAND = 0.915     # pelvis height standing (soles on the ground)
HEAD_TOP = 0.87   # head top above the pelvis

# ---------- gravity arrow (emissive, floats beside the mannequin) ----------
arrow = empty("arrow")
cyl_between((0, 0, 0.30), (0, 0, -0.12), 0.06, M_ARROW, arrow, "shaft", caps=False)
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.17, radius2=0, depth=0.28, location=(0, 0, -0.26), rotation=(math.pi, 0, 0))
link(bpy.context.object, M_ARROW, arrow)

# ---------- loose objects: they fall up exactly like the mannequin ----------
LOOSE = []
spots = [(-1.3, -0.6), (0.9, -1.0), (-0.7, 1.2), (2.4, -0.3), (-2.2, 0.5), (0.3, 1.9), (-1.8, -1.6), (1.9, 1.5), (-3.0, -0.2), (3.0, 0.9)]
for k, (x, y) in enumerate(spots):
    kind = k % 3
    if kind == 0:
        r = 0.16; bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=9, radius=r); o = bpy.context.object
        bpy.ops.object.shade_smooth(); link(o, M_BALL[k % 6]); z0 = r
    elif kind == 1:
        bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=0.16, radius2=0.03, depth=0.5); o = bpy.context.object
        link(o, M_CONE); z0 = 0.25
    else:
        bpy.ops.mesh.primitive_cube_add(size=0.4); o = bpy.context.object; link(o, M_CRATE); z0 = 0.2
    LOOSE.append((o, Vector((x, y, z0)), Vector([random.uniform(-2.5, 2.5) for _ in range(3)]), random.uniform(0.9, 1.1)))

# ---------- interior room (the twist) at x = 40 ----------
RX = 40.0; CEIL = 2.60
box((RX, 0, -0.045), (6, 6, 0.12), M_FLOOR, "floor")
box((RX, 0, CEIL + 0.05), (6, 6, 0.1), M_ICEIL, "ceil")
for x, y, sx, sy in [(RX, 3, 6, 0.1), (RX, -3, 6, 0.1), (RX + 3, 0, 0.1, 6), (RX - 3, 0, 0.1, 6)]:
    box((x, y, CEIL / 2), (sx, sy, CEIL), M_IWALL, "iwall")
box((RX + 0.4, 2.94, 1.5), (1.6, 0.02, 1.1), M_IWIN, "iwin")
box((RX - 1.6, 2.94, 1.6), (0.8, 0.02, 0.6), M_FRAME, "frame")
box((RX + 1.7, 2.3, 0.25), (2.0, 0.8, 0.5), M_SOFA, "sofa"); box((RX + 1.7, 2.65, 0.6), (2.0, 0.2, 0.7), M_SOFA, "sofaback")
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.28, depth=0.05, location=(RX - 1.9, -0.6, CEIL - 0.03))
link(bpy.context.object, M_LAMP)
il = bpy.data.objects.new("ilamp", bpy.data.lights.new("ilamp", "POINT"))
il.data.energy = 250; il.data.shadow_soft_size = 0.4; il.data.color = (1.0, 0.88, 0.7)
il.location = (RX - 1.9, -0.6, CEIL - 0.3); S.collection.objects.link(il)
ifill = bpy.data.objects.new("ifill", bpy.data.lights.new("ifill", "AREA"))
ifill.data.energy = 120; ifill.data.size = 2.5; ifill.data.color = (0.8, 0.9, 1.0)
ifill.location = (RX + 0.4, 2.6, 1.5); ifill.rotation_euler = (math.radians(-90), 0, 0); S.collection.objects.link(ifill)

# ---------- timeline / physics ----------
G = 9.81
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_FLIP = t2 + 0.95                 # "Flip gravity…" -> lift-off
T_RET = t4 + 0.15                  # "Gravity returns" -> arrow flips back
T_PEAK = t5 - 0.05                 # peak (~9.8 m)
T_LAND = t6 + 0.12                 # (never shown: hard cut at t6 - 0.05)
IN_GAP = CEIL - 0.03 - (STAND + HEAD_TOP)       # head-to-ceiling gap indoors (~0.8 m)
T_IN = t7 + 0.25                   # indoors lift-off ("Indoors.")
T_HIT = T_IN + math.sqrt(2 * IN_GAP / G)        # head reaches the ceiling (real-time physics, ~0.4 s)
HOOK_PEAK, HOOK_G = 2.05, 0.6      # hook flash-forward: slow coast up to the 10 m mark

def outdoor_rise(t):
    """height gained above standing (m): up 4.9 m while flipped (accelerating),
    coast to 9.8 m (decelerating), then the fall (accelerating). Stylised time, real shape."""
    if t < T_FLIP: return 0.0
    if t < T_RET: u = (t - T_FLIP) / (T_RET - T_FLIP); return 4.905 * u * u
    if t < T_PEAK: u = (t - T_RET) / (T_PEAK - T_RET); return 4.905 + 4.905 * (1 - (1 - u) ** 2)
    u = (t - T_PEAK) / (T_LAND - T_PEAK); return max(0.0, 9.81 * (1 - u * u))
def hook_rise(tau):
    return 9.81 - 0.5 * HOOK_G * (HOOK_PEAK - tau) ** 2 - 0.3

def state(t):
    """-> (where, rise, flail)  where = 'out' | 'hook' | 'in'"""
    if t < t2 - 0.05: return "hook", hook_rise(t), 1.0
    if t >= tc: return "hook", hook_rise(t - DUR), 1.0
    if t >= t6 - 0.05:
        r = 0.0 if t < T_IN else min(0.5 * G * (t - T_IN) ** 2, IN_GAP)
        return "in", r, (smooth((t - T_IN) / 0.25))
    return "out", outdoor_rise(t), smooth((t - T_FLIP) / 0.4)

body.rotation_mode = "XYZ"; arrow.rotation_mode = "XYZ"
for f in range(0, N + 1):
    t = f / FPS
    where, rise, fl = state(t)
    if where == "in":
        squash = 0.05 * math.exp(-10 * (t - T_HIT)) * abs(math.sin(25 * (t - T_HIT))) if t >= T_HIT else 0.0
        body.location = Vector((RX - 0.9, 0.6, STAND + rise - squash))
        body.rotation_euler = (0, 0, math.radians(-25))
    else:
        body.location = Vector((0, 0, STAND + rise))
        wob = fl * 0.12
        body.rotation_euler = (wob * math.sin(t * 2.3), wob * math.sin(t * 1.7 + 1), math.radians(-25) + 0.15 * fl * math.sin(t * 0.9))
    body.keyframe_insert("location", frame=f); body.keyframe_insert("rotation_euler", frame=f)
    for k, sh in enumerate(arms):
        side = -1 if k == 0 else 1
        a = fl * ((math.radians(75) if where == "in" else math.radians(110)) + 0.6 * math.sin(t * 9 + k * 2))
        sh.rotation_euler = (side * a, 0, 0); sh.keyframe_insert("rotation_euler", frame=f)
    for k, hp in enumerate(legs):
        hp.rotation_euler = (0, fl * (0.35 * math.sin(t * 6 + k * math.pi) - 0.2), 0); hp.keyframe_insert("rotation_euler", frame=f)
    # arrow: beside the mannequin's head, points along gravity; flips with a quick spin
    arrow.location = body.location + (Vector((0.65, 0.6, 0.45)) if where == "in" else Vector((0.55, -0.55, 0.95)))
    if where == "out": flip = smooth((t - (T_FLIP - 0.3)) / 0.3) - smooth((t - T_RET) / 0.3)
    elif where == "in": flip = smooth((t - (T_IN - 0.3)) / 0.3)
    else: flip = 0.0
    arrow.rotation_euler = (0, math.pi * flip, 0)
    hide = where == "out" and t5 - 0.1 <= t < t5 + 1.45   # top-down fall shot: keep the arrow out of the lens
    arrow.scale = (0.001,) * 3 if hide else (1, 1, 1); arrow.keyframe_insert("scale", frame=f)
    arrow.keyframe_insert("location", frame=f); arrow.keyframe_insert("rotation_euler", frame=f)
    for o, p0, spin, kk in LOOSE:
        rr = 0.0 if where == "in" else rise * kk + (0.3 if where == "hook" else 0.0)
        o.location = p0 + Vector((0, 0, rr)); o.rotation_euler = spin * (rr * 0.35)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)

# ---------- camera: piecewise segments, hard cuts timed to the lines ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 400
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
V = Vector
def bodypos(t):
    where, rise, _ = state(t)
    return V((RX - 0.9, 0.6, STAND + rise)) if where == "in" else V((0, 0, STAND + rise))
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
OPEN = ((-0.9, -6.4, 13.3), (0.5, 0.3, 8.75))
SEG = [  # (t0, t1, spec, lens_a, lens_b)
    (0.0, t2 - 0.05, ("hook",), 25, 26),
    (t2 - 0.05, t3 - 0.05, fixed((-1.6, -5.6, 1.5), (0.5, 0, 1.5), (-1.2, -4.6, 1.5), (0.4, 0, 1.6)), 30, 30),
    (t3 - 0.05, t3 + 1.25, ("follow", (0.7, -2.4, 0), (0, 0, 0.6), "ground"), 22, 22),
    (t3 + 1.25, t4 - 0.05, ("follow", (-1.0, -5.2, 0.4), (0.4, 0, 0.1)), 30, 30),
    (t4 - 0.05, t4 + 1.4, ("follow", (-1.3, -4.2, 0.9), (0.35, 0, 0.55)), 30, 32),
    (t4 + 1.4, t5 - 0.05, fixed((-5.0, -13.0, 4.6), (0.5, 0, 7.9), (-4.6, -12.0, 5.6), (0.5, 0, 9.0)), 30, 30),
    (t5 - 0.05, t5 + 1.45, ("follow", (0.25, -0.5, 3.4), (0, 0.05, -3.0)), 24, 24),
    (t5 + 1.45, t6 - 0.05, ("follow", (-1.5, -7.5, 0.2), (0.3, 0, -0.4)), 30, 30),
    (t6 - 0.05, t7 - 0.05, fixed((RX + 2.3, -2.5, 1.6), (RX - 0.8, 0.8, 1.1), (RX + 2.1, -2.3, 1.6), (RX - 0.8, 0.8, 1.2)), 24, 24),
    (t7 - 0.05, tc, fixed((RX + 2.0, -2.5, 2.25), (RX - 0.9, 0.6, 1.75), (RX + 1.8, -2.3, 2.3), (RX - 0.9, 0.6, 1.85)), 24, 24),
    (tc, DUR + 0.01, ("hookend",), 24, 25),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    spec = seg[2]
    if spec[0] == "hook":
        p = V(OPEN[0]) + V((0.0, 0.25 * u, -0.15 * u)); q = V(OPEN[1])
    elif spec[0] == "hookend":  # slow push from slightly wide back to the opening framing (loop)
        p = V(OPEN[0]) + V((0.35 * (1 - u), -0.5 * (1 - u), 0.25 * (1 - u))); q = V(OPEN[1])
    elif spec[0] == "follow":
        bp = bodypos(t); p = bp + V(spec[1]); q = bp + V(spec[2])
        if len(spec) > 3 and spec[3] == "ground": p = V((p.x, p.y, 0.35))
    else:
        _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_flip": T_FLIP, "t_ret": T_RET, "t_peak": T_PEAK, "t_cut_fall": t6 - 0.05, "t_in": T_IN, "t_hit": T_HIT,
           "t_card": tc, "cuts": [s[0] for s in SEG[1:]]}, open("/home/claude/reel/beats.json", "w"), indent=1)

# ---------- render ----------
args = [a for a in (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]) if a != "--force"]
if args and ("," in args[0] or len(args) == 1): frames = [int(x) for x in args[0].split(",") if x]  # "12" = one frame
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
