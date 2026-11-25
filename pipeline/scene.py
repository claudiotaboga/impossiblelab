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
    return o



# ================= episode 20: a candle in space (E17 cascade middle, reel 3) =================
# Hook (wide): EARTH candle (left, kitchen tiles) vs ORBIT candle (right, station panel + porthole): both wicks light at
# 0.08 s; Earth flame = yellow teardrop, orbit flame = round ball. Line 2: close on the orbit candle (porthole Earth).
# Line 3 (cascade, wide): hot-air dots stream up on Earth, spread evenly and stall in orbit -> orbit flame turns blue.
# Line 4: timers: Earth candle shrinks, drips, goes out at 10 MIN; orbit timer runs on to 45 MIN.
# Line 5 (close): orbit candle melts into a floating molten wax ball, no drips. Line 6: flame pulses, shrinks, dies.
# Line 7: a white wax-fog sphere swells to ~2.5x the flame; red warning ring pulses. Last ~1.2 s: hook framing (loop).
M_TABLE = noise_mat("table", (0.55, 0.36, 0.22), (0.66, 0.45, 0.28), 7.0, 0.45)
M_WALLE = tiles("wallE", (0.62, 0.55, 0.45), (0.35, 0.30, 0.25), 4.0)
M_WALLS = tiles("wallS", (0.16, 0.18, 0.22), (0.06, 0.07, 0.09), 1.5)
M_WAX = mat("wax", (0.96, 0.93, 0.86), 0.45)
M_WAXL = mat("waxl", (0.98, 0.90, 0.72), 0.12)
M_HOLD = mat("holder", (0.65, 0.66, 0.70), 0.25, 0.9)
M_WICK = mat("wick", (0.05, 0.04, 0.03), 0.8)
M_DARK = mat("dark", (0.04, 0.04, 0.05), 0.5)
M_EARTHP = mat("earthp", (0.2, 0.45, 0.9), 0.5, 0, (0.15, 0.4, 1.0), 1.2)
M_PANL = mat("panl", (0.6, 0.9, 1.0), 0.4, 0, (0.5, 0.85, 1.0), 2.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_AMB = mat("lbla", (1.0, 0.65, 0.15), 0.4, 0, (1.0, 0.6, 0.12), 4.0)
M_REDL = mat("redl", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 3.0)
M_HOT = mat("hot", (1.0, 0.5, 0.15), 0.4, 0, (1.0, 0.45, 0.1), 3.0)
M_FE = mat("flameE", (1.0, 0.75, 0.25), 0.5, 0, (1.0, 0.62, 0.15), 3.2)
M_FEC = mat("flameEc", (0.3, 0.5, 1.0), 0.5, 0, (0.25, 0.45, 1.0), 2.5)

def shell_mat(name, col, estr, blend=0.45):
    """emissive rim, see-through centre (spherical diffusion flame / fog)"""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); em = nt.nodes.new("ShaderNodeEmission")
    em.inputs[0].default_value = (*col, 1); em.inputs[1].default_value = estr
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = blend
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 0.6
    nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    mx = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(pw.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    m["em"] = em.name
    return m, em
M_FS, EM_FS = shell_mat("flameS", (1.0, 0.72, 0.25), 6.0, 0.32)
M_FOG, EM_FOG = shell_mat("fog", (0.95, 0.95, 0.92), 1.4, 0.35)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.4
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.05, 0.05, 0.07, 1); WBG.inputs[1].default_value = 0.4

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_IGN = 0.08                 # both wicks light
T_HOT = t3 + 0.15            # hot-air dots start
T_BLUE = t3 + 0.95           # orbit flame turns blue
T_TIM = t4 + 0.10            # timers start
T_EOUT = t4 + 1.30           # Earth candle out at 10 MIN
T_45 = t5 - 0.25             # orbit timer reaches 45 MIN
T_WAX = t5 + 0.15            # wax melts into a ball
T_WAXF = T_WAX + 1.5
T_PULSE = t6                 # flame pulses before it dies
T_OUT = t7 - 0.02            # flame out
T_FOG = t7 + 0.05            # wax-fog sphere swells
T_RING = t7 + 1.0            # warning ring

