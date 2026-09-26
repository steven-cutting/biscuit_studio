"""Render the supplied still poses with the approved native materials and lights."""
from pathlib import Path
import hashlib
import json
import math
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import pose_io


def pose_renders():
    path = ROOT / 'model/biscuit-poseable.blend'
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    bpy.ops.wm.open_mainfile(filepath=str(path))
    spec = json.loads((ROOT / 'model/rig.json').read_text())
    scene = bpy.context.scene
    camera = bpy.data.objects.new('PoseReview.Camera', bpy.data.cameras.new('PoseReview.Camera'))
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.data.type = 'ORTHO'
    scene.render.resolution_x = scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.view_layers[0].material_override = None
    output = ROOT / 'previews/native'
    output.mkdir(parents=True, exist_ok=True)
    for name in ('standing', 'sitting', 'lying', 'paw-raised'):
        pose_io.apply(spec, pose_io.load(spec, ROOT / 'poses' / (name + '.json')))
        points = []
        graph = bpy.context.evaluated_depsgraph_get()
        for ob in scene.objects:
            if ob.type != 'MESH' or not ob.get('base_part'):
                continue
            ev = ob.evaluated_get(graph)
            mesh = ev.to_mesh()
            points.extend(ob.matrix_world @ v.co for v in mesh.vertices)
            ev.to_mesh_clear()
        low = Vector([min(p[i] for p in points) for i in range(3)])
        high = Vector([max(p[i] for p in points) for i in range(3)])
        target = (low + high) / 2
        yaw, pitch = .85, .32
        camera.location = target + Vector((9 * math.sin(yaw) * math.cos(pitch),
            -9 * math.cos(yaw) * math.cos(pitch), 9 * math.sin(pitch)))
        camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
        rotation = camera.rotation_euler.to_matrix().transposed()
        projected = [rotation @ (p - target) for p in points]
        camera.data.ortho_scale = 2 * max(abs(p[i]) for p in projected for i in (0, 1)) * 1.22
        scene.render.filepath = str(output / (name + '.png'))
        bpy.ops.render.render(write_still=True)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    print('Four native pose renders complete; saved scene unchanged.', flush=True)


def review_renders():
    from common import SOURCE
    candidate = ROOT/'model/biscuit-poseable.blend'
    hashes = {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (SOURCE,candidate)}
    output = ROOT/'previews/comparison'
    output.mkdir(parents=True,exist_ok=True)
    spec = json.loads((ROOT/'model/rig.json').read_text())
    review = pose_io.from_controls(spec,dict(front_upper_L=35,front_lower_L=-100,
                                            front_paw_L=-25,head_tilt=-6),'Toe bean review')
    review['viewer'].update(yaw=.25,pitch=.12,zoom=3.4)
    (ROOT/'qa/toe-bean-review-pose.json').write_text(json.dumps(review,indent=2)+'\n')
    for version,path in (('before',SOURCE),('after',candidate)):
        bpy.ops.wm.open_mainfile(filepath=str(path))
        scene = bpy.context.scene
        camera = bpy.data.objects.new('PadReview.Camera',bpy.data.cameras.new('PadReview.Camera'))
        scene.collection.objects.link(camera)
        scene.camera = camera
        camera.data.type = 'ORTHO'
        scene.render.resolution_x = scene.render.resolution_y = 1000
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGBA'
        scene.view_layers[0].material_override = None
        # A broad underside fill makes the matte relief legible in the study.
        # It is identical for the two versions and is never saved to the model.
        fill = bpy.data.objects.new('PadReview.Fill',bpy.data.lights.new('PadReview.Fill','AREA'))
        scene.collection.objects.link(fill)
        fill.location = (-1,-2,-3)
        fill.rotation_euler = (Vector((0,0,.3))-fill.location).to_track_quat('-Z','Y').to_euler()
        fill.data.energy = 160
        fill.data.shape = 'DISK'
        fill.data.size = 3
        visible = {ob.name:ob.hide_render for ob in scene.objects}
        views = [
            ('front-sole','Front',Vector((.275,-.725,.05)),Vector((.13,-.20,-1)),.43),
            ('hind-sole','Hind',Vector((.30,1.142,.05)),Vector((.13,-.20,-1)),.43),
            ('all-soles',None,Vector((0,.20,1.0)),Vector((.08,-.05,-1)),2.60),
            ('paw-presented',None,Vector((0,.05,1.4)),Vector((.25,-1,.13)),3.70),
        ]
        for key,limb,target,direction,scale in views:
            pose_io.apply(spec,review if key=='paw-presented' else pose_io.load(spec,ROOT/'poses/standing.json'))
            for ob in scene.objects:
                ob.hide_render = visible.get(ob.name,False)
                if limb and ob.type=='MESH' and (ob.get('base_part') or ob.name.endswith('.Contour')):
                    ob.hide_render = f'.{limb}.L' not in ob.name
            camera.location = target + direction.normalized()*8
            camera.rotation_euler = (target-camera.location).to_track_quat('-Z','Y').to_euler()
            camera.data.ortho_scale = scale
            scene.render.filepath = str(output/f'{version}-{key}.png')
            bpy.ops.render.render(write_still=True)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest()==digest for p,digest in hashes.items())
    print('Eight matched toe-bean comparison renders complete.',flush=True)


if __name__ == '__main__':
    if '--review-only' not in sys.argv:
        pose_renders()
    review_renders()
