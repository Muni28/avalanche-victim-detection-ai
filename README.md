# 🚁 Avalanche Victim Detection System

AI-powered system to detect avalanche victims in thermal and normal images using deep learning, with real-time rescue alerts.

## 🎯 Features
- MobileNetV2 transfer learning model (95.36% accuracy)
- Thermal and normal image human detection
- Live GPS location tracking
- 15-minute survival countdown timer
- Snow depth estimation
- WhatsApp rescue team alert
- Detection history with filters
- Statistics dashboard with charts

## 🛠️ Tech Stack
- Python, TensorFlow / Keras
- Flask (Web Framework)
- MobileNetV2 (Transfer Learning)
- HTML, CSS, JavaScript

## 📊 Model Performance
- Test Accuracy: 95.36%
- Training Images: 122,508
- Precision (Human): 0.94
- Recall (Human): 0.97
- F1 Score: 0.95

## 🚀 How to Run

1. Clone the repository
2. Install dependencies
3. Train the model (dataset not included due to size)
4. Run the Flask app
5. Open browser
## 📁 Project Structure
├── app.py              # Flask application

├── train.py             # Model training script

├── test.py               # Model testing script

├── resize.py             # Image resizing utility

├── clean_dataset.py      # Dataset cleaning

├── balance_dataset.py    # Dataset balancing

├── templates/            # HTML pages

│   ├── index.html

│   ├── result.html

│   ├── history.html

│   └── stats.html

└── static/               # Uploaded images


## ⚠️ Note
Dataset and trained model file are not included due to GitHub size limits. Run `train.py` after preparing your own dataset to generate the model.

## 👤 Author
**Muniyammal L** — Electronics and Communication Engineering Student