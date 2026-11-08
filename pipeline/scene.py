"""The Impossible Lab #01 - bike in a whisky lake.
Builds everything from primitives, animates it frame by frame, renders with Cycles (CPU).
Usage: python3 scene.py [start end]   (frames, inclusive; default full 0..359)
"""
import bpy, addon_utils, math, random, sys, json
from mathutils import Vector

FPS, N = 24, 360
random.seed(7)
addon_utils.enable("cycles", default_set=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles", default_set=True)
S = bpy.context.scene
S.render.engine = "CYCLES"
S.cycles.device = "CPU"
S.cycles.samples = 12
S.cycles.use_denoising = True
S.cycles.max_bounces = 4
S.cycles.transparent_max_bounces = 6
S.cycles.glossy_bounces = 2
S.cycles.diffuse_bounces = 1
S.render.resolution_x, S.render.resolution_y = 540, 960
S.render.fps = FPS
S.frame_start, S.frame_end = 0, N - 1
S.render.image_settings.file_format = "PNG"
S.view_settings.view_transform = "AgX"
S.view_settings.look = "AgX - Punchy"

def sec(t): return t * FPS

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

M_FRAME = mat("frame", (0.02, 0.02, 0.025), 0.35, 0.6)
M_TYRE = mat("tyre", (0.01, 0.01, 0.01), 0.8)
M_RIM = mat("rim", (0.8, 0.8, 0.82), 0.2, 1.0)
M_SEAT = mat("seat", (0.05, 0.03, 0.02), 0.6)
M_OIL = mat("oil", (0.005, 0.004, 0.003), 0.05, 0.3)
M_BED = mat("bed", (0.35, 0.16, 0.04), 0.9, 0, (1.0, 0.45, 0.08), 0.35)
M_HILL = mat("hill", (0.06, 0.035, 0.03), 1.0)

# chain: oily -> dry, keyframed
M_CHAIN = mat("chain", (0.08, 0.075, 0.07), 0.08, 1.0)
cb = M_CHAIN.node_tree.nodes["Principled BSDF"]
for f, col, r in [(sec(11.0), (0.08, 0.075, 0.07), 0.08), (sec(13.2), (0.42, 0.40, 0.37), 0.65)]:
    cb.inputs["Base Color"].default_value = (*col, 1); cb.inputs["Base Color"].keyframe_insert("default_value", frame=f)
    cb.inputs["Roughness"].default_value = r; cb.inputs["Roughness"].keyframe_insert("default_value", frame=f)

# whisky: fresnel mix of amber transparency and gloss, tiny glow
W = bpy.data.materials.new("whisky"); W.use_nodes = True
nt = W.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (1.0, 0.55, 0.10, 1)
gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.04
gl.inputs["Color"].default_value = (1.0, 0.75, 0.4, 1)
em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (0.9, 0.38, 0.05, 1); em.inputs[1].default_value = 0.35
fr = nt.nodes.new("ShaderNodeFresnel"); fr.inputs["IOR"].default_value = 1.36
mx1 = nt.nodes.new("ShaderNodeAddShader"); mx2 = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(tr.outputs[0], mx1.inputs[0]); nt.links.new(em.outputs[0], mx1.inputs[1])
nt.links.new(fr.outputs[0], mx2.inputs[0]); nt.links.new(mx1.outputs[0], mx2.inputs[1])
nt.links.new(gl.outputs[0], mx2.inputs[2]); nt.links.new(mx2.outputs[0], out.inputs[0])

def flame_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; n = m.node_tree; n.nodes.clear()
    o = n.nodes.new("ShaderNodeOutputMaterial")
    e = n.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (0.08, 0.32, 1.0, 1)
    t = n.nodes.new("ShaderNodeBsdfTransparent")
    noise = n.nodes.new("ShaderNodeTexNoise"); noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value = 4.0; noise.inputs["Roughness"].default_value = 0.6; noise.inputs["Detail"].default_value = 4
    tc = n.nodes.new("ShaderNodeTexCoord")
    grad = n.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "SPHERICAL"
    mapn = n.nodes.new("ShaderNodeMapping"); mapn.inputs["Location"].default_value = (0, 0, 0)
    mapn.inputs["Scale"].default_value = (0.9, 0.9, 0.9)
    mul = n.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    ramp = n.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.42; ramp.color_ramp.elements[1].position = 0.6
    strength = n.nodes.new("ShaderNodeMath"); strength.operation = "MULTIPLY"; strength.name = "STR"
    mix = n.nodes.new("ShaderNodeMixShader")
    n.links.new(tc.outputs["Object"], mapn.inputs[0]); n.links.new(mapn.outputs[0], grad.inputs[0])
    n.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    n.links.new(grad.outputs[1], mul.inputs[0]); n.links.new(noise.outputs[0], mul.inputs[1])
    n.links.new(mul.outputs[0], ramp.inputs[0])
    n.links.new(ramp.outputs[0], strength.inputs[0]); strength.inputs[1].default_value = 0.0
    n.links.new(strength.outputs[0], mix.inputs[0])
    n.links.new(t.outputs[0], mix.inputs[1]); n.links.new(e.outputs[0], mix.inputs[2])
    n.links.new(mix.outputs[0], o.inputs[0])
    e.inputs[1].default_value = 2.2
    return m, noise, strength

# ---------- world & light ----------
world = bpy.data.worlds.new("sky"); S.world = world; world.use_nodes = True
wn = world.node_tree; bg = wn.nodes["Background"]
grad = wn.nodes.new("ShaderNodeTexGradient"); grad.gradient_type = "LINEAR"
tcw = wn.nodes.new("ShaderNodeTexCoord"); sepz = wn.nodes.new("ShaderNodeSeparateXYZ")
mapz = wn.nodes.new("ShaderNodeMapRange")
mapz.inputs["From Min"].default_value = -0.05; mapz.inputs["From Max"].default_value = 0.6
ramp = wn.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (1.0, 0.55, 0.18, 1)
ramp.color_ramp.elements[1].color = (0.18, 0.22, 0.45, 1)
el = ramp.color_ramp.elements.new(0.35); el.color = (0.95, 0.42, 0.28, 1)
wn.links.new(tcw.outputs["Generated"], sepz.inputs[0])
wn.links.new(sepz.outputs["Z"], mapz.inputs["Value"])
tcw2 = wn.nodes.new("ShaderNodeTexCoord")
sep2 = wn.nodes.new("ShaderNodeSeparateXYZ"); wn.links.new(tcw2.outputs["Generated"], sep2.inputs[0])
mr2 = wn.nodes.new("ShaderNodeMapRange"); mr2.inputs["From Min"].default_value = 0.0; mr2.inputs["From Max"].default_value = 0.55
wn.links.new(sep2.outputs["Z"], mr2.inputs["Value"]); mr2.inputs['From Max'].default_value = 0.4
wn.links.new(mr2.outputs["Result"], ramp.inputs["Fac"])
wn.links.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.9

sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
sun.data.energy = 3.2; sun.data.color = (1.0, 0.72, 0.45); sun.data.angle = math.radians(3)
sun.rotation_euler = (math.radians(80), 0, math.radians(200)); S.collection.objects.link(sun)
fill = bpy.data.objects.new("fill", bpy.data.lights.new("fill", "AREA"))
fill.data.energy = 220; fill.data.size = 6; fill.data.color = (0.6, 0.7, 1.0)
fill.location = (-3, -6, 4); fill.rotation_euler = (math.radians(55), 0, math.radians(-30)); S.collection.objects.link(fill)

# ---------- helpers ----------
def link(o, m=None, parent=None):
    if m: o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def cyl_between(a, b, r, m, parent, name="tube"):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.name = name
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = d.to_track_quat("Z", "Y")
    bpy.ops.object.shade_smooth()
    return link(o, m, parent)

def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); e.location = loc; S.collection.objects.link(e); return e

