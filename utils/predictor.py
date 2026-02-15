import os
import time
from utils.models.common import preprocess_image
from utils.models import baseline_predict, enhanced_predict


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

def enrich(result):
    info = DISEASE_INFO.get(result["disease"], {})
    return {
        **result,
        "success": True,
        "disease_name": info.get("full_name", result["disease"]),
        "severity": info.get("severity", "Unknown"),
        "description": info.get("description", "No description available"),
        "symptoms": info.get("symptoms", "No symptoms available"),
        "treatment": info.get("treatment", "No treatment available"),
    }

def predict_image(image_path):
    if not os.path.exists(image_path):
        return {"success": False, "error": "Image not found"}

    img_array = preprocess_image(image_path)

    # Baseline prediction
    baseline_result = baseline_predict(img_array)
    # ensure lowercase key
    baseline_result["inference_time_ms"] = baseline_result.get("inference_time_ms") or baseline_result.get("Inference_Time_ms") or 0
    baseline_result = enrich(baseline_result)

    # Enhanced prediction
    enhanced_result = enhanced_predict(img_array)
    enhanced_result["inference_time_ms"] = enhanced_result.get("inference_time_ms") or enhanced_result.get("Inference_Time_ms") or 0
    enhanced_result = enrich(enhanced_result)

    return {
        "success": True,
        "baseline": baseline_result,
        "enhanced": enhanced_result
    }



