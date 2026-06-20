import os
import random
import shutil

train_folder = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\train\human"
test_folder  = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\test\human"

# ==============================
# Count current images
# ==============================
train_files = [f for f in os.listdir(train_folder)
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

test_files  = [f for f in os.listdir(test_folder)
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

total = len(train_files) + len(test_files)

correct_train = int(total * 0.8)
correct_test  = int(total * 0.2)

print(f"Total images      : {total}")
print(f"Current train     : {len(train_files)}")
print(f"Current test      : {len(test_files)}")
print(f"Correct train(80%): {correct_train}")
print(f"Correct test (20%): {correct_test}")

# ==============================
# Fix train folder
# ==============================
if len(train_files) < correct_train:
    # Move images from test to train
    needed = correct_train - len(train_files)
    print(f"\n⏳ Moving {needed} images from test to train...")

    to_move = random.sample(test_files, needed)
    for f in to_move:
        shutil.move(
            os.path.join(test_folder, f),
            os.path.join(train_folder, f)
        )
    print(f"✅ Moved {needed} images to train")

elif len(train_files) > correct_train:
    # Move images from train to test
    extra = len(train_files) - correct_train
    print(f"\n⏳ Moving {extra} images from train to test...")

    to_move = random.sample(train_files, extra)
    for f in to_move:
        shutil.move(
            os.path.join(train_folder, f),
            os.path.join(test_folder, f)
        )
    print(f"✅ Moved {extra} images to test")

# ==============================
# Final counts
# ==============================
final_train = len([f for f in os.listdir(train_folder)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
final_test  = len([f for f in os.listdir(test_folder)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

print(f"\n✅ Final Split:")
print(f"  train/human: {final_train} ({final_train/(final_train+final_test)*100:.1f}%)")
print(f"  test/human : {final_test}  ({final_test/(final_train+final_test)*100:.1f}%)")