# ---------- lake ----------
SURF = 0.45
bpy.ops.mesh.primitive_plane_add(size=80, location=(10, 10, SURF))
lake = bpy.context.object; lake.name = "lake"
oc = lake.modifiers.new("ocean", "OCEAN")
oc.geometry_mode = "DISPLACE"; oc.resolution = 10; oc.spatial_size = 40; oc.wave_scale = 0.06
oc.wind_velocity = 6; oc.choppiness = 0.4
oc.time = 0; oc.keyframe_insert("time", frame=0); oc.time = 6; oc.keyframe_insert("time", frame=N)
bpy.ops.object.shade_smooth(); link(lake, W)
bpy.ops.mesh.primitive_plane_add(size=80, location=(10, 10, -0.7)); link(bpy.context.object, M_BED)
for (x, y, sx, sz) in [(4, 30, 18, 3.5), (-14, 26, 14, 2.6), (22, 24, 16, 4.2), (36, 34, 20, 3)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=(x, y, 0))
    h = bpy.context.object; h.scale = (sx, 5, sz); link(h, M_HILL)

# ---------- bike (built from primitives) ----------
bike = empty("bike")
R = 0.34
wheels = []
for wx in (-0.52, 0.52):
    hub = empty("hub", (wx, 0, R)); hub.parent = bike
    bpy.ops.mesh.primitive_torus_add(major_radius=R - 0.015, minor_radius=0.018, location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object; bpy.ops.object.shade_smooth(); link(t, M_TYRE, hub)
    bpy.ops.mesh.primitive_torus_add(major_radius=R - 0.045, minor_radius=0.01, location=(0, 0, 0), rotation=(math.pi / 2, 0, 0))
    link(bpy.context.object, M_RIM, hub)
    for k in range(12):
        a = k * math.tau / 12
        cyl_between((0, 0, 0), (math.cos(a) * (R - 0.05), 0, math.sin(a) * (R - 0.05)), 0.003, M_RIM, hub, "spoke")
    wheels.append(hub)
BB = Vector((0, 0, 0.30)); SEAT = Vector((-0.14, 0, 0.82)); HEAD = Vector((0.40, 0, 0.78))
RH, FH = Vector((-0.52, 0, R)), Vector((0.52, 0, R))
for a, b in [(BB, SEAT), (BB, HEAD), (SEAT, HEAD), (BB, RH), (SEAT, RH), (HEAD, FH)]:
    for dy in ((0,) if (a, b) not in [(BB, RH), (SEAT, RH)] else (-0.035, 0.035)):
        cyl_between(a + Vector((0, dy, 0)), b + Vector((0, dy, 0)), 0.018, M_FRAME, bike)
cyl_between(HEAD, HEAD + Vector((0.05, 0, 0.14)), 0.016, M_FRAME, bike)
cyl_between(HEAD + Vector((0.05, -0.22, 0.14)), HEAD + Vector((0.05, 0.22, 0.14)), 0.013, M_FRAME, bike)
cyl_between(SEAT, SEAT + Vector((-0.02, 0, 0.1)), 0.012, M_RIM, bike)
bpy.ops.mesh.primitive_uv_sphere_add(location=SEAT + Vector((-0.02, 0, 0.12)))
seat = bpy.context.object; seat.scale = (0.11, 0.045, 0.02); bpy.ops.object.shade_smooth(); link(seat, M_SEAT, bike)

# drivetrain on the right side (y<0, camera side)
DY = -0.07
ring = empty("ring", BB + Vector((0, DY, 0))); ring.parent = bike
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.10, depth=0.006, rotation=(math.pi / 2, 0, 0))
link(bpy.context.object, M_RIM, ring)
for k in range(36):
    a = k * math.tau / 36
    bpy.ops.mesh.primitive_cube_add(size=1, location=(math.cos(a) * 0.105, 0, math.sin(a) * 0.105), rotation=(0, -a, 0))
    tth = bpy.context.object; tth.scale = (0.012, 0.006, 0.008); link(tth, M_RIM, ring)
