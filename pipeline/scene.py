"""The Impossible Lab #05 - boiling pasta on Mars.
Red Martian plain under a butterscotch sky; an astronaut mannequin, a camp stove on a crate,
a pot of water boiling furiously at ~0 °C (thermometer column stuck at the 0 mark, the 80 °C
mark glowing), stiff spaghetti, a pressure gauge whose needle swings to ×80, and the twist:
a pressure-cooker lid that seals the pot, whistles, and lets the thermometer climb to 80.
Usage: python3 scene.py [start end [step]] | [f1,f2,...] | [f]  [--force]   (no args = all frames)
"""
import bpy, addon_utils, math, random, sys, os, json, time
from mathutils import Vector
from config import FPS, FRAMES as N, DUR

random.seed(5)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"; S.cycles.device = "CPU"
S.cycles.samples = 8; S.cycles.use_denoising = True
S.cycles.max_bounces = 3; S.cycles.glossy_bounces = 1; S.cycles.diffuse_bounces = 1
S.cycles.transmission_bounces = 0; S.cycles.transparent_max_bounces = 2
S.render.resolution_x, S.render.resolution_y = 486, 864
S.render.fps = FPS; S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"; S.view_settings.look = "AgX - Punchy"

from timeline import LINES, CARD_START
L = {l["i"]: l for l in LINES}

# ---------- materials ----------
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
def ground_mat():
    m = bpy.data.materials.new("regolith"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.95
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.6; nz.inputs["Detail"].default_value = 6
    rp = nt.nodes.new("ShaderNodeValToRGB")
    rp.color_ramp.elements[0].color = (0.30, 0.09, 0.03, 1); rp.color_ramp.elements[1].color = (0.62, 0.27, 0.11, 1)
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.4
    nz2 = nt.nodes.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 18
    nt.links.new(nz.outputs["Fac"], rp.inputs[0]); nt.links.new(rp.outputs[0], b.inputs["Base Color"])
    nt.links.new(nz2.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs[0], b.inputs["Normal"])
    return m

M_GROUND = ground_mat()
M_ROCK = mat("rock", (0.22, 0.08, 0.04), 0.9)
M_SUIT = mat("suit", (0.86, 0.86, 0.84), 0.6)
M_SUIT2 = mat("suitorange", (0.95, 0.45, 0.08), 0.5)
M_VISOR = mat("visor", (0.9, 0.6, 0.15), 0.08, 1.0)
M_STEEL = mat("steel", (0.75, 0.76, 0.78), 0.25, 1.0)
M_DARK = mat("stove", (0.08, 0.08, 0.09), 0.5)
M_CRATE = mat("crate", (0.75, 0.75, 0.72), 0.6)
M_FLAME = mat("flame", (0.2, 0.4, 1.0), 0.5, 0, (0.25, 0.5, 1.0), 25.0)
M_WATER = mat("water", (0.55, 0.75, 0.85), 0.05, 0, (0.35, 0.6, 0.75), 0.25)
M_BUBBLE = mat("bubble", (0.85, 0.95, 1.0), 0.05, 0, (0.7, 0.85, 1.0), 0.6)
M_PASTA = mat("pasta", (0.95, 0.78, 0.30), 0.55)
M_GLASS = mat("tube", (0.92, 0.94, 0.96), 0.2)
M_RED = mat("mercuryred", (0.9, 0.05, 0.03), 0.4, 0, (1.0, 0.08, 0.04), 4.0)
M_COLD = mat("coldmark", (0.3, 0.8, 1.0), 0.4, 0, (0.3, 0.8, 1.0), 4.0)
M_HOT = mat("hotmark", (1.0, 0.6, 0.15), 0.4, 0, (1.0, 0.55, 0.1), 0.5)
M_DIAL = mat("dial", (0.95, 0.95, 0.92), 0.4)
M_NEEDLE = mat("needle", (0.9, 0.08, 0.05), 0.4)
M_STEAM = mat("steam", (1, 1, 1), 0.5, 0, (1, 1, 1), 2.5)
M_HAB = mat("hab", (0.85, 0.85, 0.82), 0.5)
M_HABWIN = mat("habwin", (1, 1, 1), 0.3, 0, (1.0, 0.8, 0.5), 4.0)
hot_emit = M_HOT.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]

