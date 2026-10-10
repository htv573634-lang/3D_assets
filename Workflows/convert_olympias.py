import bpy
import os
import sys

# Get input and output paths from command line
argv = sys.argv
argv = argv[argv.index("--") + 1:]
obj_path = argv[0]
glb_path = argv[1]

print("Converting Olympias {} to {}".format(obj_path, glb_path))

# Clear the default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import OBJ
try:
    bpy.ops.wm.obj_import(filepath=obj_path)
    print("OBJ imported successfully.")
except AttributeError:
    bpy.ops.import_scene.obj(filepath=obj_path)
    print("OBJ imported successfully (Legacy API).")

# Scale the model (Olympias is a high-poly realistic model)
# If she appears too small in your viewer, adjust these numbers.
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.scale = (10.0, 10.0, 10.0)

# Export as GLB
try:
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        export_materials='EXPORT',
        export_image_format='AUTO'
    )
    print("GLB exported successfully.")
except Exception as e:
    print("GLB export FAILED: {}".format(e))

print("Conversion complete!")
