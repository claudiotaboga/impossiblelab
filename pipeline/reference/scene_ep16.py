"""The Impossible Lab #16 - boiling an egg on Everest (E13 reel 3: consequence in motion at t = 0).
Hook set (x = 0): SEA LEVEL pot + plate (left) vs EVEREST pot + plate (right); both boiled-egg halves drop onto their
plates at 0.08 s: the sea-level egg holds its shape, the Everest egg slumps and spreads (runny). Line 2: summit set
(x = 30), pot bubbling on the summit rock, camera pulls back to reveal the peak + "8,849 m". Lines 3-4: pot close-up
(x = 60): 2/3 of the air dots vanish, thermometer climbs 20 -> 70 and the pot starts boiling at 70; the 80 °C
"white sets" mark lights up. Line 5: spoon taps the Everest egg, it wobbles. Line 7: the yolk turns matte (sets) while
the white stays glossy-soft. Last ~0.8 s: back to the hook framing (loop).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(16)
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


# ================= episode 16: boiling an egg on Everest =================
import bmesh
def bsdf(m): return m.node_tree.nodes["Principled BSDF"]
def kf_input(m, name, f, v):
    i = bsdf(m).inputs[name]; i.default_value = v; i.keyframe_insert("default_value", frame=f)
def label(body, loc, size, m, align="CENTER", rot=TR):
    o = text(body, loc, rot, size, m, align); noshadow(o); o.visible_glossy = False; return o
def cyl(loc, r, d, m, name="cyl", rot=(0, 0, 0), verts=32, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def ramp(t, a, b, v0, v1):
    return v0 + (v1 - v0) * smooth((t - a) / (b - a))

M_COUNTER = noise_mat("counter", (0.78, 0.76, 0.72), (0.88, 0.86, 0.82), 9.0, 0.35)
M_WALL = tiles("wall", (0.20, 0.30, 0.38), (0.12, 0.16, 0.20), 4.0)
M_DARK = mat("dark", (0.04, 0.04, 0.05), 0.5)
M_STEEL = mat("steel", (0.75, 0.76, 0.78), 0.22, 1.0)
M_WATER = liquid("water", (0.75, 0.88, 0.95), (0.85, 0.92, 1.0), 0.18)
M_BUBBLE = mat("bubble", (0.9, 0.96, 1.0), 0.05, 0, (0.75, 0.88, 1.0), 0.7)
M_STEAM = mat("steam", (1, 1, 1), 0.5, 0, (1, 1, 1), 0.5)
M_FLAME = mat("flame", (0.2, 0.4, 1.0), 0.5, 0, (0.25, 0.5, 1.0), 6.0)
M_PLATE = mat("plate", (0.95, 0.95, 0.97), 0.25)
M_FIRMW = mat("firmwhite", (0.93, 0.92, 0.88), 0.45)
M_FIRMY = mat("firmyolk", (0.98, 0.72, 0.12), 0.7)
M_RUNW = mat("runwhite", (0.80, 0.80, 0.74), 0.06)          # soft, glossy, slightly see-through white
bsdf(M_RUNW).inputs["Transmission Weight"].default_value = 0.35
M_RUNY = mat("runyolk", (0.95, 0.42, 0.02), 0.06)            # glossy runny yolk -> sets at line 7
M_SHELL = mat("shell", (0.92, 0.80, 0.64), 0.55)
M_ROCK = noise_mat("rock", (0.20, 0.19, 0.18), (0.38, 0.36, 0.34), 5.0, 0.9)
M_SNOW = noise_mat("snow", (0.82, 0.86, 0.95), (1.0, 1.0, 1.0), 3.0, 0.6)
M_SKY = mat("sky", (0.1, 0.3, 0.7), 0.5, 0, (0.18, 0.42, 0.85), 1.0)
M_GLASS = mat("tube", (0.92, 0.94, 0.96), 0.2)
M_RED = mat("red", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 3.0)
M_AIR = mat("air", (0.6, 0.85, 1.0), 0.4, 0, (0.55, 0.85, 1.0), 3.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_LBL = mat("lbl", (1.0, 0.7, 0.2), 0.4, 0, (1.0, 0.62, 0.15), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_GREEN = mat("grn", (0.3, 1.0, 0.5), 0.4, 0, (0.3, 1.0, 0.5), 3.0)
M_DIM = mat("dim", (0.5, 0.5, 0.55), 0.4, 0, (0.5, 0.5, 0.55), 1.2)
M_DIV = mat("div", (1, 1, 1), 0.4, 0, (1, 1, 1), 2.0)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.6
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.02, 0.025, 0.04, 1); WBG.inputs[1].default_value = 1.0

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_DROP = 0.08                  # hook: both cooked eggs drop onto their plates
T_LAND = T_DROP + 0.17
T_THIN = t3 + 0.85             # 2/3 of the air dots vanish ("a third of the air pressure")
T_HEAT = t3 + 1.55             # thermometer climbs ...
T_BOIL = t3 + 2.35             # ... and the pot starts boiling at 70
T_80 = t4 + 0.35               # 80 °C "white sets" mark lights up
TAPS = [t5 + 0.25, t5 + 0.85]  # spoon taps the Everest egg: it wobbles
T_SET = t7 + 0.15              # yolk sets (glossy orange -> matte yellow)

# ---------- shared props ----------
def stove_pot(x, y, top, pr=0.16, ph=0.17, n_bub=26, seed=1, water=True):
    """stove block + steel pot with water and surface bubbles; returns (water z, bubbles, flames)"""
    rnd = random.Random(seed)
    box((x, y, top + 0.04), (0.40, 0.34, 0.08), M_DARK, "stove")
    fl = []
    for k in range(10):
        a = k / 10 * math.tau
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.02, radius2=0, depth=0.06, location=(x + math.cos(a) * 0.08, y + math.sin(a) * 0.08, top + 0.11))
        o = bpy.context.object; link(o, M_FLAME); fl.append(o)
    pb = top + 0.10
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=pr, depth=ph, location=(x, y, pb + ph / 2))
    pot = bpy.context.object; bpy.ops.object.shade_smooth(); link(pot, M_STEEL)
    sol = pot.modifiers.new("shell", "SOLIDIFY"); sol.thickness = 0.01
    bpy.ops.object.mode_set(mode="EDIT"); bm = bmesh.from_edit_mesh(pot.data)
    bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if fc.normal.z > 0.9], context="FACES"); bmesh.update_edit_mesh(pot.data)
    bpy.ops.object.mode_set(mode="OBJECT")
    for s in (-1, 1): box((x + s * (pr + 0.04), y, pb + ph - 0.03), (0.07, 0.025, 0.018), M_DARK, "handle")
    wz = pb + ph - 0.03
    if water: noshadow(cyl((x, y, wz - 0.004), pr - 0.011, 0.008, M_WATER, "water"))
    bub = []
    for k in range(n_bub):
        b = sphere((0, 0, 0), 1, M_BUBBLE, "bub", None, 10)
        r = rnd.uniform(0.0, pr * 0.8); a = rnd.uniform(0, math.tau)
        bub.append((b, x + math.cos(a) * r, y + math.sin(a) * r, rnd.uniform(0, 1), rnd.uniform(0.010, 0.024) * pr / 0.16, rnd.uniform(0.7, 1.3)))
    return wz, bub, fl
def egg_half(loc, runny, name):
    """half a peeled boiled egg, cut face up: white bowl + yolk dome. Root empty at the plate surface."""
    e = empty(name, loc)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, 0, 0))
    w = bpy.context.object; w.name = name + "_white"
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_outer=True, use_fill=True)
    bpy.ops.object.mode_set(mode="OBJECT"); bpy.ops.object.shade_smooth()
    w.scale = (0.085, 0.06, 0.055); bpy.ops.object.transform_apply(scale=True)
    w.location = (0, 0, 0.055); link(w, M_RUNW if runny else M_FIRMW, e)
    y = sphere((0.0, 0, 0.055), 0.032, M_RUNY if runny else M_FIRMY, name + "_yolk", e, 24)
    return e, w, y

# ================= HOOK set (x = 0): SEA LEVEL (left) vs EVEREST (right) =================
TOP = 0.90
LX, RX = -0.30, 0.30
box((0, 0, TOP / 2), (2.6, 1.0, TOP), M_COUNTER, "counter")
box((0, 0.6, 1.8), (4, 0.1, 3.6), M_WALL, "wall")
POTS = []
for x, sd in ((LX, 3), (RX, 4)):
    POTS.append(stove_pot(x, 0.30, TOP, seed=sd))
PLATES = []
PX = 0.2
for x in (-PX, PX):
    cyl((x, -0.22, TOP + 0.008), 0.15, 0.016, M_PLATE, "plate")
EGG_L = [egg_half((-PX - 0.06, -0.25, TOP + 0.016), False, "eL1"), egg_half((-PX + 0.065, -0.19, TOP + 0.016), False, "eL2")]
EGG_R = [egg_half((PX - 0.015, -0.22, TOP + 0.016), True, "eR1")]
HL = [label("SEA LEVEL", (LX, 0.5, 1.39), 0.06, M_LBLB), label("BOILS AT 100 °C", (LX, 0.5, 1.315), 0.04, M_WHITE)]
HR = [label("EVEREST", (RX, 0.5, 1.39), 0.06, M_LBL), label("BOILS AT ≈70 °C", (RX, 0.5, 1.315), 0.04, M_WHITE)]
LBL_FIRM = label("COOKED", (-PX, -0.08, TOP + 0.15), 0.035, M_GREEN)
LBL_RUNNY = label("RUNNY", (PX, -0.08, TOP + 0.15), 0.035, M_RED)
LBL_YOLK = label("YOLK: SET", (RX - 0.02, -0.2, TOP + 0.175), 0.028, M_GREEN)
LBL_WHITE = label("WHITE: SOFT", (RX - 0.02, -0.2, TOP + 0.14), 0.024, M_LBL)
# spoon (line 5)
SPOON = empty("spoon", (RX + 0.25, -0.2, TOP + 0.2))
cyl_between((0, 0, 0), (0.22, 0.05, 0.12), 0.006, M_STEEL, SPOON, "handle")
sp = sphere((-0.025, -0.005, -0.012), 0.03, M_STEEL, "bowl", SPOON, 16); sp.scale = (1.3, 0.9, 0.35)
STEAM = [noshadow(sphere((0, 0, 0), 0.022, M_STEAM, "steam", None, 8)) for k in range(12)]
kl = bpy.data.objects.new("kitchen", bpy.data.lights.new("kitchen", "AREA")); kl.data.energy = 420; kl.data.size = 3
kl.data.color = (1.0, 0.9, 0.75); kl.location = (-1.0, -2.8, 3.0); kl.rotation_euler = (math.radians(45), 0, math.radians(-20)); S.collection.objects.link(kl)
kl2 = bpy.data.objects.new("kitchen2", bpy.data.lights.new("kitchen2", "AREA")); kl2.data.energy = 260; kl2.data.size = 2.5
kl2.data.color = (0.85, 0.9, 1.0); kl2.location = (1.4, -2.6, 2.4); kl2.rotation_euler = (math.radians(50), 0, math.radians(25)); S.collection.objects.link(kl2)

# ================= SUMMIT set (x = 30) =================
MX = 30.0; MZ = 0.0
bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=5.0, radius2=0.55, depth=4.0, location=(MX, 0, MZ - 2.05))
peak = bpy.context.object; link(peak, M_SNOW); peak.rotation_euler = (0, 0, 0.3)
for (dx, dy, r, h) in ((-6, 6, 4.5, 4.6), (5.5, 7, 4.0, 3.8), (-2, 12, 6, 5.4), (8, 3, 3, 2.4)):
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=r, radius2=0.05, depth=h, location=(MX + dx, dy, MZ - 5.2 + h / 2))
    link(bpy.context.object, M_SNOW)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.5, location=(MX, 0, MZ - 0.09)); rk = bpy.context.object; rk.scale = (1.1, 0.9, 0.2); link(rk, M_ROCK)
WZ_M, BUB_M, FL_M = stove_pot(MX, 0, MZ - 0.005, seed=7)
box((MX, 30, 4), (80, 0.1, 30), M_SKY, "sky")
SUM_T1 = label("EVEREST SUMMIT", (MX, -0.3, MZ + 0.78), 0.075, M_LBL)
SUM_T2 = label("8,849 m", (MX, -0.3, MZ + 0.66), 0.07, M_WHITE)
sun = bpy.data.objects.new("msun", bpy.data.lights.new("msun", "AREA")); sun.data.energy = 9000; sun.data.size = 6
sun.data.color = (1.0, 0.95, 0.85); sun.location = (MX - 5, -9, 7); sun.rotation_euler = (math.radians(55), 0, math.radians(-30)); S.collection.objects.link(sun)
sl2 = bpy.data.objects.new("mpot", bpy.data.lights.new("mpot", "AREA")); sl2.data.energy = 120; sl2.data.size = 1.5
sl2.location = (MX + 0.8, -1.6, 1.4); sl2.rotation_euler = (math.radians(55), 0, math.radians(30)); S.collection.objects.link(sl2)

# ================= POT close-up set (x = 60): air dots + thermometer + egg in the water =================
CX = 60.0; CT = 0.6
box((CX, 0, CT / 2), (2.4, 1.2, CT), M_COUNTER, "counter2")
box((CX, 0.7, 1.6), (4, 0.1, 3.2), M_WALL, "wall2")
WZ_C, BUB_C, FL_C = stove_pot(CX - 0.12, 0, CT, pr=0.2, ph=0.2, n_bub=34, seed=11)
EGG_IN = sphere((CX - 0.12, 0.02, WZ_C - 0.012), 1, M_SHELL, "egg_in", None, 24); EGG_IN.scale = (0.055, 0.042, 0.042)
# air dots above the pot: 36, of which 24 vanish at T_THIN (a third remain)
AIR = []
rnd = random.Random(21)
for k in range(36):
    o = noshadow(sphere((CX - 0.12 + rnd.uniform(-0.26, 0.26), -0.05 + rnd.uniform(-0.1, 0.1), CT + 0.40 + rnd.uniform(0, 0.25)), 0.014, M_AIR, "air", None, 8))
    AIR.append((o, V(o.location), rnd.uniform(0, math.tau), k % 3 != 0))
AIR_T = label("", (CX - 0.12, -0.15, CT + 0.675), 0.045, M_LBLB)
# thermometer right of the pot; marks + labels on its LEFT side (inside the frame)
TX, TY = CX + 0.24, -0.08
T0Z, TSC = CT + 0.15, 0.0055        # z of 0 °C, metres per °C  -> 100 °C at CT + 1.08
cyl((TX, TY, T0Z + 0.29), 0.02, 0.62, M_GLASS, "tube")
sphere((TX, TY, T0Z - 0.02), 0.034, M_RED, "bulb", None, 16)
COL = cyl((TX, TY, T0Z), 0.022, 1.0, M_RED, "column")
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.transform.translate(value=(0, 0, 0.5)); bpy.ops.object.mode_set(mode="OBJECT")
def mark(temp, m, txt, size=0.045):
    z = T0Z + temp * TSC
    box((TX, TY - 0.005, z), (0.07, 0.02, 0.006), m, "mark")
    return label(txt, (TX - 0.05, TY - 0.03, z), size, m, "RIGHT")
M100 = mark(100, M_DIM, "100 °C: SEA LEVEL", 0.03)
M70 = mark(70, M_LBL, "BOILS ≈70 °C", 0.032)
M80m = mat("m80", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 0.4)
M80 = mark(80, M80m, "WHITE SETS ≈80 °C", 0.03)
TEMP_T = label("", (TX + 0.035, TY - 0.03, T0Z), 0.032, M_WHITE, "LEFT")
for v in (M100, M70, M80): v.visible_glossy = False
cl = bpy.data.objects.new("cl", bpy.data.lights.new("cl", "AREA")); cl.data.energy = 300; cl.data.size = 2.5
cl.data.color = (1.0, 0.92, 0.8); cl.location = (CX - 1.0, -2.4, 2.4); cl.rotation_euler = (math.radians(50), 0, math.radians(-25)); S.collection.objects.link(cl)
cl2 = bpy.data.objects.new("cl2", bpy.data.lights.new("cl2", "AREA")); cl2.data.energy = 160; cl2.data.size = 2
cl2.data.color = (0.8, 0.88, 1.0); cl2.location = (CX + 1.3, -2.2, 1.8); cl2.rotation_euler = (math.radians(55), 0, math.radians(30)); S.collection.objects.link(cl2)

# ---------- text handler ----------
def temp_at(t):
    if t < T_HEAT: return 20
    return int(round(ramp(t, T_HEAT, T_BOIL, 20, 70)))
def handler(scene, *a):
    t = scene.frame_current / FPS
    AIR_T.data.body = "" if t >= T_HEAT - 0.1 else ("AIR: SEA LEVEL" if t < T_THIN else "AIR: ≈1/3")
    TEMP_T.data.body = f"{temp_at(t)} °C"; TEMP_T.location.z = T0Z + temp_at(t) * TSC
bpy.app.handlers.frame_change_pre.append(handler)

# ---------- animation ----------
def bubbles(bub, wz, t, on, f):
    for b, bx, by, ph, rmax, spd in bub:
        u = (t * 2.2 * spd + ph) % 1.0
        r = rmax * (0.25 + 0.95 * math.sin(u * math.pi) ** 0.6) if on else 0.0001
        b.location = (bx + 0.008 * math.sin(t * 9 + ph * 6), by, wz - 0.4 * r + 0.5 * r * u); b.scale = (r, r, r * 0.9)
        b.keyframe_insert("location", frame=f); b.keyframe_insert("scale", frame=f)
def wobble(t, taps):
    w = 0.0
    for tt in taps:
        if t >= tt: w += 0.22 * math.exp(-(t - tt) * 5) * math.sin((t - tt) * 32)
    return w

for f in range(0, N + 1):
    t = f / FPS
    # flames flicker
    for fl in POTS[0][2] + POTS[1][2] + FL_M + FL_C:
        fl.scale = (1, 1, 0.8 + 0.4 * abs(math.sin(t * 17 + fl.location.x * 13 + fl.location.y * 7))); fl.keyframe_insert("scale", frame=f)
    bubbles(POTS[0][1], POTS[0][0], t, True, f); bubbles(POTS[1][1], POTS[1][0], t, True, f)
    bubbles(BUB_M, WZ_M, t, True, f)
    bubbles(BUB_C, WZ_C, t, t >= T_BOIL or t < t3 - 0.05, f)
    # steam over both hook pots
    for k, o in enumerate(STEAM):
        ph = (t * 0.4 + k / len(STEAM) * 2) % 1.0; x = LX if k % 2 == 0 else RX
        o.location = (x + 0.04 * math.sin(6 * ph + k), 0.30, TOP + 0.27 + 0.1 * ph); o.scale = ((1 - ph) * 1.0,) * 3
        o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
    # hook: eggs drop at T_DROP; at the loop they are back in the dropped/slumped state (end frame = start state)
    if t < T_DROP: drop = 0.22
    elif t < T_LAND: drop = 0.22 * (1 - ((t - T_DROP) / (T_LAND - T_DROP)) ** 2)
    else: drop = 0.0
    for (e, w, y) in EGG_L:
        e.location.z = TOP + 0.016 + drop; e.keyframe_insert("location", frame=f)
        sq = 0.06 * math.exp(-(t - T_LAND) * 12) * math.sin((t - T_LAND) * 40) if t >= T_LAND else 0
        e.scale = (1 - sq * 0.5, 1 - sq * 0.5, 1 + sq); e.keyframe_insert("scale", frame=f)
    for (e, w, y) in EGG_R:
        e.location.z = TOP + 0.016 + drop; e.keyframe_insert("location", frame=f)
        sl = smooth((t - T_LAND) / 0.35) if t >= T_LAND else 0.0        # slumps: flattens and spreads
        wb = wobble(t, [T_LAND] + TAPS)
        sxy = 1 + 0.7 * sl + 0.12 * wb; sz = 1 - 0.6 * sl - 0.25 * wb
        e.scale = (sxy, sxy * 1.05, max(0.2, sz)); e.keyframe_insert("scale", frame=f)
        y.location = (0.015 * sl, 0, 0.055 - 0.008 * sl + 0.015 * wb); y.keyframe_insert("location", frame=f)
    # yolk sets on line 7 (until the loop): glossy orange -> matte yellow
    setk = smooth((t - T_SET) / 0.5) if T_SET <= t < T_LOOP else 0.0
    kf_input(M_RUNY, "Base Color", f, (0.95 + 0.03 * setk, 0.42 + 0.30 * setk, 0.02 + 0.10 * setk, 1))
    kf_input(M_RUNY, "Roughness", f, 0.06 + 0.64 * setk)
    vis(LBL_YOLK, False, f); vis(LBL_WHITE, False, f)
    vis(LBL_FIRM, t >= T_LAND + 0.1 and (t < t5 - 0.05 or t >= T_LOOP), f)
    vis(LBL_RUNNY, t >= T_LAND + 0.1 and (t < t5 - 0.05 or t >= T_LOOP), f)
    # spoon: hidden except line 5-6; taps the egg
    on = t5 - 0.05 <= t < t6 + 0.3
    dz = 0.12
    for tt in TAPS:
        if tt - 0.18 <= t < tt + 0.12:
            u = (t - (tt - 0.18)) / 0.3; dz = 0.12 * abs(math.cos(u * math.pi)) if u < 0.6 else 0.12 * smooth((u - 0.6) / 0.4)
    SPOON.location = (PX + 0.06, -0.24, TOP + 0.075 + dz); SPOON.keyframe_insert("location", frame=f)
    vis(SPOON, on, f)
    # close-up set: air dots jiggle; 2/3 vanish at T_THIN
    for (o, p0, ph, goes) in AIR:
        o.location = p0 + V((0.02 * math.sin(t * 7 + ph), 0, 0.02 * math.cos(t * 6 + ph * 2))); o.keyframe_insert("location", frame=f)
        s = 1.0 if not (goes and t >= T_THIN) else max(0.0001, 1 - (t - T_THIN) / 0.25)
        o.scale = (s, s, s); o.keyframe_insert("scale", frame=f)
    # thermometer
    h = temp_at(t) * TSC + (0.003 * math.sin(t * 5) if t >= T_BOIL else 0)
    COL.scale = (1, 1, max(h, 0.01)); COL.keyframe_insert("scale", frame=f)
    kf_input(M80m, "Emission Strength", f, (2.0 + 1.0 * abs(math.sin(t * 6))) if t >= T_80 else 0.4)
    # egg rocks in the boiling water
    EGG_IN.rotation_euler = (0.15 * math.sin(t * 5), 0.2 * math.sin(t * 3.7), t * 0.4 if t >= T_BOIL else 0)
    EGG_IN.keyframe_insert("rotation_euler", frame=f)
    for o in HL + HR: vis(o, True, f)
    for o in (M100, M70, M80): vis(o, not (t3 - 0.05 <= t < T_HEAT - 0.1), f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -1.22, 1.36), (0.0, -0.08, 1.04), (0.0, -1.16, 1.34), (0.0, -0.08, 1.04))
SEG = [
    (0.0, t2 - 0.05, HOOK, 20, 20),
    (t2 - 0.05, t3 - 0.05, fixed((MX, -1.5, 0.62), (MX, 0, 0.42), (MX, -3.6, 1.0), (MX, 0, 0.5)), 30, 30),
    (t3 - 0.05, T_HEAT - 0.1, fixed((CX - 0.06, -2.0, 1.25), (CX - 0.06, 0, 0.96), (CX - 0.04, -1.9, 1.25), (CX - 0.04, 0, 0.96)), 30, 30),
    (T_HEAT - 0.1, t4 - 0.05, fixed((CX + 0.04, -1.9, 1.25), (CX + 0.04, 0, 0.98), (CX + 0.08, -1.7, 1.25), (CX + 0.08, 0, 1.0)), 30, 30),
    (t4 - 0.05, t5 - 0.05, fixed((CX + 0.10, -1.6, 1.3), (CX + 0.10, 0, 1.04), (CX + 0.12, -1.5, 1.32), (CX + 0.12, 0, 1.04)), 30, 30),
    (t5 - 0.05, t6 - 0.05, fixed((PX, -0.56, 1.40), (PX, -0.21, 0.975), (PX, -0.52, 1.36), (PX, -0.21, 0.975)), 30, 30),
    (t6 - 0.05, T_LOOP, fixed((PX - 0.01, -0.47, 1.34), (PX - 0.01, -0.215, 0.97), (PX - 0.01, -0.44, 1.30), (PX - 0.01, -0.215, 0.97)), 30, 30),
    (T_LOOP, DUR + 0.01, HOOK, 20, 20),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    shk = 0.0
    for te in [T_LAND]:
        if 0 <= t - te < 0.4: shk += 0.012 * math.exp(-(t - te) * 9) * math.sin((t - te) * 70)
    cam.location = p + V((shk, 0, shk * 0.6)); cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "drop": T_DROP, "land": T_LAND,
           "thin": T_THIN, "heat": T_HEAT, "boil": T_BOIL, "w80": T_80, "taps": TAPS, "set": T_SET},
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
