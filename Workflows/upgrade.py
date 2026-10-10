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

# 3. Scale the model up by 400x
print("Scaling model up by 400x...")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.scale = (400.0, 400.0, 400.0)
        bpy.context.scene.objects.active = obj
        obj.select = True
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.select = False

# 4. FIX HANDS: Apply Armature Modifier to freeze the T-pose
print("Applying armature to fix hands...")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.scene.objects.active = obj
        obj.select = True
        for mod in obj.modifiers:
            if mod.type == 'ARMATURE':
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                    print("Applied armature modifier to: {}".format(obj.name))
                except Exception as e:
                    print("Could not apply modifier: {}".format(e))
        
        # Smooth the mesh so it doesn't look like a sharp plank
        bpy.ops.object.shade_smooth()
        obj.select = False

# 5. FORCE UV UNWRAPPING
print("Forcing UV unwrap...")
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.scene.objects.active = obj
        obj.select = True
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.select = False
        print("UV Unwrapped: {}".format(obj.name))

# 6. FORCE REBUILD THE MATERIAL
if os.path.exists(texture_path):
    print("Rebuilding material with texture...")
    try:
        img = bpy.data.images.load(texture_path)
        mat = bpy.data.materials.new(name="Zuleyka_Skin_Material")
        mat.use_nodes = False
        mat.texture_slots.add()
        tex_slot = mat.texture_slots[0]
        tex = bpy.data.textures.new(name="Zuleyka_Texture", type='IMAGE')
        tex.image = img
        tex_slot.texture = tex
        tex_slot.use_map_color_diffuse = True
        tex_slot.use_map_color_alpha = True
        
        meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        for obj in meshes:
            obj.data.materials.clear()
            obj.data.materials.append(mat)
        print("Material assigned.")
    except Exception as e:
        print("Failed to rebuild material: {}".format(e))

# 7. Select only the body mesh for export
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select = True

# 8. Export OBJ
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

# 9. FORCE WRITE A PERFECT MTL FILE
mtl_path = os.path.join(export_dir, "{}.mtl".format(model_name))
mtl_content = """newmtl Zuleyka_Skin_Material
Ka 1.000 1.000 1.000
Kd 1.000 1.000 1.000
Ks 0.000 0.000 0.000
d 1.0
illum 2
map_Kd Zuleyka_Skin.PNG
"""
try:
    with open(mtl_path, "w") as f:
        f.write(mtl_content)
    print("Manually wrote perfect MTL file.")
except Exception as e:
    print("Failed to write MTL file: {}".format(e))

# 10. Manually copy the texture
if os.path.exists(texture_path):
    shutil.copy(texture_path, os.path.join(export_dir, "Zuleyka_Skin.PNG"))
    print("Texture copied to Output folder.")

print("==================================================")