TOP = 0.90; EX, SX = -0.11, 0.11
H0 = 0.10; CR = 0.022
box((0, 0, TOP / 2), (1.6, 0.8, TOP), M_TABLE, "counter")
box((-0.8, 0.35, 1.5), (1.6, 0.06, 3.0), M_WALLE, "wallE")
box((0.8, 0.35, 1.5), (1.6, 0.06, 3.0), M_WALLS, "wallS")
box((0.0, 0.31, 1.5), (0.012, 0.03, 3.0), M_DARK, "divider")
# station details: panel light strips + porthole with Earth
for (x, z) in ((0.30, 1.22), (0.30, 0.98)):
    box((x, 0.315, z), (0.10, 0.01, 0.012), M_PANL, "strip")
cyl((0.21, 0.318, 1.05), 0.050, 0.012, M_HOLD, "port_rim", rot=(math.radians(90), 0, 0))
cyl((0.21, 0.312, 1.05), 0.042, 0.012, M_DARK, "port_glass", rot=(math.radians(90), 0, 0))
sphere((0.222, 0.30, 1.025), 0.028, M_EARTHP, "earthball")

def candle(x, name):
    cyl((x, 0, TOP + 0.006), 0.04, 0.012, M_HOLD, name + "holder")
    body = cyl((x, 0, TOP + 0.012 + H0 / 2), CR, H0, M_WAX, name + "body")
    wick = cyl((x, 0, TOP + 0.012 + H0 + 0.006), 0.0018, 0.012, M_WICK, name + "wick", verts=8)
    return body, wick
EB, EW = candle(EX, "e"); SB, SW = candle(SX, "s")
def set_candle(body, wick, x, h, f):
    body.scale = (1, 1, max(h, 0.001) / H0); body.location = (x, 0, TOP + 0.012 + h / 2)
    wick.location = (x, 0, TOP + 0.012 + h + 0.006)
    for o in (body, wick):
        o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)
# Earth flame: teardrop (sphere stretched up) + small blue base
FE = sphere((EX, 0, 1.0), 1.0, M_FE, "flameE", None, 24); noshadow(FE)
FEC = sphere((EX, 0, 1.0), 1.0, M_FEC, "flameEc", None, 12); noshadow(FEC)
# orbit flame: sphere shell
FS = sphere((SX, 0, 1.0), 1.0, M_FS, "flameS", None, 32); noshadow(FS)
# lights at the flames
LE = bpy.data.objects.new("le", bpy.data.lights.new("le", "POINT")); LE.data.shadow_soft_size = 0.01; S.collection.objects.link(LE)
LS = bpy.data.objects.new("ls", bpy.data.lights.new("ls", "POINT")); LS.data.shadow_soft_size = 0.01; S.collection.objects.link(LS)
LE.data.color = (1.0, 0.7, 0.35)
# drips on the Earth candle
DRIPS = []
for k, a in enumerate((-60, -20, 25, 70)):
    xx = EX + (CR + 0.002) * math.sin(math.radians(a)); yy = -(CR + 0.002) * math.cos(math.radians(a))
    o = cyl((xx, yy, 0), 0.0035, 1.0, M_WAXL, "drip", verts=10)
    DRIPS.append((o, xx, yy, 0.02 + 0.012 * k))
# molten wax ball (orbit candle)
WB = sphere((SX, 0, 1.0), 1.0, M_WAXL, "waxball", None, 32)
# fog + warning ring
FOG = sphere((SX, 0, 1.0), 1.0, M_FOG, "fog", None, 32); noshadow(FOG)
bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.035, major_segments=64, minor_segments=8, location=(SX, -0.02, 1.0), rotation=(math.radians(90), 0, 0))
RING = link(bpy.context.object, M_REDL); RING.name = "ring"; noshadow(RING)
# hot-air dots
HOT_E, HOT_S = [], []
rh = random.Random(3)
for k in range(14):
    HOT_E.append((noshadow(sphere((EX, 0, 1), 0.0045, M_HOT, "hotE", None, 8)), rh.uniform(0, 1), rh.uniform(-1, 1)))
