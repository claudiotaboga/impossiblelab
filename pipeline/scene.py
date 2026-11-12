"""The Impossible Lab #07 - basketball on the Moon.
A basketball court under a ribbed dome on the grey lunar plain, Earth in the black sky.
Moon gravity 1.62 m/s^2: the same take-off speed as a 1 m Earth leap (4.43 m/s) lifts the
player 6.05 m (feet far above the 3.05 m rim) and keeps him airborne 5.5 s (shot clock counts it).
Twist: a normal free throw (7.55 m/s at 52 deg, dome air drag included) flies ~21 m, 5x too far;
blue dotted arc = the same shot on Earth (4.2 m to the rim), amber = on the Moon.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(7)
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
L = {l["i"]: l for l in LINES}
V = Vector

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
def plank_mat():
    m = bpy.data.materials.new("court"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.35
    br = nt.nodes.new("ShaderNodeTexBrick"); br.offset = 0.5
    br.inputs["Color1"].default_value = (0.78, 0.50, 0.25, 1); br.inputs["Color2"].default_value = (0.70, 0.44, 0.21, 1)
    br.inputs["Mortar"].default_value = (0.55, 0.34, 0.16, 1); br.inputs["Scale"].default_value = 0.5
    br.inputs["Mortar Size"].default_value = 0.003; br.inputs["Brick Width"].default_value = 2.5; br.inputs["Row Height"].default_value = 0.16
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return m

M_REGO = noise_mat("regolith", (0.20, 0.20, 0.21), (0.46, 0.46, 0.47), 0.15, 14, 0.5)
M_ROCK = mat("rock", (0.25, 0.25, 0.26), 0.9)
M_DECK = mat("deck", (0.30, 0.31, 0.34), 0.7)
M_COURT = plank_mat()
M_KEY = mat("key", (0.10, 0.22, 0.55), 0.4)
M_LINE = mat("line", (0.95, 0.95, 0.95), 0.4)
M_RIB = mat("rib", (0.80, 0.82, 0.86), 0.35, 0.6)
M_GLASS = mat("board", (0.92, 0.95, 1.0), 0.15)
M_RIM = mat("rim", (1.0, 0.30, 0.03), 0.3, 0.5)
M_NET = mat("net", (0.95, 0.95, 0.95), 0.6)
M_POLE = mat("pole", (0.12, 0.13, 0.16), 0.4, 0.5)
M_CLOCKBOX = mat("clockbox", (0.02, 0.02, 0.02), 0.5)
M_CLOCK = mat("clock", (1.0, 0.25, 0.1), 0.5, 0, (1.0, 0.22, 0.06), 9.0)
M_EARTHTXT = mat("earthtxt", (0.35, 0.65, 1.0), 0.5, 0, (0.35, 0.65, 1.0), 7.0)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_JERSEY = mat("jersey", (0.95, 0.55, 0.06), 0.6)
M_SHORTS = mat("shorts", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_BALL = mat("ball", (0.85, 0.30, 0.05), 0.55)
M_SEAM = mat("seam", (0.03, 0.02, 0.02), 0.6)
M_RED = mat("gaugered", (0.80, 0.07, 0.05), 0.45)
M_WHT = mat("gaugewhite", (0.90, 0.90, 0.88), 0.45)
M_MARK = mat("mark", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 4.0)
M_BLUEMK = mat("bluemark", (0.3, 0.6, 1.0), 0.4, 0, (0.3, 0.6, 1.0), 4.0)
M_DOT = mat("dot", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.62, 0.12), 10.0)
M_EDOT = mat("edot", (0.3, 0.6, 1.0), 0.4, 0, (0.3, 0.6, 1.0), 10.0)

def earth_mat():
    m = bpy.data.materials.new("earth"); m.use_nodes = True; nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"]); out = nt.nodes["Material Output"]
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.6
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 8
    rp = nt.nodes.new("ShaderNodeValToRGB"); e = rp.color_ramp.elements
    e[0].position = 0.45; e[0].color = (0.04, 0.16, 0.55, 1); e[1].position = 0.62; e[1].color = (0.95, 0.97, 1.0, 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"]); return m

# ---------- world: black sky with stars ----------
world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
vn = nt.nodes.new("ShaderNodeTexVoronoi"); vn.inputs["Scale"].default_value = 260
tcw = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tcw.outputs["Generated"], vn.inputs["Vector"])
rp = nt.nodes.new("ShaderNodeValToRGB"); rp.color_ramp.elements[0].position = 0.0; rp.color_ramp.elements[0].color = (1, 1, 1, 1)
rp.color_ramp.elements[1].position = 0.035; rp.color_ramp.elements[1].color = (0.004, 0.004, 0.006, 1)
nt.links.new(vn.outputs["Distance"], rp.inputs[0]); nt.links.new(rp.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 5.0; sun.data.angle = math.radians(0.6); sun.data.color = (1.0, 0.98, 0.94)
sun.rotation_euler = (math.radians(58), math.radians(0), math.radians(-120)); S.collection.objects.link(sun)
for x in (-14, 0, 14):  # dome flood lights
    lt = bpy.data.objects.new("flood", bpy.data.lights.new("flood", "AREA"))
    lt.data.energy = 9000; lt.data.size = 8; lt.data.color = (1.0, 0.95, 0.88)
    lt.location = (x, -6, 24); S.collection.objects.link(lt)

# ---------- helpers ----------
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
def text(body, loc, rot, size, m, align="LEFT"):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object
    t.data.body = body; t.data.size = size; t.data.extrude = 0.01; t.data.align_x = align; t.data.align_y = "CENTER"
    return link(t, m)
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def ring(loc, R, r, m, name="ring"):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=64, minor_segments=8, location=loc)
    o = bpy.context.object; o.name = name; return link(o, m)

# ---------- lunar plain + craters ----------
bpy.ops.mesh.primitive_plane_add(size=3000, location=(0, 0, -0.3)); link(bpy.context.object, M_REGO)
for k in range(26):
    a = random.uniform(0, 2 * math.pi); d = random.uniform(55, 400); R = random.uniform(4, 22)
    o = ring((d * math.cos(a), d * math.sin(a), -0.3), R, R * 0.12, M_REGO, "crater"); o.scale = (1, 1, 0.35)
for k in range(60):
    a = random.uniform(0, 2 * math.pi); d = random.uniform(44, 160)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.3, 1.6), location=(d * math.cos(a), d * math.sin(a), -0.3))
    o = bpy.context.object; o.scale = (1, random.uniform(0.6, 1.2), random.uniform(0.3, 0.7)); link(o, M_ROCK)

# ---------- dome (ribbed hemisphere, r = 40 m) ----------
DR = 40.0
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=DR + 0.5, depth=0.6, location=(0, 0, 0.0)); link(bpy.context.object, M_DECK)
bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=14, radius=DR, location=(0, 0, 0))
dome = bpy.context.object
import bmesh
bpy.ops.object.mode_set(mode="EDIT"); bm = bmesh.from_edit_mesh(dome.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.01], context="VERTS"); bmesh.update_edit_mesh(dome.data)
bpy.ops.object.mode_set(mode="OBJECT")
wf = dome.modifiers.new("wf", "WIREFRAME"); wf.thickness = 0.35; wf.use_replace = True
link(dome, M_RIB)

# ---------- court (NBA: 28.65 x 15.24 m, along x) ----------
CL, CW = 28.65, 15.24
box((0, 0, 0.30), (CL + 3, CW + 3, 0.02), M_COURT, "court")
BASE = -CL / 2                          # baseline x
FTX = BASE + 5.80                       # free-throw line
RIM_Z = 3.05; FLOOR = 0.31
def line_box(x0, y0, x1, y1, w=0.05):
    box(((x0 + x1) / 2, (y0 + y1) / 2, FLOOR + 0.002), (abs(x1 - x0) + w, abs(y1 - y0) + w, 0.004), M_LINE, "line")
for s in (-1, 1):
    line_box(-CL / 2, s * CW / 2, CL / 2, s * CW / 2)
    line_box(s * CL / 2, -CW / 2, s * CL / 2, CW / 2)
    bx = s * CL / 2; fx = s * (CL / 2 - 5.80)
    box(((bx + fx) / 2, 0, FLOOR + 0.001), (5.80, 4.88, 0.003), M_KEY, "key")
    line_box(bx, -2.44, fx, -2.44); line_box(bx, 2.44, fx, 2.44); line_box(fx, -2.44, fx, 2.44)
    o = ring((fx, 0, FLOOR + 0.003), 1.83, 0.025, M_LINE); o.scale = (1, 1, 0.1)
line_box(0, -CW / 2, 0, CW / 2)
o = ring((0, 0, FLOOR + 0.003), 1.83, 0.025, M_LINE); o.scale = (1, 1, 0.1)

# ---------- hoops (one at each end; the -x one has the shot clock) ----------
def hoop(s):
    rx = s * (CL / 2 - 1.575); bdx = s * (CL / 2 - 1.20)
    box((bdx + s * 0.03, 0, 3.43), (0.05, 1.83, 1.07), M_GLASS, "board")
    for zz in (2.9, 3.96):
        box((bdx, 0, zz), (0.07, 1.86, 0.04), M_POLE, "boardframe")
    box((bdx - s * 0.01, 0, 3.24), (0.03, 0.62, 0.04), M_RIM, "sq"); box((bdx - s * 0.01, 0, 3.6), (0.03, 0.62, 0.04), M_RIM, "sq")
    for yy in (-0.3, 0.3): box((bdx - s * 0.01, yy, 3.42), (0.03, 0.04, 0.4), M_RIM, "sq")
    ring((rx, 0, RIM_Z), 0.23, 0.012, M_RIM, "rim")
    cyl_between((bdx, 0, RIM_Z), (rx + s * 0.23, 0, RIM_Z), 0.015, M_RIM, caps=False)
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.23, radius2=0.15, depth=0.42, location=(rx, 0, RIM_Z - 0.21), end_fill_type="NOTHING")
    net = bpy.context.object; nw = net.modifiers.new("wf", "WIREFRAME"); nw.thickness = 0.008; link(net, M_NET)
    px = s * (CL / 2 + 1.0)
    cyl_between((px, 0, FLOOR), (px, 0, 3.6), 0.12, M_POLE, caps=False)
    cyl_between((px, 0, 3.6), (bdx + s * 0.05, 0, 3.6), 0.08, M_POLE, caps=False)
    box((px, 0, FLOOR + 0.5), (1.0, 1.0, 1.0), M_POLE, "base")
    return rx, bdx
RIMX, BDX = hoop(-1); hoop(1)
# shot clock above the board (counts the hang time)
box((BDX, 0, 4.50), (0.14, 0.95, 0.72), M_CLOCKBOX, "clockbox")
TROT = (math.radians(90), 0, math.radians(90))      # faces +x (the court)
clock_txt = text("0.0 s", (BDX + 0.08, 0, 4.62), TROT, 0.36, M_CLOCK, "CENTER")
earth_txt = text("EARTH 0.9 s", (BDX + 0.08, 0, 4.27), TROT, 0.15, M_EARTHTXT, "CENTER")

# ---------- height gauge beside the player (feet clearance; red/white 1 m bands) ----------
PX, PY = RIMX + 1.15, 0.0             # jump spot, clear of the rim
GX, GY = PX + 0.15, 1.15
GAUGE = []; GLABELS = []
for k in range(7):
    GAUGE.append(box((GX, GY, FLOOR + k + 0.5), (0.18, 0.18, 1.0), M_RED if k % 2 == 0 else M_WHT, "gauge"))
for h, mm, lab in ((1.0, M_BLUEMK, "1 m · EARTH"), (6.05, M_MARK, "6 m · MOON")):
    GAUGE.append(box((GX, GY, FLOOR + h), (0.42, 0.42, 0.05), mm, "gmark"))
    GLABELS.append(text(lab, (GX + 0.3, GY - 0.12, FLOOR + h + 0.18), (math.radians(90), 0, 0), 0.30, mm))

# ---------- player mannequin (pelvis at origin, faces -x, shoulders along y) ----------
body = empty("body")
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.30))
o = bpy.context.object; o.scale = (0.12, 0.20, 0.32); bpy.ops.object.shade_smooth(); link(o, M_JERSEY, body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.02))
o = bpy.context.object; o.scale = (0.13, 0.18, 0.13); bpy.ops.object.shade_smooth(); link(o, M_SHORTS, body)
cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, radius=0.105, location=(0, 0, 0.76))
o = bpy.context.object; bpy.ops.object.shade_smooth(); link(o, M_SKIN, body)
arms, legs = [], []
for side in (-1, 1):
    sh = empty(f"shoulder{side}", (0, side * 0.21, 0.5), body)
    cyl_between((0, 0, 0), (0, side * 0.03, -0.30), 0.045, M_SKIN, sh, "upperarm")
    cyl_between((0, side * 0.03, -0.30), (0, side * 0.04, -0.58), 0.04, M_SKIN, sh, "forearm")
    sh.rotation_mode = "XYZ"; arms.append(sh)
for side in (-1, 1):
    hp = empty(f"hip{side}", (0, side * 0.09, 0), body)
    cyl_between((0, 0, 0), (0, side * 0.01, -0.45), 0.068, M_SHORTS, hp, "thigh")
    cyl_between((0, side * 0.01, -0.45), (0, side * 0.01, -0.86), 0.05, M_SKIN, hp, "shin")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(-0.05, side * 0.01, -0.88))
    ft = bpy.context.object; ft.scale = (0.12, 0.05, 0.04); link(ft, M_SHOE, hp)
    hp.rotation_mode = "XYZ"; legs.append(hp)
STAND = FLOOR + 0.915     # pelvis height standing

# ---------- ball ----------
ball = empty("ball")
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.12); o = bpy.context.object
bpy.ops.object.shade_smooth(); link(o, M_BALL, ball)
for rot in ((0, 0, 0), (math.pi / 2, 0, 0), (0, math.pi / 2, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.121, minor_radius=0.006, rotation=rot); link(bpy.context.object, M_SEAM, ball)
ball.rotation_mode = "XYZ"

# ---------- Earth (placed in the sky per shot) ----------
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=55); earth = bpy.context.object; link(earth, earth_mat())

# ---------- physics ----------
GM, GE = 1.62, 9.80
V0 = math.sqrt(2 * GE * 1.0)                       # take-off speed of a 1 m Earth leap (4.43 m/s)
T_AIR = 2 * V0 / GM                                # 5.47 s on the Moon
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_TO = t3 + 0.30                                   # take-off ("Gravity is six times weaker...")
T_LAND = T_TO + T_AIR
def jump_rise(t):
    if t < T_TO or t > T_LAND: return 0.0
    u = t - T_TO; return V0 * u - 0.5 * GM * u * u
APEX = V0 * V0 / (2 * GM)                          # 6.05 m
def hook_rise(tau):                                # hover near the apex for the cold open / loop end
    return APEX - 0.5 * GM * (tau - 0.9) ** 2

def shot(v, deg, g, h0, x0, drag=True):
    """free throw toward -x; dome air: Cd 0.47, r 0.12 m, m 0.6 kg, rho 1.2. returns [(t, x, z)] until the floor."""
    k = 0.5 * 1.2 * 0.47 * math.pi * 0.12 ** 2 / 0.6 if drag else 0.0
    a = math.radians(deg); x, z, vx, vz = 0.0, h0, v * math.cos(a), v * math.sin(a); dt = 1 / 960; T = 0; out = [(0, x0, z)]
    while z > FLOOR + 0.12 or vz > 0:
        s = math.hypot(vx, vz); vx += -k * s * vx * dt; vz += (-g - k * s * vz) * dt
        x += vx * dt; z += vz * dt; T += dt; out.append((T, x0 - x, z))
    return out
REL_H = STAND + 1.05
SHOOTX = FTX + 0.25
MOON_PATH = shot(7.55, 52, GM, REL_H, SHOOTX)
EARTH_PATH = shot(7.55, 52, GE, REL_H, SHOOTX)
LAND_X = MOON_PATH[-1][1]
T_REL = t7 + 0.10
def ball_at(path, t):
    i = min(int(t * 960), len(path) - 1); return path[i]

# dotted arcs
def dots(path, m, every, r):
    out = []
    for i in range(0, len(path), every):
        _, x, z = path[i]
        bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=5, radius=r, location=(x, 0, z))
        o = bpy.context.object; link(o, m); out.append((o, path[i][0]))
    return out
EDOTS = dots(EARTH_PATH[: next(i for i, p in enumerate(EARTH_PATH) if p[1] <= RIMX)], M_EDOT, 48, 0.05)
MDOTS = dots(MOON_PATH, M_DOT, 160, 0.09)
LAND_RING = ring((LAND_X, 0, FLOOR + 0.02), 0.7, 0.07, M_DOT, "landring"); LAND_RING.scale = (1, 1, 0.3)
LBL5 = text("×5", (LAND_X + 0.3, 0.0, FLOOR + 2.4), (math.radians(90), 0, math.radians(73)), 2.4, M_MARK, "CENTER")
EARTH_RING = ring((RIMX, 0, RIM_Z), 0.32, 0.03, M_EDOT, "earthrimring")

def vis(o, on, f, base=(1, 1, 1)):
    o.scale = base if on else (0.0001,) * 3; o.keyframe_insert("scale", frame=f)

# ---------- animate player + ball ----------
def pose(t):
    """-> (pelvis pos, arm_x, arm_y, leg_bend, ball pos, mode)"""
    if t < t2 or t >= tc:                          # cold open / loop: hovering high above the rim, ball overhead
        tau = t if t < t2 else t - tc
        p = V((RIMX + 0.55, 0.0, STAND + hook_rise(tau)))
        return p, math.radians(165), 0.0, 0.5, p + V((-0.12, 0, 1.30)), "air"
    if t < t6:                                     # the big vertical jump (real-time Moon physics)
        r = jump_rise(t); p = V((PX, PY, STAND + r))
        crouch = 0.0
        if T_TO - 0.35 < t < T_TO: crouch = math.sin(math.pi * (t - (T_TO - 0.35)) / 0.35) * 0.22
        if T_LAND < t < T_LAND + 0.35: crouch = math.sin(math.pi * (t - T_LAND) / 0.35) * 0.18
        p.z -= crouch
        up = smooth((t - (T_TO - 0.2)) / 0.3) * (1 - smooth((t - T_LAND) / 0.4))
        arm = math.radians(20 + 145 * up)
        bpos = p + V((-0.12, 0, 0.5 + 0.8 * up)) if up > 0.3 else p + V((-0.32, 0, 0.0))
        return p, arm, 0.0, 0.25 * up + crouch * 2, bpos, "jump"
    # free throw: set, dip, release at T_REL
    p = V((SHOOTX + 0.25, 0, STAND)); dip = 0.0
    if T_REL - 0.45 < t < T_REL: dip = math.sin(math.pi * (t - (T_REL - 0.45)) / 0.45) * 0.12
    p.z -= dip
    lift = smooth((t - (T_REL - 0.25)) / 0.25)
    ay = math.radians(95 + 55 * lift)
    hand = p + V((-0.30 - 0.15 * lift, 0, 0.75 + 0.30 * lift))
    if t < T_REL: return p, 0.0, ay, dip * 1.5, hand, "set"
    _, bx, bz = ball_at(MOON_PATH, t - T_REL)
    return p, 0.0, ay, 0.0, V((bx, 0, bz)), "fly"

for f in range(0, N + 1):
    t = f / FPS
    p, ax, ay, bend, bp, mode = pose(t)
    body.location = p; body.keyframe_insert("location", frame=f)
    for k, sh in enumerate(arms):
        side = -1 if k == 0 else 1
        sh.rotation_euler = (side * ax * (0.9 if mode == "air" else 1.0), -ay, 0); sh.keyframe_insert("rotation_euler", frame=f)
    for k, hp in enumerate(legs):
        hp.rotation_euler = (0, -bend * (1 if k == 0 else 0.8), 0); hp.keyframe_insert("rotation_euler", frame=f)
    ball.location = bp; ball.rotation_euler = (0, -t * (6 if mode == "fly" else 1.5), 0)
    ball.keyframe_insert("location", frame=f); ball.keyframe_insert("rotation_euler", frame=f)
    for o, td in EDOTS: vis(o, t7 - 0.05 <= t < tc and t >= T_REL + 0.15 + td * 0.6, f)
    for o, td in MDOTS: vis(o, t7 - 0.05 <= t < tc and t >= T_REL + 0.25 + td * 0.22, f)
    on_end = t7 - 0.05 <= t < tc and t >= T_REL + 0.25 + MOON_PATH[-1][0] * 0.22
    vis(LAND_RING, on_end, f, (1, 1, 0.3)); vis(LBL5, on_end, f); vis(EARTH_RING, t7 - 0.05 <= t < tc and t >= T_REL + 0.6, f)
    vis(earth_txt, t5 + 0.5 <= t < t6, f)
    for o in GAUGE: vis(o, not (t6 - 0.05 <= t < tc), f)
    for o in GLABELS: vis(o, T_TO + 1.3 <= t < t6 - 0.05, f)          # labels only in the jump shots (no edge crops)

# shot clock text: counts the hang time of the big jump, frozen after landing
def clock_value(t):
    if t2 <= t < tc and t >= T_TO: return min(t - T_TO, T_AIR)
    if t2 <= t < tc: return 0.0
    return T_AIR
def upd(scene, *a):
    t = scene.frame_current / FPS
    clock_txt.data.body = f"{clock_value(t):.1f} s"
bpy.app.handlers.frame_change_pre.append(upd)

# ---------- camera: piecewise segments, hard cuts timed to the lines ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((RIMX + 5.0, -3.8, 1.3), (RIMX + 0.1, 0.3, 6.2), (RIMX + 4.6, -3.5, 1.35), (RIMX + 0.1, 0.3, 6.25))
SEG = [  # (t0, t1, spec, lens_a, lens_b, earth (up, side) or None)
    (0.0, t2 - 0.05, HOOK, 21, 22, (0.16, -0.24)),
    (t2 - 0.05, t3 - 0.05, fixed((27, -55, 10), (-2, 0, 11), (22, -46, 8.5), (-2, 0, 10)), 26, 27, (0.04, 0.20)),
    (t3 - 0.05, T_TO + 1.3, ("follow", (5.4, -6.0, 0.6), (0.3, 0.6, 0.6)), 26, 26, None),
    (T_TO + 1.3, t4 - 0.05, fixed((PX + 9.5, -15.5, 3.6), (PX - 0.8, 0.8, 3.9)), 28, 28, None),
    (t4 - 0.05, t4 + 0.95, fixed((PX + 4.4, -5.6, 7.6), (PX + 0.5, 0.9, 6.3), (PX + 4.2, -5.3, 7.3), (PX + 0.5, 0.9, 6.0)), 26, 27, None),
    (t4 + 0.95, t5 - 0.05, fixed((PX + 6.6, -8.6, 1.2), (PX + 0.4, 0.9, 2.9)), 26, 26, None),
    (t5 - 0.05, t6 - 0.05, fixed((BDX + 4.4, -2.6, 4.2), (BDX, 0, 4.35), (BDX + 3.6, -2.1, 4.25), (BDX, 0, 4.35)), 30, 32, None),
    (t6 - 0.05, t7 - 0.05, fixed((SHOOTX + 3.4, -2.4, 1.9), (SHOOTX - 2.2, 0.2, 2.5), (SHOOTX + 3.0, -2.2, 1.9), (SHOOTX - 2.2, 0.2, 2.5)), 26, 26, None),
    (t7 - 0.05, tc, fixed((SHOOTX + 6.5, -8.5, 7.5), (SHOOTX - 11.0, 0, 3.4), (SHOOTX + 6.0, -8.0, 7.8), (SHOOTX - 11.5, 0, 3.2)), 24, 24, None),
    (tc, DUR + 0.01, HOOK, 22, 21, (0.16, -0.24)),
]
EARTH_PARK = V((-500, 700, -400))      # below the horizon when not wanted
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    spec = seg[2]
    if spec[0] == "follow":
        bp = pose(t)[0]; p = bp + V(spec[1]); q = bp + V(spec[2])
        p.z = max(p.z * 0.55 + 0.6, 0.9)
    else:
        _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.lens = lens; cam.data.keyframe_insert("lens", frame=f)
    if seg[5]:
        fw = (q - p).normalized(); rt = fw.cross(V((0, 0, 1))).normalized(); up = rt.cross(fw)
        e = p + 1500 * (fw + seg[5][0] * up + seg[5][1] * rt).normalized()
    else:
        e = EARTH_PARK
    earth.location = e; earth.keyframe_insert("location", frame=f)

json.dump({"t_takeoff": T_TO, "t_land": T_LAND, "t_air": T_AIR, "apex": APEX, "t_release": T_REL,
           "moon_range_m": SHOOTX - LAND_X, "moon_flight_s": MOON_PATH[-1][0], "earth_rim_x_dist": SHOOTX - RIMX,
           "t_card": tc, "cuts": [s[0] for s in SEG[1:]]}, open("/home/claude/reel/beats.json", "w"), indent=1)

# ---------- render ----------
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
