import bpy
import os
import shutil

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

texture_path = os.path.join(models_dir, "Zuleyka_Skin.PNG")
print("Looking for texture at: {}".format(texture_path))

# 2. Delete the sword
if "Sword1" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Sword1"], do_unlink=True)
    print("Successfully deleted Sword1 object.")
else:
    print("Sword1 not found, skipping deletion.")

# 3. Pack all textures
try:
    bpy.ops.file.pack_all()
    print("Textures packed successfully.")
except Exception as e:
    print("Warning: Could not pack textures. {}".format(e))

# 4. Select only the body mesh (Using Blender 2.79 API syntax)
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True  # <--- FIXED: Changed from select_set(True)
    print("Selected for export: {}".format(obj.name))

# 5. Export OBJ
obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        path_mode='RELATIVE' 
    )
    print("OBJ exported successfully: {}".format(obj_path))
except Exception as e:
    print("OBJ export FAILED: {}".format(e))

# 6. Manually copy the texture to the Output folder
if os.path.exists(texture_path):
    try:
        shutil.copy(texture_path, os.path.join(export_dir, "Zuleyka_Skin.PNG"))
        print("Texture copied to Output folder successfully.")
    except Exception as e:
        print("Failed to copy texture: {}".format(e))
else:
    print("WARNING: Texture not found in Models folder! Cannot copy to Output.")

print("==================================================")
