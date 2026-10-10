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

# 2. Delete Scene Clutter AND Floating Artifact Objects
objects_to_delete = [
    # Scene Clutter
    "Backdrop", "Podium", "TestCamera", "Camera", "RightFill", "LeftFill", 
    "BackLight", "FrontLamp", "CameraTarget",
    # Floating Curve/Path Artifacts (The dashed lines and rods)
    "BeadsPath", "BezierCircle", "NurbsPath", "SnakeWidth", 
    "SnakePath.001", "SnakePath", "Circle.001", "Circle",
    # Beads and Threads
    "BeadsEmmiter", "BeadsIron2", "BeadsIron1", "Bead2", "Bead1",
    "ThreadThingy.012", "ThreadThingy.011", "ThreadThingy.010", 
    "ThreadThingy.009", "ThreadThingy.008", "ThreadThingy.007", 
    "ThreadThingy.006", "ThreadThingy.005", "ThreadThingy",
    "Clasp.002", "Clasp.001"
]

for obj_name in objects_to_delete:
    if obj_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[obj_name], do_unlink=True)
        print("Deleted artifact object: {}".format(obj_name))

# 3. Unpack all packed textures to the Output folder
print("Unpacking textures...")
bpy.ops.file.unpack_all(method='WRITE_LOCAL')
print("Textures unpacked.")

# 4. Select only the remaining character meshes for OBJ export
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True

print("Exporting {} meshes.".format(len(meshes)))

# 5. Export OBJ
obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    # path_mode='COPY' extracts the unpacked textures to the Output folder
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
