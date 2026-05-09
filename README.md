# 🌿 Visual Plant Disease Diagnosis Using AI

## DL and ML Approaches for Agricultural Disease Detection

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3-green?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/TensorFlow-2.13-orange?logo=tensorflow" alt="TensorFlow">
  <img src="https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql" alt="MySQL">
  <img src="https://img.shields.io/badge/License-Academic-lightgrey" alt="License">
</p>

---

## 📌 Project Overview

An AI-powered web application that detects plant diseases from leaf images using **Deep Learning** and **Machine Learning** models. Users upload a photo of a plant leaf and the system instantly identifies the disease, provides organic and chemical treatment recommendations, and generates downloadable PDF reports.

**Submitted by:** Dhanush M (USN: 1NT23MC016)  
**Degree:** Master of Computer Applications (MCA)  
**Institution:** Nitte Meenakshi Institute of Technology (NMIT), Yelahanka, Bengaluru — 560064  
**University:** Visvesvaraya Technological University (VTU)  
**Guide:** Dr. Sreekanth R, HOD-MCA, NMIT  
**Academic Year:** 2024-2025

---

## ✨ Features

- 🔐 **User Authentication** — Secure register/login with bcrypt password hashing
- 📸 **Image Upload** — Drag-and-drop or click-to-upload interface
- 🤖 **Multi-Model AI** — Choose from 8 AI models (DL + ML) per diagnosis
- 📊 **Confidence Score** — Visual progress bar showing prediction confidence
- 🌱 **Treatment Recommendations** — Organic & chemical remedies per disease
- 📄 **PDF Report Download** — Structured report with image, disease info, remedies
- 📜 **Prediction History** — Full history with timestamps and model info
- 📱 **Responsive Design** — Works on desktop, tablet, and mobile

---

## 🤖 AI Models

### Deep Learning (TensorFlow/Keras)
| Model | Architecture | Accuracy |
|-------|-------------|----------|
| MobileNet | Depthwise Separable CNN | ~95% |
| VGG16 | Deep CNN (16 layers) | ~94% |
| VGG19 | Deep CNN (19 layers) | ~94% |
| Custom CNN | Custom Architecture | ~93% |

### Machine Learning (Scikit-learn / XGBoost)
| Model | Algorithm | Accuracy |
|-------|-----------|----------|
| Random Forest | Ensemble | ~82% |
| XGBoost | Gradient Boosting | ~83% |
| SVM | Support Vector Machine | ~80% |
| Decision Tree | CART | ~75% |

---

## 🌿 Supported Plants & Diseases (38 Classes)

| Plant | Diseases |
|-------|----------|
| Apple | Scab, Black Rot, Cedar Apple Rust, Healthy |
| Cherry | Powdery Mildew, Healthy |
| Corn | Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy |
| Grape | Black Rot, Esca (Black Measles), Leaf Blight, Healthy |
| Orange | Huanglongbing (Citrus Greening) |
| Peach | Bacterial Spot, Healthy |
| Pepper | Bacterial Spot, Healthy |
| Potato | Early Blight, Late Blight, Healthy |
| Tomato | Bacterial Spot, Early/Late Blight, Leaf Mold, Septoria, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| Backend | Python 3.x, Flask 2.3 |
| Deep Learning | TensorFlow 2.13, Keras |
| Machine Learning | Scikit-learn, XGBoost |
| Image Processing | OpenCV, Pillow |
| Database | MySQL 8.0, mysql-connector-python |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome |
| PDF Generation | FPDF2 |
| Security | Flask-Bcrypt (password hashing) |
| Dev Tools | VS Code, Jupyter Notebook, XAMPP |

---

## 📁 Project Structure

