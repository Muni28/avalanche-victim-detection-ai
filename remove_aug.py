import os

folders = [
    r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\train\human",
    r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\train\no_human",
    r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\test\human",
    r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\test\no_human"
]

removed = 0

for folder in folders:
    for file in os.listdir(folder):
        if file.startswith("aug_"):
            os.remove(os.path.join(folder, file))
            removed += 1

print(f"✅ Removed {removed} augmented images")