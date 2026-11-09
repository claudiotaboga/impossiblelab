"""The Impossible Lab #03 - a ship launched into a sea of honey.
Low golden sun over a glassy amber sea; a primitive cargo ship that rides ~28 % higher
(red antifouling band exposed above the honey), a slipway launch with a slow viscous bulge,
honey drops whose ripples die in about a second, and barnacles that shrivel for the twist.
Usage: python3 scene.py [start end [step]] | [f1,f2,...]  [--force]
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N

random.seed(3)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 3; S.cycles.glossy_bounces = 2; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 0; S.cycles.transparent_max_bounces = 4
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"

from timeline import LINES
def sec(t): return t * FPS
L = {l["i"]: l for l in LINES}

# ---------- materials ----------
def mat(name, base=(0.5, 0.5, 0.5), rough=0.5, metal=0.0, emit=None, estr=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if coat: b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    return m

M_HONEY = mat("honey", (0.80, 0.36, 0.02), 0.06, 0, (0.95, 0.42, 0.02), 0.35)
M_RED = mat("antifoul", (0.55, 0.05, 0.03), 0.35, coat=0.6)
M_HULL = mat("hull", (0.03, 0.06, 0.14), 0.35, coat=0.4)
M_WHITE = mat("white", (0.85, 0.85, 0.83), 0.4)
M_FUNNEL = mat("funnel", (0.85, 0.45, 0.05), 0.4)
M_WIN = mat("window", (0.1, 0.1, 0.1), 0.2, 0, (1.0, 0.85, 0.6), 1.5)
M_LINE = mat("seawaterline", (0.1, 0.7, 1.0), 0.4, 0, (0.15, 0.75, 1.0), 0.0)
M_BARN = mat("barnacle", (0.40, 0.37, 0.33), 0.8)
M_WOOD = mat("slipway", (0.30, 0.20, 0.12), 0.8)
M_CONC = mat("concrete", (0.45, 0.43, 0.40), 0.9)
M_CONT = [mat(f"cont{k}", c, 0.5) for k, c in enumerate([(0.7, 0.12, 0.08), (0.08, 0.3, 0.6), (0.1, 0.45, 0.2), (0.8, 0.6, 0.1)])]
line_emit = M_LINE.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]

# ---------- world: warm late-afternoon sky ----------
world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (1.0, 0.55, 0.22, 1)
ramp.color_ramp.elements[1].position = 0.35; ramp.color_ramp.elements[1].color = (0.25, 0.42, 0.75, 1)
nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
nt.links.new(ramp.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.9

sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 4.0; sun.data.angle = math.radians(2.5); sun.data.color = (1.0, 0.82, 0.6)
sun.rotation_euler = (math.radians(-78), 0, math.radians(200)); S.collection.objects.link(sun)

# ---------- helpers ----------
def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box", parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; return link(o, m, parent)
def prism(x_flat, z, h, half_w, m, parent, name="bow"):
    """triangular bow piece: flat side at x_flat (width 2*half_w), tip towards +x"""
    r = half_w * 2 / math.sqrt(3)
    bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=r, depth=h, location=(x_flat + r / 2, 0, z))
    o = bpy.context.object; o.name = name; return link(o, m, parent)
def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); e.location = loc; S.collection.objects.link(e)
    if parent: e.parent = parent
    return e
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

# ---------- honey sea: fine grid near the ship + flat far plane to the horizon ----------
GX, GY = 30, 22
bpy.ops.mesh.primitive_grid_add(x_subdivisions=420, y_subdivisions=300, size=1, location=(0, -3, 0))
sea = bpy.context.object; sea.name = "honey"; sea.scale = (GX, GY, 1)
bpy.ops.object.transform_apply(scale=True); bpy.ops.object.shade_smooth(); link(sea, M_HONEY)
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, -0.004)); link(bpy.context.object, M_HONEY)
WAVES = []
def impact(t, x, y, height, width, speed, life, narrow=1.5):
    e = empty(f"impact{len(WAVES)}", (x, y, 0))
    w = sea.modifiers.new(f"wave{len(WAVES)}", "WAVE")
    w.start_position_object = e; w.use_normal = False
    w.height = height; w.width = width; w.speed = speed; w.narrowness = narrow
    w.time_offset = sec(t); w.lifetime = life; w.damping_time = life * 0.7
    w.falloff_radius = 0
    WAVES.append(w)

# ---------- ship (local: origin on the HONEY waterline, bow +x, port +y) ----------
HB = 0.8            # half beam
D_SEA = 1.0         # draft in seawater (red antifouling up to here)
D_HONEY = 0.72      # draft in honey = 1.025 / 1.42 of the seawater draft
EXPOSED = D_SEA - D_HONEY
ship = empty("ship")
zb = -D_HONEY       # keel
box((0, 0, zb + D_SEA / 2), (6.0, 2 * HB, D_SEA), M_RED, "red", ship)
prism(3.0, zb + D_SEA / 2, D_SEA, HB, M_RED, ship, "redbow")
TOP = 1.05
box((0, 0, zb + D_SEA + TOP / 2), (6.0, 2 * HB, TOP), M_HULL, "topsides", ship)
prism(3.0, zb + D_SEA + TOP / 2, TOP, HB, M_HULL, ship, "bowtop")
box((0, 0, zb + D_SEA), (6.02, 2 * HB + 0.02, 0.035), M_LINE, "sealine", ship)
prism(3.0, zb + D_SEA, 0.035, HB + 0.01, M_LINE, ship, "sealinebow")
deck = zb + D_SEA + TOP
box((-2.3, 0, deck + 0.55), (1.2, 1.4, 1.1), M_WHITE, "house", ship)
box((-2.3, 0, deck + 1.25), (0.9, 1.5, 0.3), M_WHITE, "bridge", ship)
box((-1.84, 0, deck + 1.25), (0.02, 1.3, 0.12), M_WIN, "windows", ship)
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.22, depth=0.9, location=(-2.75, 0, deck + 1.45))
link(bpy.context.object, M_FUNNEL, ship); bpy.ops.object.shade_smooth()
for i in range(5):
    for j in range(2):
        for k in range(2 if (i + j) % 2 else 1):
            box((-1.1 + i * 0.78, (j - 0.5) * 0.72, deck + 0.22 + k * 0.42), (0.74, 0.68, 0.4), M_CONT[(i * 2 + j + k) % 4], "container", ship)
BARN = []
for k in range(26):
    x = random.uniform(1.4, 3.0); z = zb + D_HONEY + random.uniform(0.04, EXPOSED - 0.03)
    r = random.uniform(0.022, 0.045)
    bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=r, radius2=r * 0.45, depth=r * 1.1, location=(x, -HB - r * 0.45, z), rotation=(math.radians(90), 0, 0))
    b = bpy.context.object; link(b, M_BARN, ship); BARN.append(b)

# ---------- slipway (launch beat), far to the left ----------
SLOPE = math.atan2(2.45, 8.5)
box((-10.5, 0, 0.95), (9.5, 1.0, 0.12), M_WOOD, "slipway").rotation_euler = (0, SLOPE, 0)
box((-20, 0, 1.0), (10, 8, 2.6), M_CONC, "quay")

# ---------- ship motion ----------
t_launch = L[2]["start"] - 0.05
t_side = L[3]["start"] - 0.05
t_close = (L[3]["start"] + L[3]["end"]) / 2 + 0.2
t_top = L[4]["start"] - 0.05
t_low = (L[4]["start"] + L[4]["end"]) / 2 + 0.2
t_bonus = L[5]["start"] - 0.05
t_barn = L[6]["start"] - 0.05
t_card = L[6]["end"] + 0.05
t_hit = t_launch + 0.85
t_shrivel = L[6]["start"] + 0.45

def ship_state(t):
    if t < t_launch:   # hook: released from its seawater draft, it pops up to ride high
        u = max(0.0, t - 0.1)
        z = -EXPOSED * math.exp(-3.2 * u) * math.cos(5.5 * u)
        return Vector((0, 0, z)), (0.012 * math.sin(t * 2.0), 0, 0)
    if t < t_side:     # launch down the slipway into the honey
        if t < t_hit:
            u = (t - t_launch) / (t_hit - t_launch); u = u * u
            x = -13.5 + 8.5 * u; z = 2.2 - (2.2 + 0.25) * u
            return Vector((x, 0, z)), (0, SLOPE * (1 - smooth((u - 0.7) / 0.3)), 0)
        u = t - t_hit
        x = -5.0 + 1.4 * (1 - math.exp(-2.5 * u))
        z = -0.25 * math.exp(-2.2 * u) * math.cos(4.5 * u)
        return Vector((x, 0, z)), (0, -0.05 * math.exp(-2.5 * u) * math.sin(5 * u), 0)
    return Vector((0, 0, 0.006 * math.sin(t * 1.6))), (0.01 * math.sin(t * 1.2), 0.004 * math.sin(t * 0.9), 0)

for f in range(0, N + 1):
    t = f / FPS
    loc, rot = ship_state(t)
    ship.location = loc; ship.keyframe_insert("location", frame=f)
    ship.rotation_euler = rot; ship.keyframe_insert("rotation_euler", frame=f)
    g = 2.5 * smooth((t - t_side - 0.3) / 0.3) * (1 - smooth((t - L[3]["end"] - 0.2) / 0.3))
    line_emit.default_value = g; line_emit.keyframe_insert("default_value", frame=f)
    for k, b in enumerate(BARN):
        sk = max(0.001, 1 - smooth((t - t_shrivel - k * 0.03) / 0.9))
        b.scale = (sk, sk, sk); b.keyframe_insert("scale", frame=f)

impact(0.15, 0.0, -1.2, height=0.05, width=1.2, speed=0.06, life=26, narrow=1.2)
impact(t_hit, -5.0, 0.0, height=0.16, width=1.4, speed=0.07, life=30, narrow=1.2)

# ---------- honey drops: ripples that fade in about a second ----------
DROPS = [(t_top + 0.55, 2.2, -4.2), (t_low + 0.35, -1.0, -4.6)]
for (td, x, y) in DROPS:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.09)
    d = bpy.context.object; d.scale = (1, 1, 1.5); bpy.ops.object.shade_smooth(); link(d, M_HONEY)
    for f in range(0, N + 1):
        t = f / FPS; dt = td - t
        d.location = (x, y, 0.05 + 4.9 * dt * dt) if 0 <= dt <= 0.6 else (x, y, -3)
        d.keyframe_insert("location", frame=f)
    impact(td, x, y, height=0.09, width=0.35, speed=0.05, life=14, narrow=1.6)  # visible ~1 s in total (lifetime + damping)

# ---------- camera: piecewise segments, hard cuts between them ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 800
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
V = Vector
OPEN = (V((9.6, -11.2, 0.75)), V((-0.2, 0, 0.95)), 30)
SEG = [  # (t0, t1, A, B) with (pos, target, lens)
    (0.0, t_launch, OPEN, (V((8.8, -10.4, 0.7)), V((-0.2, 0, 0.9)), 30)),
    (t_launch, t_side, (V((-7.5, -15.5, 2.6)), V((-8.0, 0, 1.0)), 24), (V((-6.0, -14.5, 2.2)), V((-5.5, 0, 0.6)), 24)),
    (t_side, t_close, (V((0.3, -10.5, 0.18)), V((0.3, 0, 0.55)), 30), (V((1.2, -10.0, 0.18)), V((0.6, 0, 0.5)), 30)),
    (t_close, t_top, (V((4.6, -3.6, 0.22)), V((2.6, -0.8, 0.12)), 34), (V((4.2, -3.3, 0.22)), V((2.3, -0.8, 0.12)), 34)),
    (t_top, t_low, (V((3.4, -8.6, 2.3)), V((2.2, -4.2, 0)), 30), (V((3.2, -8.1, 2.0)), V((2.2, -4.2, 0)), 30)),
    (t_low, t_bonus, (V((-1.4, -8.8, 1.5)), V((-1.0, -4.6, 0)), 34), (V((-1.1, -8.4, 1.3)), V((-0.9, -4.6, 0.05)), 34)),
    (t_bonus, t_barn, (V((5.0, -5.0, 0.5)), V((2.3, -0.8, 0.12)), 32), (V((3.6, -3.2, 0.3)), V((2.2, -0.8, 0.12)), 36)),
    (t_barn, t_card, (V((3.3, -2.6, 0.2)), V((2.2, -0.8, 0.12)), 38), (V((2.9, -2.45, 0.2)), V((2.1, -0.8, 0.12)), 40)),
    (t_card, N / FPS + 0.01, (V((7.6, -9.0, 0.6)), V((-0.2, 0, 0.85)), 30), OPEN),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    (pa, ta, la), (pb, tb, lb) = seg[2], seg[3]
    cam.location = pa.lerp(pb, u); cam.keyframe_insert("location", frame=f)
    tgt.location = ta.lerp(tb, u); tgt.keyframe_insert("location", frame=f)
    cam.data.lens = la + (lb - la) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_launch": t_launch, "t_hit": t_hit, "t_side": t_side, "t_close": t_close, "t_top": t_top,
           "t_low": t_low, "t_bonus": t_bonus, "t_barn": t_barn, "t_shrivel": t_shrivel, "t_card": t_card,
           "drops": [d[0] for d in DROPS], "pop": 0.1}, open("/home/claude/reel/beats.json", "w"), indent=1)

# ---------- render ----------
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
force = "--force" in args; args = [a for a in args if a != "--force"]
if len(args) == 1:
    frames = [int(a) for a in args[0].split(",")]
else:
    f_a, f_b = (int(args[0]), int(args[1])) if len(args) >= 2 else (0, N - 1)
    step = int(args[2]) if len(args) >= 3 else 1
    frames = list(range(f_a, f_b + 1, step))
for f in frames:
    out = f"/home/claude/reel/frames/{f:04d}.png"
    if os.path.exists(out) and not force: continue
    S.frame_set(f); S.render.filepath = out
    t0 = time.time(); bpy.ops.render.render(write_still=True)
    print(f"frame {f} {time.time() - t0:.1f}s", flush=True)
