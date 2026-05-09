"""
Visual Plant Disease Diagnosis Using AI: DL and ML Approaches
Flask Web Application
Student: Dhanush M | USN: 1NT23MC016
NMIT Bengaluru | Academic Year 2024-2025
"""

import os
import io
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session, send_file, jsonify)
from flask_bcrypt import Bcrypt
import mysql.connector
from fpdf import FPDF

# ── App init ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'plant_disease_nmit_2025_dhanush')

bcrypt = Bcrypt(app)

# ── Config ────────────────────────────────────────────────────────────
UPLOAD_FOLDER   = os.path.join('static', 'uploads')
REPORTS_FOLDER  = 'reports'
ALLOWED_EXT     = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
MAX_SIZE_MB     = 16

app.config['UPLOAD_FOLDER']      = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_SIZE_MB * 1024 * 1024

os.makedirs(UPLOAD_FOLDER,  exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

# ── MySQL Config  (update password if needed) ─────────────────────────
DB_CONFIG = {
    'host':     os.environ.get('DB_HOST',     'localhost'),
    'user':     os.environ.get('DB_USER',     'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME',     'plant_disease_db'),
}

# ── Lazy-load model predictor ─────────────────────────────────────────
def get_predictor():
    from utils.model_utils import get_predictor as _gp
    return _gp()

# ══════════════════════════════════════════════════════════════════════
# Helper functions
# ══════════════════════════════════════════════════════════════════════

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_disease_info(disease_name):
    """Fetch remedy data from DB. Returns a dict."""
    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diseases WHERE disease_name = %s", (disease_name,))
        row = cursor.fetchone()
        cursor.close(); conn.close()
        if row:
            return row
    except Exception as e:
        print(f"DB error fetching disease info: {e}")
    return {
        'disease_name':   disease_name,
        'plant_name':     disease_name.split('___')[0].replace('_', ' ') if '___' in disease_name else 'Unknown',
        'causes':         'Information not available in database',
        'symptoms':       'Consult local agricultural expert',
        'organic_remedy': 'Neem oil spray as general precaution',
        'chemical_remedy':'Consult local agricultural expert',
        'prevention_tips':'Regular monitoring and crop rotation recommended',
    }

def format_disease_display(disease_name):
    """Convert DB key like Apple___Apple_scab → Apple Scab"""
    if '___' in disease_name:
        plant, disease = disease_name.split('___', 1)
        plant   = plant.replace('_', ' ').replace('(', '').replace(')', '').strip()
        disease = disease.replace('_', ' ').strip()
        return plant, disease
    return 'Unknown', disease_name.replace('_', ' ')

# ══════════════════════════════════════════════════════════════════════
# Routes
# ══════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# ── Auth ──────────────────────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            conn   = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            conn.commit()
            cursor.close(); conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username or email already exists.', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        try:
            conn   = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close(); conn.close()
            if user and bcrypt.check_password_hash(user['password'], password):
                session['user_id']  = user['id']
                session['username'] = user['username']
                flash(f"Welcome back, {user['username']}!", 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            flash(f'Database error: {e}', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ── Dashboard ─────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM predictions WHERE user_id = %s ORDER BY created_at DESC LIMIT 6",
            (session['user_id'],)
        )
        recent = cursor.fetchall()
        cursor.execute(
            "SELECT COUNT(*) AS total FROM predictions WHERE user_id = %s",
            (session['user_id'],)
        )
        total = cursor.fetchone()['total']
        cursor.close(); conn.close()
    except Exception as e:
        flash(f'DB error: {e}', 'warning')
        recent, total = [], 0

    # Add display names
    for p in recent:
        p['plant'], p['disease_display'] = format_disease_display(p['disease_name'])

    return render_template('dashboard.html',
                           username=session['username'],
                           predictions=recent,
                           total=total)

# ── Predict ───────────────────────────────────────────────────────────

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    predictor = get_predictor()
    available_models = predictor.available_models()
    # default fallback list so form always renders
    if not available_models:
        available_models = ['MobileNet', 'CNN', 'VGG16', 'VGG19',
                            'SVM', 'RandomForest', 'DecisionTree', 'XGBoost']

    if request.method == 'POST':
        model_name = request.form.get('model_name', 'MobileNet')

        if 'image' not in request.files:
            flash('No file uploaded.', 'danger')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type. Use JPG, PNG, JPEG, or WEBP.', 'danger')
            return redirect(request.url)

        # Save image
        ts       = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(f"{ts}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Predict
        disease_key, confidence = predictor.predict(filepath, model_name)
        disease_info = get_disease_info(disease_key)
        plant_name, disease_display = format_disease_display(disease_key)

        # Save to DB
        try:
            conn   = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO predictions (user_id, image_path, disease_name, confidence, model_used) "
                "VALUES (%s, %s, %s, %s, %s)",
                (session['user_id'], filename, disease_key, confidence, model_name)
            )
            pred_id = cursor.lastrowid
            conn.commit()
            cursor.close(); conn.close()
        except Exception as e:
            print(f"DB save error: {e}")
            pred_id = None

        return render_template('result.html',
                               disease_key=disease_key,
                               plant_name=plant_name,
                               disease_display=disease_display,
                               confidence=confidence,
                               image_path=filename,
                               model_used=model_name,
                               pred_id=pred_id,
                               info=disease_info)

    return render_template('predict.html', models=available_models)

# ── History ───────────────────────────────────────────────────────────

@app.route('/history')
@login_required
def history():
    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM predictions WHERE user_id = %s ORDER BY created_at DESC",
            (session['user_id'],)
        )
        preds = cursor.fetchall()
        cursor.close(); conn.close()
    except Exception as e:
        flash(f'DB error: {e}', 'warning')
        preds = []

    for p in preds:
        p['plant'], p['disease_display'] = format_disease_display(p['disease_name'])

    return render_template('history.html', predictions=preds)

# ── PDF Download ──────────────────────────────────────────────────────

@app.route('/download_pdf/<int:pred_id>')
@login_required
def download_pdf(pred_id):
    try:
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM predictions WHERE id = %s AND user_id = %s",
            (pred_id, session['user_id'])
        )
        pred = cursor.fetchone()
        cursor.close(); conn.close()
    except Exception as e:
        flash(f'DB error: {e}', 'danger')
        return redirect(url_for('history'))

    if not pred:
        flash('Prediction not found.', 'danger')
        return redirect(url_for('history'))

    info        = get_disease_info(pred['disease_name'])
    plant, disease_disp = format_disease_display(pred['disease_name'])
    date_str    = pred['created_at'].strftime('%Y-%m-%d %H:%M') if pred.get('created_at') else 'N/A'

    # Build PDF
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_fill_color(45, 106, 79)
    pdf.rect(0, 0, 210, 30, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 15, "Plant Disease Diagnosis Report", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, "Visual Plant Disease Diagnosis Using AI | NMIT Bengaluru", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(8)

    # Patient/Prediction Info
    pdf.set_fill_color(232, 245, 233)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Prediction Summary", ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(60, 7, f"Date:"); pdf.cell(0, 7, date_str, ln=True)
    pdf.cell(60, 7, f"Plant:"); pdf.cell(0, 7, plant, ln=True)
    pdf.cell(60, 7, f"Detected Disease:"); pdf.cell(0, 7, disease_disp, ln=True)
    pdf.cell(60, 7, f"Confidence Score:"); pdf.cell(0, 7, f"{pred['confidence']:.1f}%", ln=True)
    pdf.cell(60, 7, f"Model Used:"); pdf.cell(0, 7, pred.get('model_used', 'MobileNet'), ln=True)
    pdf.cell(60, 7, f"User:"); pdf.cell(0, 7, session.get('username', 'N/A'), ln=True)
    pdf.ln(4)

    def section(title, text, r, g, b):
        pdf.set_fill_color(r, g, b)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 8, title, ln=True, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, str(text) if text else 'N/A')
        pdf.ln(2)

    section("Causes",            info.get('causes', 'N/A'),         255, 243, 224)
    section("Symptoms",          info.get('symptoms', 'N/A'),        232, 240, 254)
    section("Organic Treatment", info.get('organic_remedy', 'N/A'),  232, 245, 233)
    section("Chemical Treatment",info.get('chemical_remedy', 'N/A'), 255, 235, 238)
    section("Prevention Tips",   info.get('prevention_tips', 'N/A'), 240, 248, 255)

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, "Generated by Plant Disease Detection System | Dhanush M (1NT23MC016) | NMIT Bengaluru", align='C')

    # Save & send
    safe_name = f"report_{pred_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf_path  = os.path.join(REPORTS_FOLDER, safe_name)
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name=safe_name)

# ── API: available models (for JS) ───────────────────────────────────

@app.route('/api/models')
def api_models():
    predictor = get_predictor()
    return jsonify({'models': predictor.available_models()})

# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    app.run(debug=True, port=5000)
