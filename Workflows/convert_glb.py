import bpy
import os
import sys

# Get input and output paths from command line
argv = sys.argv
argv = argv[argv.index("--") + 1:]
obj_path = argv[0]
glb_path = argv[1]

print("Converting {} to {}".format(obj_path, glb_path))

# Clear the default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import OBJ using Blender 4.0 API
try:
    bpy.ops.wm.obj_import(filepath=obj_path)
    print("OBJ imported successfully.")
except AttributeError:
    bpy.ops.import_scene.obj(filepath=obj_path)
    print("OBJ imported successfully (Legacy API).")

# Scale the model up by 400x (safe here, no armature to break)
print("Scaling model up by 400x...")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.scale = (400.0, 400.0, 400.0)

# Force-create a brand-new material with the texture
texture_path = os.path.join(os.path.dirname(obj_path), "Zuleyka_Skin.PNG")
if os.path.exists(texture_path):
    print("Applying texture from: {}".format(texture_path))
    try:
        img = bpy.data.images.load(texture_path)
        
        # Create a modern Principled BSDF material
        mat = bpy.data.materials.new(name="Zuleyka_Material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        tex_node = nodes.new(type='ShaderNodeTexImage')
        tex_node.image = img
        
        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign to all meshes
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                obj.data.materials.append(mat)
        print("Material successfully assigned.")
    except Exception as e:
        print("Failed to assign material: {}".format(e))
else:
    print("Warning: Texture not found at {}".format(texture_path))

# Export as GLB with textures embedded
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
