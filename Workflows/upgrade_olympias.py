import bpy
import os

print("==================================================")
print("STARTING OLYMPIAS EXPORT SCRIPT (Blender 2.79b)")
print("==================================================")

# 1. Get paths
blend_path = bpy.data.filepath
model_name = os.path.splitext(os.path.basename(blend_path))[0]
models_dir = os.path.dirname(blend_path)
repo_root = os.path.dirname(models_dir)
export_dir = os.path.join(repo_root, "Output")
os.makedirs(export_dir, exist_ok=True)

# 2. Delete Scene Clutter specifically for Olympias
objects_to_delete = ["Backdrop", "Podium", "TestCamera", "Camera", "RightFill", "LeftFill", "BackLight", "FrontLamp", "CameraTarget", "BeadsPath", "BezierCircle", "NurbsPath", "SnakePath.001"]
for obj_name in objects_to_delete:
    if obj_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)
        print("Deleted scene object: {}".format(obj_name))

# 3. Select only the remaining meshes for OBJ export
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True

print("Exporting {} meshes.".format(len(meshes)))

# 4. Export OBJ
obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    # path_mode='COPY' extracts the packed textures to the Output folder
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        use_uvs=True,
        path_mode='COPY' 
    )
    print("OBJ exported successfully: {}".format(obj_path))
except Exception as e:
    print("OBJ export FAILED: {}".format(e))

print("==================================================")