# ---------- world: butterscotch Martian sky ----------
world = bpy.data.worlds.new("w"); S.world = world; world.use_nodes = True
nt = world.node_tree; bg = nt.nodes["Background"]
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (0.85, 0.55, 0.35, 1)
ramp.color_ramp.elements[1].position = 0.5; ramp.color_ramp.elements[1].color = (0.35, 0.20, 0.14, 1)
nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
nt.links.new(ramp.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 0.9
sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.2; sun.data.angle = math.radians(1.0); sun.data.color = (1.0, 0.92, 0.82)
sun.rotation_euler = (math.radians(50), math.radians(-15), math.radians(-40)); S.collection.objects.link(sun)

# ---------- helpers ----------
def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o
def box(loc, size, m, name="box", parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.scale = size; o.name = name; return link(o, m, parent)
def cyl(loc, r, depth, m, name="cyl", parent=None, rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; bpy.ops.object.shade_smooth(); return link(o, m, parent)
def cyl_between(a, b, r, m, parent, name="limb", caps=True):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r, depth=d.length, location=(a + b) / 2)
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
def text(body, loc, size, m, rot=(math.radians(90), 0, 0), align="CENTER", parent=None):
    bpy.ops.object.text_add(location=loc, rotation=rot); t = bpy.context.object
    t.data.body = body; t.data.size = size; t.data.extrude = 0.004; t.data.align_x = align
    return link(t, m, parent)
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def key_vis(o, f, on):  # visibility via scale keys
    o.scale = o["s"] if on else (0.0001, 0.0001, 0.0001); o.keyframe_insert("scale", frame=f)

# ---------- Martian plain ----------
bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0)); g = bpy.context.object; link(g, M_GROUND)
for k in range(70):
    a = random.uniform(0, math.tau); r = random.uniform(1.2, 30)
    x, y = math.cos(a) * r, math.sin(a) * r + 6
    if abs(x) < 1.6 and -2.5 < y < 1.5: continue
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.05, 0.4) * (1 + r / 15), location=(x, y, 0))
    o = bpy.context.object; o.scale = (1, random.uniform(0.7, 1.3), random.uniform(0.4, 0.8))
    o.rotation_euler = (0, 0, random.uniform(0, 3)); link(o, M_ROCK)
for k in range(7):  # low hills on the horizon
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(-90 + k * 30 + random.uniform(-8, 8), 110 + random.uniform(-10, 20), -2))
    o = bpy.context.object; o.scale = (random.uniform(25, 45), 18, random.uniform(5, 12)); bpy.ops.object.shade_smooth(); link(o, M_ROCK)
# habitat in the background (readable "base on Mars")
cyl((4.5, 9.0, 1.2), 1.8, 2.4, M_HAB, "hab")
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.8, location=(4.5, 9.0, 2.4)); o = bpy.context.object
o.scale = (1, 1, 0.55); bpy.ops.object.shade_smooth(); link(o, M_HAB)
for a in (-0.5, 0.0, 0.5):
    box((4.5 + math.sin(a) * 1.79, 9.0 - math.cos(a) * 1.79, 1.5), (0.35, 0.05, 0.25), M_HABWIN, "habwin").rotation_euler = (0, 0, a)
cyl((-5.5, 14.0, 0.9), 0.9, 1.8, M_HAB, "hab2")

# ---------- camp kitchen: crate, stove, pot ----------
TOP = 0.62                                   # crate top
box((0, 0, TOP / 2), (0.75, 0.55, TOP), M_CRATE, "crate")
box((0, 0, TOP + 0.05), (0.42, 0.34, 0.10), M_DARK, "stove")
FL = []
for k in range(10):
    a = k / 10 * math.tau
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.022, radius2=0, depth=0.07, location=(math.cos(a) * 0.09, math.sin(a) * 0.09, TOP + 0.135))
    f = bpy.context.object; link(f, M_FLAME); FL.append(f)
