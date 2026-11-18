"""The Impossible Lab #13 - your weight on Jupiter (and Mars, the Moon, Saturn).
Units: metres. Mannequin 1.75 m (pelvis origin, standing pelvis height 0.915).
Each station = a physician-style column scale (platform + column + display head facing the camera) with a planet
sphere behind it. Hook set (origin): EARTH scale (x = -1.3, reads 70 kg) vs JUPITER scale (x = +1.3, readout racing
100 -> 165 kg in the first 0.6 s, figure sagging, platform squashing). Line 3 MARS (x = 12, 70 -> 26), line 4 MOON
(x = 22, 70 -> 12, figure bouncing), line 5 Jupiter clouds (x = 34): scale + figure sinking through cloud bands,
"NO SOLID SURFACE"; lines 6-7 SATURN (x = 46) with a ring, 70 -> 64 kg. Last ~1 s: back to the hook framing.
Readouts are text objects updated by a frame_change_pre handler.
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

M_FLOOR = mat("floor", (0.10, 0.11, 0.13), 0.5)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_SHIRT = mat("shirt", (0.95, 0.18, 0.08), 0.6)
M_PANTS = mat("pants", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_PLAT = mat("plat", (0.92, 0.92, 0.94), 0.3, 0.2)
M_STEEL = mat("steel", (0.75, 0.77, 0.80), 0.25, 0.9)
M_HEAD = mat("head", (0.04, 0.04, 0.05), 0.4)
M_DIG = mat("dig", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.62, 0.12), 4.0)
M_DIGR = mat("digr", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.16, 0.06), 3.0)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 5.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.7, 1.0), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_EARTH = noise_mat("earth", (0.05, 0.25, 0.60), (0.20, 0.50, 0.25), 2.2, 0.6)
M_JUP = wave_mat("jup", [(0.85, 0.72, 0.55), (0.62, 0.36, 0.20), (0.95, 0.88, 0.75), (0.70, 0.45, 0.28), (0.90, 0.80, 0.65)], 2.5)
M_MARS = noise_mat("mars", (0.55, 0.20, 0.08), (0.80, 0.42, 0.20), 3.0)
M_MOON = noise_mat("moon", (0.35, 0.35, 0.37), (0.75, 0.75, 0.76), 4.0)
M_SAT = wave_mat("sat", [(0.90, 0.80, 0.55), (0.78, 0.64, 0.40), (0.95, 0.88, 0.68)], 2.0, distort=1.5)
M_RING = mat("ring", (0.85, 0.75, 0.52), 0.6)
M_CLOUD1 = wave_mat("cl1", [(0.92, 0.80, 0.62), (0.75, 0.48, 0.28), (0.96, 0.90, 0.80)], 1.2, 0.9, 6.0, estr=0.25)
M_CLOUD2 = wave_mat("cl2", [(0.70, 0.42, 0.24), (0.88, 0.70, 0.50), (0.55, 0.30, 0.18)], 1.5, 0.9, 6.0, estr=0.25)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tcw = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tcw.outputs["Generated"], sep.inputs[0])
rpw = nt.nodes.new("ShaderNodeValToRGB"); e = rpw.color_ramp.elements
e[0].position = 0.45; e[0].color = (0.03, 0.03, 0.07, 1); e[1].position = 0.85; e[1].color = (0.01, 0.01, 0.03, 1)
nt.links.new(sep.outputs["Z"], rpw.inputs[0]); nt.links.new(rpw.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0
# stars
rnd = random.Random(4); M_STAR = mat("star", (1, 1, 1), 0.5, 0, (1, 1, 1), 6.0)
for i in range(260):
    sphere((rnd.uniform(-20, 70), rnd.uniform(25, 40), rnd.uniform(-6, 22)), rnd.uniform(0.03, 0.07), M_STAR, "star", None, 6)
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.2; sun.data.angle = math.radians(6); sun.data.color = (1.0, 0.96, 0.90)
sun.rotation_euler = (math.radians(45), 0, math.radians(-25)); S.collection.objects.link(sun)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA"))
fill.data.energy = 900; fill.data.size = 14; fill.location = (0, -10, 6); fill.rotation_euler = (math.radians(60), 0, 0)
S.collection.objects.link(fill)
for x0 in (12, 22, 80, 46):
    fl = bpy.data.objects.new("fl", bpy.data.lights.new("fl", "AREA"))
    fl.data.energy = 700; fl.data.size = 10; fl.location = (x0, -10, 6); fl.rotation_euler = (math.radians(60), 0, 0)
    S.collection.objects.link(fl)

bpy.ops.mesh.primitive_plane_add(size=60, location=(4, 0, 0)); link(bpy.context.object, M_FLOOR)

# ---------- column scale ----------
PLAT_H = 0.09
def scale_unit(name, x, z=0.0, red=False, label="", lmat=None):
    root = empty(name, (x, 0, z))
    plat = box((0, 0, PLAT_H / 2), (0.62, 0.62, PLAT_H), M_PLAT, "plat", root)
    box((0, 0.36, 1.10), (0.07, 0.07, 2.0), M_STEEL, "col", root)
    box((0, 0.36, 0.06), (0.30, 0.20, 0.06), M_STEEL, "foot", root)
    box((0, 0.24, 2.35), (0.96, 0.10, 0.54), M_HEAD, "head", root)
    dig = text("70 kg", (0, 0.17, 2.27), TR, 0.27, M_DIGR if red else M_DIG, parent=root); noshadow(dig)
    nm = text(label, (0, 0.17, 2.52), TR, 0.12 if len(label) < 12 else 0.085, lmat or M_WHITE, parent=root); noshadow(nm)
    return {"root": root, "plat": plat, "dig": dig, "name": nm}
def planet(loc, r, m, name):
    return sphere(loc, r, m, name, None, 48)
def sign(body, loc, size, m):
    o = text(body, loc, TR, size, m); noshadow(o); return o

LX, RX = -0.85, 0.85
SC_E = scale_unit("scE", LX, label="EARTH", lmat=M_LBLB); SC_J = scale_unit("scJ", RX, red=True, label="JUPITER", lmat=M_LBL)
planet((LX - 1.2, 9, 3.4), 2.0, M_EARTH, "pEarth"); planet((RX + 1.8, 11, 3.6), 3.4, M_JUP, "pJup")
MX, MOX, CX, SX = 12.0, 22.0, 80.0, 46.0
SC_M = scale_unit("scM", MX, label="MARS", lmat=M_LBL); planet((MX + 1.2, 9, 3.4), 2.4, M_MARS, "pMars")
SC_MO = scale_unit("scMo", MOX, label="MOON"); planet((MOX + 1.2, 9, 3.4), 2.4, M_MOON, "pMoon")
SC_S = scale_unit("scS", SX, label="SATURN · 95× EARTH'S MASS", lmat=M_LBL); planet((SX + 1.0, 11, 3.6), 2.6, M_SAT, "pSat")
bpy.ops.mesh.primitive_torus_add(major_radius=4.6, minor_radius=0.5, location=(SX + 1.0, 11, 3.6))
rg = bpy.context.object; rg.scale = (1, 1, 0.06); rg.rotation_euler = (math.radians(70), math.radians(-12), 0); link(rg, M_RING)
# moon floor: grey regolith pad
box((MOX, 0, -0.04), (8, 8, 0.1), M_MOON, "regolith"); box((MX, 0, -0.04), (8, 8, 0.1), M_MARS, "dust")
# Jupiter clouds set: banded cloud slabs the scale sinks through
SC_C = scale_unit("scC", CX, red=True, label="JUPITER", lmat=M_LBL)
bpy.ops.mesh.primitive_plane_add(size=1, location=(CX, 3.0, -8)); wall = bpy.context.object
wall.scale = (16, 40, 1); wall.rotation_euler = (math.radians(90), 0, 0); bpy.ops.object.transform_apply(scale=True, rotation=True)
link(wall, M_CLOUD1)
rnd = random.Random(9); PUFFS = []
for i in range(14):
    side = -1 if i % 2 else 1
    p = sphere((CX + side * rnd.uniform(1.0, 1.9), rnd.uniform(-1.4, 1.5), 1.5 - i * 1.0 + rnd.uniform(-0.3, 0.3)), rnd.uniform(0.35, 0.6),
               M_CLOUD2 if i % 3 else M_CLOUD1, "puff", None, 14); p.scale = (1.6, 1.0, 0.7); noshadow(p)
FIG_E = person("figE", M_SHIRT); FIG_J = person("figJ", M_SHIRT); FIG_M = person("figM", M_SHIRT)
FIG_MO = person("figMo", M_SHIRT); FIG_C = person("figC", M_SHIRT); FIG_S = person("figS", M_SHIRT)

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
def mode_of(t):
    if t < t2: return "hook"
    if t < t3: return "close"
    if t < t4: return "mars"
    if t < t5: return "moon"
    if t < t6: return "clouds"
    if t < T_LOOP: return "saturn"
    return "hook"
def ramp(t, a, b, v0, v1):
    return v0 + (v1 - v0) * (1 - (1 - max(0.0, min(1.0, (t - a) / (b - a)))) ** 3)
def jup_val(t):
    if t >= T_LOOP: return 165
    return round(ramp(t, 0.0, 0.65, 100, 165))
def readouts(scene, *a):
    t = scene.frame_current / FPS
    SC_J["dig"].data.body = f"{jup_val(t)} kg"
    SC_M["dig"].data.body = f"{round(ramp(t, t3 + 0.15, t3 + 0.9, 70, 26))} kg"
    SC_MO["dig"].data.body = f"{round(ramp(t, t4 + 0.05, t4 + 0.6, 70, 12))} kg"
    SC_C["dig"].data.body = "165 kg"
    SC_S["dig"].data.body = f"{round(ramp(t, t7 + 0.3, t7 + 1.1, 70, 64))} kg"
bpy.app.handlers.frame_change_pre.append(readouts)

PZ = PLAT_H + STAND
for f in range(0, N + 1):
    t = f / FPS; m = mode_of(t)
    pose(FIG_E, f, V((LX, 0, PZ)), arm=math.radians(12 + 3 * math.sin(t * 2)), chest=1.0 + 0.03 * math.sin(t * 2.2))
    # Jupiter: the load hits at once -> sag (pelvis drops, torso folds), platform squashes
    k = smooth(t / 0.5) if t < t2 + 2 else 1.0
    if m == "hook" and t >= T_LOOP: k = 1.0
    pose(FIG_J, f, V((RX, -0.10 * k, PZ - 0.26 * k)), rot=(0.62 * k, 0, 0), arm=math.radians(6 - 4 * k), arm_fwd=-0.35 * k, leg=(-0.55 * k, -0.55 * k),
         chest=1.0 + 0.06 * math.sin(t * 6) * k)
    SC_J["plat"].scale = (1, 1, 1 - 0.55 * k); SC_J["plat"].keyframe_insert("scale", frame=f)
    pose(FIG_M, f, V((MX, 0, PZ + 0.02 * math.sin(t * 3))), arm=math.radians(14 + 18 * smooth((t - t3 - 0.6) / 0.6)))
    # Moon: little hops once the readout drops
    hop = abs(math.sin((t - t4 - 0.6) * 4.2)) * 0.35 if t > t4 + 0.6 and m == "moon" else 0.0
    pose(FIG_MO, f, V((MOX, 0, PZ + hop)), arm=math.radians(25 + 40 * (hop / 0.35)))
    # Jupiter clouds: scale + figure sink, clouds rush up
    if m == "clouds":
        u = (t - t5) / (t6 - t5); dz = -0.2 - 4.5 * u ** 1.4
    else: dz = 0.0
    SC_C["root"].location = (CX, 0, dz); SC_C["root"].keyframe_insert("location", frame=f)
    pose(FIG_C, f, V((CX, 0, PZ + dz + 0.05 * math.sin(t * 9))), arm=math.radians(70 + 25 * math.sin(t * 8)), leg=(0.25 * math.sin(t * 7), -0.25 * math.sin(t * 7)))
    # Saturn: shrug after the readout drops below 70
    sh = smooth((t - t7 - 1.0) / 0.4)
    pose(FIG_S, f, V((SX, 0, PZ)), arm=math.radians(12 + 55 * sh), arm_fwd=-0.5 * sh)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.05, -6.7, 1.95), (0.0, 0, 1.6), (0.0, -6.4, 1.95), (0.0, 0, 1.6))
def station(x, d0=-5.4, d1=-5.0):
    return fixed((x + 0.1, d0, 1.95), (x, 0, 1.65), (x + 0.05, d1, 1.95), (x, 0, 1.65))
SEG = [
    (0.0, t2 - 0.05, HOOK, 30, 31),
    (t2 - 0.05, t3 - 0.05, fixed((RX - 0.25, -4.5, 2.1), (RX - 0.1, 0, 1.85), (RX - 0.2, -4.1, 2.1), (RX - 0.1, 0, 1.85)), 30, 31),
    (t3 - 0.05, t4 - 0.05, station(MX), 30, 31),
    (t4 - 0.05, t5 - 0.05, station(MOX), 30, 31),
    (t5 - 0.05, t6 - 0.05, "follow", 30, 30),
    (t6 - 0.05, T_LOOP, station(SX, -5.9, -5.1), 30, 31),
    (T_LOOP, DUR + 0.01, HOOK, 30, 29),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    if seg[2] == "follow":
        uu = (t - t5) / (t6 - t5); dz = -0.2 - 4.5 * uu ** 1.4 if t >= t5 else 0.0
        p = V((CX + 0.1, -5.4, 1.95 + dz)); q = V((CX, 0, 1.65 + dz))
    else:
        pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "jup_ramp": [0.0, 0.65],
           "mars_drop": t3 + 0.15, "moon_drop": t4 + 0.05, "sink": [t5, t6], "saturn_drop": t7 + 0.3},
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
