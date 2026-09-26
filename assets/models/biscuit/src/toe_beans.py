"""Shallow sole recesses and twenty independently editable, rigidly skinned pads.

The existing paw perimeter remains at Z=0. Only the bottom cap is replaced;
the pads sit inside the original envelope and reach the same contact plane.
"""
import math
import struct
import zlib

from mathutils import Vector
from common import ROOT, SOURCE, REPO_ROOT, bpy, legacy, sha, write_json
import rig as rigging

PAWS = {f'Paw.{limb}.{side}' for limb in ('Front', 'Hind') for side in ('L', 'R')}
PAD_NAMES = {f'PawPad.{limb}.{side}.{part}'
             for limb in ('Front', 'Hind') for side in ('L', 'R')
             for part in ('Central', 'Toe.1', 'Toe.2', 'Toe.3', 'Toe.4')}
RECESS = .022
COLOR = (73, 63, 60)  # sRGB #493f3c, warm charcoal.


def flat_map(path, rgb):
    """Write a constant PNG with no optional third-party Blender dependencies."""
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    size = 8
    scanlines = (b'\0' + bytes(rgb) * size) * size
    path.write_bytes(b'\x89PNG\r\n\x1a\n' +
                     chunk(b'IHDR', struct.pack('>2I5B', size, size, 8, 2, 0, 0, 0)) +
                     chunk(b'IDAT', zlib.compress(scanlines)) + chunk(b'IEND', b''))


def material():
    # The established cel shader lights textured materials in both renderers.
    # Neutral maps give the beans smooth form without fur grain or shiny spots.
    for kind, rgb in {'color': COLOR, 'normal': (128, 128, 255),
                      'roughness': (217, 217, 217), 'occlusion': (255, 255, 255)}.items():
        flat_map(ROOT / 'textures' / f'paw-pad-{kind}.png', rgb)
    return legacy.c.material('PawPads.WarmCharcoal', texture='paw-pad', gloss=False)


def recess_sole(ob):
    source = ob.data
    group_names = [g.name for g in ob.vertex_groups]
    bottom = {v.index for v in source.vertices if abs(v.co.z) < 1e-6}
    assert len(bottom) == 10, ('Unexpected sole perimeter', ob.name)
    kept = [p for p in source.polygons if not set(p.vertices).issubset(bottom)]
    center = sum((source.vertices[i].co for i in bottom), Vector()) / len(bottom)
    rim = sorted(bottom, key=lambda i: math.atan2(source.vertices[i].co.y-center.y,
                                                source.vertices[i].co.x-center.x))
    vertices = [tuple(v.co) for v in source.vertices]
    original_count = len(vertices)
    faces = [tuple(p.vertices) for p in kept]
    original_faces = len(faces)
    # An inset ramp keeps the original contact perimeter, with a raised inner
    # sole exposing the lower half of each bean. -Z is outward on the sole.
    inset = []
    for index in rim:
        p = center + (source.vertices[index].co-center)*.90
        p.z = RECESS
        inset.append(len(vertices))
        vertices.append(tuple(p))
    for j, index in enumerate(rim):
        k = (j+1) % len(rim)
        faces.append((rim[k], index, inset[j], inset[k]))
    # Triangulate the inner cap explicitly, retaining stable packed tangents.
    cap_center = len(vertices)
    vertices.append((center.x, center.y, RECESS))
    for j, index in enumerate(inset):
        faces.append((inset[(j+1) % len(inset)], index, cap_center))
    mesh = bpy.data.meshes.new(ob.name + '.RecessedSole')
    mesh.from_pydata(vertices, [], faces)
    for mat in source.materials:
        mesh.materials.append(mat)
    for p, before in zip(mesh.polygons, kept):
        p.material_index = before.material_index
        p.use_smooth = before.use_smooth
    for p in list(mesh.polygons)[original_faces:]:
        p.use_smooth = True
    # Keep every upper/side UV and corner normal exactly as authored.
    for layer in source.uv_layers:
        uv = mesh.uv_layers.new(name=layer.name)
        for after, before in zip(mesh.polygons, kept):
            for a, b in zip(after.loop_indices, before.loop_indices):
                uv.data[a].uv = layer.data[b].uv
        for p in list(mesh.polygons)[original_faces:]:
            for li in p.loop_indices:
                point = Vector(vertices[mesh.loops[li].vertex_index]) - center
                uv.data[li].uv = (.5+point.x, .5+point.y)
    mesh.update()
    normals = [tuple(n.vector) for n in mesh.corner_normals]
    for after, before in zip(mesh.polygons, kept):
        for a, b in zip(after.loop_indices, before.loop_indices):
            normals[a] = tuple(source.corner_normals[b].vector)
    mesh.normals_split_custom_set(normals)
    ob.data = mesh
    for name in group_names:
        if name not in ob.vertex_groups:
            ob.vertex_groups.new(name=name)
    bone = ('front' if '.Front.' in ob.name else 'hind') + '.paw.' + ob.name[-1]
    ob.vertex_groups[bone].add(list(range(len(vertices))), 1., 'REPLACE')
    contour = bpy.data.objects.get(ob.name + '.Contour')
    if contour:
        contour.data = mesh
        for name in group_names:
            if name not in contour.vertex_groups:
                contour.vertex_groups.new(name=name)
    ob['construction'] = 'Approved paw exterior; locally recessed sole for foot pads'
    # Use the unmodified sole's radii; hind paws are a little narrower.
    rx = max(abs(source.vertices[i].co.x-center.x) for i in bottom) / math.cos(math.pi/10)
    ry = max(abs(source.vertices[i].co.y-center.y) for i in bottom)
    return center, rx, ry, dict(originalVertices=original_count, retainedExteriorFaces=original_faces,
                               removedSoleFaces=len(source.polygons)-original_faces, recessDepth=RECESS)


