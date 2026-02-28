import numpy as np  # type: ignore
from PIL import Image  # type: ignore
import tensorflow as tf  # type: ignore
from tensorflow import keras  # type: ignore
from tensorflow.keras.applications.resnet50 import preprocess_input 

def preprocess_image(image_path):
    img = keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array.astype(np.float32)

def confidence_level(conf):
    if conf >= 90:
        return "Very High"
    elif conf >= 75:
        return "High"
    elif conf >= 60:
        return "Moderate"
    return "Low"