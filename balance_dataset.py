import os
import random
from PIL import Image

base = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset"

def count_images(folder):
    return len([f for f in os.listdir(folder)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

def augment_images(folder, target_count):
    files = [f for f in os.listdir(folder)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    current = len(files)
    needed = target_count - current

    if needed <= 0:
        print(f"✅ No augmentation needed: {folder}")
        return

    print(f"⏳ Generating {needed} images in {os.path.basename(folder)}...")
    count = 0
    while count < needed:
        src = random.choice(files)
        try:
            img = Image.open(os.path.join(folder, src)).convert("RGB")

            # Random flip
            if random.random() > 0.5:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)

            # Random rotation
            angle = random.choice([0, 90, 180, 270])
            img = img.rotate(angle)

            new_name = f"aug_{count}_{src}"
            img.save(os.path.join(folder, new_name))
            count += 1

        except Exception as e:
            print(f"Skipped {src}: {e}")
            continue

    print(f"✅ Done. Total now: {count_images(folder)}")

# ---- TRAIN ----
print("\n📁 Balancing TRAIN folder...")
train_human   = os.path.join(base, "train", "human")
train_nohuman = os.path.join(base, "train", "no_human")

target_train = count_images(train_nohuman)  # 29,059
augment_images(train_human, target_train)

# ---- TEST ----
print("\n📁 Balancing TEST folder...")
test_human   = os.path.join(base, "test", "human")
test_nohuman = os.path.join(base, "test", "no_human")

target_test = count_images(test_nohuman)  # 23,394
augment_images(test_human, target_test)

# ---- FINAL COUNT ----
print("\n✅ Final Dataset Counts:")
for split in ["train", "test"]:
    for cls in ["human", "no_human"]:
        path = os.path.join(base, split, cls)
        print(f"  {split}/{cls}: {count_images(path)}")