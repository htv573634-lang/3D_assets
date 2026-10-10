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

# Updated to lowercase .png
texture_path = os.path.join(models_dir, "Zuleyka_Skin.png")

# 2. Delete the sword
if "Sword1" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Sword1"], do_unlink=True)
    print("Successfully deleted Sword1 object.")

# 3. Select body mesh and export OBJ (No scaling, No armature applied)
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True

obj_path = os.path.join(export_dir, "{}.obj".format(model_name))
try:
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        use_uvs=True,
        path_mode='RELATIVE' 
    )
    print("OBJ exported successfully: {}".format(obj_path))
except Exception as e:
    print("OBJ export FAILED: {}".format(e))

# 4. FORCE WRITE A PERFECT MTL FILE
# Updated to lowercase .png
mtl_path = os.path.join(export_dir, "{}.mtl".format(model_name))
mtl_content = """newmtl Zuleyka_Skin_Material
Ka 1.000 1.000 1.000
Kd 1.000 1.000 1.000
Ks 0.000 0.000 0.000
d 1.0
illum 2
map_Kd Zuleyka_Skin.png
"""
try:
    with open(mtl_path, "w") as f:
        f.write(mtl_content)
    print("Manually wrote perfect MTL file.")
except Exception as e:
    print("Failed to write MTL file: {}".format(e))

# 5. Manually copy the texture (Updated to lowercase .png)
if os.path.exists(texture_path):
    shutil.copy(texture_path, os.path.join(export_dir, "Zuleyka_Skin.png"))
    print("Texture copied to Output folder.")

print("==================================================")
