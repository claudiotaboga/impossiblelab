"""The Impossible Lab #02 - a pool of mercury.
Pool hall with a mirror-chrome mercury surface, a primitive mannequin that bounces off it,
floats with ~7 % submerged, can't swim, and a faint vapour haze for the twist.
Usage: python3 scene.py [start end [step]]   (frames, inclusive)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N

random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 4; S.cycles.glossy_bounces = 2; S.cycles.diffuse_bounces = 1
S.cycles.transparent_max_bounces = 8
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"

from timeline import LINES
def sec(t): return t * FPS

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

M_HG = mat("mercury", (0.86, 0.87, 0.9), 0.035, 1.0)
M_SKIN = mat("dummy", (0.78, 0.74, 0.70), 0.55)
M_SUIT = mat("suit", (0.05, 0.12, 0.30), 0.6)
M_GOGG = mat("goggles", (1.0, 0.45, 0.05), 0.3, 0, (1.0, 0.45, 0.05), 0.6)

def tile_mat(name, c1, c2, mortar, scale):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.25
    br = nt.nodes.new("ShaderNodeTexBrick"); br.offset = 0.0
    br.inputs["Color1"].default_value = (*c1, 1); br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (*mortar, 1); br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = 0.012
    br.inputs["Brick Width"].default_value = 0.5; br.inputs["Row Height"].default_value = 0.5
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return m
M_DECK = tile_mat("deck", (0.80, 0.82, 0.84), (0.74, 0.77, 0.80), (0.35, 0.37, 0.40), 1.6)
M_WALL = tile_mat("wall", (0.10, 0.36, 0.42), (0.09, 0.31, 0.37), (0.85, 0.85, 0.85), 1.3)
M_POOLWALL = tile_mat("poolwall", (0.08, 0.20, 0.30), (0.07, 0.18, 0.27), (0.6, 0.6, 0.6), 2.5)
M_CEIL = mat("ceiling", (0.12, 0.12, 0.13), 0.8)
M_LAMP = mat("lamp", (1, 1, 1), 0.5, 0, (1.0, 0.97, 0.92), 9.0)
M_WIN = mat("window", (1, 1, 1), 0.5, 0, (1.0, 0.82, 0.6), 4.0)
M_SIGN = mat("signred", (0.8, 0.1, 0.08), 0.4)

def vapour_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; n = m.node_tree; n.nodes.clear()
    o = n.nodes.new("ShaderNodeOutputMaterial")
    e = n.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (0.55, 0.95, 0.65, 1); e.inputs[1].default_value = 2.4
    tr = n.nodes.new("ShaderNodeBsdfTransparent")
    noise = n.nodes.new("ShaderNodeTexNoise"); noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value = 2.2; noise.inputs["Detail"].default_value = 3
    tc = n.nodes.new("ShaderNodeTexCoord")
    grad = n.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
    mp = n.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.9, 0.9, 0.9)
    mul = n.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    ramp = n.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.30; ramp.color_ramp.elements[1].position = 0.75
    st = n.nodes.new("ShaderNodeMath"); st.operation = "MULTIPLY"; st.inputs[1].default_value = 0
    mix = n.nodes.new("ShaderNodeMixShader")
    n.links.new(tc.outputs["Object"], mp.inputs[0]); n.links.new(mp.outputs[0], grad.inputs[0])
    n.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    n.links.new(grad.outputs[1], mul.inputs[0]); n.links.new(noise.outputs[0], mul.inputs[1])
    n.links.new(mul.outputs[0], ramp.inputs[0]); n.links.new(ramp.outputs[0], st.inputs[0])
    n.links.new(st.outputs[0], mix.inputs[0])
    n.links.new(tr.outputs[0], mix.inputs[1]); n.links.new(e.outputs[0], mix.inputs[2])
    n.links.new(mix.outputs[0], o.inputs[0])
    return m, noise, st

# ---------- world ----------
world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.025, 0.03, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

# ---------- helpers ----------
def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; return link(o, m)
def cyl_between(a, b, r, m, parent, name="limb"):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.name = name
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    bpy.ops.object.shade_smooth(); link(o, m, parent)
    for p in (a, b):  # rounded ends
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r, location=p)
        e = bpy.context.object; bpy.ops.object.shade_smooth(); link(e, m, parent)
    return o
def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); e.location = loc; S.collection.objects.link(e)
    if parent: e.parent = parent
    return e

# ---------- pool hall ----------
PX, PY = 4.0, 2.2          # half-size of the pool
DECK = 0.25                # deck height above the mercury surface
bpy.ops.mesh.primitive_grid_add(x_subdivisions=320, y_subdivisions=180, size=1, location=(0, 0, 0))
hg = bpy.context.object; hg.name = "mercury"; hg.scale = (2 * PX, 2 * PY, 1)
bpy.ops.object.transform_apply(scale=True); bpy.ops.object.shade_smooth(); link(hg, M_HG)
oc = hg.modifiers.new("ocean", "OCEAN"); oc.geometry_mode = "DISPLACE"
oc.resolution = 8; oc.spatial_size = 20; oc.wave_scale = 0.004; oc.wind_velocity = 3
oc.time = 0; oc.keyframe_insert("time", frame=0); oc.time = 3; oc.keyframe_insert("time", frame=N)
IMPACTS = []
def impact(t, x, y, height=0.018, width=0.30, speed=0.09, life=34):
    e = empty(f"impact{len(IMPACTS)}", (x, y, 0))
    w = hg.modifiers.new(f"wave{len(IMPACTS)}", "WAVE")
    w.start_position_object = e; w.use_normal = False
    w.height = height; w.width = width; w.speed = speed; w.narrowness = 1.6
    w.time_offset = sec(t); w.lifetime = life; w.damping_time = life * 0.6
    w.falloff_radius = 0
    IMPACTS.append(w)
# pool walls + floor under the mercury
for x, y, sx, sy in [(0, PY + 0.1, 2 * PX + 0.4, 0.2), (0, -PY - 0.1, 2 * PX + 0.4, 0.2),
                     (PX + 0.1, 0, 0.2, 2 * PY), (-PX - 0.1, 0, 0.2, 2 * PY)]:
    box((x, y, -0.6 + DECK / 2), (sx, sy, 1.2 + DECK), M_POOLWALL, "poolwall")
# deck around the pool
for x, y, sx, sy in [(0, PY + 3.2, 18, 6), (0, -PY - 3.2, 18, 6), (PX + 3.5, 0, 7, 2 * PY + 0.4), (-PX - 3.5, 0, 7, 2 * PY + 0.4)]:
    box((x, y, DECK - 0.05), (sx, sy, 0.1), M_DECK, "deck")
# hall walls, ceiling, light strips, windows
for x, y, sx, sy in [(0, 7.5, 18, 0.2), (0, -7.5, 18, 0.2), (9, 0, 0.2, 15), (-9, 0, 0.2, 15)]:
    box((x, y, 3), (sx, sy, 6), M_WALL, "wall")
box((0, 0, 6.05), (18, 15, 0.1), M_CEIL, "ceiling")
for k in range(-3, 4):
    box((k * 2.4, 0, 5.95), (0.25, 9, 0.05), M_LAMP, "lamp")
for k in range(-3, 4):
    box((k * 2.4, 7.39, 3.2), (1.6, 0.02, 2.6), M_WIN, "window")
# lane-end markers / ladder for scale
for y in (-1.2, 1.2):
    cyl_between((-PX - 0.25, y, DECK + 0.7), (-PX + 0.05, y, DECK + 0.7), 0.025, mat("rail", (0.8, 0.8, 0.82), 0.15, 1.0), None, "rail")
    cyl_between((-PX + 0.05, y, DECK + 0.7), (-PX + 0.05, y, -0.4), 0.025, M_HG, None, "rail")
box((-PX - 0.7, -PY - 0.9, DECK + 0.6), (0.9, 0.05, 0.6), M_SIGN, "sign")
sun = bpy.data.objects.new("key", bpy.data.lights.new("key", "AREA"))
sun.data.energy = 900; sun.data.size = 8; sun.data.color = (1.0, 0.95, 0.9)
sun.location = (0, 0, 5.6); S.collection.objects.link(sun); sun.visible_glossy = False
win = bpy.data.objects.new("winlight", bpy.data.lights.new("winlight", "AREA"))
win.data.energy = 500; win.data.size = 10; win.data.color = (1.0, 0.8, 0.6)
win.location = (0, 7.0, 3.2); win.rotation_euler = (math.radians(90), 0, 0); S.collection.objects.link(win)

# ---------- mannequin (local: pelvis at origin, head +z, shoulders along y, thin along x) ----------
body = empty("body")
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=(0, 0, 0.30))
torso = bpy.context.object; torso.scale = (0.12, 0.19, 0.32); bpy.ops.object.shade_smooth(); link(torso, M_SKIN, body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=(0, 0, 0.02))
hips = bpy.context.object; hips.scale = (0.125, 0.17, 0.12); bpy.ops.object.shade_smooth(); link(hips, M_SUIT, body)
cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.105, location=(0, 0, 0.76))
head = bpy.context.object; bpy.ops.object.shade_smooth(); link(head, M_SKIN, body)
bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.018, location=(0, 0, 0.78), rotation=(0, 0, 0))
link(bpy.context.object, M_GOGG, body)
arms = []
for side in (-1, 1):
    sh = empty(f"shoulder{side}", (0, side * 0.21, 0.5), body)
    cyl_between((0, 0, 0), (0, side * 0.03, -0.30), 0.045, M_SKIN, sh, "upperarm")
    cyl_between((0, side * 0.03, -0.30), (0, side * 0.04, -0.58), 0.04, M_SKIN, sh, "forearm")
    arms.append(sh)
for side in (-1, 1):
    hp = empty(f"hip{side}", (0, side * 0.09, 0), body)
    cyl_between((0, 0, 0), (0, side * 0.01, -0.45), 0.065, M_SKIN, hp, "thigh")
    cyl_between((0, side * 0.01, -0.45), (0, side * 0.01, -0.86), 0.05, M_SKIN, hp, "shin")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(-0.05, side * 0.01, -0.88))
    ft = bpy.context.object; ft.scale = (0.11, 0.045, 0.035); link(ft, M_SKIN, hp)

FLOAT_Z = 0.11   # pelvis height when floating on its back: ~7 % of the body below the surface
FLAT = math.radians(90)

def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def bounce(t, t0, z_top, z_rest, amp=0.4, w=9.0, decay=3.2):
    """height after an impact at t0: damped rebounds settling on z_rest"""
    u = t - t0
    return z_rest + amp * abs(math.sin(w * u)) * math.exp(-decay * u)

L = {l["i"]: l for l in LINES}
t_dive_cut, t_side, t_over, t_tilt, t_card = L[3]["start"] - 0.05, L[4]["start"] - 0.05, L[5]["start"] - 0.05, L[6]["start"] - 0.1, L[7]["end"] + 0.05

def body_state(t):
    """returns location, rotation (x, y, z), arm swing angle"""
    arm = 0.0
    if t < t_dive_cut:  # hook fall + bounce, then float during the premise line
        t_hit = 0.45
        if t < t_hit:
            z = 2.1 - (2.1 - FLOAT_Z) * (t / t_hit) ** 2; rot = (0, FLAT, 0)
        else:
            z = bounce(t, t_hit, 0, FLOAT_Z, amp=0.45) - 0.05 * math.exp(-30 * (t - t_hit))
            rot = (0.08 * math.sin(t * 3), FLAT, 0)
        return Vector((0.0, 0.0, z)), rot, 0.15 * math.sin(t * 2)
    if t < t_side:  # dive from the deck, bounce off the surface
        u0, t_hit = t_dive_cut + 0.15, t_dive_cut + 0.55
        x_deck, z_deck = -PX - 0.35, DECK + 0.88
        if t < u0:
            return Vector((x_deck, 0, z_deck)), (0, 0.15, 0), math.radians(170)
        if t < t_hit:
            u = (t - u0) / (t_hit - u0)
            x = x_deck + (1.5 - x_deck) * 0 + u * 1.9
            z = z_deck + 0.5 * math.sin(u * math.pi) - (z_deck - FLOAT_Z) * u
            return Vector((x, 0, z)), (0, 0.15 + u * math.radians(115), 0), math.radians(170)
        z = bounce(t, t_hit, 0, FLOAT_Z, amp=0.35, w=10)
        a = min(1, (t - t_hit) / 0.5)
        return Vector((x_deck + 1.9 + 0.3 * a, 0, z)), (0, math.radians(130) + (FLAT - math.radians(130)) * smooth(a), 0), math.radians(170) * (1 - a)
    if t < t_over:  # floating high, side view
        return Vector((-0.2, 0, FLOAT_Z + 0.008 * math.sin(t * 2.2))), (0.04 * math.sin(t * 1.3), FLAT, 0), 0.1
    if t < t_tilt:  # trying to swim: arms windmill and slap
        return Vector((-0.4 + 0.12 * (t - t_over), 0, FLOAT_Z)), (0.06 * math.sin(t * 6), FLAT, 0), (t - t_over) * 2 * math.pi / 0.85
    return Vector((0.0, 0.2, FLOAT_Z + 0.008 * math.sin(t * 2))), (0.04 * math.sin(t * 1.3), FLAT, 0), 0.1

impact(0.45, 0.0, 0.0, height=0.022, width=0.32)
impact(t_dive_cut + 0.55, -PX - 0.35 + 1.9, 0.0, height=0.02, width=0.3)

for f in range(0, N + 1):
    t = f / FPS
    loc, rot, arm = body_state(t)
    body.location = loc; body.keyframe_insert("location", frame=f)
    body.rotation_euler = rot; body.keyframe_insert("rotation_euler", frame=f)
    for k, sh in enumerate(arms):
        sh.rotation_euler = (0, arm + (math.pi if k else 0) * (t_over <= t < t_tilt), 0)
        sh.keyframe_insert("rotation_euler", frame=f)
for fc in list(body.animation_data.action.fcurves if hasattr(body.animation_data.action, "fcurves") else []):
    for kp in fc.keyframe_points: kp.interpolation = "LINEAR"


# ---------- mercury droplets thrown up by the hook impact ----------
for k in range(36):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=14, ring_count=8, radius=random.uniform(0.018, 0.05))
    d = bpy.context.object; bpy.ops.object.shade_smooth(); link(d, M_HG)
    a = random.uniform(0, math.tau); vh = random.uniform(0.6, 1.8); vz = random.uniform(1.6, 3.4)
    x0, y0 = random.uniform(-0.6, 0.6), math.sin(a) * 0.15
    f0 = int(sec(0.45))
    d.location = (0, 0, -3); d.keyframe_insert("location", frame=0); d.keyframe_insert("location", frame=f0 - 1)
    for f in range(f0, f0 + 40):
        tt = (f - f0) / FPS; z = 0.02 + vz * tt - 4.9 * tt * tt
        if z < -0.02:
            d.location = (0, 0, -3); d.keyframe_insert("location", frame=f); break
        d.location = (x0 + math.cos(a) * vh * tt, y0 + math.sin(a) * vh * tt, z); d.keyframe_insert("location", frame=f)

# ---------- vapour haze (the twist) ----------
for k in range(9):
    m, noise, st = vapour_mat(f"vap{k}")
    bpy.ops.mesh.primitive_plane_add(size=1)
    v = bpy.context.object; link(v, m)
    v.rotation_euler = (math.radians(90), 0, math.radians(random.uniform(-12, 12)))
    v.scale = (random.uniform(2.2, 3.2), random.uniform(1.0, 1.6), 1)
    x0 = -3.2 + k * 0.8; y0 = random.uniform(-1.4, 1.6); z0 = random.uniform(0.35, 0.9)
    for f, z in [(0, z0), (N, z0 + 0.6)]:
        v.location = (x0, y0, z); v.keyframe_insert("location", frame=f)
    noise.inputs["W"].default_value = 0; noise.inputs["W"].keyframe_insert("default_value", frame=0)
    noise.inputs["W"].default_value = 18; noise.inputs["W"].keyframe_insert("default_value", frame=N)
    s_in = sec(t_tilt + 0.35) + k * 2
    for f, val in [(0, 0), (s_in, 0), (s_in + 14, 0.8), (sec(t_card + 0.6), 0.8), (sec(t_card + 1.2), 0)]:
        st.inputs[1].default_value = val; st.inputs[1].keyframe_insert("default_value", frame=f)

# ---------- camera: piecewise segments, hard cuts between them ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
cam.data.dof.use_dof = True; cam.data.dof.focus_object = tgt; cam.data.dof.aperture_fstop = 8
V = Vector
bx = lambda t: body_state(t)[0]
OPEN = (V((-1.3, -3.3, 0.75)), V((0.25, 0, 0.45)), 30)
SEG = [  # (t0, t1, (posA, tgtA, lensA), (posB, tgtB, lensB))
    (0.0, L[2]["start"] - 0.05, OPEN, (V((-1.0, -2.9, 0.5)), V((0.2, 0, 0.2)), 30)),
    (L[2]["start"] - 0.05, t_dive_cut, (V((-4.6, -4.2, 1.7)), V((0, 0.2, 0.1)), 26), (V((-3.8, -3.6, 1.35)), V((0, 0.2, 0.1)), 26)),
    (t_dive_cut, t_side, (V((-3.4, -3.9, 1.55)), V((-3.4, 0, 0.6)), 30), (V((-2.2, -3.8, 1.2)), V((-2.1, 0, 0.12)), 30)),
    (t_side, t_over, (V((-0.35, -1.95, 0.075)), V((-0.2, 0, 0.09)), 30), (V((0.05, -1.85, 0.075)), V((-0.15, 0, 0.09)), 32)),
    (t_over, t_tilt, (V((-0.25, -0.35, 3.9)), V((-0.25, 0, 0)), 30), (V((0.0, -0.3, 3.4)), V((0.0, 0, 0)), 30)),
    (t_tilt, L[7]["start"], (V((0, -4.0, 0.35)), V((0, 0.4, 0.15)), 30), (V((0, -5.2, 0.9)), V((0, 1.0, 1.25)), 26)),
    (L[7]["start"], t_card, (V((0, -5.2, 0.9)), V((0, 1.0, 1.25)), 26), (V((0.6, -4.6, 1.0)), V((0.2, 1.0, 1.1)), 26)),
    (t_card, N / FPS + 0.01, (V((0.6, -4.6, 1.0)), V((0.2, 1.0, 1.1)), 26), OPEN),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next(s for s in SEG if s[0] <= t < s[1]) if t < SEG[-1][1] else SEG[-1]
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    (pa, ta, la), (pb, tb, lb) = seg[2], seg[3]
    cam.location = pa.lerp(pb, u); cam.keyframe_insert("location", frame=f)
    tgt.location = ta.lerp(tb, u); tgt.keyframe_insert("location", frame=f)
    cam.data.lens = la + (lb - la) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_dive_cut": t_dive_cut, "t_side": t_side, "t_over": t_over, "t_tilt": t_tilt, "t_card": t_card,
           "impacts": [0.45, t_dive_cut + 0.55]}, open("/home/claude/reel/beats.json", "w"), indent=1)

# ---------- render ----------
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
args = [a for a in args if a != "--force"]
f_a, f_b = (int(args[0]), int(args[1])) if len(args) >= 2 else (0, N - 1)
step = int(args[2]) if len(args) >= 3 else 1
for f in range(f_a, f_b + 1, step):
    out = f"/home/claude/reel/frames/{f:04d}.png"
    if os.path.exists(out) and "--force" not in sys.argv: continue
    S.frame_set(f); S.render.filepath = out
    t0 = time.time(); bpy.ops.render.render(write_still=True)
    print(f"frame {f} {time.time() - t0:.1f}s", flush=True)
