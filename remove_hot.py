import os

folders = [
    r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\train\human",
    r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\test\human"
]

removed = 0
kept    = 0

for folder in folders:
    print(f"\n📁 Checking {folder}...")

    for file in os.listdir(folder):
        # HOT images were saved as thermal_1_*.jpg
        # JET images were saved as thermal_0_*.jpg
        if file.startswith("thermal_1_"):
            os.remove(os.path.join(folder, file))
            removed += 1
        else:
            kept += 1

print(f"\n✅ Done!")
print(f"  Removed (HOT) : {removed}")
print(f"  Kept    (JET) : {kept}")