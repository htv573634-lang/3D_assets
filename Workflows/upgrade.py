import bpy
import os

print("==================================================")
print("STARTING UPGRADE SCRIPT (Blender 2.79)")
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

# 3. Pack all textures (requires Zuleyka_Skin.PNG to be in Models/)
try:
    bpy.ops.file.pack_all()
    print("Textures packed successfully.")
except Exception as e:
    print("Warning: Could not pack textures. {}".format(e))

# 4. Save the clean, upgraded file
new_blend_path = os.path.join(export_dir, "{}_clean.blend".format(model_name))
bpy.ops.wm.save_as_mainfile(filepath=new_blend_path)
print("Saved clean, modernized file to: {}".format(new_blend_path))
print("==================================================")