for k in range(5):
    a = k * math.tau / 5
    cyl_between((0, 0, 0), (math.cos(a) * 0.09, 0, math.sin(a) * 0.09), 0.008, M_FRAME, ring, "arm")
crank = cyl_between(BB + Vector((0, DY - 0.01, 0)), BB + Vector((0, DY - 0.01, -0.17)), 0.012, M_FRAME, None, "crank")
crank_p = empty("crankpivot", BB + Vector((0, DY - 0.01, 0))); crank_p.parent = bike
crank.parent = crank_p; crank.location -= crank_p.location
cog = empty("cog", RH + Vector((0, DY, 0))); cog.parent = bike
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.045, depth=0.006, rotation=(math.pi / 2, 0, 0))
link(bpy.context.object, M_RIM, cog)
# chain links along a stadium path between ring and cog
c1, r1, c2, r2 = BB + Vector((0, DY, 0)), 0.112, RH + Vector((0, DY, 0)), 0.055
pts = []
L = (c2 - c1).length; dirv = (c2 - c1).normalized(); perp = Vector((-dirv.z, 0, dirv.x))
def stadium(u):  # u in [0,1): top run -> around cog (rear) -> bottom run -> around ring
    seg = [L, math.pi * r2, L, math.pi * r1]; s = u * sum(seg)
    if s < seg[0]:
        k = s / L; return (c1 + Vector((0, 0, r1))).lerp(c2 + Vector((0, 0, r2)), k)
    s -= seg[0]
    if s < seg[1]:
        a = math.pi / 2 + s / r2; return c2 + Vector((math.cos(a) * r2, 0, math.sin(a) * r2))
    s -= seg[1]
    if s < seg[2]:
        k = s / L; return (c2 - Vector((0, 0, r2))).lerp(c1 - Vector((0, 0, r1)), k)
    s -= seg[2]
    a = -math.pi / 2 + s / r1; return c1 + Vector((math.cos(a) * r1, 0, math.sin(a) * r1))
