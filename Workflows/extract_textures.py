import bpy
import os
import shutil

print("==================================================")
print("STARTING PURE TEXTURE EXTRACTION")
print("==================================================")

# 1. Get paths
blend_path = bpy.data.filepath
models_dir = os.path.dirname(blend_path)
repo_root = os.path.dirname(models_dir)
export_dir = os.path.join(repo_root, "Output", "Textures")
os.makedirs(export_dir, exist_ok=True)

print("Extracting to: {}".format(export_dir))

# 2. Loop through all images in the blend file
for img in bpy.data.images:
    # Skip Blender internal images like 'Render Result'
    if img.name in ['Render Result', 'Viewer Node']:
        continue
        
    # Determine the filename
    if img.filepath:
        filename = os.path.basename(img.filepath)
    else:
        filename = img.name + ".png"
        
    # Clean up filename
    filename = "".join([c for c in filename if c.isalnum() or c in "._- "])
    if not filename:
        filename = "texture_" + str(len(os.listdir(export_dir))) + ".png"

    new_path = os.path.join(export_dir, filename)
    
    try:
        if img.packed_file:
            # Force save the packed image to the new location
            img.filepath_raw = new_path
            # Keep original format if possible, otherwise default to PNG
            if img.file_format not in ['PNG', 'JPEG', 'TARGA', 'TIFF', 'BMP']:
                img.file_format = 'PNG'
            img.save()
            print("Saved packed image: {}".format(filename))
        else:
            # If it's not packed, try to copy it from the original location
            src = bpy.path.abspath(img.filepath)
            if os.path.exists(src):
                shutil.copy(src, new_path)
                print("Copied external image: {}".format(filename))
            else:
                print("Warning: Image missing and not packed: {}".format(img.name))
    except Exception as e:
        print("Failed to extract {}: {}".format(filename, e))

print("==================================================")
print("TEXTURE EXTRACTION COMPLETE")
print("==================================================")
