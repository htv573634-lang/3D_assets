import bpy

print("="*50)
print("BLEND FILE INSPECTION REPORT")
print("="*50)

# 1. Scene Objects
print("\n--- SCENE OBJECTS ---")
for obj in bpy.context.scene.objects:
    print("Object: '{}' | Type: {}".format(obj.name, obj.type))
    if obj.type == 'MESH':
        print("   -> Vertices: {} | Polygons: {}".format(len(obj.data.vertices), len(obj.data.polygons)))
        mats = [mat.name for mat in obj.data.materials if mat]
        print("   -> Materials: {}".format(mats))
    elif obj.type == 'ARMATURE':
        print("   -> Bones: {}".format(len(obj.data.bones)))

# 2. Materials and their Textures
print("\n--- MATERIALS & TEXTURES ---")
for mat in bpy.data.materials:
    print("Material: '{}'".format(mat.name))
    if mat.use_nodes:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                img = node.image
                packed_status = "Packed" if img.packed_file else "NOT Packed (Missing!)"
                print("   -> Image: '{}' | Path: '{}' | Status: {}".format(img.name, img.filepath, packed_status))

# 3. All Images in the file
print("\n--- ALL IMAGES ---")
for img in bpy.data.images:
    packed_status = "Packed" if img.packed_file else "NOT Packed (Missing!)"
    print("Image: '{}' | Path: '{}' | Status: {}".format(img.name, img.filepath, packed_status))

# 4. Animations / Actions
print("\n--- ANIMATIONS (ACTIONS) ---")
for action in bpy.data.actions:
    print("Action: '{}' | Frame Range: {:.0f} to {:.0f}".format(action.name, action.frame_range[0], action.frame_range[1]))

print("="*50)
print("END OF REPORT")
print("="*50)