PB = TOP + 0.12                              # pot bottom
PR, PH = 0.19, 0.22
bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=PR, depth=PH, location=(0, 0, PB + PH / 2))
pot = bpy.context.object; bpy.ops.object.shade_smooth(); link(pot, M_STEEL)
sol = pot.modifiers.new("shell", "SOLIDIFY"); sol.thickness = 0.012
bpy.ops.object.mode_set(mode="EDIT"); import bmesh
bm = bmesh.from_edit_mesh(pot.data)
for fc in bm.faces:
    if fc.normal.z > 0.9: bm.faces.remove(fc) if False else None
top_faces = [fc for fc in bm.faces if fc.normal.z > 0.9]
bmesh.ops.delete(bm, geom=top_faces, context="FACES"); bmesh.update_edit_mesh(pot.data)
bpy.ops.object.mode_set(mode="OBJECT")
for s in (-1, 1):  # handles
    box((s * (PR + 0.05), 0, PB + PH - 0.04), (0.08, 0.03, 0.02), M_DARK, "handle")
WZ = PB + PH - 0.035                         # water surface
cyl((0, 0, WZ - 0.005), PR - 0.012, 0.01, M_WATER, "water")
# bubbles: rise from the bottom, swell, pop at the surface (continuous rolling boil)
BUB = []
for k in range(40):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=1)
    b = bpy.context.object; bpy.ops.object.shade_smooth(); link(b, M_BUBBLE)
    r = random.uniform(0.0, 0.15); a = random.uniform(0, math.tau)
    BUB.append((b, math.cos(a) * r, math.sin(a) * r, random.uniform(0, 1), random.uniform(0.012, 0.03), random.uniform(0.7, 1.3)))
# spaghetti: stiff strands fanned out of the pot
PASTA = empty("pasta")
for k in range(14):
    a = k / 14 * math.tau + random.uniform(-0.2, 0.2); tilt = math.radians(random.uniform(12, 24))
    base = Vector((math.cos(a) * 0.05, math.sin(a) * 0.05, WZ - 0.12))
    tip = base + Vector((math.cos(a) * math.sin(tilt), math.sin(a) * math.sin(tilt), math.cos(tilt))) * 0.34
    cyl_between(base, tip, 0.0045, M_PASTA, PASTA, "strand", caps=False)

# thermometer (tall prop): 0 °C mark glowing cold, 80 °C mark that lights up
TX, TY, T0, T80 = 0.42, -0.05, TOP + 0.10, TOP + 0.62
cyl((TX, TY, TOP + 0.38), 0.03, 0.66, M_GLASS, "tube")
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.05, location=(TX, TY, TOP + 0.06)); link(bpy.context.object, M_RED)
col = cyl((TX, TY, T0), 0.034, 1.0, M_RED, "column"); col.location.z = T0  # scaled in z; origin at the bottom
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.transform.translate(value=(0, 0, 0.5)); bpy.ops.object.mode_set(mode="OBJECT")
box((TX, TY, T0 + 0.04), (0.10, 0.02, 0.012), M_COLD, "mark0")
box((TX, TY, T80), (0.10, 0.02, 0.012), M_HOT, "mark80")
text("0 °C", (TX + 0.07, TY, T0 + 0.025), 0.05, M_COLD, align="LEFT")
text("80 °C", (TX + 0.07, TY, T80 - 0.015), 0.05, M_HOT, align="LEFT")

# pressure gauge on a post (beat 3)
GX, GY, GZ = -0.48, -0.05, TOP + 0.55
cyl_between((GX, GY + 0.05, 0), (GX, GY + 0.05, GZ), 0.02, M_STEEL, None, "post", caps=False)
cyl((GX, GY, GZ), 0.14, 0.05, M_STEEL, "rim", rot=(math.radians(90), 0, 0))
cyl((GX, GY - 0.027, GZ), 0.125, 0.01, M_DIAL, "face", rot=(math.radians(90), 0, 0))
for k in range(9):  # ticks over 270°
    a = math.radians(225 - k * 270 / 8)
    box((GX + math.cos(a) * 0.1, GY - 0.034, GZ + math.sin(a) * 0.1), (0.008, 0.004, 0.025), M_DARK, "tick").rotation_euler = (0, -a + math.pi / 2, 0)