NL = 110
chain_links = []
for k in range(NL):
    p, q = stadium(k / NL), stadium((k + 0.6) / NL)
    o = cyl_between(p, q, 0.0075, M_CHAIN, bike, "link")
    chain_links.append(o)

# ---------- bike motion ----------
def bike_x(f):
    t = f / FPS
    if t < 0.35: return 0.0
    if t < 4.9: return 0.0 + (t - 0.35) * 0.32
    if t < 10.1: return 1.456 + (t - 4.9) * 0.12
    return 2.08 + (t - 10.1) * 0.05
def bike_z(f):
    t = f / FPS
    if t < 0.33: return 1.7 - 1.75 * (t / 0.33) ** 2
    if t < 0.6: return -0.05 + 0.10 * math.sin((t - 0.33) / 0.27 * math.pi) * math.exp(-(t - 0.33) * 4)
    z = 0.06
    if t > 3.0: z -= min((t - 3.0) / 1.2, 1) * 0.14   # sinks lower: less buoyancy
    return z + 0.012 * math.sin(t * 2.1)
spin = 0.0
for f in range(0, N + 1, 2):
    t = f / FPS
    bike.location = (bike_x(f), 0, bike_z(f)); bike.keyframe_insert("location", frame=f)
    bike.rotation_euler = (0.02 * math.sin(t * 1.7), 0.015 * math.sin(t * 1.3), 0); bike.keyframe_insert("rotation_euler", frame=f)
    v = (bike_x(f + 1) - bike_x(f)) * FPS
    spin += v / R * (2 / FPS)
    for w in wheels:
        w.rotation_euler = (0, spin, 0); w.keyframe_insert("rotation_euler", frame=f)
    cadence = spin * 0.55
    ring.rotation_euler = (0, cadence, 0); ring.keyframe_insert("rotation_euler", frame=f)
    crank_p.rotation_euler = (0, cadence, 0); crank_p.keyframe_insert("rotation_euler", frame=f)
    cog.rotation_euler = (0, spin, 0); cog.keyframe_insert("rotation_euler", frame=f)

# ---------- splash (first-second trick) ----------
for k in range(4):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.5, minor_radius=0.02, location=(0, 0, SURF + 0.01))
    rg = bpy.context.object; link(rg, mat(f"ripple{k}", (1, 0.7, 0.35), 0.05, 0, (1, 0.6, 0.2), 0.6))
    f0 = sec(0.33) + k * 4
    rg.scale = (0.01, 0.01, 1); rg.keyframe_insert("scale", frame=0); rg.keyframe_insert("scale", frame=f0)
    rg.scale = (5 + k, 5 + k, 1); rg.keyframe_insert("scale", frame=f0 + 40)
    rg.scale = (0.01, 0.01, 1); rg.keyframe_insert("scale", frame=f0 + 41)
