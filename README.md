# Enhanced ResNet50 for Banana Leaf Disease Detection

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange.svg)](https://www.tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Optimizing ResNet50 for Efficient Banana Leaf Disease Classification**  
> A deep learning approach to detect Black Sigatoka and Cordana diseases in banana crops, achieving **99.44% test accuracy** with only **9.84 minutes** of training time.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Research Objectives](#research-objectives)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Key Enhancements](#key-enhancements)
- [Results](#results)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [License](#license)

---

## 🌟 Overview

This repository contains the implementation of an **Enhanced ResNet50** architecture for automated detection of banana leaf diseases, served through a **Flask web application** with real-time inference. The system compares a baseline ResNet50 against an enhanced variant across two experiments, demonstrating significant gains in both accuracy and training efficiency.

Both models are exported as **TFLite** files for fast CPU-based inference and deployed via **Gunicorn + Docker**.

### Actual Results (from training notebook `pipeline/v10.ipynb`)

| Model | Test Accuracy | Training Time | Epochs |
|---|---|---|---|
| Baseline ResNet50 | 93.33% | 19.99 min | 100 |
| Enhanced (Architecture only) | 98.89% | 39.49 min | 100 |
| **Enhanced + Optimizations (final)** | **99.44%** | **9.84 min** | **23 (early stop)** |

---

## 🔬 Problem Statement

Banana crops are severely threatened by foliar diseases such as:

- **Black Sigatoka** (*Pseudocercospora fijiensis*): Can cause up to 80% yield loss
- **Cordana Leaf Spot** (*Cordana musae*): Leads to premature leaf senescence and reduced fruit quality

### Current Challenges

1. **Manual Inspection**: Labor-intensive, unreliable, requires expert knowledge
2. **Computational Intensity**: Training complex models can take tens of minutes to hours
3. **Field Deployment**: Models must be lightweight enough for CPU-only inference in the field

---

## 🎯 Research Objectives

### General Objective
Develop an optimized ResNet50-based CNN for faster and more accurate banana leaf disease classification, with a working deployment pipeline.

### Specific Objectives

1. **Data Preparation**: Preprocess 1,200 banana leaf images (Healthy, Sigatoka, Cordana) with augmentation
2. **Architecture Enhancement**: Optimize ResNet50 with partial fine-tuning, GAP, and a larger classification head
3. **Performance Comparison**: Evaluate baseline vs. enhanced model across two experiments
4. **Practical Deployment**: Serve predictions via a Flask app with TFLite inference

---

## 📊 Dataset

### Composition

| Class | Original Images | Augmented | Total |
|---|---|---|---|
| **Healthy (Sanas)** | 100 | 300 | 400 |
| **Black Sigatoka (SigatokaNegra)** | 100 | 300 | 400 |
| **Cordana** | 100 | 300 | 400 |
| **Total** | **300** | **900** | **1,200** |

### Data Split
- **Training**: 80% (960 images)
- **Validation**: 10% (120 images)
- **Test**: 10% (120 images, fixed held-out set of 180 in notebook)

### Preprocessing
- **Image Size**: 224 × 224 RGB
- **Normalization**: `tf.keras.applications.resnet50.preprocess_input` (ImageNet mean subtraction)
- **Augmentation**: Rotation (±15°), horizontal flip (training set only)

### Visual Characteristics

- **Healthy**: Uniform green color, smooth texture, no lesions
- **Black Sigatoka**: Dark brown-to-black streaks along veins, necrotic lesions, yellow halos
- **Cordana**: Irregular oval-to-circular brown spots with distinct edges

---

## 🔧 Methodology

Following the **CRISP-DM Framework**:

1. **Business Understanding**: Identify need for efficient, deployable disease detection
2. **Data Understanding**: Analyze 1,200 banana leaf images across 3 classes
3. **Data Preparation**: 80/10/10 split with image augmentation
4. **Modeling**: Two experiments — architecture-only vs. architecture + training optimizations
5. **Evaluation**: Statistical & computational metrics (accuracy, F1, training time, inference speed)
6. **Deployment**: TFLite model export, Flask web app, Docker container

---

## 🚀 Key Enhancements

### Architectural Improvements (Experiment 1)

| Component | Baseline | Enhanced | Rationale |
|---|---|---|---|
| **Layer Freezing** | All layers frozen | Conv1–3 frozen, Conv4–5 trainable | Allows domain-specific feature adaptation |
| **Pooling** | Flatten | GlobalAveragePooling2D | Removes spatial dimensions, reduces overfitting |
| **Dense Head** | Dense(32) | Dense(512) → BN → ReLU → Dropout(0.3) | Deeper classification capacity |
| **Batch Normalization** | None | After Dense(512), pre-activation | Stabilizes internal covariate shift |
| **Dropout** | 0.5 | 0.3 | Less aggressive — model generalizes well with BN |
| **Trainable Parameters** | 3,211,395 | 23,203,331 | More capacity for fine-tuning |

### Training Optimizations (Experiment 2, final model)

| Setting | Baseline | Enhanced + Opt | Benefit |
|---|---|---|---|
| **Optimizer** | Adam (LR=0.001) | Adam (LR=0.0001, cosine annealing) | Smoother convergence |
| **Epochs** | 100 fixed | 60 max, early stopping (patience=10) | Stopped at epoch 23 |
| **Mixed Precision** | FP32 | FP16 | ~30–50% faster GPU training |
| **Batch Size** | 64 | 64 | Unchanged |
| **Training Time** | 19.99 min | **9.84 min** | **~51% reduction** |

---

## 📈 Results

All metrics are from the held-out test set (180 images, 60 per class) evaluated in `pipeline/v10.ipynb`.

### Full Comparative Table (Table 4 from notebook)

| Metric | Baseline (Exp1) | Enhanced (Exp1) | Enhanced + Opt (Exp2) |
|---|---|---|---|
| **Test Accuracy** | 93.33% | 98.89% | **99.44%** |
| **Test Loss** | 0.4442 | 0.0861 | 0.1676 |
| **Precision (Weighted)** | 0.9345 | 0.9892 | **0.9945** |
| **Recall (Weighted)** | 0.9333 | 0.9889 | **0.9944** |
| **F1-Score (Weighted)** | 0.9333 | 0.9889 | **0.9944** |
| **Training Time** | 19.99 min | 39.49 min | **9.84 min** |
| **Epochs Completed** | 100 | 100 | 23 |
| **Inference Speed** | 211.63 img/s | 206.34 img/s | 210.49 img/s |
| **Trainable Parameters** | 3,211,395 | 23,203,331 | 23,203,331 |

### Improvement Breakdown

- **Architecture alone** (Exp1 Enhanced − Baseline): **+5.56 percentage points**
- **Optimizations alone** (Exp2 − Exp1 Enhanced): **+0.56 percentage points**
- **Total system gain** (Exp2 − Baseline): **+6.11 percentage points**
- **Training time reduction** (Exp2 vs. Baseline): **~51% faster** (9.84 vs. 19.99 min)
- **Inference speed**: Comparable across all three (~210 img/s on GPU batch inference)

### Per-Class Report — Final Enhanced Model (Exp2)

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Cordana | 1.0000 | 0.9833 | 0.9916 | 60 |
| Healthy (Sanas) | 1.0000 | 1.0000 | 1.0000 | 60 |
| Black Sigatoka | 0.9836 | 1.0000 | 0.9917 | 60 |
| **Weighted avg** | **0.9945** | **0.9944** | **0.9944** | **180** |

### Per-Class Report — Baseline Model (Exp1)

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Cordana | 0.9286 | 0.8667 | 0.8966 | 60 |
| Healthy (Sanas) | 1.0000 | 1.0000 | 1.0000 | 60 |
| Black Sigatoka | 0.8750 | 0.9333 | 0.9032 | 60 |
| **Weighted avg** | **0.9345** | **0.9333** | **0.9333** | **180** |

---

## 💻 Installation

### Prerequisites

- Python 3.11
- 8 GB+ RAM
- GPU recommended for training (inference runs on CPU via TFLite)

### Clone & Set Up

```bash
git clone https://github.com/eej-sinining/Thesis-Banana-CNN.git
cd Thesis-Banana-CNN
```

#### Option A — Using `uv` (recommended)

```bash
pip install uv
uv sync
uv run python main.py
```

#### Option B — Plain `pip`

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

The app will start at `http://localhost:5000`.

---

## 🖥️ Usage

1. Open `http://localhost:5000` in your browser
2. Upload a banana leaf image (JPG or PNG)
3. The system runs a **leaf validity check** first (rejects non-leaf images)
4. Both the **Baseline** and **Enhanced** models run inference simultaneously
5. Results include: predicted disease, confidence score, per-class probabilities, inference time, and an **occlusion-sensitivity bounding box** highlighting the detected disease region

### Supported Classes

| Label | Display Name | Severity |
|---|---|---|
| `Sanas` | Healthy Leaf | None |
| `SigatokaNegra` | Black Sigatoka | Severe |
| `Cordana` | Cordana Leaf Spot | Moderate |

---

## 🐳 Deployment

### Docker

```bash
docker build -t banana-cnn .
docker run -p 5000:5000 banana-cnn
```

The container uses **Python 3.11-slim**, installs dependencies via `uv`, and serves the app with **Gunicorn** (1 worker, port 5000).

### Heroku / Render

A `Procfile` is included:

```
web: gunicorn app:app
```

Deploy to any platform that supports Python 3.11 and a `Procfile`.

---

## 📁 Project Structure

```
Thesis-Banana-CNN/
├── app.py                    # Flask application (routes)
├── config.py                 # Paths and allowed extensions
├── main.py                   # Entry point
├── Dockerfile                # Container definition
├── Procfile                  # Gunicorn process file
├── requirements.txt          # pip dependencies
├── pyproject.toml            # uv/pip project metadata
├── pipeline/                 # Training notebooks (v7–v11)
│   └── v10.ipynb             # Final training run (reported results)
├── utils/
│   ├── predictor.py          # Leaf validation + inference orchestration
│   ├── reporting.py          # Consistency metrics + bounding box annotation
│   ├── models/
│   │   ├── baseline.py       # TFLite baseline inference
│   │   ├── enhanced.py       # TFLite enhanced inference
│   │   └── common.py         # Shared preprocessing + confidence levels
│   └── artifacts/            # .tflite model files + class index JSONs
├── static/                   # CSS, JS, uploaded images
└── templates/                # Jinja2 HTML templates
```

---

## 📖 Citation

If you use this work, please cite:

```
@thesis{sinining2026banana,
  title   = {Enhanced ResNet50 for Banana Leaf Disease Detection},
  author  = {Sinining, EEJ},
  year    = {2026},
  school  = {[Your Institution]},
  note    = {https://github.com/eej-sinining/Thesis-Banana-CNN}
}
```

---

## 🪪 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
