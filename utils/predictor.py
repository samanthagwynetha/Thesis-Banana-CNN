import os
import json
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model #type: ignore
from keras.preprocessing import image

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, 'enhanced_resnet50_final_fixed.keras')
CLASS_MAPPING_PATH = os.path.join(CURRENT_DIR, 'class_indices.json')

# Load model
try:
    model = load_model(MODEL_PATH, compile=False)
    print(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

# ===============================
# LOAD CLASS MAPPING
# ===============================
if os.path.exists(CLASS_MAPPING_PATH):
    with open(CLASS_MAPPING_PATH, 'r') as f:
        CLASS_MAPPING = json.load(f)
    print(f"Class mapping loaded from {CLASS_MAPPING_PATH}")
else:
    print(f"Class mapping file not found at {CLASS_MAPPING_PATH}")
    CLASS_MAPPING = {}

# Reverse mapping: index -> class
INDEX_TO_CLASS = {v: k for k, v in CLASS_MAPPING.items()}

# ===============================
# DISEASE INFORMATION
# ===============================
DISEASE_INFO = {
    "Cordana": {
        "full_name": "Cordana Leaf Spot",
        "severity": "Moderate",
        "description": "A fungal disease causing oval-shaped spots with gray centers and dark borders.",
        "symptoms": "Small, circular to oval brown spots with yellow halos",
        "treatment": "Remove infected leaves, apply fungicide, improve air circulation"
    },
    "Sanas": {
        "full_name": "Healthy Leaf",
        "severity": "None",
        "description": "The leaf appears healthy with uniform green coloration.",
        "symptoms": "No visible symptoms",
        "treatment": "No treatment needed"
    },
    "SigatokaNegra": {
        "full_name": "Black Sigatoka",
        "severity": "Severe",
        "description": "A destructive banana disease causing dark streaks and rapid leaf death.",
        "symptoms": "Yellow streaks that turn brown or black",
        "treatment": "Remove infected leaves and apply fungicides immediately"
    }
}

# ===============================
# PREDICTION FUNCTION
# ===============================
def predict_image(image_path):
    if model is None:
        return {"success": False, "error": "Model not loaded."}

    # Load and preprocess image
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

    # Predict
    preds = model.predict(img_array, verbose=0)[0]

    predicted_idx = int(np.argmax(preds))
    predicted_class = list(CLASS_MAPPING.keys())[predicted_idx]
    confidence = float(preds[predicted_idx]) * 100

    disease_data = DISEASE_INFO.get(predicted_class, {})

    # Confidence levels
    if confidence >= 90:
        confidence_level = "Very High"
    elif confidence >= 75:
        confidence_level = "High"
    elif confidence >= 60:
        confidence_level = "Moderate"
    else:
        confidence_level = "Low"

    return {
        "success": True,
        "disease": predicted_class,
        "disease_name": disease_data.get('full_name', predicted_class),
        "confidence": round(confidence, 2),
        "confidence_level": confidence_level,
        "severity": disease_data.get('severity', "Unknown"),
        "description": disease_data.get('description', "No description available"),
        "symptoms": disease_data.get('symptoms', "No symptoms available"),
        "treatment": disease_data.get('treatment', "No treatment available"),
        "all_probabilities": {list(CLASS_MAPPING.keys())[i]: float(p)*100 for i, p in enumerate(preds)}
    }
