import os
import random
import shutil

# Path to your no_human folder
source_folder = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\coco\no_human"

# Target number
target_count = 25000

# Get all images
all_images = os.listdir(source_folder)

print(f"Total images before: {len(all_images)}")

# Shuffle randomly
random.shuffle(all_images)

# Select only 25000
images_to_keep = all_images[:target_count]

# Create temp folder
temp_folder = os.path.join(source_folder, "temp")
os.makedirs(temp_folder, exist_ok=True)

# Move selected images to temp
for img in images_to_keep:
    src = os.path.join(source_folder, img)
    dst = os.path.join(temp_folder, img)
    shutil.move(src, dst)

# Delete remaining images
for img in os.listdir(source_folder):
    path = os.path.join(source_folder, img)
    if os.path.isfile(path):
        os.remove(path)

# Move back selected images
for img in os.listdir(temp_folder):
    src = os.path.join(temp_folder, img)
    dst = os.path.join(source_folder, img)
    shutil.move(src, dst)

# Remove temp folder
os.rmdir(temp_folder)

print("✅ Reduced to 25000 images successfully!")