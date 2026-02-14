import numpy as np
from PIL import Image

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)

def confidence_level(conf):
    if conf >= 90:
        return "Very High"
    elif conf >= 75:
        return "High"
    elif conf >= 60:
        return "Moderate"
    return "Low"
