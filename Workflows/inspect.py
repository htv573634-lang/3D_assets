import bpy

print("="*50)
print("BLEND FILE INSPECTION REPORT")
print("="*50)

# 1. Scene Objects
print("\n--- SCENE OBJECTS ---")
for obj in bpy.context.scene.objects:
    print(f"Object: '{obj.name}' | Type: {obj.type}")
    if obj.type == 'MESH':
        print(f"   -> Vertices: {len(obj.data.vertices)} | Polygons: {len(obj.data.polygons)}")
        mats = [mat.name for mat in obj.data.materials if mat]
        print(f"   -> Materials: {mats}")
    elif obj.type == 'ARMATURE':
        print(f"   -> Bones: {len(obj.data.bones)}")

# 2. Materials and their Textures
print("\n--- MATERIALS & TEXTURES ---")
for mat in bpy.data.materials:
    print(f"Material: '{mat.name}'")
    if mat.use_nodes:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                img = node.image
                packed_status = "Packed" if img.packed_file else "NOT Packed (Missing!)"
                print(f"   -> Image: '{img.name}' | Path: '{img.filepath}' | Status: {packed_status}")

# 3. All Images in the file
print("\n--- ALL IMAGES ---")
for img in bpy.data.images:
    packed_status = "Packed" if img.packed_file else "NOT Packed (Missing!)"
    print(f"Image: '{img.name}' | Path: '{img.filepath}' | Status: {packed_status}")

# 4. Animations / Actions
print("\n--- ANIMATIONS (ACTIONS) ---")
for action in bpy.data.actions:
    print(f"Action: '{action.name}' | Frame Range: {action.frame_range[0]:.0f} to {action.frame_range[1]:.0f}")

print("="*50)
print("END OF REPORT")
print("="*50)
