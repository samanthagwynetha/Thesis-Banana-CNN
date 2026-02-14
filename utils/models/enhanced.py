from multiprocessing import dummy
import os
import json
import numpy as np
import tensorflow as tf
from .common import confidence_level

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

MODEL_PATH = os.path.join(
    ARTIFACTS_DIR, "enhanced_resnet50_deployment_v1.tflite"
)
CLASS_MAPPING_PATH = os.path.join(
    ARTIFACTS_DIR, "class_indices_v1.json"
)

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open(CLASS_MAPPING_PATH) as f:
    CLASS_MAPPING = json.load(f)

INDEX_TO_CLASS = {v: k for k, v in CLASS_MAPPING.items()}

def predict(img_array):
    dummy = np.zeros((1,224,224,3), dtype=np.float32)
    interpreter.set_tensor(input_details[0]["index"], dummy)
    interpreter.invoke()

    preds = interpreter.get_tensor(output_details[0]["index"])[0]
    idx = int(np.argmax(preds))
    conf = float(preds[idx]) * 100

    inferenceTime = None
    if len(output_details) > 1:
        inferenceTime = round(interpreter.get_tensor(output_details[1]["index"])[0], 2)

    return {
        "disease": INDEX_TO_CLASS.get(idx, "Unknown"),
        "confidence": round(conf, 2),
        "confidence_level": confidence_level(conf),
        "all_probabilities": {
            INDEX_TO_CLASS.get(i, str(i)): float(p) * 100
            for i, p in enumerate(preds)
        },
        "Inference_Time_ms": inferenceTime
    }
