import bpy
import os

# 1. Get the path of the current .blend file being processed
blend_path = bpy.data.filepath
if not blend_path:
    print("Error: Please run this script with a .blend file loaded.")
    exit()

# Extract the model name (e.g., "Zuleyka" from "Zuleyka.blend")
model_name = os.path.splitext(os.path.basename(blend_path))[0]

# 2. Define Paths dynamically based on the repo structure
models_dir = os.path.dirname(blend_path)
repo_root = os.path.dirname(models_dir)
export_dir = os.path.join(repo_root, "Output")

# Create Output directory if it doesn't exist
os.makedirs(export_dir, exist_ok=True)

print(f"--- Processing Model: {model_name} ---")

# 3. Deselect all objects and select all meshes
bpy.ops.object.select_all(action='DESELECT')
meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    obj.select_set(True)

if not meshes:
    print(f"Warning: No meshes found in {model_name}. Skipping export.")
    exit()

# 4. Export as OBJ
obj_path = os.path.join(export_dir, f"{model_name}.obj")
try:
    bpy.ops.wm.obj_export(
        filepath=obj_path,
        export_selected_objects=True,
        export_materials=True,
        path_mode='COPY'
    )
    print(f"[{model_name}] OBJ export successful.")
except AttributeError:
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        use_materials=True,
        path_mode='COPY'
    )
    print(f"[{model_name}] OBJ export successful (legacy).")

# 5. Export as GLB
glb_path = os.path.join(export_dir, f"{model_name}.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    use_selection=True,
    export_animations=True
)
print(f"[{model_name}] GLB export successful.")
print("Done!")
