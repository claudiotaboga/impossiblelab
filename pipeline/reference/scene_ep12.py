"""The Impossible Lab #12 - making toast on Venus.
Units: metres (props at sculpture scale). Set (origin): YOUR OVEN (x = -1.4, kitchen tiles behind) vs VENUS (x = +1.4,
basalt ground, orange haze wall). Thermometers above each set (0-500 C over 1.9 m) rise to 260 vs 464 C in the hook
(value text via frame_change_pre). Line 2: a bread slice lowers onto a steel toast fork on Venus. Line 3: both thermometers,
OVEN MAX line + "~1.8x". Line 4: 10 pressure arrows squeeze in, "92 BAR". Line 5: bread chars golden -> brown -> black
(keyframed Base Color), "CHARCOAL". Line 7: crossed-out flame, NO OXYGEN / 96.5% CO2. Card: back to the hook framing.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(12)
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


M_PLINTH = mat("plinth", (0.10, 0.11, 0.13), 0.5)
M_TILE = tiles("tile", (0.80, 0.84, 0.86), (0.35, 0.37, 0.40), 3.0)
M_VROCK = noise_mat("vrock", (0.22, 0.10, 0.04), (0.45, 0.24, 0.10), 3.0)
M_OVEN = mat("oven", (0.75, 0.76, 0.78), 0.25, 0.8)
M_OVENDK = mat("ovendk", (0.04, 0.04, 0.05), 0.3)
M_OVWIN = mat("ovwin", (0.3, 0.1, 0.02), 0.2, 0, (1.0, 0.45, 0.10), 2.2)
M_STEEL = mat("steel", (0.6, 0.6, 0.62), 0.3, 1.0)
M_GLASS = liquid("glass", (0.92, 0.97, 1.0), (0.85, 0.92, 1.0), 0.06)
M_FILL = mat("fill", (1.0, 0.15, 0.08), 0.35, 0, (1.0, 0.15, 0.06), 2.5)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.65, 0.15), 5.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.7, 1.0), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_RED = mat("red", (0.8, 0.02, 0.01), 0.4, 0, (0.9, 0.03, 0.01), 2.0)
M_FLAME = mat("flame", (1.0, 0.5, 0.05), 0.4, 0, (1.0, 0.45, 0.05), 3.0)
M_SIGN = mat("sign", (0.05, 0.05, 0.06), 0.5)
M_ARROW = mat("arrow", (0.85, 0.9, 1.0), 0.3, 0, (0.7, 0.85, 1.0), 1.6)
M_HAZE = mat("haze", (0.85, 0.45, 0.12), 0.9, 0, (0.95, 0.50, 0.15), 0.7)
M_CRUMB = mat("crumb", (0.93, 0.85, 0.66), 0.8)
M_CRUST = mat("crust", (0.62, 0.38, 0.14), 0.7)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.05, 0.06, 0.09, 1); bg.inputs[1].default_value = 1.0
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.0; sun.data.angle = math.radians(8); sun.data.color = (1.0, 0.95, 0.88)
sun.rotation_euler = (math.radians(45), 0, math.radians(-25)); S.collection.objects.link(sun)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA"))
fill.data.energy = 1100; fill.data.size = 10; fill.location = (0, -10, 6); fill.rotation_euler = (math.radians(60), 0, 0)
S.collection.objects.link(fill)
vlight = bpy.data.objects.new("vlight", bpy.data.lights.new("vlight", "AREA"))
vlight.data.energy = 260; vlight.data.size = 3; vlight.data.color = (1.0, 0.55, 0.2)
vlight.location = (1.6, -2.6, 3.2); vlight.rotation_euler = (math.radians(45), 0, math.radians(10)); S.collection.objects.link(vlight)

LX, RX, TOP = -1.4, 1.4, 0.9
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0)); link(bpy.context.object, M_PLINTH)
# backdrops: kitchen tiles (left) vs Venus orange haze (right)
box((-1.6, 1.3, 4.0), (3.2, 0.05, 8.0), M_TILE, "tilewall")
box((1.6, 1.3, 4.0), (3.2, 0.05, 8.0), M_HAZE, "hazewall")
box((LX, 0, TOP / 2), (2.0, 1.8, TOP), M_PLINTH, "lplinth")
box((RX, 0, TOP / 2), (2.0, 1.8, TOP), M_PLINTH, "rplinth")
box((RX, 0, TOP + 0.05), (2.0, 1.8, 0.1), M_VROCK, "vground")
rnd = random.Random(12)
for i in range(9):
    r = rnd.uniform(0.06, 0.16)
    o = sphere((RX + rnd.uniform(-0.9, 0.9), rnd.uniform(-0.2, 0.8), TOP + 0.1), r, M_VROCK, "rock", None, 10)
    o.scale = (1.0, 0.8, 0.5)
# oven (left)
box((LX, 0, TOP + 0.45), (1.2, 0.9, 0.9), M_OVEN, "oven")
box((LX, -0.455, TOP + 0.40), (0.86, 0.02, 0.48), M_OVENDK, "door")
box((LX, -0.47, TOP + 0.40), (0.70, 0.02, 0.34), M_OVWIN, "ovwin")
cyl_between((LX - 0.35, -0.53, TOP + 0.72), (LX + 0.35, -0.53, TOP + 0.72), 0.022, M_STEEL, None, "handle")
box((LX, -0.455, TOP + 0.83), (1.2, 0.02, 0.10), M_OVENDK, "panel")
for k in range(4):
    cyl_between((LX - 0.42 + 0.28 * k, -0.46, TOP + 0.83), (LX - 0.42 + 0.28 * k, -0.50, TOP + 0.83), 0.035, M_STEEL, None, "knob", caps=False)
SIGNS = [box((LX + 0.15, -1.2, 0.6), (1.5, 0.04, 0.38), M_SIGN, "lsign"), box((RX - 0.15, -1.2, 0.6), (1.5, 0.04, 0.38), M_SIGN, "rsign"),
         text("YOUR OVEN", (LX + 0.15, -1.25, 0.6), TR, 0.21, M_LBLB), text("VENUS", (RX - 0.15, -1.25, 0.6), TR, 0.26, M_LBL)]

# toast stand + bread slice (Venus side)
BZ0 = TOP + 0.10
cyl_between((RX, 0.0, BZ0), (RX, 0.0, BZ0 + 0.30), 0.025, M_STEEL, None, "rod")
cyl_between((RX - 0.2, 0.0, BZ0 + 0.30), (RX + 0.2, 0.0, BZ0 + 0.30), 0.02, M_STEEL, None, "fork")
for dx in (-0.2, 0.2): cyl_between((RX + dx, 0, BZ0 + 0.30), (RX + dx, 0, BZ0 + 0.46), 0.015, M_STEEL, None, "prong", caps=False)
bread = empty("bread")
crust = box((0, 0.006, 0.28), (0.58, 0.07, 0.56), M_CRUST, "crustb", bread)
crumb = box((0, -0.004, 0.28), (0.52, 0.068, 0.50), M_CRUMB, "crumbb", bread)
for dx in (-0.14, 0.14):
    o = sphere((dx, 0.006, 0.56), 1.0, M_CRUST, "lobe", bread, 20); o.scale = (0.17, 0.035, 0.12)
    o = sphere((dx, -0.004, 0.55), 1.0, M_CRUMB, "lobec", bread, 20); o.scale = (0.15, 0.034, 0.105)
for o in list(bread.children):
    bv = o.modifiers.new("bv", "BEVEL") if o.name.startswith(("crust", "crumb")) else None
    if bv: bv.width = 0.02; bv.segments = 2
BREAD_REST = V((RX, 0.0, BZ0 + 0.31))

# thermometers above each set (0-500 C over 1.9 m)
TZ0 = 2.15; TH = 1.9; TMAX = 500.0
THERMO_OBJ = []
def thermo(cx):
    g = cyl_between((cx, 0, TZ0), (cx, 0, TZ0 + TH + 0.06), 0.085, M_GLASS, None, "tube", caps=False); noshadow(g)
    THERMO_OBJ.append(g); THERMO_OBJ.append(sphere((cx, 0, TZ0 - 0.05), 0.15, M_FILL, "bulb", None, 20))
    f_ = box((0, 0, 0.5), (0.09, 0.09, 1.0), M_FILL, "tfill")
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR"); f_.location = (cx, 0, TZ0)
    return f_
FL = thermo(LX); FR = thermo(RX)
VAL_L = text("0 °C", (LX + 0.22, -0.05, TZ0), TR, 0.26, M_WHITE, align="LEFT")
VAL_R = text("0 °C", (RX - 0.2, -0.05, TZ0), TR, 0.26, M_LBL, align="RIGHT")
for o in (VAL_L, VAL_R): o.visible_shadow = False
OVLINE = box((0, -0.06, 0), (4.0, 0.01, 0.018), M_WHITE, "ovline"); OVLINE.location = (0, -0.06, TZ0 + TH * 260 / TMAX)
OVLINE_T = text("OVEN MAX", (0.0, -0.08, TZ0 + TH * 260 / TMAX - 0.14), TR, 0.16, M_WHITE)
X2 = text("≈1.8×", (0.0, -0.06, TZ0 + TH * 0.84), TR, 0.30, M_LBL)

# pressure arrows around the bread (line 4)
ARROWS = []
BC = BREAD_REST + V((0, 0, 0.32))
for k in range(10):
    a = 2 * math.pi * k / 10
    d = V((math.cos(a), 0, math.sin(a)))
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.07, radius2=0, depth=0.22, location=(0, 0, 0))
    c_ = bpy.context.object; link(c_, M_ARROW); c_.rotation_mode = "QUATERNION"; c_.rotation_quaternion = (-d).to_track_quat("Z", "Y")
    ARROWS.append((c_, d))
for k in range(4):   # front/back arrows (seen at an angle)
    pass
P_LBL = text("92 BAR", (RX + 0.52, -0.3, BC.z + 0.56), TR, 0.12, M_ARROW)
CH_LBL = text("CHARCOAL", (RX, -0.25, BC.z + 0.50), TR, 0.12, M_LBL)
# twist: crossed-out flame + NO OXYGEN
flame = empty("flame", (RX + 0.52, -0.25, BC.z + 0.05))
bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.11, radius2=0, depth=0.32, location=(0, 0, 0.14)); link(bpy.context.object, M_FLAME, flame)
sphere((0, 0, 0.0), 0.11, M_FLAME, "fball", flame, 16)
for s_ in (1, -1):
    xb = box((0, -0.15, 0.06), (0.5, 0.02, 0.05), M_RED, "xbar", flame); xb.rotation_euler = (0, math.radians(45 * s_), 0)
NO_LBL = text("NO OXYGEN", (RX + 0.5, -0.3, BC.z - 0.24), TR, 0.095, M_WHITE)
CO2_LBL = text("96.5% CO₂", (RX - 0.52, -0.3, BC.z - 0.24), TR, 0.085, M_LBL)

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
W5 = {w["w"].strip(".,"): w["t"] for w in L[5]["words"]}
T_CHAR = W5.get("charcoal", t5 + 1.5)
T_LOOP = tc + 0.25
def mode_of(t):
    if t < t2: return "hook"
    if t < t3: return "bread"
    if t < t4: return "thermo"
    if t < t5: return "press"
    if t < t6: return "char"
    if t < t7: return "weird"
    if t < T_LOOP: return "noflame"
    return "loop"

def temps(t):
    kl = smooth((t - 0.15) / 1.4); return 260 * kl, 464 * kl
def labels(scene, *a):
    t = scene.frame_current / FPS
    l, r = temps(t) if t < t2 else (260, 464)
    VAL_L.data.body = f"{int(round(l))} °C"; VAL_R.data.body = f"{int(round(r))} °C"
bpy.app.handlers.frame_change_pre.append(labels)

C0 = (0.93, 0.85, 0.66); C1 = (0.80, 0.55, 0.22); C2 = (0.30, 0.15, 0.05); C3 = (0.025, 0.022, 0.02)
K0 = (0.62, 0.38, 0.14); K3 = (0.015, 0.013, 0.012)
def lerp3(a, b, u): return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))
def char_col(u):
    if u < 0.33: return lerp3(C0, C1, u / 0.33)
    if u < 0.66: return lerp3(C1, C2, (u - 0.33) / 0.33)
    return lerp3(C2, C3, (u - 0.66) / 0.34)
bc_crumb = M_CRUMB.node_tree.nodes["Principled BSDF"].inputs["Base Color"]
bc_crust = M_CRUST.node_tree.nodes["Principled BSDF"].inputs["Base Color"]
for f in range(0, N + 1):
    t = f / FPS; m = mode_of(t)
    # bread: off-screen above during hook, lowers onto the stand on line 2
    if m == "hook": pos = BREAD_REST + V((0, 0, 30))
    elif m == "bread": pos = BREAD_REST + V((0, 0, 1.4 * (1 - smooth((t - t2) / 0.7))))
    else: pos = BREAD_REST
    bread.location = pos; bread.keyframe_insert("location", frame=f)
    # charring: starts on line 5, black by "charcoal"
    if t < t5: u = 0
    else: u = smooth((t - t5) / max(T_CHAR - t5 + 0.1, 0.3))
    bc_crumb.default_value = (*char_col(u), 1); bc_crumb.keyframe_insert("default_value", frame=f)
    bc_crust.default_value = (*lerp3(K0, K3, u), 1); bc_crust.keyframe_insert("default_value", frame=f)
    bread.scale = (1 - 0.06 * u, 1, 1 - 0.07 * u); bread.keyframe_insert("scale", frame=f)
    # thermometers
    l, r = temps(t) if t < t2 else (260, 464)
    FL.scale = (1, 1, max(TH * l / TMAX, 0.001)); FL.keyframe_insert("scale", frame=f)
    FR.scale = (1, 1, max(TH * r / TMAX, 0.001)); FR.keyframe_insert("scale", frame=f)
    VAL_L.location = (LX + 0.17, -0.05, TZ0 + TH * l / TMAX + 0.18); VAL_L.keyframe_insert("location", frame=f)
    VAL_R.location = (RX - 0.17, -0.05, TZ0 + TH * r / TMAX + 0.18); VAL_R.keyframe_insert("location", frame=f)
    on_th = m in ("hook", "thermo", "loop")
    for o in THERMO_OBJ: vis(o, on_th, f)
    for o in SIGNS: vis(o, m in ("hook", "loop", "thermo"), f)
    if not on_th:
        FL.scale = FR.scale = (0.0001,) * 3; FL.keyframe_insert("scale", frame=f); FR.keyframe_insert("scale", frame=f)
    for o in (VAL_L, VAL_R): vis(o, on_th, f)
    vis(OVLINE, m == "thermo" and t > t3 + 0.3, f); vis(OVLINE_T, m == "thermo" and t > t3 + 0.3, f)
    vis(X2, m == "thermo" and t > t3 + 0.7, f)
    # pressure arrows
    for (c_, d) in ARROWS:
        if m == "press":
            k = smooth((t - t4 - 0.1) / 0.5); pulse = 0.04 * math.sin(t * 9)
            c_.location = BC + d * (0.80 - 0.22 * k + pulse)
            c_.scale = (1, 1, 1)
        else:
            c_.location = BC + d * 0.9; c_.scale = (0.0001,) * 3
        c_.keyframe_insert("location", frame=f); c_.keyframe_insert("scale", frame=f)
    vis(P_LBL, m == "press" and t > t4 + 0.4, f)
    vis(CH_LBL, (m == "char" and t > T_CHAR - 0.05) or m == "weird", f)
    vis(flame, m == "noflame", f); vis(NO_LBL, m == "noflame" and t > t7 + 0.4, f); vis(CO2_LBL, m == "noflame" and t > t7 + 0.8, f)
    # oven window flicker a little
    vl = 260 + 40 * smooth((t - 0.1) / 1.2)
    vlight.data.energy = vl; vlight.data.keyframe_insert("energy", frame=f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return ("lerp", V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -9.6, 2.5), (0.0, 0, 2.05), (0.0, -9.1, 2.45), (0.0, 0, 2.05))
BZC = BC.z
SEG = [
    (0.0, t2 - 0.05, HOOK, 25, 26),
    (t2 - 0.05, t3 - 0.05, fixed((RX + 0.3, -4.6, BZC + 0.35), (RX, 0, BZC - 0.05), (RX + 0.2, -4.2, BZC + 0.3), (RX, 0, BZC - 0.05)), 30, 30),
    (t3 - 0.05, t4 - 0.05, fixed((0.0, -9.4, TZ0 + 0.9), (0.0, 0, TZ0 + 0.55), (0.0, -8.9, TZ0 + 0.9), (0.0, 0, TZ0 + 0.55)), 26, 26),
    (t4 - 0.05, t5 - 0.05, fixed((RX + 0.2, -4.4, BZC + 0.35), (RX, 0, BZC + 0.05), (RX + 0.1, -4.0, BZC + 0.3), (RX, 0, BZC + 0.05)), 30, 30),
    (t5 - 0.05, t6 - 0.05, fixed((RX + 0.3, -4.8, BZC + 0.35), (RX, 0, BZC + 0.15), (RX + 0.2, -4.3, BZC + 0.3), (RX, 0, BZC + 0.15)), 30, 30),
    (t6 - 0.05, t7 - 0.05, fixed((RX + 0.15, -3.6, BZC + 0.25), (RX, 0, BZC + 0.12), (RX + 0.1, -3.2, BZC + 0.22), (RX, 0, BZC + 0.12)), 31, 32),
    (t7 - 0.05, T_LOOP, fixed((RX + 0.1, -4.6, BZC + 0.3), (RX, 0, BZC - 0.05), (RX + 0.05, -4.3, BZC + 0.3), (RX, 0, BZC - 0.05)), 30, 30),
    (T_LOOP, DUR + 0.01, HOOK, 25, 24.5),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0])); spec = seg[2]
    _, pa, ta, pb, tb = spec; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_char": T_CHAR, "t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]],
           "venus_c": 464, "oven_max_c": 260}, open("/home/claude/reel/beats.json", "w"), indent=1)

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