M_DROP = mat("drop", (1.0, 0.5, 0.1), 0.02, 0.0, (1.0, 0.45, 0.06), 1.5)
for k in range(46):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=random.uniform(0.015, 0.05))
    d = bpy.context.object; link(d, M_DROP)
    a = random.uniform(0, math.tau); vh = random.uniform(0.8, 2.6); vz = random.uniform(2.0, 4.2)
    f0 = int(sec(0.33)); x0, y0 = math.cos(a) * 0.35, math.sin(a) * 0.35
    d.location = (0, 0, -3); d.keyframe_insert("location", frame=0); d.keyframe_insert("location", frame=f0 - 1)
    for f in range(f0, f0 + 40, 2):
        tt = (f - f0) / FPS; z = SURF + vz * tt - 4.9 * tt * tt
        if z < SURF - 0.05: d.location = (0, 0, -3); d.keyframe_insert("location", frame=f); break
        d.location = (x0 + math.cos(a) * vh * tt, y0 + math.sin(a) * vh * tt, z); d.keyframe_insert("location", frame=f)

# ---------- ghost "seawater level" ring: where the bike would float in water ----------
M_GHOST = mat("ghost", (0.3, 0.6, 1.0), 0.2, 0, (0.3, 0.6, 1.0), 2.5)
bpy.ops.mesh.primitive_cube_add(size=1)
gh = bpy.context.object; gh.scale = (1.6, 0.004, 0.004); link(gh, M_GHOST)
gh.parent = None
for f in range(0, N + 1, 2):
    t = f / FPS
    on = 3.0 < t < 7.6
    gh.location = (bike_x(f), -0.12, SURF + (0.14 if on else -2)); gh.keyframe_insert("location", frame=f)

# ---------- blue flames (vapour above 26 C) ----------
flames = []
for k in range(7):
    m, noise, strength = flame_mat(f"flame{k}")
    bpy.ops.mesh.primitive_plane_add(size=1)
    fl = bpy.context.object; link(fl, m)
    fl.rotation_euler = (math.radians(90), 0, math.radians(random.uniform(-25, 25)))
    fl.scale = (random.uniform(1.0, 1.6), random.uniform(1.2, 1.9), 1.0)
    fl.location = (2.6 + k * 0.8 + random.uniform(-0.2, 0.2), 1.6 + random.uniform(0, 3.5), SURF + 0.7)
    noise.inputs["W"].default_value = 0; noise.inputs["W"].keyframe_insert("default_value", frame=0)
    noise.inputs["W"].default_value = 30; noise.inputs["W"].keyframe_insert("default_value", frame=N)
    st = strength.inputs[1]
    f_in = sec(7.9) + k * 3; f_out = sec(10.0) + k * 2
    for f, v in [(0, 0), (f_in, 0), (f_in + 8, 1), (f_out, 1), (f_out + 10, 0)]:
        st.default_value = v; st.keyframe_insert("default_value", frame=f)

# ---------- oil leaving the chain ----------
for k in range(60):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=random.uniform(0.004, 0.011))
    o = bpy.context.object; o.scale = (1.4, 1.4, 1.4); link(o, M_OIL, bike)
    base = stadium(random.random()) + Vector((0, random.uniform(-0.01, 0.01), 0))
    f0 = sec(11.4) + random.randint(0, 30); f1 = f0 + random.randint(28, 45)
    drift = Vector((random.uniform(-0.04, 0.04), random.uniform(-0.09, -0.02), random.uniform(0.05, 0.14)))
    o.location = base; o.scale = (0, 0, 0)
    o.keyframe_insert("scale", frame=0); o.keyframe_insert("scale", frame=f0 - 6)
    o.scale = (1.4, 1.4, 1.4); o.keyframe_insert("scale", frame=f0); o.keyframe_insert("location", frame=f0)
    o.location = base + drift; o.keyframe_insert("location", frame=f1)
    o.scale = (0, 0, 0); o.keyframe_insert("scale", frame=f1)

