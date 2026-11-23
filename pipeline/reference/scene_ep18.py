"""The Impossible Lab #18 - a glass of water on the Moon (E17 cascade middle).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(18)
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



# ================= episode 18: a glass of water on the Moon =================
# Hook (x = 0): EARTH glass (left, calm) vs MOON glass (right, black starry wall): from 0.08 s the Moon glass boils
# violently and an ice crust spreads over it by ~1.2 s. Line 2: Moon surface set (x = 30), the glass is set down on a
# small table and starts boiling on contact. Line 3: air dots vanish; the mug of tea next to it erupts (cascade 1).
# Line 4: thermometer reads 20 C while boiling; the bowl of soup erupts (2), then the flower vase (3). Line 5: ice
# crusts form one after another (glass, mug, bowl, vase) while the thermometer drops to 0 C. Line 6: the ice shrinks
# and steams away (sublimation). Line 7: dark polar crater (x = 60) with ice glinting in its shadow, -238 C.
# Last ~1 s: hook framing (loop).
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

M_TABLE = noise_mat("table", (0.55, 0.36, 0.22), (0.66, 0.45, 0.28), 7.0, 0.45)
M_WALLE = tiles("wallE", (0.20, 0.30, 0.40), (0.12, 0.16, 0.20), 4.0)
M_SPACE = mat("space", (0.01, 0.01, 0.015), 0.8)
M_STAR = mat("star", (1, 1, 1), 0.5, 0, (1, 1, 1), 6.0)
M_GLASS = liquid("glass", (0.97, 0.99, 1.0), (0.92, 0.96, 1.0), 0.02)
M_WATER = liquid("water", (0.12, 0.45, 0.95), (0.45, 0.72, 1.0), 0.10)
M_TEA = mat("tea", (0.30, 0.14, 0.05), 0.12)
M_SOUP = mat("soup", (0.85, 0.42, 0.10), 0.2)
M_MUG = mat("mug", (0.90, 0.25, 0.22), 0.35)
M_BOWL = mat("bowl", (0.92, 0.92, 0.88), 0.3)
M_ICE = mat("ice", (0.95, 0.98, 1.0), 0.5, 0, (0.85, 0.94, 1.0), 1.6)
M_BUB = mat("bub", (1, 1, 1), 0.2, 0, (0.9, 0.97, 1.0), 1.2)
M_STEAM = mat("steam", (0.9, 0.92, 0.95), 0.9, 0, (0.85, 0.9, 0.95), 0.5)
M_GROUND = noise_mat("moonground", (0.30, 0.30, 0.31), (0.55, 0.55, 0.56), 2.5, 0.95)
M_ROCK = noise_mat("rock", (0.20, 0.20, 0.21), (0.38, 0.38, 0.40), 6.0, 0.9)
M_EARTH = noise_mat("earthp", (0.10, 0.30, 0.75), (0.85, 0.90, 0.95), 4.0, 0.6)
M_STEM = mat("stem", (0.15, 0.55, 0.15), 0.5)
M_PETAL = mat("petal", (0.95, 0.80, 0.10), 0.5)
M_AIR = mat("air", (0.6, 0.85, 1.0), 0.4, 0, (0.55, 0.85, 1.0), 3.0)
M_LBLB = mat("lblb", (0.4, 0.7, 1.0), 0.4, 0, (0.4, 0.75, 1.0), 5.0)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_ICEL = mat("icel", (0.6, 0.9, 1.0), 0.4, 0, (0.6, 0.9, 1.0), 4.0)
M_RED = mat("red", (1.0, 0.2, 0.1), 0.4, 0, (1.0, 0.18, 0.06), 4.0)
M_DARK = mat("dark", (0.04, 0.04, 0.05), 0.5)
M_ICEPATCH = mat("icepatch", (0.8, 0.92, 1.0), 0.15, 0, (0.55, 0.8, 1.0), 1.2)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.5
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.01, 0.012, 0.02, 1); WBG.inputs[1].default_value = 1.0

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
T_HB = 0.08                 # hook: Moon glass starts boiling
T_HF = 0.45                 # hook: ice crust starts spreading
T_SET = t2 + 0.55           # glass touches the Moon table, boiling starts
T_THIN = t3 + 0.45          # air dots vanish
T_MUG = t3 + 1.25           # cascade 1: tea erupts
T_BOWL = t4 + 0.55          # cascade 2: soup erupts
T_VASE = t4 + 1.5           # cascade 3: flower vase erupts
T_FR = [t5 + 0.25, t5 + 0.70, t5 + 1.15, t5 + 1.55]   # ice crusts: glass, mug, bowl, vase
T_SUB = t6 + 0.15           # ice starts steaming away
T_ICEP = t7 + 0.6           # crater ice glints + label

# ---------- vessels ----------
VES = []
def vessel(kind, x, y, z0, boil_t, freeze_t, scale=1.0, hook=False):
    """returns dict with liquid, ice, bubbles, steam; z0 = table top"""
    d = dict(kind=kind, x=x, y=y, z0=z0, bt=boil_t, ft=freeze_t, bub=[], steam=[], drops=[], hook=hook)
    if kind in ("glass", "vase"):
        r, h, fill = (0.055 * scale, 0.15 * scale, 0.78) if kind == "glass" else (0.04, 0.24, 0.72)
        open_cyl((x, y, z0 + h / 2), r, h, M_GLASS, kind, 0.004)
        cyl((x, y, z0 + 0.004), r, 0.008, M_GLASS, kind + "base")
        lq = noshadow(cyl((x, y, z0 + 0.008 + fill * h / 2), r - 0.005, fill * h, M_WATER, kind + "water"))
        lq.visible_glossy = False
        surf = z0 + 0.008 + fill * h; rin = r - 0.005; bottom = z0 + 0.012
        if kind == "vase":
            cyl_between((x, y, z0 + 0.03), (x + 0.01, y, z0 + 0.36), 0.004, M_STEM, None, "stem", caps=False)
            for k in range(6):
                a = k / 6 * math.tau
                sphere((x + 0.01 + math.cos(a) * 0.025, y + math.sin(a) * 0.012, z0 + 0.37 + math.sin(a) * 0.02), 0.018, M_PETAL, "petal", None, 10)
            sphere((x + 0.01, y - 0.01, z0 + 0.37), 0.014, M_SOUP, "centre", None, 10)
    elif kind == "mug":
        r, h = 0.045, 0.10
        open_cyl((x, y, z0 + h / 2), r, h, M_MUG, "mug", 0.006)
        cyl((x, y, z0 + 0.004), r, 0.008, M_MUG, "mugbase")
        bpy.ops.mesh.primitive_torus_add(major_radius=0.028, minor_radius=0.007, location=(x + r + 0.012, y, z0 + 0.055), rotation=(math.radians(90), 0, 0))
        link(bpy.context.object, M_MUG)
        lq = cyl((x, y, z0 + h - 0.016), r - 0.006, 0.006, M_TEA, "tea"); surf = z0 + h - 0.013; rin = r - 0.006; bottom = None
    else:  # bowl
        r = 0.085
        bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=r, location=(x, y, z0 + r * 0.95))
        o = bpy.context.object; bpy.ops.object.shade_smooth()
        bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.bisect(plane_co=(x, y, z0 + r * 0.95), plane_no=(0, 0, 1), clear_outer=True)
        bpy.ops.object.mode_set(mode="OBJECT"); o.modifiers.new("s", "SOLIDIFY").thickness = 0.006; link(o, M_BOWL)
        lq = cyl((x, y, z0 + r * 0.95 - 0.012), r * 0.93, 0.006, M_SOUP, "soup"); surf = z0 + r * 0.95 - 0.009; rin = r * 0.92; bottom = None
    d.update(lq=lq, surf=surf, rin=rin, bottom=bottom)
    ice = cyl((x, y, surf + 0.002), rin, 0.010, M_ICE, kind + "ice"); ice.scale = (0.0001,) * 3; d["ice"] = ice
    rnd = random.Random(int(x * 1000) + 7)
    nb = 22 if bottom is not None else 0
    for k in range(nb):
        o = noshadow(sphere((x, y, surf), 1, M_BUB, "bub", None, 8))
        d["bub"].append((o, rnd.uniform(-0.8, 0.8) * rin, rnd.uniform(-0.8, 0.8) * rin, rnd.random(), rnd.uniform(1.5, 3.0), rnd.uniform(0.004, 0.009)))
    for k in range(10):   # surface blips / droplets
        o = noshadow(sphere((x, y, surf), 1, M_BUB if bottom is not None else (M_TEA if kind == "mug" else M_SOUP), "drop", None, 8))
        d["drops"].append((o, rnd.uniform(-0.8, 0.8) * rin, rnd.uniform(-0.8, 0.8) * rin, rnd.random(), rnd.uniform(2.0, 3.5), rnd.uniform(0.004, 0.008)))
    for k in range(8):
        o = noshadow(sphere((x, y, surf), 1, M_STEAM, "steam", None, 10))
        d["steam"].append((o, rnd.uniform(-0.5, 0.5) * rin, rnd.uniform(-0.3, 0.3) * rin, rnd.random(), rnd.uniform(0.6, 1.0)))
    VES.append(d)
    return d

# ================= HOOK set (x = 0) =================
TOP = 0.90
LX, RX = -0.20, 0.20
box((0, 0, TOP / 2), (2.6, 1.0, TOP), M_TABLE, "counter")
box((-1.0, 0.6, 1.8), (2.0, 0.1, 3.6), M_WALLE, "wallE")
box((1.0, 0.6, 1.8), (2.0, 0.1, 3.6), M_SPACE, "wallM")
rs = random.Random(3)
for k in range(70):
    sphere((rs.uniform(0.03, 1.4), 0.54, rs.uniform(0.95, 2.2)), rs.uniform(0.002, 0.005), M_STAR, "star", None, 6)
HE = vessel("glass", LX, 0.0, TOP, 99, 99, 1.5, hook=True)
HM = vessel("glass", RX, 0.0, TOP, T_HB, T_HF, 1.5, hook=True)
label("EARTH", (LX, 0.5, 1.36), 0.10, M_LBLB); label("AIR: 1 BAR", (LX, 0.5, 1.27), 0.06, M_WHITE)
label("MOON", (RX, 0.5, 1.36), 0.10, M_WHITE); label("AIR: ≈ 0", (RX, 0.5, 1.27), 0.06, M_WHITE)
H_E = label("CALM", (LX, -0.1, TOP + 0.30), 0.05, M_LBLB)
H_M = label("BOILS + FREEZES", (RX - 0.03, -0.1, TOP + 0.30), 0.034, M_ICEL)
kl = bpy.data.objects.new("kitchen", bpy.data.lights.new("kitchen", "AREA")); kl.data.energy = 380; kl.data.size = 3
kl.data.color = (1.0, 0.92, 0.8); kl.location = (-1.0, -2.8, 3.0); kl.rotation_euler = (math.radians(45), 0, math.radians(-20)); S.collection.objects.link(kl)
kl2 = bpy.data.objects.new("kitchen2", bpy.data.lights.new("kitchen2", "AREA")); kl2.data.energy = 240; kl2.data.size = 2.5
kl2.data.color = (0.95, 0.95, 1.0); kl2.location = (1.4, -2.6, 2.4); kl2.rotation_euler = (math.radians(50), 0, math.radians(25)); S.collection.objects.link(kl2)

# ================= MOON surface set (x = 30) =================
MX = 30.0; MT = 0.55
bpy.ops.mesh.primitive_plane_add(size=120, location=(MX, 30, 0)); link(bpy.context.object, M_GROUND)
rr = random.Random(9)
for k in range(30):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rr.uniform(0.04, 0.3), location=(MX + rr.uniform(-5, 5), rr.uniform(0.8, 12), 0))
    o = bpy.context.object; o.scale = (1, rr.uniform(0.7, 1.2), rr.uniform(0.3, 0.6)); link(o, M_ROCK)
for (dx, dy, r) in ((-3, 9, 1.4), (4, 14, 2.2), (-6, 20, 3.0), (1.5, 5, 0.6)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=r * 0.18, location=(MX + dx, dy, 0)); o = bpy.context.object
    o.scale = (1, 1, 0.35); link(o, M_GROUND)
for k in range(140):
    a = rr.uniform(0, math.tau)
    sphere((MX + rr.uniform(-40, 40), 60, rr.uniform(3, 30)), rr.uniform(0.04, 0.1), M_STAR, "star", None, 6)
sphere((MX - 2.2, 40, 6.2), 1.6, M_EARTH, "earth", None, 32)
box((MX, 0, MT - 0.02), (0.95, 0.42, 0.04), M_TABLE, "mtable_top")
for (dx, dy) in ((-0.42, -0.16), (0.42, -0.16), (-0.42, 0.16), (0.42, 0.16)):
    box((MX + dx, dy, (MT - 0.04) / 2), (0.03, 0.03, MT - 0.04), M_DARK, "leg")
GX_ = MX + 0.02
MUGX, BOWLX, VASEX = MX - 0.20, MX + 0.23, MX + 0.40
GM = vessel("glass", GX_, 0.0, MT, T_SET, T_FR[0], 1.0)
MG = vessel("mug", MUGX, 0.02, MT, T_MUG, T_FR[1])
BW = vessel("bowl", BOWLX, 0.03, MT, T_BOWL, T_FR[2])
VS = vessel("vase", VASEX, 0.08, MT, T_VASE, T_FR[3])
GLASS_PARTS = [o for o in bpy.data.objects if o.name.startswith("glass") and "ice" not in o.name and "water" not in o.name and abs(o.location.x - GX_) < 0.08 and o.location.x > 20]
# thermometer left of the mug
TX = MX - 0.09
cyl((TX, 0.12, MT + 0.13), 0.010, 0.24, M_GLASS, "ttube")
sphere((TX, 0.12, MT + 0.015), 0.018, M_RED, "tbulb", None, 12)
TCOL = empty("tcol", (TX, 0.12, MT + 0.02)); cyl((0, 0, 0.11), 0.005, 0.22, M_RED, "tred", parent=TCOL)
TT = label("", (TX, 0.10, MT + 0.31), 0.055, M_WHITE)
AIR = []
rnd = random.Random(21)
for k in range(40):
    o = noshadow(sphere((MX + rnd.uniform(-0.45, 0.45), -0.08 + rnd.uniform(-0.1, 0.1), MT + 0.12 + rnd.uniform(0, 0.35)), 0.012, M_AIR, "air", None, 8))
    AIR.append((o, V(o.location), rnd.uniform(0, math.tau), k != 13))
AIR_T = label("", (MX, -0.15, MT + 0.47), 0.045, M_LBLB)
sun = bpy.data.objects.new("msun", bpy.data.lights.new("msun", "SUN")); sun.data.energy = 4.0
sun.data.color = (1.0, 0.97, 0.92); sun.rotation_euler = (math.radians(55), 0, math.radians(-40)); S.collection.objects.link(sun)

# ================= polar crater set (x = 90) =================
CX = 90.0
bpy.ops.mesh.primitive_plane_add(size=80, location=(CX, 10, 0)); link(bpy.context.object, M_GROUND)
bpy.ops.mesh.primitive_torus_add(major_radius=2.2, minor_radius=0.55, location=(CX, 3.0, 0), major_segments=64, minor_segments=16)
o = bpy.context.object; o.scale = (1, 1, 0.9); link(o, M_GROUND)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.0, depth=0.02, location=(CX, 3.0, 0.005)); link(bpy.context.object, M_ROCK)
ICEP = []
ri = random.Random(31)
for k in range(28):
    a = ri.uniform(0, math.tau); rad = 1.6 * math.sqrt(ri.random())
    p = (CX + math.cos(a) * rad, 3.0 + math.sin(a) * rad * 0.9, 0.02)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=ri.uniform(0.06, 0.16), location=p)
    o = bpy.context.object; o.scale = (1, ri.uniform(0.6, 1.0), 0.25); link(o, M_ICEPATCH); ICEP.append((o, V(o.scale), ri.uniform(0, 6)))
CR_T = label("-238 °C", (CX, 2.2, 0.95), 0.32, M_ICEL)
CR_T2 = label("ICE SURVIVES HERE", (CX, 1.6, 0.62), 0.22, M_ICEL)
csun = bpy.data.objects.new("csun", bpy.data.lights.new("csun", "SUN")); csun.data.energy = 4.0
csun.data.color = (1.0, 0.97, 0.92); csun.rotation_euler = (math.radians(84), 0, math.radians(-60)); S.collection.objects.link(csun)
# keep the two suns apart: the crater sun only lights the crater shot (hide others by distance isn't possible) -> animate energy
for f, e1, e2 in ((0, 4.0, 0.0),):
    pass

# ---------- text handler ----------
def temp_at(t):
    if t < T_FR[0] - 0.2: return 20.0
    return max(0.0, 20.0 - 20.0 * smooth((t - (T_FR[0] - 0.2)) / 1.2))
def handler(scene, *a):
    t = scene.frame_current / FPS
    AIR_T.data.body = "AIR: EARTH" if t < T_THIN else "AIR: MOON (≈ 0)"
    TT.data.body = f"{temp_at(t):.0f} °C"
bpy.app.handlers.frame_change_pre.append(handler)

# ---------- animation ----------
def boil_level(d, t):
    if t < d["bt"]: return 0.0
    up = smooth((t - d["bt"]) / 0.2)
    down = 1.0 - smooth((t - d["ft"]) / 0.35) if t >= d["ft"] else 1.0
    return up * down
def frz(d, t): return smooth((t - d["ft"]) / 0.45) if t >= d["ft"] else 0.0
for o in GLASS_PARTS: o["base0"] = o.location.z
for f in range(0, N + 1):
    t = f / FPS
    DZ = 0.25 * (1 - smooth((t - t2) / 0.55)) if t < T_SET else 0.0
    # hook loop: Moon glass replays the boil-and-freeze after T_LOOP
    for d in VES:
        tt = t
        if d["hook"] and t >= T_LOOP: tt = t - T_LOOP
        b = boil_level(d, tt); fz = frz(d, tt)
        # sublimation (Moon set only): ice thins and the level drops
        sub = smooth((t - T_SUB) / 1.4) if (not d["hook"] and t >= T_SUB) else 0.0
        x, y, surf, rin = d["x"], d["y"], d["surf"], d["rin"]
        if d["bottom"] is not None:
            for (o, ox, oy, ph, rate, r) in d["bub"]:
                if b > 0.02:
                    u = (tt * rate + ph) % 1.0
                    o.location = (x + ox * (1 - 0.2 * u), y + oy, d["bottom"] + (surf - d["bottom"]) * u)
                    s = r * (0.5 + 0.8 * u) * b
                else:
                    o.location = (x, y, surf); s = 0.0001
                o.scale = (max(s, 0.0001),) * 3; o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
        for (o, ox, oy, ph, rate, r) in d["drops"]:
            if b > 0.02:
                u = (tt * rate + ph) % 1.0
                hgt = (0.05 if d["bottom"] is not None else 0.035) * math.sin(u * math.pi) * (0.6 + 0.4 * b)
                o.location = (x + ox, y + oy, surf + 0.003 + hgt); s = r * b
            else:
                o.location = (x, y, surf); s = 0.0001
            o.scale = (max(s, 0.0001),) * 3; o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
        steam_on = max(b, 0.7 * sub * (1 - smooth((t - T_SUB - 2.5) / 0.5)) if not d["hook"] else 0)
        for (o, ox, oy, ph, rate) in d["steam"]:
            if steam_on > 0.02:
                u = (tt * rate + ph) % 1.0
                o.location = (x + ox + 0.02 * math.sin(tt * 3 + ph * 6), y + oy, surf + 0.02 + (0.11 if d["hook"] else 0.22) * u)
                s = (0.012 + 0.035 * u) * steam_on * (1 - u * 0.6)
            else:
                o.location = (x, y, surf); s = 0.0001
            o.scale = (max(s, 0.0001),) * 3; o.keyframe_insert("location", frame=f); o.keyframe_insert("scale", frame=f)
        ice = d["ice"]
        if fz > 0:
            rr_ = (0.25 + 0.75 * fz) * (1 - 0.35 * sub); thick = (1 + 5.0 * fz) if d["hook"] else (1 + 2.5 * fz * (1 - 0.8 * sub))
            ice.scale = (rr_, rr_, thick)
        else:
            ice.scale = (0.0001,) * 3
        ice.location = (x, y, surf + 0.002 - (0.02 * fz if d["hook"] else 0.03 * sub * (1 if d["bottom"] is not None else 0.2)))
        ice.keyframe_insert("scale", frame=f); ice.keyframe_insert("location", frame=f)
        if d["bottom"] is not None and not d["hook"]:
            lq = d["lq"]; lvl = 1 - 0.3 * sub
            lq.scale = (1, 1, lvl); lq.location.z = d["bottom"] - 0.004 + (surf - d["bottom"] + 0.004) * lvl / 2 + (DZ if d is GM else 0.0)
            lq.keyframe_insert("scale", frame=f); lq.keyframe_insert("location", frame=f)
    # hook labels
    vis(H_E, True, f); vis(H_M, 0.55 <= t < t2 - 0.05, f)   # not at the loop: it would peek out beside the card
    # glass is set down onto the Moon table during line 2
    for o in GLASS_PARTS:
        o.location.z = o["base0"] + DZ; o.keyframe_insert("location", frame=f)
    # air dots: all but one vanish at T_THIN
    for (o, p0, ph, goes) in AIR:
        o.location = p0 + V((0.02 * math.sin(t * 7 + ph), 0, 0.02 * math.cos(t * 6 + ph * 2))); o.keyframe_insert("location", frame=f)
        s = 1.0 if not (goes and t >= T_THIN) else max(0.0001, 1 - (t - T_THIN) / 0.25)
        if t < t3 - 0.05 or t >= t4: s = 0.0001
        o.scale = (s, s, s); o.keyframe_insert("scale", frame=f)
    vis(AIR_T, t3 - 0.05 <= t < t4, f)
    TCOL.scale = (1, 1, 0.25 + 0.75 * temp_at(t) / 20.0); TCOL.keyframe_insert("scale", frame=f)
    vis(TT, t4 - 0.05 <= t < t6, f)
    # crater: ice glints
    for (o, s0, ph) in ICEP:
        g = 1 + 0.25 * math.sin(t * 5 + ph) if t >= T_ICEP else 1
        o.scale = s0 * g; o.keyframe_insert("scale", frame=f)
    vis(CR_T, t >= T_ICEP, f); vis(CR_T2, t >= T_ICEP + 0.4, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 3000; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((0.0, -1.10, 1.36), (0.0, -0.02, 1.10), (0.0, -1.04, 1.35), (0.0, -0.02, 1.10))
SEG = [
    (0.0, t2 - 0.05, HOOK, 20, 20),
    (t2 - 0.05, t3 - 0.05, fixed((MX + 0.3, -2.4, 1.05), (MX + 0.05, 0, 0.75), (MX + 0.15, -1.7, 0.95), (MX + 0.05, 0, 0.70)), 22, 24),
    (t3 - 0.05, t5 - 0.05, fixed((MX + 0.02, -1.75, 1.05), (MX + 0.02, 0, 0.72), (MX + 0.02, -1.6, 1.02), (MX + 0.02, 0, 0.72)), 24, 24),
    (t5 - 0.05, t6 - 0.05, fixed((MX + 0.02, -1.5, 1.0), (MX + 0.02, 0, 0.70), (MX + 0.02, -1.42, 0.98), (MX + 0.02, 0, 0.70)), 24, 24),
    (t6 - 0.05, t7 - 0.05, fixed((MX - 0.06, -1.05, 0.95), (MX - 0.06, 0, 0.66), (MX - 0.06, -0.95, 0.93), (MX - 0.06, 0, 0.66)), 26, 26),
    (t7 - 0.05, T_LOOP, fixed((CX, -4.2, 3.2), (CX, 3.0, 0.3), (CX, -3.6, 2.9), (CX, 3.0, 0.3)), 20, 20),
    (T_LOOP, DUR + 0.01, HOOK, 20, 20),
]
# crater sun only on in the crater shot; Moon sun off there (both are infinite lights)
for f in range(0, N + 1):
    t = f / FPS
    inc = t7 - 0.05 <= t < T_LOOP
    csun.data.energy = 4.0 if inc else 0.0; csun.data.keyframe_insert("energy", frame=f)
    sun.data.energy = 0.0 if inc else 4.0; sun.data.keyframe_insert("energy", frame=f)
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    pa, ta, pb, tb = seg[2]; p = pa.lerp(pb, u); q = ta.lerp(tb, u)
    cam.location = p; cam.keyframe_insert("location", frame=f)
    tgt.location = q; tgt.keyframe_insert("location", frame=f)
    cam.data.lens = seg[3] + (seg[4] - seg[3]) * u; cam.data.keyframe_insert("lens", frame=f)
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action:
        pass

json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "hb": T_HB, "hf": T_HF, "set": T_SET,
           "thin": T_THIN, "mug": T_MUG, "bowl": T_BOWL, "vase": T_VASE, "freeze": T_FR, "sub": T_SUB, "icep": T_ICEP},
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