text("×80", (GX + 0.075, GY - 0.035, GZ - 0.095), 0.04, M_NEEDLE, align="CENTER")
text("MARS", (GX - 0.075, GY - 0.035, GZ - 0.095), 0.03, M_DARK, align="CENTER")
needle = empty("needle", (GX, GY - 0.04, GZ)); needle.rotation_mode = "XYZ"
box((0, 0, 0.045), (0.008, 0.004, 0.09), M_NEEDLE, "needlebar", needle)
needle.rotation_euler = (0, math.radians(-130), 0)
cyl((0, -0.003, 0), 0.015, 0.008, M_DARK, "hub", needle, rot=(math.radians(90), 0, 0))

# pressure-cooker lid (twist)
LID = empty("lid")
cyl((0, 0, 0.012), PR + 0.015, 0.025, M_STEEL, "lidplate", LID)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=12, radius=PR, location=(0, 0, 0.02)); o = bpy.context.object
o.scale = (1, 1, 0.25); bpy.ops.object.shade_smooth(); link(o, M_STEEL, LID)
box((0, 0, 0.075), (0.26, 0.04, 0.03), M_DARK, "lidhandle", LID)
cyl((0.08, 0.06, 0.07), 0.015, 0.05, M_DARK, "valve", LID)
JET = empty("jet", (0.08, 0.06, 0.1), LID)
bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.008, radius2=0.03, depth=0.22, location=(0, 0, 0.11))
link(bpy.context.object, M_STEAM, JET)

# ---------- astronaut mannequin (faces -y) ----------
body = empty("body", (0.05, 0.62, 0.915)); body.rotation_euler = (0, 0, math.radians(-90))
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.30))
o = bpy.context.object; o.scale = (0.16, 0.23, 0.34); bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
box((0.12, 0, 0.32), (0.12, 0.30, 0.38), M_SUIT, "pack", body).location = (0.17, 0, 0.32)   # life-support pack (behind)
bpy.ops.mesh.primitive_uv_sphere_add(segments=22, ring_count=11, location=(0, 0, 0.02))
o = bpy.context.object; o.scale = (0.15, 0.19, 0.13); bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.16, location=(0, 0, 0.78))
o = bpy.context.object; bpy.ops.object.shade_smooth(); link(o, M_SUIT, body)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.13, location=(-0.06, 0, 0.79))
o = bpy.context.object; o.scale = (0.75, 1, 0.8); bpy.ops.object.shade_smooth(); link(o, M_VISOR, body)
bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.02, location=(0, 0, 0.64)); link(bpy.context.object, M_SUIT2, body)
arms = []
for side in (-1, 1):
    sh = empty(f"shoulder{side}", (0, side * 0.25, 0.5), body); sh.rotation_mode = "XYZ"
    cyl_between((0, 0, 0), (0, side * 0.03, -0.30), 0.06, M_SUIT, sh, "upperarm")
    cyl_between((0, side * 0.03, -0.30), (0, side * 0.04, -0.56), 0.055, M_SUIT, sh, "forearm")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.06, location=(0, side * 0.04, -0.6)); link(bpy.context.object, M_SUIT2, sh)
    arms.append(sh)
for side in (-1, 1):
    hp = empty(f"hip{side}", (0, side * 0.1, 0), body)
    cyl_between((0, 0, 0), (0, side * 0.01, -0.45), 0.08, M_SUIT, hp, "thigh")
    cyl_between((0, side * 0.01, -0.45), (0, side * 0.01, -0.82), 0.07, M_SUIT, hp, "shin")
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=(-0.05, side * 0.01, -0.86))
    ft = bpy.context.object; ft.scale = (0.13, 0.07, 0.06); link(ft, M_SUIT2, hp)