# ---------- camera ----------
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); S.collection.objects.link(cam); S.camera = cam
cam.data.lens = 30; cam.data.sensor_fit = "VERTICAL"; cam.data.sensor_height = 24
tgt = empty("tgt"); c = cam.constraints.new("TRACK_TO"); c.target = tgt
c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
cam.data.dof.use_dof = True; cam.data.dof.focus_object = tgt; cam.data.dof.aperture_fstop = 5.6
ringw = lambda f: Vector((bike_x(f), DY, bike_z(f) + 0.30))
KEYS = [  # (time, cam pos fn, target fn, lens, fstop)
    (0.0,  lambda f: Vector((-0.7, -3.3, 1.25)),  lambda f: Vector((0, 0, 0.55)), 30, 8),
    (1.4,  lambda f: Vector((-1.6, -3.6, 0.9)),  lambda f: Vector((bike_x(f) + 0.2, 0, 0.5)), 30, 8),
    (2.9,  lambda f: Vector((bike_x(f) - 0.4, -3.0, 0.62)), lambda f: Vector((bike_x(f) + 0.1, 0, 0.45)), 32, 8),
    (4.9,  lambda f: Vector((bike_x(f) - 0.2, -2.3, 0.52)), lambda f: Vector((bike_x(f), 0, 0.42)), 35, 6),
    (7.6,  lambda f: Vector((bike_x(f) - 0.75, -1.25, 0.38)), lambda f: Vector((bike_x(f) - 0.45, 0, 0.36)), 35, 4),
    (8.6,  lambda f: Vector((bike_x(f) - 1.4, -5.8, 2.1)), lambda f: Vector((bike_x(f) + 2.4, 2.2, 0.6)), 28, 11),
    (10.1, lambda f: Vector((bike_x(f) - 1.0, -5.0, 1.7)), lambda f: Vector((bike_x(f) + 2.4, 2.2, 0.6)), 28, 11),
    (11.2, lambda f: Vector((bike_x(f) - 0.05, -1.25, 0.62)), lambda f: ringw(f) + Vector((-0.24, 0, 0.02)), 35, 5),
    (13.6, lambda f: Vector((bike_x(f) - 0.18, -0.82, 0.48)), lambda f: ringw(f) + Vector((-0.24, 0, 0.02)), 35, 4),
    (15.1, lambda f: Vector((bike_x(f) - 0.2, -0.78, 0.47)), lambda f: ringw(f) + Vector((-0.24, 0, 0.02)), 35, 4),
]
def smooth(x): return x * x * (3 - 2 * x)
for f in range(0, N + 1):
    t = f / FPS
    for i in range(len(KEYS) - 1):
        if KEYS[i][0] <= t <= KEYS[i + 1][0]: break
    a, b = KEYS[i], KEYS[i + 1]
    u = smooth((t - a[0]) / (b[0] - a[0]))
    cam.location = a[1](f).lerp(b[1](f), u); cam.keyframe_insert("location", frame=f)
    tgt.location = a[2](f).lerp(b[2](f), u); tgt.keyframe_insert("location", frame=f)
    cam.data.lens = a[3] + (b[3] - a[3]) * u; cam.data.keyframe_insert("lens", frame=f)
    cam.data.dof.aperture_fstop = a[4] + (b[4] - a[4]) * u; cam.data.dof.keyframe_insert("aperture_fstop", frame=f)

# ---------- render ----------
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
f_a, f_b = (int(args[0]), int(args[1])) if len(args) >= 2 else (0, N - 1)
step = int(args[2]) if len(args) >= 3 else 1
import time
import os
for f in range(f_a, f_b + 1, step):
    if os.path.exists(f"/home/claude/reel/frames/{f:04d}.png") and "--force" not in sys.argv: continue
    S.frame_set(f)
    S.render.filepath = f"/home/claude/reel/frames/{f:04d}.png"
    t0 = time.time(); bpy.ops.render.render(write_still=True)
    print(f"frame {f} {time.time() - t0:.1f}s", flush=True)
