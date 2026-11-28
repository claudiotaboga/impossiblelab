"""The Impossible Lab #23 - push a 100,000-tonne ship with one finger (CORE, lane D).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(23)
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


import bmesh
FNT = bpy.data.fonts.load("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def label(body, loc, size, m, align="CENTER", rot=TR):
    o = text(body, loc, rot, size, m, align); o.data.font = FNT; noshadow(o); o.visible_glossy = False; return o
def cyl(loc, r, d, m, name="cyl", rot=(0, 0, 0), verts=32, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def open_cyl(loc, r, d, m, name, thick=0.006, verts=40):
    o = cyl(loc, r, d, m, name, verts=verts)
    bpy.ops.object.mode_set(mode="EDIT"); bm = bmesh.from_edit_mesh(o.data)
    bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if fc.normal.z > 0.9], context="FACES"); bmesh.update_edit_mesh(o.data)
    bpy.ops.object.mode_set(mode="OBJECT")
    if thick > 0.0045:
        sol = o.modifiers.new("shell", "SOLIDIFY"); sol.thickness = thick


# ================= episode 23: push a 100,000-tonne ship with one finger (single harbour scene) =================
# Hook (flash-forward): a person on the quay presses one finger on a rib of a 330 m grey ship; a TIME-LAPSE timer
# races 0 -> 60 MIN while the hull's red mark slides 65 cm past the yellow START mark on the quay.
# L2 aerial: the whole ship + tiny person, "100,000 T" on the hull. L3: close-up finger + amber 10 N arrow, "NO GRIP".
# L4: macro on the marks, timer 1 MIN, "≈ 0.2 MM". L5: time-lapse 1 -> 60 MIN, gap opens to 65 cm, the person walks along.
# L6: wide side shot, hands off, ship keeps drifting "STILL MOVING". L7: person turns round and pushes back:
# timer 70 -> 130 MIN, ship slows to a stop, "STOPPED". After the card starts: hook framing (loop).
M_WATER = noise_mat("water", (0.015, 0.07, 0.10), (0.03, 0.11, 0.15), 0.6, 0.06)
M_QUAY = noise_mat("quay", (0.58, 0.56, 0.52), (0.70, 0.68, 0.63), 3.0, 0.85)
M_HULL = noise_mat("hull", (0.07, 0.10, 0.15), (0.10, 0.13, 0.19), 0.08, 0.5)
M_DECK = mat("deck", (0.10, 0.11, 0.12), 0.8)
M_BOOT = mat("boot", (0.45, 0.06, 0.05), 0.6)
M_EDGE = mat("edge", (0.92, 0.92, 0.90), 0.6)
M_SKIN = mat("skin", (0.62, 0.45, 0.32), 0.55)
M_SHIRT = mat("shirt", (0.95, 0.18, 0.08), 0.6)
M_PANTS = mat("pants", (0.06, 0.10, 0.28), 0.6)
M_SHOE = mat("shoe", (0.95, 0.95, 0.95), 0.5)
M_BOLL = mat("boll", (0.08, 0.08, 0.09), 0.5, 0.3)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_AMB = mat("lbla", (1.0, 0.55, 0.08), 0.4, 0, (1.0, 0.5, 0.06), 3.0)
M_RED = mat("redl", (0.9, 0.04, 0.02), 0.4, 0, (1.0, 0.06, 0.03), 3.0)
M_GRN = mat("grnl", (0.05, 0.8, 0.15), 0.4, 0, (0.08, 1.0, 0.25), 2.4)
M_YEL = mat("yel", (1.0, 0.80, 0.05), 0.5, 0, (1.0, 0.75, 0.05), 1.2)
M_RMK = mat("rmk", (0.85, 0.05, 0.03), 0.5, 0, (1.0, 0.05, 0.02), 1.5)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.35
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.55, 0.70, 0.90, 1); WBG.inputs[1].default_value = 0.9
# water bump
bw = bsdf(M_WATER); nt = M_WATER.node_tree
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.5; nz.inputs["Detail"].default_value = 3
bm_ = nt.nodes.new("ShaderNodeBump"); bm_.inputs["Strength"].default_value = 0.12
nt.links.new(nz.outputs["Fac"], bm_.inputs["Height"]); nt.links.new(bm_.outputs["Normal"], bw.inputs["Normal"])

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
HOOK_A = (0.08, 1.45)                 # time-lapse 0 -> 60 MIN in the hook
PUSH5 = (t5 + 0.05, 1.65)             # line 5: 1 -> 60 MIN
STOP7 = (t7 + 0.05, 1.30)             # line 7: 70 -> 130 MIN
GAP_H = 0.65                          # m after one hour (0.5 * 1e-7 * 3600^2 = 0.648)

def clamp01(x): return max(0.0, min(1.0, x))
def state(t):
    """(ship x offset [m], timer minutes or None, pushing side: +1 behind rib / -1 in front / 0 hands off)"""
    if t >= T_LOOP: return 0.0, None, 1
    if t < t2 - 0.05:
        u = clamp01((t - HOOK_A[0]) / HOOK_A[1]); return GAP_H * u * u, 60 * u, 1
    if t < t4 - 0.05: return 0.0, None, 1
    if t < t5 - 0.05:
        u = clamp01((t - t4 - 0.2) / 1.2); return 0.00018 * u * u, 1.0 * u, 1
    if t < t6 - 0.05:
        u = clamp01((t - PUSH5[0]) / PUSH5[1]); m = 1 + 59 * u; return GAP_H * (m / 60) ** 2, m, 1
    if t < t7 - 0.05:
        u = clamp01((t - t6) / (t7 - t6)); m = 60 + 10 * u; return GAP_H + 1.3 * (m - 60) / 60, m, 0
    u = clamp01((t - STOP7[0]) / STOP7[1]); m = 70 + 60 * u
    x70 = GAP_H + 1.3 * 10 / 60
    return x70 + GAP_H * (1 - (1 - u) ** 2), m, -1

# ---------- harbour ----------
QE = 0.25            # quay edge y
QZ = 2.0             # quay top above water
HY = 0.85            # hull side y
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 300, 0)); wtr = bpy.context.object; wtr.scale = (3000, 3000, 1); link(wtr, M_WATER)
box((0, QE - 40, QZ / 2 - 1), (600, 80, QZ + 2), M_QUAY, "quay")
box((0, QE - 0.12, QZ + 0.004), (600, 0.24, 0.01), M_EDGE, "edge")
for bx in range(-60, 61, 12):
    cyl((bx + 4.5, QE - 0.6, QZ + 0.25), 0.18, 0.5, M_BOLL, "bollard", verts=16)
START = box((0.25, QE - 0.45, QZ + 0.006), (0.06, 0.9, 0.012), M_YEL, "startmark"); noshadow(START)
START_T = label("START", (0.25, QE - 1.05, QZ + 0.01), 0.16, M_YEL, rot=(0, 0, 0))

SHIP = empty("ship")
HL = 330.0
def hull():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); o = bpy.context.object; o.name = "bow"
    for v in o.data.vertices:
        fwd = v.co.x > 0
        x = XS + (165.0 if fwd else 125.0) + 20
        y = HY + 20 + v.co.y * (8 if fwd else 40)
        z = 3.5 + v.co.z * 29 if not (fwd and v.co.z < 0) else -6.0
        v.co = (x, y, z)
    link(o, M_HULL, SHIP); return o
XS = 145.0   # stern (transom) at ship-local x = 0, bow at +330
HULL = box((XS, HY + 20, 3.5), (290, 40, 29), M_HULL, "hullmain", SHIP)
BOW = hull()
box((XS, HY + 20, -0.05), (290.4, 40.4, 1.2), M_BOOT, "boot", SHIP)
box((XS, HY + 20, 18.02), (289.8, 39.8, 0.05), M_DECK, "deck", SHIP)
box((XS + 55, HY + 36, 30), (30, 5, 24), M_HULL, "island", SHIP)
box((XS + 55, HY + 36, 43), (6, 3, 2), M_DECK, "mast", SHIP)
RIB_W = 0.15
M_STEEL = mat("steel", (0.62, 0.64, 0.66), 0.35, 0.6)
RIB = box((-RIB_W / 2, (QE + 0.05 + HY) / 2, 3.6), (RIB_W, HY - QE - 0.05, 3.2), M_STEEL, "rib", SHIP)
RMARK = box((0.25, HY - 0.006, 1.75), (0.06, 0.01, 2.5), M_RMK, "redmark", SHIP); noshadow(RMARK)
RMARK2 = box((0.25, (QE + HY) / 2, 0.8), (0.06, HY - QE - 0.02, 0.012), M_RMK, "redwater", SHIP); noshadow(RMARK2)
BIG = label("100,000 T", (XS + 10, HY + 20, 18.2), 26.0, M_WHITE, rot=(0, 0, math.radians(180))); BIG.parent = SHIP
box((XS, HY - 0.01, 17.3), (290, 0.02, 0.5), M_EDGE, "sheer", SHIP)
for k in range(2, 100): box((k * 3.0, HY - 0.01, 10.0), (0.4, 0.02, 0.4), M_EDGE, "port", SHIP)

sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); sun.data.energy = 3.2; sun.data.angle = math.radians(2)
sun.rotation_euler = (math.radians(50), 0, math.radians(-35)); S.collection.objects.link(sun)

# ---------- person (faces +x after a +90° turn; shoulders along y) ----------
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
        cyl_between((0, 0, 0), (0, 0, -0.30), 0.045, M_SKIN, sh, "upperarm")
        cyl_between((0, 0, -0.30), (0, 0, -0.56), 0.04, M_SKIN, sh, "forearm")
        cyl_between((0, 0, -0.56), (0, 0, -0.64), 0.013, M_SKIN, sh, "finger")
        sh.rotation_mode = "XYZ"; arms.append(sh)
    for side in (-1, 1):
        hp = empty(f"{name}hp{side}", (side * 0.09, 0, 0), body)
        cyl_between((0, 0, 0), (side * 0.01, 0, -0.45), 0.068, M_PANTS, hp, "thigh")
        cyl_between((side * 0.01, 0, -0.45), (side * 0.01, 0, -0.86), 0.05, M_SKIN, hp, "shin")
        ft = sphere((side * 0.01, -0.05, -0.88), 1.0, M_SHOE, "foot", hp, 12); ft.scale = (0.05, 0.12, 0.04)
        hp.rotation_mode = "XYZ"; legs.append(hp)
    body.rotation_mode = "XYZ"
    return {"body": body, "arms": arms, "legs": legs}
P = person("you", M_SHIRT)
REACH = 0.64 + 0.01
RIB_HALF = 0.075

# ---------- labels (camera-facing, set up after the camera) ----------
TIMER = label("", (0, 0, 0), 0.26, M_WHITE)
GAP_T = label("", (0, 0, 0), 0.24, M_RED)
NOGRIP = label("NO GRIP", (0, 0, 0), 0.13, M_GRN)
F_T = label("10 N", (0, 0, 0), 0.10, M_AMB)
MM_T = label("1 MIN → 0.2 MM", (0, 0, 0), 0.06, M_RED)
SPD_T = label("STILL MOVING", (0, 0, 0), 5.0, M_AMB)
STOP_T = label("", (0, 0, 0), 0.17, M_GRN)
ARROW = box((0, 0, 0), (0.30, 0.025, 0.025), M_AMB, "arrow"); noshadow(ARROW)
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.05, depth=0.10, location=(0, 0, 0), rotation=(0, math.radians(90), 0))
ARH = link(bpy.context.object, M_AMB); noshadow(ARH)

def fmt_min(m):
    return f"{m:.0f} MIN" if m < 60 or m >= 120 else (f"1 H {m - 60:02.0f} MIN" if m >= 60.5 else "1 HOUR")
def handler(scene, *a):
    t = scene.frame_current / FPS
    x, m, side = state(t)
    TIMER.data.body = ("TIME-LAPSE · " + fmt_min(m)) if m is not None else ""
    GAP_T.data.body = f"+{x * 100:.0f} CM" if x >= 0.005 else ""
    if t >= t7 - 0.05 and t < T_LOOP:
        STOP_T.data.body = "STOPPED · +1 HOUR" if m >= 129.5 else "SLOWING"
bpy.app.handlers.frame_change_pre.append(handler)

for f in range(0, N + 1):
    t = f / FPS
    x, m, side = state(t)
    SHIP.location = (x, 0, 0); SHIP.keyframe_insert("location", frame=f)
    rib_x = x
    b = P["body"]
    walk = 0.0
    if side >= 0:   # behind the rib, facing +x
        px = rib_x - RIB_W - REACH; b.rotation_euler = (0, 0, math.radians(90)); push_arm = 0; py = QE - 0.04 - 0.21 + 0.13
    else:           # in front of the rib, facing -x
        px = rib_x + 0.0 + REACH; b.rotation_euler = (0, 0, math.radians(-90)); push_arm = 0; py = QE - 0.04 - 0.21 + 0.13
    if side == 0: px -= 0.25
    b.location = (px, py, QZ + STAND)
    b.keyframe_insert("location", frame=f); b.keyframe_insert("rotation_euler", frame=f)
    # with +90° the arm at local x=-0.21 sits at y=-0.21 (away from hull); local x=+0.21 -> y=+0.21 (hull side)
    hull_arm = 1 if side >= 0 else 0
    for k, sh in enumerate(P["arms"]):
        if k == hull_arm and side != 0: sh.rotation_euler = (math.radians(-90), 0, 0)
        else: sh.rotation_euler = (0, 0, (-1 if k == 0 else 1) * 0.12)
        sh.keyframe_insert("rotation_euler", frame=f)
    moving = (HOOK_A[0] < t < sum(HOOK_A) and t < t2) or (PUSH5[0] < t < sum(PUSH5) and t5 <= t < t6) or (STOP7[0] < t < sum(STOP7) and t >= t7)
    sw = 0.22 * math.sin(t * 9.0) if moving else 0.0
    for k, hp in enumerate(P["legs"]):
        hp.rotation_euler = ((sw if k == 0 else -sw), 0, 0); hp.keyframe_insert("rotation_euler", frame=f)
    # hand position (world) for the arrow
    hand = V((rib_x - RIB_W - 0.02, py + 0.21, QZ + STAND + 0.5)) if side >= 0 else V((rib_x + 0.02, py + 0.21, QZ + STAND + 0.5))
    lab_x = px
    # labels
    on3 = t3 - 0.05 <= t < t4 - 0.05
    ARROW.location = hand + V((-0.30, -0.12, 0.10)); ARH.location = hand + V((-0.10, -0.12, 0.10))
    for o in (ARROW, ARH): o.keyframe_insert("location", frame=f)
    vis(ARROW, on3, f, base=(0.30, 0.025, 0.025)); vis(ARH, on3, f)
    F_T.location = hand + V((-0.12, -0.14, 0.17)); F_T.keyframe_insert("location", frame=f); vis(F_T, on3, f)
    NOGRIP.location = hand + V((-0.27, -0.05, -0.38)); NOGRIP.keyframe_insert("location", frame=f); vis(NOGRIP, on3, f)
    show_timer = m is not None and not (t6 - 0.05 <= t < t7 - 0.05) and not (t4 - 0.05 <= t < t5 - 0.05)
    TIMER.location = (lab_x - (1.3 if t >= t7 - 0.05 and t < T_LOOP else 0.0), py - 0.30, QZ + 2.25)
    TIMER.keyframe_insert("location", frame=f); vis(TIMER, show_timer, f)
    GAP_T.location = (0.25 + x / 2, QE - 0.35, QZ + 1.05); GAP_T.keyframe_insert("location", frame=f)
    vis(GAP_T, (t < t2 - 0.05 or t5 - 0.05 <= t < t6 - 0.05 or t >= t7 - 0.05) and t < T_LOOP and x >= 0.005, f)
    vis(MM_T, t4 + 0.6 <= t < t5 - 0.05, f); MM_T.location = (0.25, QE - 0.10, QZ + 0.36); MM_T.keyframe_insert("location", frame=f)
    vis(SPD_T, t6 + 0.15 <= t < t7 - 0.05, f); SPD_T.location = (x + XS + 10, HY + 20, 30); SPD_T.keyframe_insert("location", frame=f)
    STOP_T.location = (lab_x - 1.3, py - 0.30, QZ + 1.85); STOP_T.keyframe_insert("location", frame=f)
    vis(STOP_T, t7 + 0.1 <= t < T_LOOP, f)
    vis(BIG, t2 - 0.05 <= t < t3 - 0.05 or t6 - 0.05 <= t < t7 - 0.05, f)
    vis(START_T, False, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HZ = QZ + 1.6
HOOK = fixed((-6.5, -4.2, QZ + 4.2), (0.5, 2.0, QZ + 0.6), (-6.2, -4.0, QZ + 4.0), (0.5, 2.0, QZ + 0.6))
SEG = [
    (0.0, t2 - 0.05, HOOK, 22, 22),
    (t2 - 0.05, t3 - 0.05, fixed((-5, 230, 150), (165, 15, 0), (-35, 270, 180), (165, 15, 0)), 24, 24),
    (t3 - 0.05, t4 - 0.05, fixed((-0.75, 2.3, HZ + 0.25), (-0.15, 0.35, HZ - 0.40), (-0.70, 2.1, HZ + 0.22), (-0.15, 0.35, HZ - 0.40)), 26, 26),
    (t4 - 0.05, t5 - 0.05, fixed((0.25, -1.20, QZ + 0.95), (0.25, 0.50, QZ - 0.10), (0.25, -1.08, QZ + 0.86), (0.25, 0.50, QZ - 0.10)), 30, 30),
    (t5 - 0.05, t6 - 0.05, fixed((-6.2, -4.0, QZ + 4.0), (0.7, 2.0, QZ + 0.6), (-6.7, -4.4, QZ + 4.3), (0.8, 2.0, QZ + 0.6)), 22, 22),
    (t6 - 0.05, t7 - 0.05, fixed((95, 150, 55), (170, 15, 6), (101, 140, 52), (174, 15, 6)), 24, 24),
    (t7 - 0.05, T_LOOP, fixed((-3.3, -3.6, QZ + 3.4), (1.5, 1.0, QZ + 0.7), (-3.5, -3.8, QZ + 3.5), (1.7, 1.0, QZ + 0.7)), 22, 22),
    (T_LOOP, DUR + 0.01, HOOK, 22, 22),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

M_PLATEL = mat("lplate", (0.02, 0.02, 0.03), 0.6)
for o, nch in ((TIMER, 22), (GAP_T, 6), (NOGRIP, 7), (F_T, 4), (MM_T, 14), (SPD_T, 12), (STOP_T, 17), (START_T, 5)):
    o.rotation_euler = (0, 0, 0); cc = o.constraints.new("TRACK_TO"); cc.target = cam
    cc.track_axis = "TRACK_Z"; cc.up_axis = "UP_Y"
    sz = o.data.size; w = nch * sz * 0.72 + sz * 0.5
    bpy.ops.mesh.primitive_plane_add(size=1); pl = bpy.context.object; pl.name = o.name + "_bg"
    pl.data.materials.append(M_PLATEL); noshadow(pl); pl.visible_glossy = False
    for v in pl.data.vertices: v.co.x = v.co.x * w; v.co.y = v.co.y * sz * 1.35; v.co.z = -0.012
    pl.parent = o
json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "hook": HOOK_A, "push5": PUSH5, "stop7": STOP7},
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
