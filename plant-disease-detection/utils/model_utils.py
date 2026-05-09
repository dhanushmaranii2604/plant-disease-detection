import os
import numpy as np
import cv2
import joblib
from PIL import Image

# Try importing tensorflow/keras
try:
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Deep learning models disabled.")

# ============================================================
# Full PlantVillage class list (38 classes)
# ============================================================
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
]

IMG_SIZE = (224, 224)

class PlantDiseasePredictor:
    """
    Handles loading and inference for all trained models:
    Deep Learning: MobileNet, CustomCNN, VGG16, VGG19
    Machine Learning: SVM, Random Forest, Decision Tree, XGBoost
    """

    def __init__(self):
        self.models = {}
        self._load_all_models()

    def _load_all_models(self):
        base = 'models'

        # --- Deep Learning models ---
        dl_models = {
            'MobileNet':  os.path.join(base, 'MobileNetModel_best.h5'),
            'CNN':        os.path.join(base, 'CustomCNNModel_best.h5'),
            'VGG16':      os.path.join(base, 'VGG16Model_best.h5'),
            'VGG19':      os.path.join(base, 'VGG19Model_best.h5'),
        }

        if TF_AVAILABLE:
            for name, path in dl_models.items():
                if os.path.exists(path):
                    try:
                        self.models[name] = ('dl', load_model(path))
                        print(f"[OK] Loaded DL model: {name}")
                    except Exception as e:
                        print(f"[WARN] Could not load {name}: {e}")

        # --- Machine Learning models ---
        ml_models = {
            'SVM':           os.path.join(base, 'svm_model.joblib'),
            'RandomForest':  os.path.join(base, 'random_forest_model.joblib'),
            'DecisionTree':  os.path.join(base, 'decision_tree_model.joblib'),
            'XGBoost':       os.path.join(base, 'xgboost_model.joblib'),
        }

        for name, path in ml_models.items():
            if os.path.exists(path):
                try:
                    self.models[name] = ('ml', joblib.load(path))
                    print(f"[OK] Loaded ML model: {name}")
                except Exception as e:
                    print(f"[WARN] Could not load {name}: {e}")

        if not self.models:
            print("[WARN] No models found in models/ folder.")

    def preprocess_for_dl(self, image_path):
        """Resize + normalize for DL models."""
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMG_SIZE)
            img = img.astype('float32') / 255.0
            return np.expand_dims(img, axis=0)
        except Exception as e:
            print(f"DL preprocess error: {e}")
            return None

    def preprocess_for_ml(self, image_path):
        """Flatten normalized image for ML models."""
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMG_SIZE)
            img = img.astype('float32') / 255.0
            return img.flatten().reshape(1, -1)
        except Exception as e:
            print(f"ML preprocess error: {e}")
            return None

    def predict(self, image_path, model_name='MobileNet'):
        """
        Returns (disease_name, confidence_percent).
        Falls back gracefully if model is unavailable.
        """
        if model_name not in self.models:
            # Try any available model
            if self.models:
                model_name = list(self.models.keys())[0]
            else:
                return 'Model_not_loaded', 0.0

        kind, model = self.models[model_name]

        if kind == 'dl':
            img = self.preprocess_for_dl(image_path)
            if img is None:
                return 'Preprocessing_error', 0.0
            try:
                preds = model.predict(img)
                idx = int(np.argmax(preds[0]))
                conf = float(np.max(preds[0])) * 100
                disease = DISEASE_CLASSES[idx] if idx < len(DISEASE_CLASSES) else 'Unknown'
                return disease, round(conf, 2)
            except Exception as e:
                print(f"DL predict error: {e}")
                return 'Prediction_error', 0.0

        else:  # ml
            img = self.preprocess_for_ml(image_path)
            if img is None:
                return 'Preprocessing_error', 0.0
            try:
                pred_class = model.predict(img)[0]
                # Confidence: use predict_proba if available
                conf = 0.0
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(img)[0]
                    conf = float(np.max(proba)) * 100
                else:
                    conf = 75.0  # default for models without proba
                disease = DISEASE_CLASSES[int(pred_class)] if int(pred_class) < len(DISEASE_CLASSES) else 'Unknown'
                return disease, round(conf, 2)
            except Exception as e:
                print(f"ML predict error: {e}")
                return 'Prediction_error', 0.0

    def available_models(self):
        return list(self.models.keys())


# Singleton — loaded once at app startup
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = PlantDiseasePredictor()
    return _predictor

def predict_disease(image_path, model_name='MobileNet'):
    return get_predictor().predict(image_path, model_name)

def get_available_models():
    return get_predictor().available_models()
