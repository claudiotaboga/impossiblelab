"""The Impossible Lab #22 - every bacterium in your body on one scale (lane A, E17 cascade middle kept).
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(22)
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


# ================= episode 22: every bacterium in your body on one scale =================
# Hook: a jar of glowing green "bacteria" drops onto a balance at 0.08 s (beam slams left), an apple drops on the other
# pan at 0.40 s and the beam swings back to almost level (0.2 kg vs a ~182 g apple).
# L2: a see-through body beside the table; its gut beads stream out into the empty jar; beam goes from apple-down to level.
# L3: two stacks of discs, 1 disc = 1 trillion: BACTERIA 38 vs YOUR CELLS 30, growing together, green keeps going.
# L4: one human cell vs one bacterium (~1,000x smaller), then back to the balance: "ALL OF THEM ~200 g".
# L5: close on the body: the colon lights up. L6: back to the stacks. L7: flush: the top third of the green stack
# flies off, green drops below red -> "HUMAN CELLS AHEAD". After the card starts: hook framing (loop).
M_WOOD = noise_mat("wood", (0.50, 0.32, 0.18), (0.62, 0.42, 0.25), 7.0, 0.45)
M_FLOOR = tiles("floor", (0.78, 0.76, 0.72), (0.45, 0.43, 0.40), 1.2)
M_WALL = tiles("wall", (0.55, 0.68, 0.70), (0.85, 0.88, 0.86), 3.0)
M_CREAM = mat("cream", (0.92, 0.90, 0.84), 0.8)
M_STEEL = mat("steel", (0.80, 0.81, 0.84), 0.25, 0.9)
M_BRASS = mat("brass", (0.85, 0.62, 0.25), 0.3, 0.9)
M_GLASS = liquid("glass", (0.95, 0.98, 0.98), (0.9, 0.95, 1.0), 0.0)
M_BODY = liquid("body", (0.70, 0.86, 0.98), (0.75, 0.88, 1.0), 0.30)
M_BUG = mat("bug", (0.01, 0.38, 0.04), 0.3, 0, (0.03, 0.8, 0.08), 0.7)
M_COLON = mat("colon", (0.10, 0.55, 0.18), 0.5, 0, (0.15, 1.0, 0.3), 0.4)
M_APPLE = mat("apple", (0.62, 0.03, 0.03), 0.35)
M_STEM = mat("stem", (0.25, 0.15, 0.05), 0.8)
M_LEAF = mat("leaf", (0.15, 0.45, 0.10), 0.6)
M_GDISC = mat("gdisc", (0.10, 0.70, 0.20), 0.35, 0, (0.10, 0.9, 0.25), 0.6)
M_RDISC = mat("rdisc", (0.75, 0.08, 0.10), 0.35, 0, (0.9, 0.10, 0.12), 0.35)
M_CELL = mat("cell", (0.85, 0.35, 0.40), 0.45, 0, (0.9, 0.3, 0.35), 0.25)
M_NUC = mat("nuc", (0.35, 0.10, 0.30), 0.5)
M_NAVY = mat("navy", (0.03, 0.05, 0.10), 0.9)
M_WHITE = mat("lblw", (1, 1, 1), 0.4, 0, (1, 1, 1), 3.0)
M_AMB = mat("lbla", (1.0, 0.55, 0.08), 0.4, 0, (1.0, 0.5, 0.06), 3.0)
M_RED = mat("redl", (0.9, 0.04, 0.02), 0.4, 0, (1.0, 0.06, 0.03), 3.0)
M_GRN = mat("grnl", (0.05, 0.8, 0.15), 0.4, 0, (0.08, 1.0, 0.25), 2.4)

world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
S.view_settings.exposure = -0.5
WBG = world.node_tree.nodes["Background"]; WBG.inputs[0].default_value = (0.75, 0.78, 0.82, 1); WBG.inputs[1].default_value = 0.35

# ---------- timing ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LOOP = tc + 0.25
JAR_DROP = (0.08, 0.17)          # jar falls onto the left pan
APP_DROP = (0.40, 0.15)          # apple falls onto the right pan
STREAM = (t2 + 0.15, t3 - 0.35)  # gut beads fly into the jar
DISC = (t3 + 0.12, 0.034)        # stacks grow: start, seconds per disc
T_CELL, T_BUG, T_X = t4 + 0.05, t4 + 0.55, t4 + 1.05
T_BAL2 = t4 + 1.40               # back to the balance: "~200 g"
T_GLOW = t5 + 0.10
FLUSH = (t7 + 0.25, 0.075)       # top green discs fly off: start, seconds per disc
NG, NR, NG_END = 38, 30, 25

# ---------- kitchen + balance ----------
TOP = 0.75
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 4, 0)); fl = bpy.context.object; fl.scale = (40, 40, 1); link(fl, M_FLOOR)
box((-0.3, 0.75, 2.5), (5.0, 0.06, 5.0), M_WALL, "wall")
box((1.5, 0.70, 0.45), (1.4, 0.06, 0.9), M_CREAM, "cupboard")
box((0, 0, TOP - 0.0175), (1.0, 0.6, 0.035), M_WOOD, "top")
for sx in (-1, 1):
    for sy in (-1, 1):
        cyl((sx * 0.45, sy * 0.25, (TOP - 0.035) / 2), 0.022, TOP - 0.035, M_WOOD, "leg", verts=12)
BX = 0.10                         # balance centre x
box((BX, 0, TOP + 0.02), (0.30, 0.14, 0.04), M_STEEL, "bbase")
cyl((BX, 0, TOP + 0.17), 0.013, 0.26, M_BRASS, "post", verts=16)
PIV = V((BX, 0, TOP + 0.30)); ARM, STR = 0.18, 0.12
sphere(PIV, 0.022, M_BRASS, "pivot")
bpy.ops.mesh.primitive_cube_add(size=1, location=PIV); BEAM = bpy.context.object; BEAM.scale = (2 * ARM + 0.04, 0.018, 0.016); link(BEAM, M_BRASS)
PANS, STRS = [], []
for k in range(2):
    PANS.append(cyl((0, 0, 0), 0.078, 0.010, M_STEEL, f"pan{k}", verts=40))
    STRS.append(cyl((0, 0, 0), 0.0035, 1.0, M_BRASS, f"str{k}", verts=8))
JAR_R, JAR_H = 0.05, 0.12
JAR = cyl((0, 0, 0), JAR_R, JAR_H, M_GLASS, "jar", verts=40)
noshadow(JAR); JAR.visible_glossy = True
bpy.ops.object.mode_set(mode="EDIT"); bm = bmesh.from_edit_mesh(JAR.data)
bmesh.ops.delete(bm, geom=[fc for fc in bm.faces if fc.normal.z > 0.9], context="FACES"); bmesh.update_edit_mesh(JAR.data)
bpy.ops.object.mode_set(mode="OBJECT")
APPLE = sphere((0, 0, 0), 0.045, M_APPLE, "apple", seg=32); APPLE.scale = (1, 1, 0.88)
STEM = cyl((0, 0, 0), 0.004, 0.03, M_STEM, "stem", verts=8)
LEAF = sphere((0, 0, 0), 0.016, M_LEAF, "leaf", seg=12); LEAF.scale = (1.4, 0.5, 0.25)
# jar beads (final positions relative to the jar's bottom centre)
JB = []
rnd = random.Random(7)
for k in range(64):
    lay = k // 9; ang = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0.0, JAR_R - 0.015)
    rel = V((rr * math.cos(ang), rr * math.sin(ang), 0.014 + lay * 0.0155 + rnd.uniform(0, 0.004)))
    JB.append((sphere((0, 0, 0), 0.0125, M_BUG, f"jb{k}", seg=10), rel))
def beam_angle(t):
    """>0 = left (jar) pan down"""
    if t >= T_LOOP or t < t2 - 0.05:
        tt = t if t < T_LOOP else 99
        if tt < sum(JAR_DROP): return 0.0
        if tt < APP_DROP[0] + APP_DROP[1]: return 0.38 * smooth((tt - sum(JAR_DROP)) / 0.12)
        d = tt - sum(APP_DROP)
        return 0.025 + 0.355 * math.exp(-d * 3.2) * math.cos(2 * math.pi * 1.25 * d)
    if t < t3 - 0.05:   # filling from the body: apple-down -> level
        fr = smooth((t - STREAM[0]) / (STREAM[1] - STREAM[0] + 0.5))
        return -0.30 + 0.325 * fr
    return 0.025
def pan_pos(k, a):
    sgn = -1 if k == 0 else 1
    end = PIV + V((sgn * ARM * math.cos(a), 0, sgn * ARM * math.sin(a)))
    return end, end - V((0, 0, STR))

# ---------- body (see-through) ----------
BXB = -0.72; BYB = 0.10
BODY = []
BODY.append(cyl_between((BXB - 0.09, BYB, 0.04), (BXB - 0.09, BYB, 0.86), 0.065, M_BODY, name="legL"))
BODY.append(cyl_between((BXB + 0.09, BYB, 0.04), (BXB + 0.09, BYB, 0.86), 0.065, M_BODY, name="legR"))
TORSO = sphere((BXB, BYB, 1.13), 0.20, M_BODY, "torso", seg=32); TORSO.scale = (1.0, 0.62, 1.55)
HEAD = sphere((BXB, BYB, 1.62), 0.11, M_BODY, "head", seg=24)
cyl_between((BXB, BYB, 1.43), (BXB, BYB, 1.52), 0.045, M_BODY, name="neck")
cyl_between((BXB - 0.22, BYB, 1.38), (BXB - 0.27, BYB, 0.88), 0.045, M_BODY, name="armL")
cyl_between((BXB + 0.22, BYB, 1.38), (BXB + 0.27, BYB, 0.88), 0.045, M_BODY, name="armR")
for o in list(S.objects):
    if o.name.startswith(("torso", "head", "neck", "arm", "leg", "Sphere")) and o.data and o.data.materials and o.data.materials[0] == M_BODY:
        noshadow(o)
GUT = V((BXB, BYB - 0.02, 0.98))
bpy.ops.mesh.primitive_torus_add(major_radius=0.10, minor_radius=0.024, location=GUT, rotation=(math.radians(90), 0, 0))
COLON = bpy.context.object; COLON.name = "colon"; bpy.ops.object.shade_smooth(); link(COLON, M_COLON)
GB = [sphere(GUT + V((0.10 * math.cos(a), -0.03, 0.10 * math.sin(a))), 0.010, M_BUG, f"gb{k}", seg=8)
      for k, a in enumerate([2 * math.pi * k / 26 for k in range(26)])]
COLON_T = label("COLON", (BXB + 0.20, -0.16, 1.22), 0.05, M_GRN)

# ---------- stacks (1 disc = 1 trillion) ----------
SX = 6.0; PITCH = 0.03; DR = 0.20; DH = 0.025
box((SX, 1.2, 2.5), (5.0, 0.06, 5.0), M_WALL, "swall")
GD = [cyl((SX - 0.30, 0, 0.02 + k * PITCH), DR, DH, M_GDISC, f"gd{k}", verts=40) for k in range(NG)]
RDs = [cyl((SX + 0.30, 0, 0.02 + k * PITCH), DR, DH, M_RDISC, f"rd{k}", verts=40) for k in range(NR)]
G_LAB = label("BACTERIA", (SX - 0.30, -0.25, 0.62), 0.06, M_GRN)
R_LAB = label("YOUR CELLS", (SX + 0.32, -0.25, 0.62), 0.06, M_WHITE)
G_CNT = label("", (SX - 0.30, -0.25, 1.62), 0.11, M_GRN)
R_CNT = label("", (SX + 0.30, -0.25, 1.32), 0.11, M_WHITE)
AHEAD = label("HUMAN CELLS AHEAD", (SX, -0.30, 1.30), 0.075, M_RED)
sk = bpy.data.objects.new("skey", bpy.data.lights.new("skey", "AREA")); sk.data.energy = 500; sk.data.size = 3
sk.location = (SX - 1.0, -2.5, 3.2); sk.rotation_euler = (math.radians(40), 0, math.radians(-20)); S.collection.objects.link(sk)

# ---------- cells (one human cell vs one bacterium) ----------
CX = -6.0
box((CX, 0.8, 1.5), (4.0, 0.06, 3.0), M_NAVY, "cwall")
box((CX, 0.0, 0.40), (3.0, 1.6, 0.04), M_NAVY, "cfloor")
CELL = sphere((CX - 0.12, 0, 1.0), 0.26, M_CELL, "cell", seg=40)
NUC = sphere((CX - 0.12, -0.10, 1.03), 0.10, M_NUC, "nuc", seg=24); NUC.parent = None
BUG = cyl_between((CX + 0.36, 0, 0.95), (CX + 0.42, 0, 0.99), 0.017, M_BUG, name="bug")
BUGP = [o for o in S.objects if o.name.startswith("Sphere") and o.location.x > CX + 0.3 and o.location.x < CX + 0.5]
bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.004, location=(CX + 0.39, -0.02, 0.97), rotation=(math.radians(90), 0, 0))
RING = bpy.context.object; RING.name = "ring"; link(RING, M_AMB)
C_LAB = label("1 HUMAN CELL", (CX - 0.12, -0.32, 1.0), 0.05, M_WHITE)
B_LAB = label("1 BACTERIUM", (CX + 0.40, -0.25, 0.82), 0.045, M_GRN)
X_LAB = label("~1,000× SMALLER", (CX + 0.40, -0.25, 1.13), 0.045, M_AMB)
ck = bpy.data.objects.new("ckey", bpy.data.lights.new("ckey", "AREA")); ck.data.energy = 260; ck.data.size = 2
ck.location = (CX - 0.8, -1.8, 2.2); ck.rotation_euler = (math.radians(45), 0, math.radians(-25)); S.collection.objects.link(ck)

# kitchen labels
L_BUG = label("BACTERIA", (BX - 0.16, -0.12, TOP + 0.42), 0.030, M_GRN)
L_APP = label("1 APPLE", (BX + 0.17, -0.12, TOP + 0.42), 0.030, M_WHITE)
L_200 = label("ALL ≈ 200 g", (BX - 0.12, -0.14, TOP + 0.42), 0.026, M_GRN)
key = bpy.data.objects.new("key", bpy.data.lights.new("key", "AREA")); key.data.energy = 220; key.data.size = 2.5
key.data.color = (1.0, 0.94, 0.85); key.location = (-0.8, -2.2, 3.2); key.rotation_euler = (math.radians(40), 0, math.radians(-20)); S.collection.objects.link(key)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA")); fill.data.energy = 90; fill.data.size = 2.0
fill.data.color = (0.85, 0.9, 1.0); fill.location = (1.8, -1.8, 1.6); fill.rotation_euler = (math.radians(60), 0, math.radians(45)); S.collection.objects.link(fill)

def n_green(t):
    if t < DISC[0]: return 0
    if t < t7 + 0.1 or t >= T_LOOP:
        return min(NG, int((t - DISC[0]) / DISC[1]) + 1)
    return max(NG_END, NG - int(max(0, t - FLUSH[0]) / FLUSH[1]))
def n_red(t): return 0 if t < DISC[0] else min(NR, int((t - DISC[0]) / DISC[1]) + 1)
def handler(scene, *a):
    t = scene.frame_current / FPS
    g = n_green(t)
    flushing = t7 + 0.1 <= t < T_LOOP
    G_CNT.data.body = (f"{g} T" if (g >= 30 or not flushing) else "< 30 T") if g else ""
    R_CNT.data.body = f"{n_red(t)} T" if n_red(t) else ""
bpy.app.handlers.frame_change_pre.append(handler)

def kf(o, f, loc=True, rot=False, sc=False):
    if loc: o.keyframe_insert("location", frame=f)
    if rot: o.keyframe_insert("rotation_euler", frame=f)
    if sc: o.keyframe_insert("scale", frame=f)

STREAM_ST = [STREAM[0] + (STREAM[1] - STREAM[0]) * k / len(JB) for k in range(len(JB))]
for f in range(0, N + 1):
    t = f / FPS
    loop = t >= T_LOOP
    kitchen = t < t3 - 0.05 or T_BAL2 <= t < t6 - 0.05 or loop
    a = beam_angle(t)
    BEAM.location = PIV; BEAM.rotation_euler = (0, -a, 0); kf(BEAM, f, rot=True)
    for k in range(2):
        end, pc = pan_pos(k, a)
        PANS[k].location = pc; kf(PANS[k], f)
        STRS[k].location = (end + pc) / 2; STRS[k].scale = (1, 1, STR); kf(STRS[k], f, sc=True)
    endL, pL = pan_pos(0, a); endR, pR = pan_pos(1, a)
    # jar
    jb0 = pL + V((0, 0, 0.006))
    if not loop and t < t2 - 0.05:
        u = smooth((t - JAR_DROP[0]) / JAR_DROP[1]) if t >= JAR_DROP[0] else 0
        jz = jb0.z + 0.55 * (1 - u) ** 1.0 if u < 1 else jb0.z
        jpos = V((jb0.x, jb0.y, jz)) if t >= JAR_DROP[0] else V((jb0.x, jb0.y, jb0.z + 0.9))
    else: jpos = jb0
    JAR.location = jpos + V((0, 0, JAR_H / 2)); kf(JAR, f)
    vis(JAR, kitchen and (t >= JAR_DROP[0] or loop), f)
    # apple
    ab0 = pR + V((0, 0, 0.006 + 0.045 * 0.88))
    if not loop and t < t2 - 0.05:
        if t < APP_DROP[0]: apos = ab0 + V((0, 0, 0.9))
        else:
            u = smooth((t - APP_DROP[0]) / APP_DROP[1]); apos = ab0 + V((0, 0, 0.5 * (1 - u)))
    else: apos = ab0
    APPLE.location = apos; kf(APPLE, f); STEM.location = apos + V((0, 0, 0.045)); kf(STEM, f)
    LEAF.location = apos + V((0.014, 0, 0.052)); kf(LEAF, f)
    for o, bs in ((APPLE, (1, 1, 0.88)), (STEM, (1, 1, 1)), (LEAF, (1.4, 0.5, 0.25))):
        vis(o, kitchen and (t >= APP_DROP[0] or t >= t2 - 0.05), f, base=bs)
    # jar beads
    for k, (b, rel) in enumerate(JB):
        fin = jpos + rel
        if t2 - 0.05 <= t < t3 - 0.05 and not loop:
            s0 = STREAM_ST[k]
            if t < s0: vis(b, False, f); b.location = GUT; kf(b, f); continue
            u = min(1.0, (t - s0) / 0.45)
            p = GUT.lerp(fin, u) + V((0, -0.06 * math.sin(math.pi * u), 0.28 * math.sin(math.pi * u)))
            b.location = p; kf(b, f); vis(b, True, f)
        else:
            b.location = fin; kf(b, f); vis(b, kitchen and (t >= JAR_DROP[0] or loop), f)
    # colon glow
    g = 0.4 + 3.4 * smooth((t - T_GLOW) / 0.35) if t5 - 0.05 <= t < t6 - 0.05 else 0.4
    bsdf(M_COLON).inputs["Emission Strength"].default_value = g
    bsdf(M_COLON).inputs["Emission Strength"].keyframe_insert("default_value", frame=f)
    vis(COLON_T, t5 - 0.05 <= t < t6 - 0.05 and t >= T_GLOW + 0.1, f)
    # stacks
    ng, nr = n_green(t), n_red(t)
    for k, d in enumerate(GD):
        z0 = 0.02 + k * PITCH
        if k >= NG_END and t7 + 0.1 <= t < T_LOOP:
            ft = FLUSH[0] + (NG - 1 - k) * FLUSH[1]
            u = max(0.0, (t - ft) / 0.45)
            d.location = (SX - 0.30 - 1.2 * u, -0.4 * u, z0 + 0.3 * math.sin(min(u, 1) * math.pi) - 0.8 * u * u)
            d.rotation_euler = (0.8 * u, 1.5 * u, 0); kf(d, f, rot=True); vis(d, u < 1.0, f)
        else:
            d.location = (SX - 0.30, 0, z0); d.rotation_euler = (0, 0, 0); kf(d, f, rot=True)
            vis(d, k < ng, f)
    for k, d in enumerate(RDs): vis(d, k < nr, f)
    G_CNT.location = (SX - 0.30, -0.25, 0.02 + max(ng, 1) * PITCH + 0.10); kf(G_CNT, f)
    R_CNT.location = (SX + 0.30, -0.25, 0.02 + max(nr, 1) * PITCH + 0.10); kf(R_CNT, f)
    G_LAB.location = G_CNT.location + V((0, 0, 0.15)); kf(G_LAB, f); R_LAB.location = R_CNT.location + V((0.02, 0, 0.15)); kf(R_LAB, f)
    vis(G_LAB, ng > 0, f); vis(R_LAB, nr > 0, f)
    vis(AHEAD, t >= FLUSH[0] + (NG - NG_END) * FLUSH[1] + 0.25 and t < T_LOOP, f)
    # cells
    cell_on = t4 - 0.05 <= t < T_BAL2
    pc = smooth((t - T_CELL) / 0.25); pb = smooth((t - T_BUG) / 0.2)
    vis(CELL, cell_on and pc > 0, f, base=(max(pc, 1e-4),) * 3); vis(NUC, cell_on and pc > 0, f, base=(max(pc, 1e-4),) * 3)
    for o in [BUG] + BUGP: vis(o, cell_on and t >= T_BUG, f)
    vis(RING, cell_on and t >= T_BUG, f, base=(max(pb, 1e-4),) * 3)
    vis(C_LAB, cell_on and t >= T_CELL + 0.2, f); vis(B_LAB, cell_on and t >= T_BUG + 0.15, f)
    vis(X_LAB, cell_on and t >= T_X, f)
    # kitchen labels
    hook_lab = (t < t2 - 0.05 and t >= sum(APP_DROP) + 0.1)   # not in the loop: they peek out behind the card
    vis(L_BUG, hook_lab, f); vis(L_APP, hook_lab or (T_BAL2 <= t < t5 - 0.05), f)
    vis(L_200, T_BAL2 + 0.15 <= t < t5 - 0.05, f)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 100; cam.data.clip_start = 0.02
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
def fixed(pa, ta, pb=None, tb=None):
    pb = pb or pa; tb = tb or ta
    return (V(pa), V(ta), V(pb), V(tb))
HOOK = fixed((BX + 0.20, -1.50, 1.20), (BX, 0, 0.98), (BX + 0.18, -1.42, 1.18), (BX, 0, 0.98))
SEG = [
    (0.0, t2 - 0.05, HOOK, 34, 34),
    (t2 - 0.05, t3 - 0.05, fixed((-0.08, -3.20, 1.55), (-0.28, 0, 1.20), (-0.04, -3.00, 1.50), (-0.28, 0, 1.20)), 30, 30),
    (t3 - 0.05, t4 - 0.05, fixed((SX + 0.4, -3.9, 1.6), (SX, 0, 0.85), (SX + 0.3, -3.7, 1.55), (SX, 0, 0.85)), 30, 30),
    (t4 - 0.05, T_BAL2, fixed((CX + 0.25, -2.6, 1.25), (CX + 0.10, 0, 0.92), (CX + 0.22, -2.4, 1.22), (CX + 0.12, 0, 0.92)), 30, 30),
    (T_BAL2, t5 - 0.05, HOOK, 34, 34),
    (t5 - 0.05, t6 - 0.05, fixed((BXB + 0.25, -1.55, 1.25), (BXB + 0.05, 0, 1.04), (BXB + 0.22, -1.42, 1.22), (BXB + 0.05, 0, 1.04)), 34, 34),
    (t6 - 0.05, T_LOOP, fixed((SX + 0.3, -3.7, 1.55), (SX, 0, 0.85), (SX + 0.2, -3.5, 1.5), (SX, 0, 0.82)), 30, 30),
    (T_LOOP, DUR + 0.01, HOOK, 34, 34),
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
for o, nch in ((L_BUG, 8), (L_APP, 7), (L_200, 11), (COLON_T, 5), (G_LAB, 8), (R_LAB, 10), (G_CNT, 6), (R_CNT, 4),
               (AHEAD, 17), (C_LAB, 12), (B_LAB, 11), (X_LAB, 15)):
    o.rotation_euler = (0, 0, 0); cc = o.constraints.new("TRACK_TO"); cc.target = cam
    cc.track_axis = "TRACK_Z"; cc.up_axis = "UP_Y"
    sz = o.data.size; w = nch * sz * 0.72 + sz * 0.5
    bpy.ops.mesh.primitive_plane_add(size=1); pl = bpy.context.object; pl.name = o.name + "_bg"
    pl.data.materials.append(M_PLATEL); noshadow(pl); pl.visible_glossy = False
    ox = -w / 2 + sz * 0.25 if o.data.align_x == "RIGHT" else 0.0
    for v in pl.data.vertices: v.co.x = v.co.x * w + ox; v.co.y = v.co.y * sz * 1.35; v.co.z = -0.012
    pl.parent = o
json.dump({"t_loop": T_LOOP, "t_card": tc, "cuts": [s[0] for s in SEG[1:]], "jar": sum(JAR_DROP), "apple": sum(APP_DROP),
           "stream": STREAM, "n_beads": len(JB), "disc": DISC, "ng": NG, "nr": NR, "cell": T_CELL, "bug": T_BUG, "x": T_X,
           "bal2": T_BAL2, "glow": T_GLOW, "flush": FLUSH, "n_flush": NG - NG_END},
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
