"""The Impossible Lab #20 - a candle in space (E17 cascade middle, reel 3).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(20)
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


# ================= episode 21: does toast land butter-down? (single escalating scene) =================
# Hook: buttered toast slides off a 75 cm kitchen table at 0.08 s, flips half a turn, lands BUTTER-DOWN by ~0.9 s.
# L2: replay with a 75 CM height bar. L3: two kitchen scales: toast ~40 g vs butter pat <=4 g (butter lifts off).
# L4: slow-mo drop with ghost copies along the arc -> "1/2 TURN". L5: cascade: a row of 8 school tables, toasts drop
# one after another, 5 of 8 land butter-down, counter -> "62 % BUTTER-DOWN". L6: the table grows to 3 m (camera tilts up).
# L7: toast slides off the 3 m table, follow-cam: a full turn, lands BUTTER-UP. After the card starts: hook framing (loop).
M_WOOD = noise_mat("wood", (0.50, 0.32, 0.18), (0.62, 0.42, 0.25), 7.0, 0.45)
M_FLOOR = tiles("floor", (0.78, 0.76, 0.72), (0.45, 0.43, 0.40), 1.2)
M_WALL = tiles("wall", (0.55, 0.68, 0.70), (0.85, 0.88, 0.86), 3.0)
M_CREAM = mat("cream", (0.92, 0.90, 0.84), 0.8)
M_TOAST = noise_mat("toast", (0.62, 0.36, 0.12), (0.80, 0.52, 0.20), 30.0, 0.85)
M_CRUST = mat("crust", (0.36, 0.18, 0.06), 0.8)
M_BUT = mat("butter", (1.0, 0.86, 0.30), 0.25, 0, (1.0, 0.8, 0.2), 0.25)
M_GHOST = mat("ghost", (0.95, 0.85, 0.6), 0.6, 0, (1.0, 0.85, 0.55), 0.6)
M_PLATE = mat("plate", (0.95, 0.95, 0.97), 0.2)
M_SCALE = mat("scale", (0.85, 0.86, 0.88), 0.3, 0.3)
M_DARK = mat("dark", (0.04, 0.05, 0.06), 0.4)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_AMB = mat("lbla", (1.0, 0.55, 0.08), 0.4, 0, (1.0, 0.5, 0.06), 3.0)
M_RED = mat("redl", (0.9, 0.04, 0.02), 0.4, 0, (1.0, 0.06, 0.03), 3.0)
M_GRN = mat("grnl", (0.05, 0.8, 0.15), 0.4, 0, (0.08, 1.0, 0.25), 2.4)
M_LCD = mat("lcd", (0.4, 1.0, 0.8), 0.4, 0, (0.35, 1.0, 0.75), 3.0)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.5
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.75, 0.78, 0.82, 1); WBG.inputs[1].default_value = 0.35

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
DROP_A = (0.08, 0.85)            # hook drop (start, duration)
DROP_B = (t2 + 0.55, 0.85)       # replay with the 75 cm bar
T_LIFT = t3 + 0.55               # butter lifts onto its own scale
DROP_C = (t4 + 0.05, 1.45)       # slow-mo with ghosts
DROP_D = (t7 + 0.02, 1.25)       # from the 3 m table
T_GROW = (t6 - 0.05, t7 - 0.05)  # table grows 0.75 -> 3.0 m
ROW_T0 = t5 + 0.15; ROW_DT = 0.33; ROW_DUR = 0.75
ROW_DOWN = [1, 1, 0, 1, 1, 0, 1, 0]   # 5 of 8 butter-down (62.5 %)

# ---------- hero kitchen ----------
TOP0, TOP3 = 0.75, 3.0
TW, TD, TT = 0.90, 0.60, 0.035
XE = TW / 2                      # table edge x
bpy.ops.mesh.primitive_plane_add(size=1, location=(3, 4, 0)); fl = bpy.context.object; fl.scale = (30, 30, 1); link(fl, M_FLOOR)
box((0.3, 0.75, 2.5), (5.0, 0.06, 5.0), M_WALL, "wall")
box((-1.2, 0.70, 0.45), (1.4, 0.06, 0.9), M_CREAM, "cupboard")
def ubox(loc, size, m, name):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = size; o.name = name; return link(o, m)
TOPB = ubox((0, 0, TOP0 - TT / 2), (TW, TD, TT), M_WOOD, "top")
LEGS = []
for sx in (-1, 1):
    for sy in (-1, 1):
        lg = cyl((sx * (TW / 2 - 0.05), sy * (TD / 2 - 0.05), 0.5), 0.022, 1.0, M_WOOD, "leg", verts=12); LEGS.append(lg)
PLATE = cyl((0.30, 0, TOP0 + 0.006), 0.11, 0.012, M_PLATE, "plate", verts=40)
def make_toast(m_bread, m_but, name):
    t = ubox((0, 0, 0), (0.15, 0.14, 0.02), m_bread, name)
    b = ubox((0, 0, 0), (0.115, 0.105, 0.007), m_but, name + "_butter")
    return t, b
T1, B1 = make_toast(M_TOAST, M_BUT, "hero")
GH = [make_toast(M_GHOST, M_GHOST, f"ghost{k}") for k in range(4)]
for g in GH:
    for o in g: noshadow(o)
SPLAT = cyl((0, 0, 0.002), 1.0, 0.003, M_BUT, "splat", verts=24)
# scales (line 3)
SC = []
for k, x in enumerate((0.02, 0.27)):
    base = ubox((x, -0.05, TOP0 + 0.02), (0.17, 0.17, 0.04), M_SCALE, f"scale{k}")
    pan = ubox((x, -0.05, TOP0 + 0.043), (0.15, 0.15, 0.006), M_PLATE, f"pan{k}")
    lcd = ubox((x, -0.137, TOP0 + 0.02), (0.12, 0.004, 0.032), M_DARK, f"lcd{k}")
    SC.append((base, pan, lcd, x))
RD0 = label("", (0.02, -0.142, TOP0 + 0.020), 0.026, M_LCD); RD1 = label("", (0.27, -0.142, TOP0 + 0.020), 0.026, M_LCD)
TL0 = label("TOAST", (0.02, -0.15, TOP0 + 0.085), 0.034, M_WHITE); TL1 = label("BUTTER", (0.27, -0.15, TOP0 + 0.085), 0.034, M_AMB)
# labels
LB_DOWN = label("BUTTER-DOWN", (0.64, -0.10, 0.36), 0.085, M_RED)
LB_UP = label("BUTTER-UP", (0.72, -0.10, 0.34), 0.085, M_GRN)
BAR = ubox((0.95, -0.05, TOP0 / 2), (0.012, 0.012, TOP0), M_AMB, "bar"); noshadow(BAR)
BAR_T = label("75 CM", (0.92, -0.06, 0.16), 0.085, M_AMB, align="RIGHT")
HALF_T = label("½ TURN", (0.80, -0.10, 0.34), 0.095, M_AMB)
BAR3 = ubox((0.95, -0.05, TOP3 / 2), (0.02, 0.02, TOP3), M_AMB, "bar3"); noshadow(BAR3)
BAR3_T = label("3 M", (0.78, -0.06, 2.15), 0.22, M_AMB)
key = bpy.data.objects.new("key", bpy.data.lights.new("key", "AREA")); key.data.energy = 220; key.data.size = 2.5
key.data.color = (1.0, 0.94, 0.85); key.location = (-0.8, -2.2, 3.2); key.rotation_euler = (math.radians(40), 0, math.radians(-20)); S.collection.objects.link(key)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA")); fill.data.energy = 90; fill.data.size = 2.0
fill.data.color = (0.85, 0.9, 1.0); fill.location = (1.8, -1.8, 1.6); fill.rotation_euler = (math.radians(60), 0, math.radians(45)); S.collection.objects.link(fill)

# ---------- school row (line 5) ----------
RX = 6.0; RY = [k * 1.15 for k in range(8)]
ROW = []
for k, y in enumerate(RY):
    box((RX, y, TOP0 - TT / 2), (TW, TD, TT), M_WOOD, "rtop")
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl((RX + sx * (TW / 2 - 0.05), y + sy * (TD / 2 - 0.05), (TOP0 - TT) / 2), 0.022, TOP0 - TT, M_WOOD, "rleg", verts=10)
    cyl((RX + 0.30, y, TOP0 + 0.006), 0.11, 0.012, M_PLATE, "rplate", verts=32)
    t, b = make_toast(M_TOAST, M_BUT, f"r{k}")
    mk = cyl((RX + 0.62, y, 0.003), 0.10, 0.004, M_RED if ROW_DOWN[k] else M_GRN, "rmark", verts=24); noshadow(mk)
    ROW.append((t, b, mk, y))
CNT = label("", (RX + 0.55, 1.6, 1.22), 0.17, M_RED)
rk = bpy.data.objects.new("rkey", bpy.data.lights.new("rkey", "AREA")); rk.data.energy = 900; rk.data.size = 5
rk.location = (RX + 1.5, 2.0, 4.5); rk.rotation_euler = (math.radians(15), 0, math.radians(20)); S.collection.objects.link(rk)

# ---------- toast motion ----------
def drop_pose(t, t0, dur, top, turns_end, x_rest=0.34, y=0.0, x0=0.0, land_dx=0.17):
    """return (location, rot_y) of a toast that slides off the +x edge and falls to the floor"""
    zr = top + 0.012 + 0.010
    u = (t - t0) / dur
    if u <= 0: return V((x0 + x_rest, y, zr)), 0.0
    u = min(u, 1.0)
    if u < 0.22:                                  # slide + tip over the edge
        s = smooth(u / 0.22)
        return V((x0 + x_rest + (XE + 0.02 - x_rest) * s, y, zr - 0.004 * s)), 0.35 * s ** 2
    s = (u - 0.22) / 0.78
    z = zr + (0.010 - zr) * s * s
    x = x0 + XE + 0.02 + land_dx * s
    th = 0.35 + (turns_end - 0.35) * s
    return V((x, y, z)), th
def place(o_t, o_b, loc, th, f, scale_t=(0.15, 0.14, 0.02)):
    o_t.location = loc; o_t.rotation_euler = (0, th, 0); o_t.scale = scale_t
    off = V((0, 0, 0.0135)); off.rotate(o_t.rotation_euler)
    o_b.location = loc + off; o_b.rotation_euler = (0, th, 0); o_b.scale = (0.115, 0.105, 0.007)
    for o in (o_t, o_b):
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f); o.keyframe_insert("scale", frame=f)
def hide(o_t, o_b, f):
    for o in (o_t, o_b):
        o.scale = (0.0001,) * 3; o.keyframe_insert("scale", frame=f)
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)
def top_z(t):
    if t < T_GROW[0] or t >= T_LOOP: return TOP0
    return TOP0 + (TOP3 - TOP0) * smooth((t - T_GROW[0]) / (T_GROW[1] - T_GROW[0]))

def handler(scene, *a):
    t = scene.frame_current / FPS
    if t3 - 0.05 <= t < t4 - 0.05:
        RD0.data.body = f"{40 * smooth((t - t3 - 0.1) / 0.6):.0f} g"
        RD1.data.body = f"{4 * smooth((t - T_LIFT - 0.4) / 0.5):.0f} g" if t >= T_LIFT + 0.4 else "0 g"
    if t5 - 0.05 <= t < t6 - 0.05:
        landed = [k for k in range(8) if t >= ROW_T0 + k * ROW_DT + ROW_DUR]
        dn = sum(ROW_DOWN[k] for k in landed)
        CNT.data.body = "62 % BUTTER-DOWN" if len(landed) == 8 else (f"DOWN {dn} · UP {len(landed) - dn}" if landed else "")
bpy.app.handlers.frame_change_pre.append(handler)

for f in range(0, N + 1):
    t = f / FPS
    loop = t >= T_LOOP
    tz = top_z(t)
    # table (top + legs follow height)
    TOPB.location = (0, 0, tz - TT / 2); TOPB.keyframe_insert("location", frame=f)
    for lg in LEGS:
        h = tz - TT; lg.scale = (1, 1, h); lg.location = (lg.location.x, lg.location.y, h / 2)
        lg.keyframe_insert("scale", frame=f); lg.keyframe_insert("location", frame=f)
    PLATE.location = (0.30, 0, tz + 0.006); PLATE.keyframe_insert("location", frame=f)
    # hero toast
    splat = False; on_scale = t3 - 0.05 <= t < t4 - 0.05 and not loop
    if loop: loc, th = drop_pose(t, 99, 1, TOP0, math.pi)
    elif t < t2 - 0.05: loc, th = drop_pose(t, *DROP_A, TOP0, math.pi); splat = t >= sum(DROP_A)
    elif t < t3 - 0.05: loc, th = drop_pose(t, *DROP_B, TOP0, math.pi); splat = t >= sum(DROP_B)
    elif on_scale: loc, th = V((0.02, -0.05, TOP0 + 0.046 + 0.010)), 0.0
    elif t < t5 - 0.05: loc, th = drop_pose(t, *DROP_C, TOP0, math.pi); splat = t >= sum(DROP_C)
    elif t < t6 - 0.05: loc, th = None, 0
    elif t < t7: loc, th = drop_pose(t, 99, 1, tz, 0)
    else: loc, th = drop_pose(t, *DROP_D, TOP3, 2 * math.pi)
    if loc is None: hide(T1, B1, f)
    else:
        place(T1, B1, loc, th, f)
        if on_scale:   # butter pat lifts off the toast onto scale 2
            k = smooth((t - T_LIFT) / 0.45); arc = math.sin(math.pi * k) * 0.08
            B1.location = V((0.02 + 0.25 * k, -0.05, TOP0 + 0.046 + 0.0235 - 0.0165 * k + arc)); B1.keyframe_insert("location", frame=f)
    SPLAT.scale = (0.085, 0.078, 1) if splat else (0.0001,) * 3
    if loc is not None: SPLAT.location = (loc.x, loc.y, 0.002)
    SPLAT.keyframe_insert("scale", frame=f); SPLAT.keyframe_insert("location", frame=f)
    # ghosts along the slow-mo arc (line 4)
    for j, (gt, gb) in enumerate(GH):
        s_at = DROP_C[0] + DROP_C[1] * (0.30 + 0.17 * j)
        if t4 - 0.05 <= t < t5 - 0.05 and t >= s_at:
            gl, gth = drop_pose(s_at, *DROP_C, TOP0, math.pi); place(gt, gb, gl, gth, f)
        else: hide(gt, gb, f)
    # school row
    for k, (rt, rb, mk, y) in enumerate(ROW):
        t0 = ROW_T0 + k * ROW_DT
        if t5 - 0.05 <= t < t6 - 0.05:
            if ROW_DOWN[k]: loc_r, th_r = drop_pose(t, t0, ROW_DUR, TOP0, math.pi, y=y, x0=RX)
            else:
                loc_r, _ = drop_pose(t, t0, ROW_DUR, TOP0, 0.0, y=y, x0=RX)
                u = max(0, min(1, (t - t0) / ROW_DUR)); th_r = 0.9 * math.sin(math.pi * u)
            place(rt, rb, loc_r, th_r, f)
            vis(mk, t >= t0 + ROW_DUR, f)
        else:
            place(rt, rb, *drop_pose(t, 99, 1, TOP0, 0, y=y, x0=RX), f); vis(mk, False, f)
    # labels
    landA = sum(DROP_A) <= t < t2 - 0.05; landB = sum(DROP_B) <= t < t3 - 0.05
    vis(LB_DOWN, (landA or landB) and not loop, f)
    vis(BAR, t2 + 0.1 <= t < t3 - 0.05, f, base=(0.012, 0.012, TOP0)); vis(BAR_T, t2 + 0.1 <= t < t3 - 0.05, f)
    for o in (RD0, RD1, TL0): vis(o, on_scale, f)
    vis(TL1, on_scale and t >= T_LIFT + 0.3, f)
    for (b_, p_, l_, x_) in SC:
        for o, bs in ((b_, (0.17, 0.17, 0.04)), (p_, (0.15, 0.15, 0.006)), (l_, (0.12, 0.004, 0.032))): vis(o, on_scale, f, base=bs)
    vis(HALF_T, sum(DROP_C) - 0.05 <= t < t5 - 0.05, f)
    vis(CNT, t5 - 0.05 <= t < t6 - 0.05, f)
    vis(BAR3, T_GROW[1] - 0.2 <= t < t7 + 0.5, f, base=(0.02, 0.02, TOP3)); vis(BAR3_T, T_GROW[1] - 0.2 <= t < t7 + 0.5, f)
    vis(LB_UP, sum(DROP_D) - 0.03 <= t < T_LOOP, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 100; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((1.30, -1.50, 1.30), (0.52, 0, 0.36), (1.24, -1.42, 1.26), (0.52, 0, 0.36))
SEG = [
    (0.0, t2 - 0.05, HOOK, 24, 24),
    (t2 - 0.05, t3 - 0.05, fixed((-0.10, -1.95, 1.20), (0.50, 0, 0.36), (0.0, -1.85, 1.15), (0.50, 0, 0.36)), 24, 24),
    (t3 - 0.05, t4 - 0.05, fixed((0.30, -0.95, 1.08), (0.15, -0.05, 0.79), (0.29, -0.90, 1.06), (0.15, -0.05, 0.79)), 28, 28),
    (t4 - 0.05, t5 - 0.05, fixed((0.55, -2.05, 0.95), (0.55, 0, 0.36), (0.55, -1.95, 0.92), (0.55, 0, 0.36)), 24, 24),
    (t5 - 0.05, t6 - 0.05, fixed((RX + 1.55, -1.75, 1.45), (RX + 0.25, 2.2, 0.62), (RX + 1.45, -1.55, 1.40), (RX + 0.25, 2.2, 0.62)), 26, 26),
    (t6 - 0.05, t7, fixed((1.30, -1.50, 1.30), (0.52, 0, 0.36), (2.6, -3.6, 2.7), (0.50, 0, 1.85)), 24, 24),
    (t7, T_LOOP, None, 24, 24),
    (T_LOOP, DUR + 0.01, HOOK, 24, 24),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    if seg[2] is None:   # follow-cam on the falling toast (3 m table)
        lz, _ = drop_pose(t, *DROP_D, TOP3, 2 * math.pi)
        k = smooth((t - t7) / 0.30)
        zt = max(0.22, lz.z - 0.15)
        qf = V((0.55, 0, zt)); pf = qf + V((0.80, -1.55, 0.85))
        p = V((2.6, -3.6, 2.7)).lerp(pf, k); q = V((0.50, 0, 1.85)).lerp(qf, k)
    else:
        pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

M_PLATEL = mat("lplate", (0.02, 0.02, 0.03), 0.6)
for o, nch in ((LB_DOWN, 11), (LB_UP, 9), (BAR_T, 5), (HALF_T, 6), (BAR3_T, 4), (TL0, 5), (TL1, 6), (CNT, 16)):
    o.rotation_euler = (0, 0, 0); cc = o.constraints.new("TRACK_TO"); cc.target = cam
    cc.track_axis = "TRACK_Z"; cc.up_axis = "UP_Y"
    sz = o.data.size; w = nch * sz * 0.72 + sz * 0.5
    bpy.ops.mesh.primitive_plane_add(size=1); pl = bpy.context.object; pl.name = o.name + "_bg"
    pl.data.materials.append(M_PLATEL); noshadow(pl); pl.visible_glossy = False
    ox = -w / 2 + sz * 0.25 if o.data.align_x == "RIGHT" else 0.0
    for v in pl.data.vertices: v.co.x = v.co.x * w + ox; v.co.y = v.co.y * sz * 1.35; v.co.z = -0.012
    pl.parent = o
json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "drop_a": DROP_A, "drop_b": DROP_B,
           "lift": T_LIFT, "drop_c": DROP_C, "row_t0": ROW_T0, "row_dt": ROW_DT, "grow": T_GROW, "drop_d": DROP_D},
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
