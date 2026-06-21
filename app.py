import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from flask import Flask, render_template, request
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import platform
if platform.system() == "Windows":
    import winsound
import gc
import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
# ==============================
# Setup
# ==============================
app = Flask(__name__)
history = []

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

# ==============================
# Load Model
# ==============================
model = load_model("human_detection_model.keras")  # ✅ Fixed from .h5
print("✅ Model loaded successfully")

# ==============================
# Home Page
# ==============================
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/stats')
def stats():
    total    = len(history)
    humans   = sum(1 for h in history if "✅ Human Detected" == h["result"])
    no_human = total - humans
    return render_template('stats.html',
        total=total, humans=humans, no_human=no_human)

# ==============================
# Prediction
# ==============================
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    # ✅ Save image
    filepath = os.path.join(STATIC_FOLDER, file.filename)
    file.save(filepath)

    try:
        # ✅ Use Pillow instead of OpenCV (no warnings)
        img = Image.open(filepath).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = img_array.reshape(1, 224, 224, 3)

    except Exception as e:
        return f"Image processing error: {str(e)}"

    # ✅ Predict
    confidence = float(model.predict(img_array, verbose=0)[0][0])
    gc.collect() 
    print(f"Raw confidence: {confidence:.4f}")

    # ✅ Threshold 0.5
    # confidence > 0.5 → no_human (class 1)
    # confidence < 0.5 → human   (class 0)
    threshold = 0.3

    if confidence > threshold:
        result     = "❌ No Human Detected"
        final_conf = confidence * 100
        lat, lon   = None, None

    else:
        result     = "✅ Human Detected"
        final_conf = (1 - confidence) * 100
        lat, lon   = 11.1271, 78.6569

        # ✅ Beep alert for human detection
        try:
            if platform.system() == "Windows":
                winsound.Beep(1000, 500)
        except:
            pass

    image_path = "static/" + file.filename

    # ✅ Save to history
    history.append({
        "result"    : result,
        "confidence": round(final_conf, 2),
        "image"     : image_path,
        "lat"       : lat,
        "lon"       : lon
    })

    return render_template(
        'result.html',
        result    = result,
        confidence= round(final_conf, 2),
        image     = image_path,
        lat       = lat,
        lon       = lon
    )

# ==============================
# History Page
# ==============================
@app.route('/history')
def show_history():
    return render_template('history.html', history=history)

# ==============================
# Run
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)