def bean(name, center, radii, mat, angle=0., central=False):
    """Closed rounded volume, with a softly triangular central-pad footprint."""
    cx, cy, cz = center
    rx, ry, rz = radii
    def shape(p):
        x, y, z = p
        if central:
            theta = math.atan2(x/rx, -y/ry)
            f = 1 + .13 * math.cos(3*theta)
            x *= f
            y *= f
        return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle), z)
    ob = legacy.c.ellipsoid(name, (cx, cy, cz), radii, mat, ns=32, nr=16,
                           deform=shape, group='02 Limbs', outline=False)
    ob['construction'] = 'Softly sculpted central foot pad' if central else 'Softly sculpted toe pad'
    return ob


def add(rig, spec):
    mat = material()
    added = []
    edited = {}
    for name in sorted(PAWS):
        paw = bpy.data.objects[name]
        center, rx, ry, record = recess_sole(paw)
        limb, side = name.split('.')[1:]
        prefix = f'PawPad.{limb}.{side}'
        sign = 1 if side == 'L' else -1
        # The two middle toes lead the outside pair. Layout mirrors across X.
        layout = [(-.61, -.30, -.27, .185, .205), (-.23, -.61, -.10, .19, .215),
                  (.23, -.61, .10, .19, .215), (.61, -.30, .27, .185, .205)]
        for i, (x, y, angle, width, length) in enumerate(layout, 1):
            z = .017
            ob = bean(f'{prefix}.Toe.{i}', (center.x+sign*x*rx, center.y+y*ry, z),
                      (rx*width, ry*length, z), mat, sign*angle)
            added.append(ob)
        z = .020
        added.append(bean(f'{prefix}.Central', (center.x, center.y+.28*ry, z),
                          (rx*.56, ry*.42, z), mat, central=True))
        edited[name] = record
    # New pads use the same coordinate system and single-bone weights as paws.
    rigging.prepare_meshes(added)
    rigging.bind(added, rig, spec)
    assert {ob.name for ob in added} == PAD_NAMES
    write_json(ROOT/'qa/change-manifest.json', dict(
        source=str(SOURCE.relative_to(REPO_ROOT)), sourceSha256=sha(SOURCE),
        status='approved', modified=edited, added=sorted(PAD_NAMES),
        padColorSRGB='#493f3c', roughness=217/255,
        restSkeletonChanged=False, savedPosesChanged=False))
    return added
