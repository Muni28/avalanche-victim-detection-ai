import os
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"  # ✅ Suppresses warnings

import cv2
from PIL import Image

base = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset"

removed = 0
kept    = 0

for split in ["train", "test"]:
    for cls in ["human", "no_human"]:
        folder = os.path.join(base, split, cls)
        print(f"\n🔍 Checking {split}/{cls}...")

        for file in os.listdir(folder):
            path = os.path.join(folder, file)

            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            try:
                # Use PIL instead of OpenCV (no warnings)
                img = Image.open(path)
                img.verify()  # checks if image is valid
                kept += 1

            except Exception:
                try:
                    os.remove(path)
                    removed += 1
                    print(f"  ❌ Removed: {file}")
                except:
                    pass

print(f"\n✅ Cleaning Done!")
print(f"  Kept   : {kept}")
print(f"  Removed: {removed}")