for k in range(16):
    u = rh.uniform(-0.9, 0.9); a = rh.uniform(0, math.tau)
    d = V((math.sqrt(1 - u * u) * math.cos(a), math.sqrt(1 - u * u) * math.sin(a) * 0.4 - 0.6, u)).normalized()
    HOT_S.append((noshadow(sphere((SX, 0, 1), 0.0045, M_HOT, "hotS", None, 8)), d, rh.uniform(0, 0.4)))
# labels
LBL_Y = -0.05
LB_E = label("EARTH", (EX, LBL_Y, 1.165), 0.030, M_WHITE); LB_S = label("ORBIT", (SX, LBL_Y, 1.165), 0.030, M_LBLB)
SUB_E = label("", (EX, LBL_Y, 1.130), 0.020, M_AMB); SUB_S = label("", (SX, LBL_Y, 1.130), 0.020, M_AMB)
WAX_T = label("MOLTEN\nWAX BALL", (SX - 0.036, -0.06, 1.012), 0.0115, M_AMB, align="RIGHT")
NODRIP_T = label("NO DRIPS", (SX - 0.036, -0.06, 0.968), 0.0115, M_WHITE, align="RIGHT")
FOG_T = label("FLAMMABLE", (SX, -0.10, 1.003), 0.016, M_REDL)
kl = bpy.data.objects.new("key", bpy.data.lights.new("key", "AREA")); kl.data.energy = 30; kl.data.size = 1.5
kl.data.color = (1.0, 0.92, 0.8); kl.location = (-0.6, -1.6, 1.9); kl.rotation_euler = (math.radians(50), 0, math.radians(-20)); S.collection.objects.link(kl)
kl2 = bpy.data.objects.new("key2", bpy.data.lights.new("key2", "AREA")); kl2.data.energy = 18; kl2.data.size = 1.2
kl2.data.color = (0.85, 0.9, 1.0); kl2.location = (0.7, -1.5, 1.7); kl2.rotation_euler = (math.radians(50), 0, math.radians(25)); S.collection.objects.link(kl2)

# ---------- state functions ----------
def e_height(t):  return H0 - 0.06 * smooth((t - T_TIM) / (T_EOUT - T_TIM)) if t < T_LOOP else H0
def s_height(t):  return H0 - 0.065 * smooth((t - T_WAX) / (T_WAXF - T_WAX)) if t < T_LOOP else H0
def e_timer(t):   return 10.0 * smooth((t - T_TIM) / (T_EOUT - T_TIM))
def s_timer(t):   return 45.0 * smooth((t - T_TIM) / (T_45 - T_TIM))
def handler(scene, *a):
    t = scene.frame_current / FPS
    if t3 - 0.05 <= t < t4 - 0.05:
        SUB_E.data.body = "HOT AIR RISES"; SUB_S.data.body = "BLUE · NO SOOT" if t >= T_BLUE else "HOT AIR STAYS"
    elif t4 - 0.05 <= t < t5 - 0.05:
        SUB_E.data.body = "OUT AT 10 MIN" if t >= T_EOUT else f"{e_timer(t):.0f} MIN"
        SUB_S.data.body = f"{s_timer(t):.0f} MIN" + (" · STILL LIT" if t >= T_45 - 0.1 else "")
    else:
        SUB_E.data.body = ""; SUB_S.data.body = ""
bpy.app.handlers.frame_change_pre.append(handler)

