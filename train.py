import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import class_weight

# 👉 Dataset path
dataset_path = r"C:\Users\Muniyammal L\Desktop\Avalanche victims\dataset"

# 🔥 Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.2,
    shear_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

# 👉 Load data
train_data = train_datagen.flow_from_directory(
    dataset_path + "/train",
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# ✅ Print class indices to verify order
print("Class Indices:", train_data.class_indices)
# Expected: {'human': 0, 'no_human': 1}

test_data = test_datagen.flow_from_directory(
    dataset_path + "/test",
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    shuffle=False  # IMPORTANT - never change this
)

# 🚀 Load Pretrained Model
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

# ❄ Freeze base layers, unfreeze last 20
for layer in base_model.layers:
    layer.trainable = False
for layer in base_model.layers[-20:]:
    layer.trainable = True

# 🧠 Custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=output)

# ⚙️ Compile
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ⏱️ Callbacks
early_stop = EarlyStopping(
    patience=3,                  # ✅ Fixed from 10 to 3
    restore_best_weights=True,
    monitor='val_loss'
)

lr_reduce = ReduceLROnPlateau(   # ✅ New - improves accuracy
    monitor='val_loss',
    factor=0.3,
    patience=2,
    min_lr=1e-6,
    verbose=1
)

# 👉 Compute class weights
labels = train_data.classes
weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights = dict(enumerate(weights))
print("Class Weights:", class_weights)

# 🚀 Train
history = model.fit(
    train_data,
    epochs=10,
    validation_data=test_data,
    callbacks=[early_stop, lr_reduce],  # ✅ Added lr_reduce
    class_weight=class_weights
)

# 📊 Predictions
y_pred = model.predict(test_data)
threshold = 0.7                  # ✅ Changed from 0.5 to 0.7
y_pred_classes = (y_pred > threshold).astype("int32")
y_true = test_data.classes

# ✅ target_names matches {'human':0, 'no_human':1}
print("\n📊 Classification Report:")
print(classification_report(
    y_true,
    y_pred_classes,
    target_names=['human', 'no_human']   # ✅ Fixed order
))

print("\n📉 Confusion Matrix:")
print(confusion_matrix(y_true, y_pred_classes))

# 📈 Accuracy
loss, accuracy = model.evaluate(test_data)
print(f"\n✅ Test Accuracy: {accuracy*100:.2f}%")

# 💾 Save model
model.save("human_detection_model.keras")  # ✅ Fixed from .h5 to .keras
print("✅ Model saved as human_detection_model.keras")