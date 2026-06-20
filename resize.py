import os
import cv2

# Dataset path
dataset_path = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset"

total   = 0
success = 0
failed  = 0

for folder in ["train", "test"]:
    for category in ["human", "no_human"]:

        path = os.path.join(dataset_path, folder, category)
        files = os.listdir(path)

        print(f"\n📁 Resizing {folder}/{category} ({len(files)} files)...")

        for i, img_name in enumerate(files):

            # ✅ Only process image files
            if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            img_path = os.path.join(path, img_name)

            try:
                img = cv2.imread(img_path)

                # ✅ Check if image loaded correctly
                if img is None:
                    failed += 1
                    continue

                # ✅ Resize and save
                img = cv2.resize(img, (224, 224))
                cv2.imwrite(img_path, img)
                success += 1
                total   += 1

            except Exception as e:
                failed += 1
                continue

            # ✅ Progress every 1000 images
            if total % 1000 == 0 and total > 0:
                print(f"  Progress: {total} images resized...")

print(f"\n✅ Resizing Complete!")
print(f"  Success : {success}")
print(f"  Failed  : {failed}")