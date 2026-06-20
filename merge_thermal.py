import os
import shutil
import random

# ===== INPUT FOLDERS =====
thermal_human = "thermal/human"
thermal_no_human = "thermal/no_human_thermal"

# ===== OUTPUT (MAIN DATASET) =====
train_human = "dataset/train/human"
test_human = "dataset/test/human"

train_no_human = "dataset/train/no_human"
test_no_human = "dataset/test/no_human"

# Create folders if not exist
os.makedirs(train_human, exist_ok=True)
os.makedirs(test_human, exist_ok=True)
os.makedirs(train_no_human, exist_ok=True)
os.makedirs(test_no_human, exist_ok=True)

# ===== FUNCTION TO PROCESS =====
def process_images(input_folder, train_folder, test_folder):

    all_images = []

    # collect images from subfolders
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                all_images.append(os.path.join(root, file))

    print(f"Found {len(all_images)} images in {input_folder}")

    random.shuffle(all_images)

    split = int(0.8 * len(all_images))

    train_imgs = all_images[:split]
    test_imgs = all_images[split:]

    # copy train
    for img in train_imgs:
        shutil.copy(img, train_folder)

    # copy test
    for img in test_imgs:
        shutil.copy(img, test_folder)

    print(f"✅ Done for {input_folder}")


# ===== RUN =====
process_images(thermal_human, train_human, test_human)
process_images(thermal_no_human, train_no_human, test_no_human)

print("🔥 Thermal data merged successfully!")