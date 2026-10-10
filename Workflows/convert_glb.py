import bpy
import os
import sys

# Get the input and output paths from the command line arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
obj_path = argv[0]
glb_path = argv[1]

print("Converting {} to {}".format(obj_path, glb_path))

# Clear the default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the OBJ file (Blender 4.0+ API syntax)
try:
    # New Blender 4.0 importer
    bpy.ops.wm.obj_import(filepath=obj_path)
    print("OBJ imported successfully (New API).")
except AttributeError:
    # Fallback for older Blender versions
    bpy.ops.import_scene.obj(filepath=obj_path)
    print("OBJ imported successfully (Legacy API).")

# Export as GLB with textures embedded
try:
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        export_materials=True,
        export_image_format='AUTO'
    )
    print("GLB exported successfully.")
except Exception as e:
    print("GLB export FAILED: {}".format(e))

print("Conversion complete!")
