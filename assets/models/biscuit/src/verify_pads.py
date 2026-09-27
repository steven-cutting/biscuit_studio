"""Check sole-local edits, closed pad geometry, skinning, and ground clearance."""
import itertools
import math
from collections import Counter

from mathutils import Vector
from mathutils.bvhtree import BVHTree
from common import ROOT, bpy
import pose_io
import toe_beans


def check(original, spec, source_floor):
    result = {'pads': {}, 'paws': {}, 'ground': {}, 'approvedSourceGround': source_floor}
    for name in sorted(toe_beans.PAWS):
        ob = bpy.data.objects[name]
        old = original[name]
        vertices = [tuple(v.co) for v in ob.data.vertices]
        assert vertices[:len(old['vertices'])] == old['vertices'], ('Paw exterior moved', name)
        bottom = {i for i, p in enumerate(old['vertices']) if abs(p[2]) < 1e-6}
        retained = [i for i, f in enumerate(old['faces']) if not set(f).issubset(bottom)]
        offsets = [0]
        for face in old['faces']:
            offsets.append(offsets[-1]+len(face))
        for after, before in zip(ob.data.polygons, retained):
            assert tuple(after.vertices) == old['faces'][before]
            assert after.material_index == old['materialIndices'][before]
            assert after.use_smooth == old['smooth'][before]
            for layer, previous in zip(ob.data.uv_layers, old['uv']):
                assert [tuple(layer.data[i].uv) for i in after.loop_indices] == previous[offsets[before]:offsets[before+1]]
        assert [m.name for m in ob.data.materials] == old['materials']
        result['paws'][name] = dict(originalVerticesExact=len(old['vertices']), exteriorFacesExact=len(retained))
    trees = {}
    for name in sorted(toe_beans.PAD_NAMES):
        ob = bpy.data.objects[name]
        limb, side = name.split('.')[1:3]
        bone = limb.lower() + '.paw.' + side
        for v in ob.data.vertices:
            active = [(ob.vertex_groups[g.group].name, g.weight) for g in v.groups if g.weight > 0]
            assert active == [(bone, 1.)], (name, active)
            assert all(math.isfinite(x) for x in v.co)
        mesh = ob.data
        mesh.calc_loop_triangles()
        edges = Counter(tuple(sorted((a, b))) for p in mesh.polygons
                        for a, b in zip(p.vertices, (*p.vertices[1:], p.vertices[0])))
        assert all(count == 2 for count in edges.values()), ('Open pad mesh', name)
        assert all(t.area > 1e-12 for t in mesh.loop_triangles), ('Degenerate pad face', name)
        assert len(mesh.uv_layers) == 1
        positions = [tuple(v.co) for v in mesh.vertices]
        low = [min(p[i] for p in positions) for i in range(3)]
        high = [max(p[i] for p in positions) for i in range(3)]
        paw = original[f'Paw.{limb}.{side}']['vertices']
        for i in range(3):
            assert low[i] >= min(p[i] for p in paw)-1e-6, ('Pad outside paw bounds', name, i)
            assert high[i] <= max(p[i] for p in paw)+1e-6, ('Pad outside paw bounds', name, i)
        assert abs(low[2]) < 1e-6 and high[2] > toe_beans.RECESS+.005
        trees[name] = BVHTree.FromPolygons([Vector(p) for p in positions],
                                         [list(t.vertices) for t in mesh.loop_triangles], all_triangles=True)
        result['pads'][name] = dict(bone=bone, weight=1, closed=True, vertices=len(positions), bounds=[low, high])
    for a, b in itertools.combinations(sorted(trees), 2):
        if a.split('.')[1:3] == b.split('.')[1:3]:
            assert not trees[a].overlap(trees[b]), ('Pads intersect', a, b)
    for key in ('standing', 'sitting', 'lying', 'paw-raised'):
        pose_io.apply(spec, pose_io.load(spec, ROOT/'poses'/f'{key}.json'))
        minima = {}
        for name in sorted(toe_beans.PAWS | toe_beans.PAD_NAMES):
            ob = bpy.data.objects[name]
            ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
            mesh = ev.to_mesh()
            minima[name] = min((ev.matrix_world@v.co).z for v in mesh.vertices)
            ev.to_mesh_clear()
        # Compare all feet to the approved source. Its sitting forepaws already
        # sit below Z=0; changing that pose would violate pose compatibility.
        for name, minimum in minima.items():
            limb, side = name.split('.')[1:3]
            baseline = source_floor[key][f'Paw.{limb}.{side}']
            assert minimum >= baseline-1e-5, ('New ground penetration', key, name, minimum, baseline)
        result['ground'][key] = minima
    pose_io.apply(spec, pose_io.load(spec, ROOT/'poses/standing.json'))
    result.update(padCount=20, padsDoNotIntersect=True, noAdditionalGroundPenetration=True,
                  standingPadsClearFloor=True,
                  exteriorPawVerticesExact=True, rigVersion=spec['rigVersion'])
    return result
