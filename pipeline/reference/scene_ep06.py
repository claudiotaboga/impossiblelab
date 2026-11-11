"""The Impossible Lab #06 - running a marathon at the speed of sound.
A primitive mannequin sprints down a red athletics track wrapped in a translucent vapour cone
with speed streaks. Cold open on the finish (tape snaps, "2:03" on the trackside clock behind),
side shot past distance boards, a glowing ghost car pressing on the runner (drag = a car's weight),
a crane-up reveal of ~17,000 runners (the power of 17,000 champions), the tight stadium bend ahead,
and the twist: an aerial pull-up to ~20 km showing the 12 km-radius turn a 1 g corner needs.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(6)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 3; S.cycles.glossy_bounces = 1; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 0; S.cycles.transparent_max_bounces = 4
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"
S.render.use_motion_blur = True; S.render.motion_blur_shutter = 0.35

from timeline import LINES, CARD_START
L = {l["i"]: l for l in LINES}
V = Vector

# ---------- materials ----------
def mat(name, base=(0.5, 0.5, 0.5), rough=0.5, metal=0.0, emit=None, estr=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    if alpha < 1: b.inputs["Alpha"].default_value = alpha
    return m
def ground_mat():
    m = bpy.data.materials.new("ground"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.9
    ck = nt.nodes.new("ShaderNodeTexChecker"); ck.inputs["Scale"].default_value = 0.08   # mowing stripes ~6 m
    ck.inputs["Color1"].default_value = (0.13, 0.33, 0.07, 1); ck.inputs["Color2"].default_value = (0.10, 0.27, 0.06, 1)
    br = nt.nodes.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 0.0015       # fields ~300 m
    br.inputs["Color1"].default_value = (1.0, 1.0, 0.9, 1); br.inputs["Color2"].default_value = (0.8, 0.95, 0.75, 1)
    br.inputs["Mortar"].default_value = (0.75, 0.7, 0.55, 1); br.inputs["Mortar Size"].default_value = 0.01
    br.offset = 0.3
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.0004; nz.inputs["Detail"].default_value = 4
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (0.75, 0.85, 0.55, 1); rp.color_ramp.elements[1].color = (1.25, 1.05, 0.75, 1)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    for n in (ck, br, nz): nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], rp.inputs[0])
    m1 = nt.nodes.new("ShaderNodeMix"); m1.data_type = "RGBA"; m1.blend_type = "MULTIPLY"; m1.inputs[0].default_value = 1
    m2 = nt.nodes.new("ShaderNodeMix"); m2.data_type = "RGBA"; m2.blend_type = "MULTIPLY"; m2.inputs[0].default_value = 1
    nt.links.new(ck.outputs["Color"], m1.inputs[6]); nt.links.new(br.outputs["Color"], m1.inputs[7])
    nt.links.new(m1.outputs[2], m2.inputs[6]); nt.links.new(rp.outputs[0], m2.inputs[7])
    nt.links.new(m2.outputs[2], b.inputs["Base Color"])
    return m

M_GROUND = ground_mat()
M_TRACK = mat("tartan", (0.55, 0.12, 0.07), 0.8)
M_LINE = mat("line", (0.95, 0.95, 0.95), 0.6)
M_SKIN = mat("dummy", (0.78, 0.74, 0.70), 0.55)
M_SUIT = mat("suit", (0.04, 0.12, 0.35), 0.55)
M_BIB = mat("bib", (1.0, 0.55, 0.08), 0.5, 0, (1.0, 0.5, 0.05), 0.4)
M_GOGG = mat("goggles", (1.0, 0.45, 0.05), 0.3, 0, (1.0, 0.45, 0.05), 0.6)
M_CONE = mat("vapour", (1, 1, 1), 0.3, 0, (0.85, 0.92, 1.0), 1.0, alpha=0.24)
M_STREAK = mat("streak", (1, 1, 1), 0.3, 0, (0.9, 0.95, 1.0), 3.0, alpha=0.55)
M_GHOST = mat("ghostcar", (0.3, 0.8, 1.0), 0.3, 0, (0.25, 0.75, 1.0), 4.0, alpha=0.45)
M_BOARD = mat("board", (0.06, 0.18, 0.55), 0.6)
M_BOARDW = mat("boardw", (0.9, 0.9, 0.9), 0.6)
M_POST = mat("post", (0.85, 0.85, 0.85), 0.4, 0.6)
M_TAPE = mat("tape", (1.0, 0.75, 0.1), 0.5, 0, (1.0, 0.7, 0.1), 1.5)
M_CLOCKB = mat("clockbg", (0.02, 0.02, 0.03), 0.5)
M_CLOCK = mat("clock", (1.0, 0.65, 0.1), 0.4, 0, (1.0, 0.6, 0.1), 8.0)
M_CROWD = mat("crowd", (1.0, 0.55, 0.08), 0.5, 0, (1.0, 0.5, 0.05), 0.5)
M_RING = mat("ring", (1.0, 0.65, 0.1), 0.4, 0, (1.0, 0.6, 0.1), 6.0)
M_RAD = mat("radius", (1, 1, 1), 0.4, 0, (1, 1, 1), 4.0)
M_BAR_R = mat("barred", (0.8, 0.06, 0.04), 0.5); M_BAR_W = mat("barwhite", (0.9, 0.9, 0.9), 0.5)

# ---------- world ----------
world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.85, 0.80, 0.70, 1)
ramp.color_ramp.elements[1].position = 0.40; ramp.color_ramp.elements[1].color = (0.15, 0.38, 0.85, 1)
nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
nt.links.new(ramp.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 4.2; sun.data.angle = math.radians(2.0); sun.data.color = (1.0, 0.93, 0.82)
sun.rotation_euler = (math.radians(50), math.radians(8), math.radians(-60)); S.collection.objects.link(sun)

# ---------- helpers ----------
def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box", parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; return link(o, m, parent)
def cyl_between(a, b, r, m, parent, name="limb", caps=True, verts=16):
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
def text(body, loc, size, m, rot=(math.radians(90), 0, 0), align="CENTER", parent=None, extrude=0.02):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object
    t.data.body = body; t.data.size = size; t.data.extrude = extrude
    t.data.align_x = align; t.data.align_y = "CENTER"; return link(t, m, parent)
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def show(o, f, on):
    o.scale = (1, 1, 1) if on else (0.0001,) * 3; o.keyframe_insert("scale", frame=f)

# ---------- timing ----------
t2, t3, t4, t5, t6 = (L[i]["start"] for i in range(2, 7))
tc = CARD_START
VEL = 30.0                       # stylised on-screen speed (m/s); the science is in the narration/card
X0 = 0.0
def runx(t): return X0 + VEL * t  # hook/card use the same law with tau = t or t - DUR (loop)
T_TAPE = 0.55                    # runner breaks the finish tape
XF = runx(T_TAPE) + 0.35
T_BEND = 9.75                    # the runner would reach the bend here (never shown: cut at t6 - 0.05)
XB = runx(T_BEND)

# ---------- ground + track ----------
box((XB, 0, -0.06), (400000, 400000, 0.1), M_GROUND, "ground")
TW = 9.76
x_a = X0 - 140
box(((x_a + XB) / 2, 0, -0.005), (XB - x_a, TW, 0.012), M_TRACK, "track")
for k in range(9):
    y = -TW / 2 + k * TW / 8
    box(((x_a + XB) / 2, y, 0.004), (XB - x_a, 0.05, 0.004), M_LINE, "lane")
box((XF, 0, 0.005), (0.3, TW, 0.006), M_LINE, "finishline")
# trackside advertising boards every 12 m (array) on both sides
for side in (-1, 1):
    b = box((x_a, side * (TW / 2 + 1.6), 0.5), (2.2, 0.08, 0.9), M_BOARD if side < 0 else M_BOARDW, "boards")
    ar = b.modifiers.new("arr", "ARRAY"); ar.count = int((XB - x_a) / 12); ar.use_relative_offset = False
    ar.use_constant_offset = True; ar.constant_offset_displace = (12.0 / 2.2, 0, 0)
# finish: posts, tape, trackside clock reading 2:03
for side in (-1, 1):
    cyl_between((XF, side * 3.0, 0), (XF, side * 3.0, 1.4), 0.04, M_POST, None, "post", caps=False)
tape = box((XF, 0, 1.2), (0.03, 6.0, 0.05), M_TAPE, "tape")
tapeL = box((XF, -2.2, 1.2), (0.03, 1.6, 0.05), M_TAPE, "tapeL"); tapeR = box((XF, 2.2, 1.2), (0.03, 1.6, 0.05), M_TAPE, "tapeR")
CLX, CLY = XF - 5.0, TW / 2 + 2.6
# the tight stadium bend ahead (36.5 m radius, turning left) + crash barrier
RB = 36.5
for k in range(40):
    a0 = -math.pi / 2 + k * (math.pi / 2) / 40; a1 = a0 + (math.pi / 2) / 40
    am = (a0 + a1) / 2; cx, cy = XB, RB
    seg_len = RB * (a1 - a0) + 0.2
    o = box((cx + RB * math.cos(am), cy + RB * math.sin(am), -0.005), (seg_len, TW, 0.012), M_TRACK, "bend")
    o.rotation_euler = (0, 0, am + math.pi / 2)
    R2 = RB - TW / 2 - 0.8
    w = box((cx + R2 * math.cos(am), cy + R2 * math.sin(am), 0.45), (R2 * (a1 - a0) + 0.05, 0.4, 0.9),
            M_BAR_R if k % 2 == 0 else M_BAR_W, "barrier")
    w.rotation_euler = (0, 0, am + math.pi / 2)

# ---------- the runner (rig follows position, body leans; feet point +x) ----------
rig = empty("rig")
body = empty("body", parent=rig)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, location=(0, 0, 0.30))
o = bpy.context.object; o.scale = (0.12, 0.19, 0.32); bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
box((0.115, 0, 0.30), (0.02, 0.2, 0.16), M_BIB, "bib", body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, location=(0, 0, 0.02))
o = bpy.context.object; o.scale = (0.125, 0.17, 0.12); bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=0.105, location=(0, 0, 0.76))
o = bpy.context.object; bpy.ops.object.shade_smooth(); link(o, M_SKIN, body)
bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.018, location=(0.01, 0, 0.78))
link(bpy.context.object, M_GOGG, body)
arms, elbows, legs, knees = [], [], [], []
for side in (-1, 1):
    sh = empty(f"shoulder{side}", (0, side * 0.21, 0.5), body)
    cyl_between((0, 0, 0), (0, side * 0.02, -0.29), 0.045, M_SKIN, sh, "upperarm")
    el = empty(f"elbow{side}", (0, side * 0.02, -0.29), sh)
    cyl_between((0, 0, 0), (0, 0, -0.27), 0.04, M_SKIN, el, "forearm")
    arms.append(sh); elbows.append(el)
for side in (-1, 1):
    hp = empty(f"hip{side}", (0, side * 0.09, 0), body)
    cyl_between((0, 0, 0), (0, 0, -0.44), 0.065, M_SUIT, hp, "thigh")
    kn = empty(f"knee{side}", (0, 0, -0.44), hp)
    cyl_between((0, 0, 0), (0, 0, -0.41), 0.05, M_SKIN, kn, "shin")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(0.05, 0, -0.43))
    ft = bpy.context.object; ft.scale = (0.11, 0.045, 0.035); link(ft, M_SUIT, kn)
    legs.append(hp); knees.append(kn)
STAND = 0.86
# vapour cone (apex at the chest, opening backwards) + speed streaks
bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=1.15, radius2=0.0, depth=2.6, end_fill_type="NOTHING",
                                location=(-0.75, 0, 1.15), rotation=(0, math.radians(90), 0))
cone = link(bpy.context.object, M_CONE, rig); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=0.85, radius2=0.0, depth=2.0, end_fill_type="NOTHING",
                                location=(-0.55, 0, 1.15), rotation=(0, math.radians(90), 0))
cone2 = link(bpy.context.object, M_CONE, rig); bpy.ops.object.shade_smooth()
STREAKS = []
for k in range(26):
    ln = random.uniform(1.5, 5.0); y = random.uniform(-1.6, 1.6); z = random.uniform(0.15, 2.2)
    x1 = random.uniform(-1.2, -0.3)
    if abs(y) < 0.35 and z < 1.9: y += 0.6 if y >= 0 else -0.6
    STREAKS.append(cyl_between((x1, y, z), (x1 - ln, y, z), random.uniform(0.006, 0.014), M_STREAK, rig, "streak", caps=False, verts=6))

# ghost car (symbol of the drag force: about a car's weight) pressing on the runner's chest
car = empty("car", parent=rig)
box((2.55, 0, 0.62), (4.2, 1.75, 0.62), M_GHOST, "carbody", car)
box((2.85, 0, 1.18), (2.1, 1.55, 0.55), M_GHOST, "carcabin", car)
for wx in (1.25, 3.85):
    for wy in (-0.8, 0.8):
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.33, depth=0.22, location=(wx, wy, 0.33), rotation=(math.radians(90), 0, 0))
        link(bpy.context.object, M_GHOST, car)
for k, z in enumerate((0.55, 1.0, 1.45)):  # air arrows pushing back (-x)
    cyl_between((5.8, -0.95, z), (4.9, -0.95, z), 0.03, M_GHOST, car, "airarrow", caps=False)
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.08, radius2=0, depth=0.2, location=(4.8, -0.95, z), rotation=(0, math.radians(-90), 0))
    link(bpy.context.object, M_GHOST, car)

# ~17,000 runners (131 x 130 array of a simple figure), travelling with the runner
crowd = empty("crowd", parent=None)
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.17, depth=1.25, location=(0, 0, 0.62)); fig = bpy.context.object
bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=5, radius=0.13, location=(0.03, 0, 1.42))
hd = bpy.context.object; hd.select_set(True); fig.select_set(True); bpy.context.view_layer.objects.active = fig
bpy.ops.object.join(); fig.rotation_euler = (0, math.radians(14), 0); link(fig, M_CROWD, crowd)
GX, GY, SP = 131, 130, 1.2      # 17,030 figures
fig.location = (-2.5, -(GY - 1) * SP / 2, 0)
a1 = fig.modifiers.new("ax", "ARRAY"); a1.count = GX; a1.use_relative_offset = False; a1.use_constant_offset = True
a1.constant_offset_displace = (-SP, 0, 0)
a2 = fig.modifiers.new("ay", "ARRAY"); a2.count = GY; a2.use_relative_offset = False; a2.use_constant_offset = True
a2.constant_offset_displace = (0, SP, 0)

# twist: the 12 km-radius turn (flat glowing ring), radius line, label, runner marker
R12 = 343.0 ** 2 / 9.81          # = 11,993 m
RINGS = []
def annulus(name, r, w, z, segs=1440):  # flat ring built directly (the torus operator caps major_radius at 10 km)
    vs, fs = [], []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        vs += [((r - w / 2) * math.cos(a), (r - w / 2) * math.sin(a), 0), ((r + w / 2) * math.cos(a), (r + w / 2) * math.sin(a), 0)]
        j = (i + 1) % segs; fs.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    o = bpy.data.objects.new(name, me); o.location = (XB, R12, z); S.collection.objects.link(o); return link(o, M_RING)
for k, wdt in enumerate((40.0, 140.0)):
    RINGS.append(annulus(f"ring{k}", R12, wdt, 0.3 + k * 0.2))
rline = box((XB, R12 / 2, 0.6), (70, R12, 0.5), M_RAD, "radius"); bpy.ops.object.transform_apply(scale=True)
lbl = text("12 km", (XB - 2500, R12 * 0.42, 1.0), 1600, M_RAD, rot=(0, 0, 0), extrude=0)
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1.0, location=(XB, 0, 0)); marker = link(bpy.context.object, M_RAD)

# ---------- animation ----------
OMEGA = 2 * math.pi * 3.0
def seg_of(t):
    if t < t2 - 0.05: return "hook"
    if t >= tc: return "card"
    if t < t3 - 0.05: return "side"
    if t < t4 - 0.05: return "car"
    if t < t5 - 0.05: return "crowd"
    if t < t6 - 0.05: return "bend"
    return "aerial"
def runner_t(t):
    return t - DUR if seg_of(t) == "card" else t
for f in range(0, N + 1):
    t = f / FPS; sg = seg_of(t); tau = runner_t(t)
    x = runx(tau)
    ph = OMEGA * tau
    rig.location = V((x, 0, 0)); rig.keyframe_insert("location", frame=f)
    push = sg == "car"
    body.location = V((0, 0, STAND + 0.035 * abs(math.sin(ph))))
    body.rotation_euler = (0, math.radians(30 if push else 14), 0)
    body.keyframe_insert("location", frame=f); body.keyframe_insert("rotation_euler", frame=f)
    for k in range(2):
        p = ph + k * math.pi
        legs[k].rotation_euler = (0, -0.75 * math.sin(p) - 0.1, 0)
        knees[k].rotation_euler = (0, 0.35 + 0.85 * (0.5 + 0.5 * math.sin(p + 1.4)), 0)
        if push:  # arms forward, braced against the ghost car
            arms[k].rotation_euler = (0, math.radians(-75) + 0.05 * math.sin(p), 0); elbows[k].rotation_euler = (0, -0.25, 0)
        else:
            arms[k].rotation_euler = (0, 0.9 * math.sin(p), 0); elbows[k].rotation_euler = (0, -1.45, 0)
        for o in (legs[k], knees[k], arms[k], elbows[k]): o.keyframe_insert("rotation_euler", frame=f)
    show(car, f, push)
    show(cone, f, sg not in ("aerial", "bend")); show(cone2, f, sg not in ("aerial", "bend"))
    crowd.location = V((x, 0, 0)); crowd.keyframe_insert("location", frame=f)
    show(crowd, f, sg == "crowd")
    broke = sg == "hook" and t >= T_TAPE
    show(tape, f, not broke); show(tapeL, f, broke); show(tapeR, f, broke)
    if broke:  # tape ends flutter back
        u = t - T_TAPE
        tapeL.location = V((XF - 0.9 * u, -3.0 + 0.8 * math.cos(u * 3), 1.2 - 0.3 * u)); tapeL.rotation_euler = (0, 0, 0.8 + u)
        tapeR.location = V((XF - 0.9 * u, 3.0 - 0.8 * math.cos(u * 3), 1.2 - 0.3 * u)); tapeR.rotation_euler = (0, 0, -0.8 - u)
        tapeL.keyframe_insert("location", frame=f); tapeR.keyframe_insert("location", frame=f)
        tapeL.keyframe_insert("rotation_euler", frame=f); tapeR.keyframe_insert("rotation_euler", frame=f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_start = 0.1; cam.data.clip_end = 120000
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
HOOK = ((4.6, -3.9, 0.55), (0.0, 0.0, 0.95))
P_A = V((XB - 6, -9, 9)); P_E = V((XB, -17000, 19000)); Q_A = V((XB + 40, 4, 0)); Q_E = V((XB, 4200, 0))
def expo(u, k=5.0): return (math.exp(k * u) - 1) / (math.exp(k) - 1)
SEG = [  # (t0, t1, name, lens_a, lens_b)
    (0.0, t2 - 0.05, "hook", 22, 23),
    (t2 - 0.05, t3 - 0.05, "side", 24, 24),
    (t3 - 0.05, t4 - 0.05, "car", 24, 25),
    (t4 - 0.05, t5 - 0.05, "crowd", 24, 24),
    (t5 - 0.05, t6 - 0.05, "bend", 22, 24),
    (t6 - 0.05, tc, "aerial", 24, 24),
    (tc, DUR + 0.01, "card", 23, 22),
]
for f in range(0, N + 1):
    t = f / FPS
    s = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - s[0]) / (s[1] - s[0])); ul = (t - s[0]) / (s[1] - s[0])
    r = V((runx(runner_t(t)), 0, 0)); nm = s[2]
    if nm == "hook":
        p = r + V(HOOK[0]) + V((0.0, 0.3 * ul, 0.1 * ul)); q = r + V(HOOK[1])
    elif nm == "card":   # ease back into the opening framing (loop)
        p = r + V(HOOK[0]) + V((0.5 * (1 - u), -0.6 * (1 - u), 0.25 * (1 - u))); q = r + V(HOOK[1])
    elif nm == "side":
        p = r + V((0.6 - 0.8 * ul, -7.2, 1.25)); q = r + V((0.2, 0, 1.05))
    elif nm == "car":
        p = r + V((1.6 + 0.3 * ul, -7.6, 1.5)); q = r + V((1.25, 0, 1.0))
    elif nm == "crowd":
        k = smooth(ul * 1.15)
        p = r + V((-3.5, -3.2, 1.6)).lerp(V((-40, -95, 95)), k); q = r + V((1.0, 0, 1.0)).lerp(V((-70, 0, 0)), k)
    elif nm == "bend":
        p = r + V((-7.5 - 1.0 * ul, -2.4, 2.4 + 0.4 * ul)); q = r + V((10, 3, -0.6))
    else:  # aerial pull-up from just behind the runner to ~20 km
        g = expo(min(1.0, ul / 0.6), 4.0); g = g + 0.06 * max(0.0, ul - 0.6) / 0.4
        p = P_A.lerp(P_E, g); q = Q_A.lerp(Q_E, g)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = s[3] + (s[4] - s[3]) * u; cam.data.keyframe_insert("lens", frame=f)
    aer = nm == "aerial"   # twist props scale with altitude so they stay readable
    show(RINGS[0], f, aer and 600 < p.z <= 4000); show(RINGS[1], f, aer and p.z > 4000)
    show(rline, f, aer and p.z > 2500); show(lbl, f, aer and p.z > 6000)
    ms = max(1.0, p.z * 0.012) if aer else 0.0001
    marker.location = V((runx(t), 0, ms * 0.5)); marker.scale = (ms,) * 3
    marker.keyframe_insert("location", frame=f); marker.keyframe_insert("scale", frame=f)
    show(rig, f, not (aer and p.z > 300))

json.dump({"t_tape": T_TAPE, "t_car": t3 - 0.05, "t_crowd": t4 - 0.05, "t_bend": t5 - 0.05, "t_aerial": t6 - 0.05,
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
