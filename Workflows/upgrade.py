import bpy
import os

print("==================================================")
print("STARTING EXPORT SCRIPT (Blender 2.79b)")
print("==================================================")

# 1. Get paths
blend_path = bpy.data.filepath
model_name = os.path.splitext(os.path.basename(blend_path))[0]
models_dir = os.path.dirname(blend_path)
repo_root = os.path.dirname(models_dir)
export_dir = os.path.join(repo_root, "Output")
os.makedirs(export_dir, exist_ok=True)

# 2. Delete the sword
if "Sword1" in bpy.data.objects:
    obj = bpy.data.objects["Sword1"]
    bpy.data.objects.remove(obj, do_unlink=True)
    print("Successfully deleted Sword1 object.")
else:
    print("Sword1 not found, skipping deletion.")

# 3. Pack all textures (ensures Zuleyka_Skin.PNG is embedded)
try:
    bpy.ops.file.pack_all()
    print("Textures packed successfully.")
except Exception as e:
    print("Warning: Could not pack textures. {}".format(e))

# 4. Select only the body mesh for export
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        print("Selected for export: {}".format(obj.name))

# 5. Export OBJ with materials and copy the texture to the Output folder
obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        path_mode='COPY' # CRITICAL: This copies Zuleyka_Skin.PNG to the Output folder
    )
    print("OBJ exported successfully: {}".format(obj_path))
except Exception as e:
    print("OBJ export failed: {}".format(e))

print("==================================================")
