# import os
# from tensorflow.keras.applications import ResNet50
# from tensorflow.keras import layers, models
# import tensorflow as tf

# # Paths
# WEIGHTS_PATH = os.path.join('utils', 'enhanced_resnet50_final.h5')  # your trained weights
# FIXED_MODEL_PATH = os.path.join('utils', 'enhanced_resnet50_final_flask.keras')

# # Model parameters
# IMG_SIZE = 224
# NUM_CLASSES = 3  # adjust if needed

# # 1. Rebuild model architecture
# inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
# base_model = ResNet50(weights='imagenet', include_top=False, input_tensor=inputs)
# for layer in base_model.layers[:60]:
#     layer.trainable = False

# x = base_model.output
# x = layers.BatchNormalization()(x)
# x = layers.GlobalAveragePooling2D()(x)
# x = layers.Dense(512, activation='relu')(x)
# x = layers.Dropout(0.3)(x)
# outputs = layers.Dense(NUM_CLASSES, activation='softmax', dtype='float32')(x)

# model = models.Model(inputs, outputs)

# # 2. Load weights
# if os.path.exists(WEIGHTS_PATH):
#     model.load_weights(WEIGHTS_PATH)
#     print(f"✅ Weights loaded from {WEIGHTS_PATH}")
# else:
#     raise FileNotFoundError(f"Trained weights not found at {WEIGHTS_PATH}")

# # 3. Save fixed model for Flask
# model.save(FIXED_MODEL_PATH)
# print(f"✅ Fixed Flask-compatible model saved at {FIXED_MODEL_PATH}")