# ---------- timeline ----------
t2, t3, t4, t5, t6, t7 = (L[i]["start"] for i in range(2, 8))
tc = CARD_START
T_LIDUP = t6 - 0.05                          # astronaut holds the lid above the pot
T_SEAL = t7 + 0.10                           # lid drops on
T_HISS = T_SEAL + 0.35                       # valve starts hissing, thermometer climbs
T_80 = T_HISS + 1.1                          # thermometer reaches the 80 °C mark
T_GAUGE = t5 + 0.15                          # needle swings from Mars to ×80
COL_ZERO, COL_80 = 0.05, T80 - T0

for o in (LID, JET, PASTA): o["s"] = tuple(o.scale)
for f in range(0, N + 1):
    t = f / FPS
    loop = t >= tc                           # last ~1 s: back to the opening state (loop)
    sealed = (t >= T_SEAL) and not loop
    # flames flicker
    for k, fl in enumerate(FL):
        fl.scale = (1, 1, 0.8 + 0.4 * abs(math.sin(t * 17 + k * 1.3))); fl.keyframe_insert("scale", frame=f)
    # bubbles (hidden once the lid is on)
    for b, bx, by, ph, rmax, sp in BUB:
        u = (t * 2.2 * sp + ph) % 1.0            # surface bubble: swells, then pops
        r = rmax * (0.25 + 0.95 * math.sin(u * math.pi) ** 0.6)
        z = WZ - 0.4 * r + 0.5 * r * u
        if sealed: r = 0.0001
        b.location = (bx + 0.01 * math.sin(t * 9 + ph * 6), by, z); b.scale = (r, r, r * 0.9)
        b.keyframe_insert("location", frame=f); b.keyframe_insert("scale", frame=f)
    # pasta: visible until the lid seals the pot
    key_vis(PASTA, f, not sealed)
    # thermometer column: stuck near 0 °C, climbs to 80 after sealing
    h = COL_ZERO + (COL_80 - COL_ZERO) * smooth((t - T_HISS) / (T_80 - T_HISS)) if sealed else COL_ZERO + 0.004 * math.sin(t * 5)
    col.scale = (1, 1, max(h, 0.01)); col.keyframe_insert("scale", frame=f)
    hot_emit.default_value = (2.0 + 2.0 * abs(math.sin(t * 6))) if (t4 - 0.05 <= t < t5 or (sealed and t >= T_80 - 0.1)) else 0.5
    hot_emit.keyframe_insert("default_value", frame=f)
    # gauge needle: rests at "Mars" (left), swings to ×80 on the line
    g = smooth((t - T_GAUGE) / 0.7) if t < tc else 0.0
    wob = 0.05 * math.sin((t - T_GAUGE) * 20) * math.exp(-4 * max(0, t - T_GAUGE - 0.7)) if t > T_GAUGE + 0.6 and t < tc else 0
    needle.rotation_euler = (0, math.radians(-130) + g * math.radians(255) + wob, 0); needle.keyframe_insert("rotation_euler", frame=f)
    # lid: hidden, then held above the pot, then drops on
    if T_LIDUP <= t < tc:
        if t < T_SEAL: z = WZ + 0.30 + 0.02 * math.sin(t * 4)
        else: z = PB + PH + max(0.0, 0.30 * (1 - ((t - T_SEAL) / 0.18) ** 2)) * (t < T_SEAL + 0.18)
        LID.location = (0, 0, z); key_vis(LID, f, True)
    else:
        LID.location = (0, 0, WZ + 0.3); key_vis(LID, f, False)
    LID.keyframe_insert("location", frame=f)
    js = 0.0
    if sealed and t >= T_HISS: js = 0.7 + 0.3 * abs(math.sin(t * 23))
    JET.scale = (js or 0.0001,) * 3; JET.keyframe_insert("scale", frame=f)
    # astronaut arms: idle; leans to look at the pot; right arm holds the lid on the twist
    ra = math.radians(10) + 0.05 * math.sin(t * 1.5); la = math.radians(10) + 0.05 * math.sin(t * 1.3 + 1)
    if t4 - 0.05 <= t < t5: ra = math.radians(55) + 0.15 * math.sin(t * 7)          # pokes at the stiff pasta
    if T_LIDUP <= t < T_SEAL + 0.2 and not loop: ra = math.radians(75)
    arms[0].rotation_euler = (0, -ra, 0); arms[1].rotation_euler = (0, -la, 0)
    for a in arms: a.keyframe_insert("rotation_euler", frame=f)

