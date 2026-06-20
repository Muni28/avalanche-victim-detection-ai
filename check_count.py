import os

base = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset"

for split in ["train", "test"]:
    for cls in ["human", "no_human"]:
        path = os.path.join(base, split, cls)
        print(f"{split}/{cls}: {len(os.listdir(path))} images")