# ---------- animation ----------
for f in range(0, N + 1):
    t = f / FPS
    loop = t >= T_LOOP
    tt = t - T_LOOP if loop else t
    ign = smooth((tt - T_IGN) / 0.3)
    fl = 1 + 0.06 * math.sin(t * 23) + 0.04 * math.sin(t * 37)
    # candles
    he = e_height(t); hs = s_height(t)
    set_candle(EB, EW, EX, he, f); set_candle(SB, SW, SX, hs, f)
    # Earth flame
    eon = ign * (0 if (T_EOUT <= t < T_LOOP) else 1) * (1 - 0.6 * smooth((t - (T_EOUT - 0.3)) / 0.3) if t < T_LOOP else 1)
    zt = TOP + 0.012 + he + 0.008
    FE.scale = (0.011 * eon * fl, 0.011 * eon * fl, 0.034 * eon * fl) if eon > 0.01 else (0.0001,) * 3
    FE.location = (EX + 0.001 * math.sin(t * 11), 0, zt + 0.026 * eon)
    FEC.scale = (0.006 * eon, 0.006 * eon, 0.007 * eon) if eon > 0.01 else (0.0001,) * 3
    FEC.location = (EX, 0, zt + 0.002)
    for o in (FE, FEC): o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)
    LE.location = (EX, -0.03, zt + 0.03); LE.data.energy = 0.6 * eon; LE.keyframe_insert("location", frame=f); LE.data.keyframe_insert("energy", frame=f)
    # drips (line 4 only)
    for (o, xx, yy, ln) in DRIPS:
        g = smooth((t - T_TIM - 0.2) / 0.8) if (t4 - 0.05 <= t < t5 - 0.05) else 0.0
        L_ = max(0.0001, ln * g); top_z = TOP + 0.012 + he
        o.scale = (1, 1, L_) if g > 0 else (0.0001,) * 3; o.location = (xx, yy, top_z - L_ / 2)
        o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)
    # orbit flame + wax ball
    wb = smooth((t - T_WAX) / (T_WAXF - T_WAX)) if not loop else 0.0
    RWB = 0.030 * wb ** 0.6
    ztop = TOP + 0.012 + hs
    WB.scale = (RWB, RWB, RWB) if RWB > 0.001 else (0.0001,) * 3
    WB.location = (SX + 0.002 * math.sin(t * 3), 0, ztop + RWB * 0.55); WB.keyframe_insert("scale", frame=f); WB.keyframe_insert("location", frame=f)
    die = smooth((t - T_PULSE) / (T_OUT - T_PULSE)) if not loop else 0.0
    pulse = 1 + (0.18 * math.sin(math.tau * 1.6 * (t - T_PULSE)) if (T_PULSE <= t < T_OUT and not loop) else 0)
    son = ign * (0 if (T_OUT <= t < T_LOOP) else 1)
    rs = 0.030 * son * (1 - 0.45 * die) * pulse * (1 + 0.015 * math.sin(t * 9))
    zc = ztop + 2 * RWB * 0.55 + 0.016 if wb > 0 else ztop + 0.020
    FS.scale = (rs, rs, rs) if rs > 0.001 else (0.0001,) * 3; FS.location = (SX, 0, zc)
    FS.keyframe_insert("scale", frame=f); FS.keyframe_insert("location", frame=f)
    blue = smooth((t - T_BLUE) / 0.6) if not loop else 0.0
    EM_FS.inputs[0].default_value = (1.0 - 0.78 * blue, 0.72 - 0.30 * blue, 0.25 + 0.75 * blue, 1)
    EM_FS.inputs[1].default_value = (3.0 + 1.5 * blue) * (1 - 0.5 * die)
    EM_FS.inputs[0].keyframe_insert("default_value", frame=f); EM_FS.inputs[1].keyframe_insert("default_value", frame=f)
    LS.location = (SX, -0.04, zc); LS.data.energy = 0.5 * son * (1 - 0.5 * die)
    LS.data.color = (1.0 - 0.7 * blue, 0.75 - 0.25 * blue, 0.35 + 0.65 * blue)
    LS.keyframe_insert("location", frame=f); LS.data.keyframe_insert("energy", frame=f); LS.data.keyframe_insert("color", frame=f)
    # fog
    fg = smooth((t - T_FOG) / 0.9) if (T_FOG <= t < T_LOOP) else 0.0
    rf = 0.065 * fg ** 0.7 * (1 + 0.03 * math.sin(t * 4))
    FOG.scale = (rf, rf, rf) if rf > 0.002 else (0.0001,) * 3; FOG.location = (SX, 0, ztop + 0.03 + 0.004 * math.sin(t * 2))
    FOG.keyframe_insert("scale", frame=f); FOG.keyframe_insert("location", frame=f)
    rg = smooth((t - T_RING) / 0.25) if (T_RING <= t < tc) else 0.0
    rr_ = 0.078 * rg * (1 + 0.05 * math.sin(math.tau * 2 * (t - T_RING)))
    RING.scale = (rr_, rr_, rr_) if rr_ > 0.002 else (0.0001,) * 3; RING.location = (SX, -0.02, ztop + 0.03)
    RING.keyframe_insert("scale", frame=f); RING.keyframe_insert("location", frame=f)
    # hot-air dots (line 3)
    on3 = t3 - 0.05 <= t < t4 - 0.05
    for (o, ph, sw) in HOT_E:
        if on3 and t >= T_HOT:
            u = ((t - T_HOT) * 0.9 + ph) % 1.0
            o.location = (EX + 0.012 * sw + 0.006 * math.sin(u * 9 + ph * 7), 0, zt + 0.045 + u * 0.10)
            s_ = 1.0 - u * 0.6; o.scale = (s_, s_, s_)
        else: o.scale = (0.0001,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    for (o, d, dl) in HOT_S:
        if on3 and t >= T_HOT + dl:
            r_ = 0.03 + 0.03 * smooth((t - T_HOT - dl) / 1.2)
            o.location = V((SX, 0, zc)) + d * r_
            o.scale = (1, 1, 1)
        else: o.scale = (0.0001,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    vis(SUB_E, t3 - 0.05 <= t < t5 - 0.05, f); vis(SUB_S, t3 - 0.05 <= t < t5 - 0.05, f)
    vis(WAX_T, T_WAX + 0.4 <= t < t6, f); vis(NODRIP_T, T_WAX + 0.9 <= t < t6, f)
    vis(FOG_T, T_RING <= t < tc, f)
    wide = (t < t2 - 0.05) or (t3 - 0.05 <= t < t5 - 0.05) or t >= T_LOOP
    vis(LB_E, wide, f); vis(LB_S, wide, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 100; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
WIDE_Z = 1.035
HOOK = fixed((0.0, -0.80, 1.06), (0.0, 0, WIDE_Z), (0.0, -0.76, 1.06), (0.0, 0, WIDE_Z))
CLOSE = fixed((SX - 0.03, -0.60, 1.03), (SX - 0.03, 0, 1.005), (SX - 0.03, -0.56, 1.03), (SX - 0.03, 0, 1.005))
SEG = [
    (0.0, t2 - 0.05, HOOK, 30, 30),
    (t2 - 0.05, t3 - 0.05, fixed((SX + 0.05, -0.75, 1.06), (SX + 0.03, 0, 1.03), (SX, -0.62, 1.04), (SX, 0, 1.02)), 30, 30),
    (t3 - 0.05, t5 - 0.05, fixed((0.0, -0.82, 1.06), (0.0, 0, WIDE_Z), (0.0, -0.78, 1.06), (0.0, 0, WIDE_Z)), 30, 30),
    (t5 - 0.05, t7 - 0.05, CLOSE, 30, 32),
    (t7 - 0.05, T_LOOP, fixed((SX - 0.02, -0.66, 1.03), (SX - 0.02, 0, 1.0), (SX - 0.02, -0.62, 1.03), (SX - 0.02, 0, 1.0)), 30, 30),
    (T_LOOP, DUR + 0.01, HOOK, 30, 30),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "ign": T_IGN, "hot": T_HOT, "blue": T_BLUE,
           "timers": T_TIM, "earth_out": T_EOUT, "t45": T_45, "wax": T_WAX, "pulse": T_PULSE, "out": T_OUT, "fog": T_FOG, "ring": T_RING},
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