# ---------- camera: piecewise segments, hard cuts timed to the lines ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24; cam.data.clip_end = 600
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
V = Vector
OPEN = ((0.55, -0.98, 1.34), (0.0, 0.05, 0.97), 27)
SEG = [  # (t0, t1, (posA, tgtA, lensA), (posB, tgtB, lensB))
    (0.0, t2 - 0.05, OPEN, ((0.50, -0.90, 1.30), (0.0, 0.05, 0.98), 28)),
    (t2 - 0.05, t3 - 0.05, ((-2.6, -4.6, 1.5), (0.6, 1.2, 1.1), 26), ((-2.0, -3.8, 1.4), (0.5, 1.0, 1.05), 26)),
    (t3 - 0.05, t3 + 1.25, ((0.10, -0.42, 1.55), (0.0, 0.0, WZ - 0.02), 30), ((0.08, -0.36, 1.45), (0.0, 0.0, WZ - 0.02), 32)),
    (t3 + 1.25, t4 - 0.05, ((TX + 0.10, -0.80, T0 + 0.02), (TX + 0.05, TY, T0 - 0.06), 32), ((TX + 0.08, -0.74, T0 + 0.02), (TX + 0.05, TY, T0 - 0.06), 32)),
    (t4 - 0.05, t4 + 1.35, ((-0.55, -0.75, 1.20), (0.0, 0.0, WZ + 0.12), 30), ((-0.48, -0.66, 1.22), (0.0, 0.0, WZ + 0.12), 32)),
    (t4 + 1.35, t5 - 0.05, ((TX + 0.12, -0.85, T80 - 0.02), (TX + 0.06, TY, T80 - 0.13), 30), ((TX + 0.10, -0.78, T80 - 0.02), (TX + 0.06, TY, T80 - 0.13), 30)),
    (t5 - 0.05, t6 - 0.05, ((-0.62, -0.78, 1.25), (GX, GY, GZ - 0.02), 34), ((-0.58, -0.68, 1.23), (GX, GY, GZ - 0.02), 36)),
    (t6 - 0.05, t7 - 0.05, ((1.0, -1.9, 1.45), (0.05, 0.25, 1.2), 26), ((0.95, -1.8, 1.45), (0.05, 0.25, 1.2), 26)),
    (t7 - 0.05, tc, ((0.75, -1.25, 1.10), (0.18, 0.0, 1.05), 28), ((0.70, -1.15, 1.10), (0.18, 0.0, 1.07), 29)),
    (tc, DUR + 0.01, ((0.70, -1.15, 1.08), (0.05, 0.05, 1.03), 27), OPEN),
]
for f in range(0, N + 1):
    t = f / FPS
    seg = next((s for s in SEG if s[0] <= t < s[1]), SEG[-1])
    u = smooth((t - seg[0]) / (seg[1] - seg[0]))
    (pa, ta, la), (pb, tb, lb) = seg[2], seg[3]
    cam.location = V(pa).lerp(V(pb), u); cam.keyframe_insert("location", frame=f)
    tgt.location = V(ta).lerp(V(tb), u); tgt.keyframe_insert("location", frame=f)
    cam.data.lens = la + (lb - la) * u; cam.data.keyframe_insert("lens", frame=f)

json.dump({"t_lidup": T_LIDUP, "t_seal": T_SEAL, "t_hiss": T_HISS, "t_80": T_80, "t_gauge": T_GAUGE, "t_card": tc,
           "cuts": [s[0] for s in SEG[1:]]}, open("/home/claude/reel/beats.json", "w"), indent=1)

# ---------- render ----------
args = [a for a in (sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]) if a != "--force"]
if args and ("," in args[0] or len(args) == 1): frames = [int(x) for x in args[0].split(",") if x]  # "12" = one frame
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