```
plant-disease-detection/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .gitignore
├── README.md
│
├── models/                 # Trained model files (.h5, .joblib)
│   ├── MobileNetModel_best.h5
│   ├── CustomCNNModel_best.h5
│   ├── VGG16Model_best.h5
│   ├── VGG19Model_best.h5
│   ├── svm_model.joblib
│   ├── random_forest_model.joblib
│   ├── decision_tree_model.joblib
│   └── xgboost_model.joblib
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── uploads/            # User-uploaded images (gitignored)
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── result.html
│   ├── history.html
│   └── about.html
│
├── database/
│   └── schema.sql          # MySQL database schema + seed data
│
├── utils/
│   └── model_utils.py      # Model loading and inference
│
└── reports/                # Generated PDF reports (gitignored)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL 8.0+ (or XAMPP/phpMyAdmin)
- Git

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/plant-disease-detection.git
cd plant-disease-detection
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MySQL database
Open phpMyAdmin or MySQL CLI and run:
```sql
source database/schema.sql
```
Or import `database/schema.sql` via phpMyAdmin.

### 5. Copy your trained models
Copy your `.h5` and `.joblib` files into the `models/` folder:
```
models/MobileNetModel_best.h5
models/CustomCNNModel_best.h5
models/VGG16Model_best.h5
models/VGG19Model_best.h5
models/svm_model.joblib
models/random_forest_model.joblib
models/decision_tree_model.joblib
models/xgboost_model.joblib
```

### 6. Configure database credentials
Edit the `DB_CONFIG` in `app.py`:
```python
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'your_mysql_password',  # Update this
    'database': 'plant_disease_db',
}
```

### 7. Run the application
```bash
python app.py
```

### 8. Open in browser
Navigate to: **http://127.0.0.1:5000**

---

## 📸 Usage Guide

1. **Register** a new account at `/register`
2. **Login** with your credentials
3. Go to **Diagnose** and upload a clear plant leaf image
4. **Select a model** (MobileNet recommended for best accuracy)
5. Click **Diagnose Disease**
6. View results: disease name, confidence score, causes, and treatments
7. **Download PDF** report for records or expert consultation
8. Check **History** to review past predictions

---

## 📊 Methodology

1. **Data Collection** — PlantVillage dataset (87,000+ images, 38 classes)
2. **Preprocessing** — Resize to 224×224, normalize pixel values, data augmentation
3. **Model Training** — DL: transfer learning + fine-tuning; ML: feature extraction
4. **Evaluation** — Accuracy, precision, recall, F1-score, confusion matrix
5. **Deployment** — Flask web app with MySQL backend

---

## 🧪 Testing

- Unit Testing — Individual component validation
- Functional Testing — All features tested (register, login, upload, predict, PDF)
- Integration Testing — Frontend ↔ Backend ↔ Database flow
- Usability Testing — Responsive across desktop and mobile
- Security Testing — SQL injection prevention, file validation
- Performance Testing — Load time and prediction speed

---

## 🔮 Future Enhancements

- 📱 Android/iOS mobile application
- 🌐 Multilingual support (Kannada, Hindi, Telugu)
- 🎤 Voice-based control for low-literacy users
- 🌦️ Weather and soil data integration
- 🚁 Drone-assisted large-scale crop monitoring
- 🌍 Expanded disease database for more crops

---

## 📚 References

1. Salathé, M. et al. (2016). *Using deep learning for image-based plant disease detection.* Frontiers in Plant Science.
2. Yujian, L. et al. (2019). *Evaluation of refined deep learning models.* Computers and Electronics in Agriculture.
3. Howard, A. G. et al. (2017). *MobileNets.* arXiv:1704.04861.
4. PlantVillage Dataset — https://www.kaggle.com/emmarex/plantdisease

---

## 👨‍💻 Author

**Dhanush M**  
USN: 1NT23MC016  
MCA — 4th Semester  
Nitte Meenakshi Institute of Technology, Bengaluru  
Under guidance of **Dr. Sreekanth R** (HOD-MCA, NMIT)

---

*This project is developed for academic purposes as part of the MCA degree requirements at NMIT, Bengaluru.*
