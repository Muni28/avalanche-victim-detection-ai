import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import numpy as np
import tensorflow as tf
from PIL import Image

# ==============================
# Load Model
# ==============================
model = tf.keras.models.load_model("human_detection_model.keras")
print("✅ Model loaded successfully")

# ==============================
# Settings
# ==============================
folder    = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset\test"
threshold = 0.3
img_size  = (224, 224)

# ==============================
# Counters
# ==============================
total        = 0
correct      = 0
wrong        = 0
wrong_images = []

# ==============================
# Loop Through Test Images
# ==============================
for label in ["human", "no_human"]:
    path_folder = os.path.join(folder, label)

    print(f"\n📁 Testing folder: {label}")
    folder_total   = 0
    folder_correct = 0

    for file in os.listdir(path_folder):
        path = os.path.join(path_folder, file)

        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            # ✅ Use Pillow instead of OpenCV
            img = Image.open(path).convert("RGB")
            img = img.resize(img_size)
            img_array = np.array(img) / 255.0
            img_array = img_array.reshape(1, img_size[0], img_size[1], 3)

            # Predict
            confidence = float(model.predict(img_array, verbose=0)[0][0])

            # Result
            if confidence > threshold:
                predicted = "no_human"
            else:
                predicted = "human"

            # Check correctness
            folder_total += 1
            total        += 1

            if predicted == label:
                folder_correct += 1
                correct        += 1
            else:
                wrong += 1
                wrong_images.append({
                    "file"      : file,
                    "true"      : label,
                    "predicted" : predicted,
                    "confidence": confidence
                })

            # ✅ Print progress every 500 images
            if folder_total % 500 == 0:
                print(f"  Progress: {folder_total} images done...")

        except Exception as e:
            continue

    # Per folder summary
    folder_acc = (folder_correct / folder_total * 100) if folder_total > 0 else 0
    print(f"  ✅ Correct : {folder_correct}/{folder_total}")
    print(f"  ❌ Wrong   : {folder_total - folder_correct}/{folder_total}")
    print(f"  📊 Accuracy: {folder_acc:.2f}%")

# ==============================
# Overall Summary
# ==============================
overall_acc = (correct / total * 100) if total > 0 else 0

print("\n" + "="*40)
print("📊 OVERALL TEST RESULTS")
print("="*40)
print(f"  Total Images : {total}")
print(f"  Correct      : {correct}")
print(f"  Wrong        : {wrong}")
print(f"  Accuracy     : {overall_acc:.2f}%")

# ==============================
# Show Wrong Predictions
# ==============================
if wrong_images:
    print(f"\n❌ Wrong Predictions (first 10):")
    print("-"*40)
    for w in wrong_images[:10]:
        print(f"  File      : {w['file']}")
        print(f"  True      : {w['true']}")
        print(f"  Predicted : {w['predicted']}")
        print(f"  Confidence: {w['confidence']:.2f}")
        print("-"*40)
else:
    print("\n✅ No wrong predictions!")