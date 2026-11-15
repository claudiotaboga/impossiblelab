"""The Impossible Lab #10 - you, 10x taller (square-cube law).
Units: metres. The giant is the standard mannequin (1.75 units) scaled x10 = 17.5 m; a 1.75 m person stands at its feet.
Shots: (hook) giant running down a suburban street, shins glowing red (x10 stress), houses at knee height;
grow x10 beside a house with a height bar; WEIGHT x1,000: a 10x10x10 cube of 1 m blocks assembles next to one block;
BONE x100: a 10x10 tile slab (cross-section) appears beside it; run: shins heat up, the giant buckles at "break";
the only fix: the giant stands chest-deep in a lake, glow gone, a whale surfaces. Card: back to the hook framing.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, bmesh, addon_utils, math, random, sys, os, json, time
from mathutils import Vector, Matrix
from config import FPS, FRAMES as N, DUR

random.seed(10)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 6; S.cycles.glossy_bounces = 2; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 4; S.cycles.transparent_max_bounces = 4
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
def noise_mat(name, c1, c2, scale, rough=0.95):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = scale; nz.inputs["Detail"].default_value = 6
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (*c1, 1); rp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(nz.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
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

M_GRASS = noise_mat("grass", (0.12, 0.30, 0.07), (0.24, 0.46, 0.12), 0.08, 0.8)
M_ROAD = noise_mat("road", (0.10, 0.10, 0.11), (0.18, 0.18, 0.19), 1.5, 0.85)
M_LINE = mat("line", (0.95, 0.92, 0.80), 0.6)
M_PLAZA = noise_mat("plaza", (0.55, 0.53, 0.50), (0.68, 0.66, 0.62), 0.6, 0.9)
M_WALLS = [mat("w1", (0.86, 0.80, 0.68), 0.8), mat("w2", (0.70, 0.78, 0.84), 0.8), mat("w3", (0.90, 0.72, 0.62), 0.8)]
M_ROOF = mat("roof", (0.45, 0.16, 0.12), 0.7)
M_WIN = mat("win", (0.15, 0.22, 0.30), 0.15)
M_TRUNK = mat("trunk", (0.25, 0.16, 0.09), 0.9)
M_LEAF = mat("leaf", (0.10, 0.32, 0.10), 0.8)
M_CAR = mat("car", (0.10, 0.35, 0.75), 0.3, 0.3)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_SHIRT = mat("shirt", (0.95, 0.55, 0.06), 0.6)
M_PANTS = mat("pants", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_SHIRT2 = mat("shirt2", (0.15, 0.55, 0.30), 0.6)
M_BLOCK = mat("block", (0.95, 0.62, 0.15), 0.5)
M_TILE = mat("tile", (0.85, 0.88, 0.92), 0.4, 0, (0.55, 0.75, 1.0), 0.6)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 6.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.45, 0.75, 1.0), 6.0)
M_LBLW = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 4.0)
M_WATER = liquid("lake", (0.30, 0.55, 0.72), (0.18, 0.38, 0.58), 0.30)
M_WHALE = mat("whale", (0.13, 0.20, 0.32), 0.4)
M_SAND = noise_mat("sand", (0.60, 0.55, 0.40), (0.72, 0.66, 0.50), 0.3)
# stress glow on the giant's shins: emission strength animated per frame
M_HOT = mat("hot", (0.9, 0.05, 0.02), 0.5, 0, (1.0, 0.04, 0.01), 0.0)
HOT = M_HOT.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tcw = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tcw.outputs["Generated"], sep.inputs[0])
rpw = nt.nodes.new("ShaderNodeValToRGB"); e = rpw.color_ramp.elements
e[0].position = 0.48; e[0].color = (0.70, 0.78, 0.88, 1); e[1].position = 0.85; e[1].color = (0.28, 0.45, 0.72, 1)
nt.links.new(sep.outputs["Z"], rpw.inputs[0]); nt.links.new(rpw.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.1
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.4; sun.data.angle = math.radians(6); sun.data.color = (1.0, 0.95, 0.88)
sun.rotation_euler = (math.radians(48), 0, math.radians(-30)); S.collection.objects.link(sun)

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
def text(body, loc, size, m, rot=(math.radians(90), 0, 0)):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object
    t.data.body = body; t.data.size = size; t.data.extrude = 0.02; t.data.align_x = "CENTER"; t.data.align_y = "CENTER"
    t.visible_shadow = False
    return link(t, m)
def sphere(loc, r, m, name="sph", parent=None, seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def vis(o, on, f, base=(1, 1, 1)):
    o.scale = base if on else (0.0001,) * 3; o.keyframe_insert("scale", frame=f)
def grid_mesh(name, nx, ny, nz, size, gap, m, origin):
    """One mesh of nx*ny*nz cubes (edge `size`, spacing size+gap), min corner at origin."""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); st = size + gap
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                c = V((i * st + size / 2, j * st + size / 2, k * st + size / 2))
                bmesh.ops.create_cube(bm, size=size, matrix=Matrix.Translation(c))
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); S.collection.objects.link(o)
    o.location = origin; return link(o, m)

# ---------- ground: grass, a street along x ----------
box((-40, 0, -0.5), (400, 400, 1.0), M_GRASS, "ground")       # top at z=0, x in [-240, 160]
box((-40, 0, 0.01), (400, 9, 0.02), M_ROAD, "road")
for k in range(-40, 27):
    box((k * 6.0, 0, 0.03), (3.0, 0.25, 0.01), M_LINE, "dash")
def house(x, y, w, d, h, mw):
    box((x, y, h / 2), (w, d, h), mw, "house")
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=w * 0.78, depth=3.2, location=(x, y, h + 1.6))
    r = bpy.context.object; r.rotation_euler = (0, 0, math.radians(45)); r.scale = (1, d / w, 1); link(r, M_ROOF)
    for k in (-1, 1):
        box((x + k * w * 0.25, y - d / 2 - 0.02, h * 0.55), (1.4, 0.05, 1.3), M_WIN, "win")
    box((x, y - d / 2 - 0.02, 1.0), (1.1, 0.05, 2.0), M_WIN, "door")
for k, x in enumerate(range(-230, 150, 15)):
    if -175 < x < -115: continue                                # plaza for the cube shot
    house(x + random.uniform(-2, 2), 14 + random.uniform(0, 3), random.uniform(8, 10), 8, random.uniform(4.5, 5.5), M_WALLS[k % 3])
def tree(x, y, s=1.0):
    cyl_between((x, y, 0), (x, y, 2.5 * s), 0.25 * s, M_TRUNK, caps=False, verts=8)
    sphere((x, y, 3.8 * s), 1.9 * s, M_LEAF, "crown", None, 14)
for x in range(-235, 150, 11):
    if -175 < x < -115: continue
    tree(x + 4, 8.0 + random.uniform(-0.5, 0.5), random.uniform(0.9, 1.2))
for x in (-52, 12, 47, 95):
    box((x, -2.0, 0.75), (4.3, 1.8, 1.1), M_CAR, "car"); box((x - 0.3, -2.0, 1.55), (2.4, 1.6, 0.7), M_WIN, "carcab")

# ---------- lake (x > 160): basin floor at -14, water surface at -0.3 ----------
LX = 210.0
box((LX, 0, -14.5), (100, 400, 1.0), M_SAND, "lakebed")
box((LX, 0, -7.15), (100, 400, 13.7), M_WATER, "water").visible_shadow = False
for y in range(-60, 120, 14):
    tree(LX + 55, y, 1.2)
whale = empty("whale")
bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=14, radius=1, location=(0, 0, 0))
o = bpy.context.object; o.scale = (13, 3.0, 2.4); bpy.ops.object.shade_smooth(); link(o, M_WHALE, whale)
cyl_between((-10, 0, 0.3), (-16, 0, 4.0), 1.0, M_WHALE, whale, "tailstock", caps=True)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1, location=(-16.5, 0, 4.6))
o = bpy.context.object; o.scale = (1.6, 4.2, 0.35); bpy.ops.object.shade_smooth(); link(o, M_WHALE, whale)
whale.rotation_mode = "XYZ"; whale.scale = (0.7, 0.7, 0.7)

# ---------- plaza: one 1 m block vs 1,000 blocks; bone cross-section slab ----------
PX = -145.0
box((PX + 5, 0, 0.02), (60, 40, 0.04), M_PLAZA, "plaza")
CUBE0 = V((PX - 4.8, -4.8, 0.04))
LAYERS = [grid_mesh(f"layer{k}", 10, 10, 1, 0.94, 0.06, M_BLOCK, CUBE0 + V((0, 0, k * 1.0))) for k in range(10)]
ONE = grid_mesh("one", 1, 1, 1, 0.94, 0.06, M_BLOCK, V((PX - 8.5, -6.0, 0.04)))
SLAB = grid_mesh("slab", 10, 10, 1, 0.94, 0.06, M_TILE, V((PX - 4.8, -17.5, 0.04)))
T1 = text("x1", (PX - 8.0, -6.6, 2.0), 1.1, M_LBL)
T1000 = text("WEIGHT x1,000", (PX, -5.2, 12.0), 1.45, M_LBL)
T100 = text("BONE x100", (PX + 0.2, -12.5, 1.2), 2.0, M_LBL, rot=(math.radians(25), 0, 0))

# ---------- people ----------
def person(shirt):
    body = empty("body")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.30))
    o = bpy.context.object; o.scale = (0.20, 0.12, 0.32); bpy.ops.object.shade_smooth(); link(o, shirt, body)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.02))
    o = bpy.context.object; o.scale = (0.18, 0.13, 0.13); bpy.ops.object.shade_smooth(); link(o, M_PANTS, body)
    cyl_between((0, 0, 0.58), (0, 0, 0.66), 0.045, M_SKIN, body, "neck")
    sphere((0, 0, 0.76), 0.105, M_SKIN, "head", body, 22)
    arms, legs, knees, shins = [], [], [], []
    for side in (-1, 1):
        sh = empty(f"shoulder{side}", (side * 0.21, 0, 0.5), body)
        cyl_between((0, 0, 0), (side * 0.03, 0, -0.30), 0.045, M_SKIN, sh, "upperarm")
        cyl_between((side * 0.03, 0, -0.30), (side * 0.04, 0, -0.58), 0.04, M_SKIN, sh, "forearm")
        sh.rotation_mode = "XYZ"; arms.append(sh)
    for side in (-1, 1):
        hp = empty(f"hip{side}", (side * 0.09, 0, 0), body)
        cyl_between((0, 0, 0), (side * 0.01, 0, -0.45), 0.068, M_PANTS, hp, "thigh")
        kn = empty(f"knee{side}", (side * 0.01, 0, -0.45), hp)
        cyl_between((0, 0, 0), (0, 0, -0.41), 0.05, M_SKIN, kn, "shin")
        shn = cyl_between((0, 0, -0.06), (0, 0, -0.36), 0.054, M_HOT, kn, "hotshin", caps=False)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(0, -0.05, -0.43))
        ft = bpy.context.object; ft.scale = (0.05, 0.12, 0.04); link(ft, M_SHOE, kn)
        hp.rotation_mode = "XYZ"; kn.rotation_mode = "XYZ"; legs.append(hp); knees.append(kn); shins.append(shn)
    body.rotation_mode = "XYZ"
    return body, arms, legs, knees, shins
STAND = 0.915
G, G_ARMS, G_LEGS, G_KNEES, G_SHINS = person(M_SHIRT)
P, P_ARMS, P_LEGS, P_KNEES, P_SHINS = person(M_SHIRT2)
for s in P_SHINS: s.hide_render = True          # the normal person has no stress glow
GX = -60.0
HB = [box((GX + 6.5, -1.0, 8.75), (0.25, 0.25, 17.5), M_LBLW, "hbar"),
      box((GX + 6.5, -1.0, 17.5), (1.6, 0.25, 0.25), M_LBLW, "htop")]
HT = text("17.5 m", (GX + 10.2, -1.0, 17.4), 1.5, M_LBLW)
H1 = text("1.75 m", (GX - 4.2, -1.6, 2.5), 0.9, M_LBLW)

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_BREAK = next(w["t"] for w in L[5]["words"] if w["w"].startswith("break")) + 0.05
RUN_V = 7.0
def mode_of(t):
    if t < t2: return "hook"
    if t < t3: return "grow"
    if t < t4: return "weight"
    if t < t5: return "bone"
    if t < t6 + 0.4: return "run"
    if t < tc + 0.25: return "lake"
    return "hook"

def pose(f, body, arms, legs, knees, loc, scl, yaw, ph, amp, hip=None, knee=None, pitch=0.0):
    body.location = loc; body.scale = (scl,) * 3; body.rotation_euler = (pitch, 0, yaw)
    s = math.sin(ph)
    for k, sh in enumerate(arms):
        side = -1 if k == 0 else 1
        sh.rotation_euler = (amp * 0.9 * s * (1 if k == 0 else -1), -side * math.radians(8), 0)
        sh.keyframe_insert("rotation_euler", frame=f)
    for k, hp in enumerate(legs):
        sgn = -1 if k == 0 else 1
        hp.rotation_euler = (hip if hip is not None else amp * s * sgn, 0, 0)
        kb = knee if knee is not None else max(0.0, amp * 1.3 * math.sin(ph + (0 if k == 0 else math.pi) + 1.2))
        knees[k].rotation_euler = (kb, 0, 0)
        hp.keyframe_insert("rotation_euler", frame=f); knees[k].keyframe_insert("rotation_euler", frame=f)
    body.keyframe_insert("location", frame=f); body.keyframe_insert("rotation_euler", frame=f); body.keyframe_insert("scale", frame=f)

GPOS = {}
for f in range(0, N + 1):
    t = f / FPS; m = mode_of(t)
    glow = 0.0
    if m == "hook":
        tau = t if t < t2 else t - tc
        x = -10 + RUN_V * tau; z = STAND * 10 + 0.5 * abs(math.sin(tau * 5.2))
        pose(f, G, G_ARMS, G_LEGS, G_KNEES, V((x, 0, z)), 10, math.radians(90), tau * 5.2, 0.6)
        glow = 2.0 + 0.8 * math.sin(t * 14)
        pose(f, P, P_ARMS, P_LEGS, P_KNEES, V((x + 9.0, -3.2, STAND)), 1, math.radians(-30), 0, 0.0)
    elif m == "grow":
        u = smooth((t - t2 - 0.1) / 1.0); scl = 1 + 9 * u
        pose(f, G, G_ARMS, G_LEGS, G_KNEES, V((GX, 0, STAND * scl)), scl, 0, 0, 0.0)
        pose(f, P, P_ARMS, P_LEGS, P_KNEES, V((GX - 2.2, -1.5, STAND)), 1, 0, 0, 0.0)
    elif m in ("weight", "bone"):
        pose(f, G, G_ARMS, G_LEGS, G_KNEES, V((GX, 0, STAND * 10)), 10, 0, 0, 0.0)
        pose(f, P, P_ARMS, P_LEGS, P_KNEES, V((PX - 10.5, -6.5, STAND)), 1, 0, 0, 0.0)
    elif m == "run":
        tau = t - t5; x = 10 + RUN_V * tau
        if t < T_BREAK:
            z = STAND * 10 + 0.5 * abs(math.sin(tau * 5.2))
            pose(f, G, G_ARMS, G_LEGS, G_KNEES, V((x, 0, z)), 10, math.radians(90), tau * 5.2, 0.6)
            glow = 0.3 + 2.7 * smooth(tau / (T_BREAK - t5))
        else:
            k = smooth((t - T_BREAK) / 0.45); xb = 10 + RUN_V * (T_BREAK - t5) + 3.0 * k
            pose(f, G, G_ARMS, G_LEGS, G_KNEES, V((xb, 0, STAND * 10 - 3.5 * k)), 10, math.radians(90), 0, 0.0,
                 hip=-0.9 * k, knee=1.9 * k, pitch=0.35 * k)
            glow = 5.0 * (1 - 0.4 * smooth((t - T_BREAK - 0.3) / 0.6))
        pose(f, P, P_ARMS, P_LEGS, P_KNEES, V((70, -3.5, STAND)), 1, math.radians(-20), 0, 0.0)
    else:  # lake: standing chest-deep
        pose(f, G, G_ARMS, G_LEGS, G_KNEES, V((LX - 2, 10, STAND * 10 - 10.6)), 10, math.radians(-10), t * 1.2, 0.05)
        pose(f, P, P_ARMS, P_LEGS, P_KNEES, V((LX - 52, -6, STAND)), 1, math.radians(20), 0, 0.0)
    HOT.default_value = max(glow, 0.0); HOT.keyframe_insert("default_value", frame=f)
    GPOS[f] = G.location.copy()
    for k, lay in enumerate(LAYERS):
        vis(lay, m == "bone" or (m == "weight" and t >= t3 + 0.08 + k * 0.1), f)
    vis(ONE, m in ("weight", "bone"), f); vis(T1, m in ("weight", "bone"), f)
    vis(T1000, (m == "weight" and t > t3 + 1.05) or m == "bone", f)
    vis(SLAB, m == "bone" and t > t4 + 0.1, f, (1, 1, 0.3)); vis(T100, m == "bone" and t > t4 + 0.25, f)
    for o in HB: vis(o, m == "grow" and t > t2 + 1.1, f)
    vis(HT, m == "grow" and t > t2 + 1.1, f); vis(H1, m == "grow", f)
    wu = (t - t6) / (DUR - t6)
    whale.location = V((LX + 1 - 3 * wu, 40, -0.4 + 0.3 * math.sin(t * 2.0))); whale.rotation_euler = (0, 0.04 * math.sin(t * 2), 0)
    whale.keyframe_insert("location", frame=f); whale.keyframe_insert("rotation_euler", frame=f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.05
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
HOOK = ("follow", (6.0, -42.0, 2.0), (2.0, 0, 9.6))
SEG = [
    (0.0, t2 - 0.05, HOOK, 24, 25),
    (t2 - 0.05, t3 - 0.05, fixed((GX + 2.0, -40.0, 4.0), (GX + 2.0, 0, 8.0), (GX + 2.0, -42.0, 4.5), (GX + 2.0, 0, 8.3)), 24, 24),
    (t3 - 0.05, t4 - 0.05, fixed((PX - 4.0, -42.0, 7.0), (PX - 1.5, 0, 6.6), (PX - 3.0, -44.0, 7.5), (PX - 1.0, 0, 6.6)), 24, 24),
    (t4 - 0.05, t5 - 0.05, fixed((PX - 1.0, -58.0, 23.0), (PX, -6.0, 2.4), (PX, -60.0, 24.0), (PX, -6.0, 2.2)), 24, 24),
    (t5 - 0.05, t6 + 0.4, ("follow", (-6.0, -44.0, 2.5), (1.0, 0, 9.4)), 24, 24),
    (t6 + 0.4, tc + 0.25, fixed((LX - 24, -38.0, 4.0), (LX - 10, 4, 2.0), (LX - 20, -34.0, 3.5), (LX - 9, 4, 2.0)), 24, 25),
    (tc + 0.25, DUR + 0.01, HOOK, 25, 25),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0])); spec = seg[2]
    if spec[0] == "follow":
        bp = GPOS[f]; p = V((bp.x, 0, 0)) + V(spec[1]); q = V((bp.x, 0, 0)) + V(spec[2])
    else:
        _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_break": T_BREAK, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "run_v": RUN_V},
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
