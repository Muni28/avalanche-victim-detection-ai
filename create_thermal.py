import cv2
import os
import random

# ==============================
# Settings
# ==============================
input_folder = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\archive (1)\Human Action Recognition\test"

output_train = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\train\human"
output_test  = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\test\human"

os.makedirs(output_train, exist_ok=True)
os.makedirs(output_test,  exist_ok=True)

# ✅ Only 2 color maps — prevents overfitting
color_maps = [
    cv2.COLORMAP_JET,  # Red/Yellow/Blue
    cv2.COLORMAP_HOT,  # Red/Orange/Yellow
]

# ==============================
# Get All Images
# ==============================
all_files = [
    f for f in os.listdir(input_folder)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

random.shuffle(all_files)

# 80% train, 20% test
split       = int(len(all_files) * 0.8)
train_files = all_files[:split]
test_files  = all_files[split:]

print(f"Total images found : {len(all_files)}")
print(f"Going to train     : {len(train_files)}")
print(f"Going to test      : {len(test_files)}")

# ==============================
# Convert Function
# ==============================
def convert_to_thermal(files, output_folder, label):
    count = 0
    for img_name in files:
        img_path = os.path.join(input_folder, img_name)
        img      = cv2.imread(img_path)

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for i, cmap in enumerate(color_maps):
            thermal   = cv2.applyColorMap(gray, cmap)
            name      = f"thermal_{i}_{img_name}"
            save_path = os.path.join(output_folder, name)
            cv2.imwrite(save_path, thermal)
            count += 1

        if count % 1000 == 0 and count > 0:
            print(f"  {label} progress: {count} images created...")

    print(f"  ✅ {label} done: {count} thermal images created")
    return count

# ==============================
# Run
# ==============================
print("\n📁 Creating train thermal images...")
train_count = convert_to_thermal(train_files, output_train, "Train")

print("\n📁 Creating test thermal images...")
test_count  = convert_to_thermal(test_files, output_test, "Test")

print(f"\n✅ Total thermal images created: {train_count + test_count}")