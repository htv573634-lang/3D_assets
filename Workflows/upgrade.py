import bpy
import os
import shutil

print("==================================================")
print("STARTING EXPORT SCRIPT (Blender 2.79b)")
print("==================================================")

blend_path = bpy.data.filepath
model_name = os.path.splitext(os.path.basename(blend_path))[0]
models_dir = os.path.dirname(blend_path)
repo_root = os.path.dirname(models_dir)
export_dir = os.path.join(repo_root, "Output")
os.makedirs(export_dir, exist_ok=True)

texture_path = os.path.join(models_dir, "Zuleyka_Skin.PNG")

# Delete the sword
if "Sword1" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Sword1"], do_unlink=True)
    print("Successfully deleted Sword1 object.")

# Select only the body mesh for OBJ export
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True
    print("Selected for export: {}".format(obj.name))

# Export OBJ with UVs but minimal material handling
obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        use_uvs=True,
        path_mode='RELATIVE'
    )
    print("OBJ exported: {}".format(obj_path))
except Exception as e:
    print("OBJ export FAILED: {}".format(e))

# Manually copy the texture file to Output folder
if os.path.exists(texture_path):
    shutil.copy(texture_path, os.path.join(export_dir, "Zuleyka_Skin.PNG"))
    print("Texture copied to Output folder.")
else:
    print("WARNING: Texture not found at {}".format(texture_path))

print("==================================================")
