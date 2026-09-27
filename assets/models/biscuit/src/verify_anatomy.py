"""Check the rear joint layout and ground contact of the supplied poses."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, bpy, json, parts, write_json
import pose_io


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/biscuit-poseable.blend'))
    spec = json.loads((ROOT/'model/rig.json').read_text())
    bones = bpy.data.objects['Biscuit.Rig'].data.bones
    joints = {}
    for side in ('L', 'R'):
        thigh, shin, hock, paw = [bones[f'hind.{part}.{side}'] for part in ('thigh', 'shin', 'hock', 'paw')]
        hip, knee, heel, ankle, toe = (thigh.head_local, shin.head_local, hock.head_local, paw.head_local, paw.tail_local)
        # -Y is forward; the knee leads the hip, then the shin slopes back.
        assert knee.y < hip.y and heel.y > knee.y
        assert hip.z > knee.z > heel.z > ankle.z > toe.z
        assert 0.8 < thigh.length/shin.length < 1.25
        assert hock.length < shin.length*0.6
        assert abs(heel.y-ankle.y) < 0.03
        assert toe.y < ankle.y
        # Rear legs remain parallel in the standing pose rather than toeing out.
        assert abs(toe.x-ankle.x) < 0.01
        joints[side] = dict(hip=list(hip), knee=list(knee), hock=list(heel),
            ankle=list(ankle), toe=list(toe), thighShinRatio=thigh.length/shin.length,
            hockShinRatio=hock.length/shin.length)
    for name in ('hip', 'knee', 'hock', 'ankle', 'toe'):
        left, right = joints['L'][name], joints['R'][name]
        assert abs(left[0]+right[0]) < 1e-6
        assert max(abs(left[i]-right[i]) for i in (1, 2)) < 1e-6

    rear = [ob for ob in parts() if ob.name.startswith('Hindleg.') or '.Hind.' in ob.name]
    contact = {}
    for key in ('standing', 'sitting', 'lying', 'paw-raised'):
        pose_io.apply(spec, pose_io.load(spec, ROOT/'poses'/f'{key}.json'))
        floor = {}
        for ob in rear:
            ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get())
            mesh = ev.to_mesh()
            floor[ob.name] = min((ev.matrix_world@v.co).z for v in mesh.vertices)
            ev.to_mesh_clear()
        assert min(floor.values()) >= -1e-5, (key, floor)
        assert all(abs(floor[f'Paw.Hind.{side}']) < 0.01 for side in ('L', 'R')), (key, floor)
        contact[key] = floor
    write_json(ROOT/'qa/anatomy-verification.json', dict(
        rearJointLayout=joints, rearSurfaceMinimumZ=contact,
        symmetricStandingJoints=True, parallelStandingFeet=True,
        suppliedPosesClearFloor=True, rearPawGroundTolerance=0.01))
    print('Rear joint layout and ground-contact checks passed.', flush=True)


if __name__ == '__main__':
    main()
