import cv2
import os

input_folder = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\fake_no_human"
output_folder = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\thermal_dataset/no_human"

os.makedirs(output_folder, exist_ok=True)

for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)

    img = cv2.imread(img_path)

    if img is None:
        continue

    # Convert to grayscale (thermal style)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Optional: Apply color map (makes it look like thermal)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    save_path = os.path.join(output_folder, img_name)
    cv2.imwrite(save_path, thermal)

print("✅ Fake thermal no-human images created!")
