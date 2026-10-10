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

# 3. Scale the model up by 400x (from mm to human scale)
print("Scaling model up by 400x...")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.scale = (400.0, 400.0, 400.0)
        bpy.context.scene.objects.active = obj
        obj.select = True
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.select = False

# 4. FORCE REBUILD THE MATERIAL (The fix for the black model!)
if os.path.exists(texture_path):
    print("Found texture. Rebuilding material for OBJ export...")
    try:
        img = bpy.data.images.load(texture_path)
        
        # Create a new Blender Internal material
        mat = bpy.data.materials.new(name="Zuleyka_Skin_Material")
        mat.use_nodes = False # Important for 2.79 OBJ exporter
        
        # Add a texture slot
        mat.texture_slots.add()
        tex_slot = mat.texture_slots[0]
        
        # Create the texture
        tex = bpy.data.textures.new(name="Zuleyka_Texture", type='IMAGE')
        tex.image = img
        
        # Link texture to diffuse channel
        tex_slot.texture = tex
        tex_slot.use_map_color_diffuse = True
        tex_slot.use_map_color_alpha = True # Handles hair transparency
        
        # Assign this new material to all meshes
        meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        for obj in meshes:
            obj.data.materials.clear()
            obj.data.materials.append(mat)
        print("Material rebuilt and assigned successfully.")
    except Exception as e:
        print("Failed to rebuild material: {}".format(e))
else:
    print("WARNING: Texture file not found! Cannot rebuild material.")

# 5. Select only the body mesh for export
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True
    print("Selected for export: {}".format(obj.name))

# 6. Export OBJ
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

# 7. Manually copy the texture to the Output folder
if os.path.exists(texture_path):
    try:
        shutil.copy(texture_path, os.path.join(export_dir, "Zuleyka_Skin.PNG"))
        print("Texture copied to Output folder successfully.")
    except Exception as e:
        print("Failed to copy texture: {}".format(e))

print("==================================================")q
