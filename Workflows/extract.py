import bpy
import os
import addon_utils

print("==================================================")
print("STARTING EXTRACTION SCRIPT (Blender 4.0)")
print("==================================================")

# 1. Enable GLTF exporter
try:
    addon_utils.enable("io_scene_gltf2")
except Exception as e:
    print("Failed to enable GLTF addon: {}".format(e))

# 2. Get paths
blend_path = bpy.data.filepath
# Remove the "_clean" suffix so the final files are just named "Zuleyka"
model_name = os.path.splitext(os.path.basename(blend_path))[0].replace("_clean", "")
repo_root = os.path.dirname(os.path.dirname(blend_path))
export_dir = os.path.join(repo_root, "Output")

# 3. Select all mesh objects (which is now just the body)
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select_set(True)
    print("Selected object for export: {}".format(obj.name))

if not meshes:
    print("Error: No meshes found. Exiting.")
    exit()

# 4. Export as OBJ
obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    bpy.ops.wm.obj_export(
        filepath=obj_path,
        export_selected_objects=True,
        export_materials=True,
        path_mode='COPY'
    )
    print("OBJ exported: {}".format(obj_path))
except AttributeError:
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        path_mode='COPY'
    )
    print("OBJ exported (legacy): {}".format(obj_path))

# 5. Export as GLB
glb_path = os.path.join(export_dir, "{}.glb".format(model_name))
try:
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=True,
        export_animations=True
    )
    print("GLB exported: {}".format(glb_path))
except Exception as e:
    print("GLB export FAILED: {}".format(e))

# 6. Clean up the intermediate _clean blend file so it doesn't clutter the repo
if os.path.exists(blend_path) and "_clean" in blend_path:
    os.remove(blend_path)
    print("Removed temporary clean blend file.")

print("==================================================")
