"""The Impossible Lab #09 - a pool of olive oil.
Units: metres. Mannequin 1.75 m (pelvis origin, standing pelvis height 0.915).
Sets: (hook, x = 30) two narrow glass-front tanks: WATER (figure floats, head out) vs OLIVE OIL (figure sinks);
(story, origin) a 5 m cutaway pool of olive oil with a deck on the right: jump in, full breath but still sinking,
lands on the floor with a "≈4 kg" down arrow, kicks upward through thick oil (drag trails), a 1 m block of
pure fat drops in and floats with only ~11 mm above the surface (0.9007 / 0.911). Last ~1 s returns to the hook.
Oil and water are tinted Transparent/Glossy mixes with shadow visibility off (no refraction): readable and noise-free.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(9)
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

M_TILE = tiles("tile", (0.80, 0.88, 0.92), (0.35, 0.42, 0.48), 4.0)
M_DECK = noise_mat("deck", (0.55, 0.52, 0.48), (0.70, 0.67, 0.62), 1.5)
M_RIM = mat("rim", (0.92, 0.92, 0.90), 0.4)
M_PLINTH = mat("plinth", (0.10, 0.11, 0.13), 0.5)
M_OIL = liquid("oil", (1.0, 0.70, 0.12), (0.95, 0.70, 0.18), 0.18)
M_WATER = liquid("water", (0.55, 0.85, 1.0), (0.7, 0.9, 1.0), 0.10)
M_OILDROP = mat("oildrop", (0.95, 0.68, 0.10), 0.1, 0, (0.9, 0.6, 0.1), 0.6)
M_FAT = mat("fat", (0.96, 0.92, 0.74), 0.55)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_SHIRT = mat("shirt", (0.95, 0.18, 0.08), 0.6)
M_PANTS = mat("pants", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 5.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.7, 1.0), 5.0)
M_RED = mat("red", (1.0, 0.25, 0.15), 0.4, 0, (1.0, 0.25, 0.12), 6.0)
M_TRAIL = mat("trail", (1.0, 0.85, 0.45), 0.2, 0, (1.0, 0.8, 0.35), 1.5)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tcw = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tcw.outputs["Generated"], sep.inputs[0])
rpw = nt.nodes.new("ShaderNodeValToRGB"); e = rpw.color_ramp.elements
e[0].position = 0.45; e[0].color = (0.62, 0.70, 0.80, 1); e[1].position = 0.85; e[1].color = (0.25, 0.45, 0.75, 1)
nt.links.new(sep.outputs["Z"], rpw.inputs[0]); nt.links.new(rpw.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.1
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.4; sun.data.angle = math.radians(6); sun.data.color = (1.0, 0.96, 0.90)
sun.rotation_euler = (math.radians(35), 0, math.radians(-25)); S.collection.objects.link(sun)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA"))
fill.data.energy = 900; fill.data.size = 8; fill.location = (2, -9, 5); fill.rotation_euler = (math.radians(65), 0, 0)
S.collection.objects.link(fill)
fill2 = bpy.data.objects.new("fill2", bpy.data.lights.new("fill2", "AREA"))
fill2.data.energy = 600; fill2.data.size = 5; fill2.location = (30, -7, 4); fill2.rotation_euler = (math.radians(65), 0, 0)
S.collection.objects.link(fill2)

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

def tank(cx, w, d, h, level, liq_m, name):
    """Cutaway tank: tiled floor/back/sides, open front, liquid block. Interior x in cx±w/2, y in ±d/2, z 0..h."""
    T = 0.15
    box((cx, 0, -T / 2), (w + 2 * T, d + 2 * T, T), M_TILE, name + "floor")
    box((cx, d / 2 + T / 2, h / 2), (w + 2 * T, T, h), M_TILE, name + "back")
    for s in (-1, 1):
        box((cx + s * (w / 2 + T / 2), 0, h / 2), (T, d + 2 * T, h), M_TILE, name + "side")
        box((cx + s * (w / 2 + T / 2), 0, h + 0.04), (T + 0.06, d + 2 * T + 0.06, 0.08), M_RIM, name + "rimS")
    box((cx, d / 2 + T / 2, h + 0.04), (w + 2 * T + 0.06, T + 0.06, 0.08), M_RIM, name + "rimB")
    liq = box((cx, 0, level / 2), (w, d, level), liq_m, name + "liq"); noshadow(liq)
    return liq

# ---------- story pool (origin): interior x -2.5..2.5, y ±1.25, z 0..2.6, oil level 2.3 ----------
PW, PD, PH, LEV = 5.0, 2.5, 2.6, 2.3
tank(0.0, PW, PD, PH, LEV, M_OIL, "pool")
box((4.4, 0, PH / 2), (3.5, PD + 0.3, PH), M_DECK, "deck")                    # deck on the right
box((-4.4, 0, PH / 2), (3.5, PD + 0.3, PH), M_DECK, "deckL")
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.16)); link(bpy.context.object, M_DECK)
box((0, PD / 2 + 3.0, PH + 1.0), (14, 0.3, 2.0), M_RIM, "fence")
# fat block (1 m cube, density 0.9007 vs oil 0.911 -> 1.1 % above the surface)
FAT_ABOVE = 1.0 * (1 - 0.9007 / 0.911)                                         # 0.0113 m
FATX = -1.2
fat = box((0, 0, 0), (1.0, 1.0, 1.0), M_FAT, "fat")
fat_lbl = text("BODY FAT 0.90", (0, -0.505, 0.25), TR, 0.13, M_LBL, parent=fat)
oil_lbl = text("OLIVE OIL 0.91", (FATX, PD / 2 - 0.02, LEV - 0.5), TR, 0.16, M_LBL)
mm_lbl = text("ONLY 11 mm ABOVE", (FATX, -0.3, LEV + 0.22), TR, 0.12, M_LBL)
mm_lbl.visible_glossy = False
mm_bar = box((FATX, -0.505, LEV + FAT_ABOVE / 2), (1.0, 0.012, FAT_ABOVE), M_LBL, "mmbar")
# down arrow "≈4 kg"
arrow = empty("arrow")
cyl_between((0, 0, 0.55), (0, 0, 0.12), 0.035, M_RED, arrow, "ashaft", caps=False)
bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.10, depth=0.20, location=(0, 0, 0.06), rotation=(math.pi, 0, 0))
link(bpy.context.object, M_RED, arrow)
text("≈4 kg", (0.0, 0, 0.75), TR, 0.2, M_RED, parent=arrow)
DROPS = [sphere((0, 0, -20), random.uniform(0.04, 0.09), M_OILDROP, "drop", None, 10) for _ in range(18)]
DROP_V = [V((random.uniform(-1.6, 1.6), random.uniform(-0.6, 0.3), random.uniform(2.5, 4.2))) for _ in DROPS]
TRAIL = [sphere((0, 0, -20), 0.05, M_TRAIL, "trail", None, 10) for _ in range(14)]

# ---------- hook set (x = 30): two narrow tanks ----------
HX = 30.0; HW, HD, HHt, HLEV = 1.5, 1.4, 2.8, 2.5
tank(HX - 0.9, HW, HD, HHt, HLEV, M_WATER, "tw")
tank(HX + 0.9, HW, HD, HHt, HLEV, M_OIL, "to")
box((HX, -0.05, -0.45), (3.9, HD + 0.6, 0.6), M_PLINTH, "plinth")
LW1 = text("WATER", (HX - 0.9, -HD / 2 - 0.02, 0.42), TR, 0.24, M_LBLB)
LW2 = text("FLOATS", (HX - 0.9, -HD / 2 - 0.02, 0.16), TR, 0.17, M_LBLB)
LO1 = text("OLIVE OIL", (HX + 0.9, -HD / 2 - 0.02, 0.42), TR, 0.24, M_LBL)
LO2 = text("SINKS", (HX + 0.9, -HD / 2 - 0.02, 0.16), TR, 0.17, M_LBL)
box((HX, -0.05, -0.9), (6, 4, 0.3), M_DECK, "hookfloor")

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

FIG = person("fig", M_SHIRT)
FW = person("figw", M_SHIRT)
FO = person("figo", M_SHIRT)

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_ENTRY = t2 + 0.75                       # hits the oil
T_FLOOR = t4 + 0.55                       # lands on the pool floor
T_KICK0, T_KICK1 = t5 + 0.15, t6 - 0.05   # swimming up
T_FATIN = t6 + 0.05                       # fat block hits the oil
FIGX = 1.0

def mode_of(t):
    if t < t2: return "hook"
    if t < t3: return "jump"
    if t < t4: return "breath"
    if t < t5: return "floor"
    if t < t6: return "kick"
    if t < t7: return "fatin"
    if t < tc + 0.9: return "fatclose"
    return "hook"

def oil_fig(t):
    """Hook tank figure in oil: sinking. Loops: same height at t = 0 and t = DUR."""
    u = t if t < t2 else t - DUR
    return max(STAND, 1.55 - 0.64 * smooth((u + 1.2) / 2.6))

POS = {}
for f in range(0, N + 1):
    t = f / FPS; m = mode_of(t)
    # hook-set figures always animated (cheap)
    bob = 0.03 * math.sin(t * 2.6)
    pose(FW, f, V((HX - 0.9, 0.05, HLEV - 0.62 + bob)), arm=math.radians(55 + 10 * math.sin(t * 3)), leg=(0.15 * math.sin(t * 3), -0.15 * math.sin(t * 3)), chest=1.1)
    zo = oil_fig(t)
    pose(FO, f, V((HX + 0.9, 0.05, zo)), arm=math.radians(150 + 12 * math.sin(t * 5)), leg=(0.2 * math.sin(t * 6), -0.2 * math.sin(t * 6)), chest=1.1)
    # story figure
    rot = (0, 0, 0); arm = 0.2; leg = (0, 0); chest = 1.0; fwd = 0.0
    if m == "jump":
        if t < t2 + 0.25:
            p = V((3.3, 0.0, PH + STAND - 0.15 * smooth((t - t2) / 0.25))); arm = math.radians(40); leg = (0.3, 0.3)
        else:
            u = min((t - t2 - 0.25) / (T_ENTRY - t2 - 0.25), 1.0)
            if t < T_ENTRY:
                x = 3.3 + (FIGX - 3.3) * u; z = PH + STAND + 0.35 * math.sin(math.pi * u) - (PH + STAND - LEV - 0.2) * u
                p = V((x, 0.0, z)); arm = math.radians(160); leg = (-0.2, -0.2); rot = (0, -0.25 * u, 0)
            else:
                k = smooth((t - T_ENTRY) / (t3 - T_ENTRY))
                p = V((FIGX, 0.0, LEV + 0.2 - 0.75 * k)); arm = math.radians(160 - 40 * k); leg = (0.25 * math.sin(t * 8), -0.25 * math.sin(t * 8))
    elif m == "breath":
        k = (t - t3) / (t4 - t3)
        p = V((FIGX, 0.0, LEV - 0.55 - 0.45 * k)); chest = 1.0 + 0.10 * smooth((t - t3 - 0.3) / 0.6)
        arm = math.radians(110 + 20 * math.sin(t * 4)); leg = (0.15 * math.sin(t * 5), -0.15 * math.sin(t * 5))
    elif m == "floor":
        z0 = LEV - 1.0
        if t < T_FLOOR:
            k = (t - t4) / (T_FLOOR - t4); p = V((FIGX, 0.0, z0 + (STAND - z0) * smooth(k))); chest = 1.10; arm = math.radians(120)
        else:
            k = min((t - T_FLOOR) / 0.5, 1.0)
            p = V((FIGX, 0.0, STAND - 0.12 * math.sin(math.pi * k))); chest = 1.10; arm = math.radians(120 - 70 * smooth(k))
            leg = (0.35 * math.sin(math.pi * k), 0.35 * math.sin(math.pi * k))
    elif m == "kick":
        k = smooth((t - T_KICK0) / (T_KICK1 - T_KICK0)) if t > T_KICK0 else 0.0
        p = V((FIGX - 0.5 * k, 0.0, STAND + 0.65 * k)); rot = (0, math.radians(35) * smooth((t - t5) / 0.4), 0)
        arm = math.radians(150 + 25 * math.sin(t * 3.0)); kick = 0.45 * math.sin(t * 9)
        leg = (kick, -kick); chest = 1.10
    elif m in ("fatin", "fatclose"):
        k = smooth((t - t6) / 1.2)
        p = V((FIGX - 0.5, 0.0, STAND + 0.65 - 0.65 * k)); rot = (0, math.radians(35) * (1 - k), 0)
        arm = math.radians(140 - 30 * k); chest = 1.10; fwd = -0.3 * k
    else:
        p = V((FIGX, 0.0, -30))
    pose(FIG, f, p, rot, arm, leg, chest, fwd)
    POS[f] = p.copy()
    # splash drops at entry
    for d, v in zip(DROPS, DROP_V):
        u = t - T_ENTRY; on = m == "jump" and 0 <= u < 0.6
        loc = V((FIGX, -0.2, LEV)) + V((v.x * u, v.y * u, v.z * u - 9.8 * u * u)) if on else V((0, 0, -20))
        if on and loc.z < LEV - 0.05: on = False; loc = V((0, 0, -20))
        d.location = loc; d.keyframe_insert("location", frame=f); vis(d, on, f)
    # drag trails behind the kicking feet
    for i, tr in enumerate(TRAIL):
        on = m == "kick" and t > T_KICK0
        fp = POS.get(max(0, f - (i + 1) * 2), p)
        tr.location = (fp + V((0.35 + 0.05 * math.sin(i * 1.7), -0.1, -0.75 + 0.06 * math.sin(t * 9 + i)))) if on else V((0, 0, -20))
        tr.keyframe_insert("location", frame=f); vis(tr, on, f, (1 - i / 16,) * 3)
    # arrow
    on = m == "floor" and t > t4 + 0.35
    arrow.location = V((FIGX + 0.55, -0.3, STAND - 0.2)); arrow.keyframe_insert("location", frame=f); vis(arrow, on, f)
    # fat block
    if m in ("fatin", "fatclose"):
        u = t - T_FATIN
        top_rest = LEV + FAT_ABOVE
        if u < 0: zc = top_rest - 0.5 + 1.2 + (-u) * 6
        else: zc = top_rest - 0.5 - 0.22 * math.exp(-u * 2.5) * math.cos(u * 7)
        fat.location = V((FATX, 0.0, zc)); vis(fat, True, f)
    else:
        fat.location = V((FATX, 0.0, -20)); vis(fat, False, f)
    fat.keyframe_insert("location", frame=f)
    vis(mm_lbl, m == "fatclose", f); vis(mm_bar, m == "fatclose", f); vis(oil_lbl, m in ("fatin", "fatclose"), f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((HX + 0.4, -9.6, 1.9), (HX + 0.15, 0, 1.15), (HX + 0.3, -9.0, 1.85), (HX + 0.15, 0, 1.15))
SEG = [
    (0.0, t2 - 0.05, HOOK, 28, 29),
    (t2 - 0.05, t3 - 0.05, fixed((2.6, -9.5, 2.9), (2.0, 0, 2.6), (2.3, -9.0, 2.8), (1.8, 0, 2.5)), 26, 26),
    (t3 - 0.05, t4 - 0.05, fixed((FIGX + 0.3, -7.2, 1.9), (FIGX, 0, 1.75), (FIGX + 0.3, -6.8, 1.7), (FIGX, 0, 1.5)), 30, 31),
    (t4 - 0.05, t5 - 0.05, fixed((FIGX + 0.6, -6.8, 1.1), (FIGX + 0.2, 0, 0.8), (FIGX + 0.5, -6.4, 1.0), (FIGX + 0.2, 0, 0.8)), 30, 30),
    (t5 - 0.05, t6 - 0.05, ("follow", (0.2, -6.0, 0.5), (0.0, 0, 0.1)), 30, 30),
    (t6 - 0.05, t7 - 0.05, fixed((-0.2, -8.6, 2.0), (-0.2, 0, 1.6), (-0.3, -8.3, 2.0), (-0.3, 0, 1.6)), 28, 28),
    (t7 - 0.05, tc + 0.9, fixed((FATX + 0.1, -3.8, LEV + 0.9), (FATX + 0.1, 0, LEV - 0.3), (FATX + 0.1, -3.4, LEV + 0.8), (FATX + 0.1, 0, LEV - 0.3)), 30, 31),
    (tc + 0.9, DUR + 0.01, HOOK, 29, 28),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0])); spec = seg[2]
    if spec[0] == "follow":
        bp = POS[f]; p = bp + V(spec[1]); q = bp + V(spec[2])
    else:
        _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_entry": T_ENTRY, "t_floor": T_FLOOR, "t_kick0": T_KICK0, "t_fatin": T_FATIN, "t_card": tc,
           "cuts": [s[0] for s in SEG[1:]], "fat_above_m": FAT_ABOVE},
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
