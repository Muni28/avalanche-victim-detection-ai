import os
import random
from PIL import Image, ImageEnhance, ImageFilter

train_nohuman = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\train\no_human"
target        = 38304  # match train/human count

def count_images(folder):
    return len([f for f in os.listdir(folder)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

current = count_images(train_nohuman)
needed  = target - current

print(f"Current no_human : {current}")
print(f"Target           : {target}")
print(f"Need to generate : {needed}")

if needed <= 0:
    print("✅ Already balanced!")
else:
    files = [f for f in os.listdir(train_nohuman)
             if f.lower().endswith(('.jpg', '.jpeg', '.png'))
             and not f.startswith("aug_")]

    print(f"\n⏳ Generating {needed} augmented images...")
    count = 0

    while count < needed:
        src = random.choice(files)
        try:
            img    = Image.open(os.path.join(train_nohuman, src)).convert("RGB")
            choice = random.randint(1, 5)

            if choice == 1:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif choice == 2:
                img = img.rotate(random.choice([90, 180, 270]))
            elif choice == 3:
                enhancer = ImageEnhance.Brightness(img)
                img      = enhancer.enhance(random.uniform(0.6, 1.4))
            elif choice == 4:
                enhancer = ImageEnhance.Contrast(img)
                img      = enhancer.enhance(random.uniform(0.7, 1.3))
            elif choice == 5:
                img = img.filter(ImageFilter.GaussianBlur(radius=1))

            new_name  = f"aug_{count}_{src}"
            img.save(os.path.join(train_nohuman, new_name))
            count += 1

            if count % 1000 == 0:
                print(f"  Progress: {count} images done...")

        except Exception:
            continue

    print(f"\n✅ Done!")
    print(f"  train/human    : {count_images(os.path.join(os.path.dirname(train_nohuman), 'human'))}")
    print(f"  train/no_human : {count_images(train_nohuman)}")
