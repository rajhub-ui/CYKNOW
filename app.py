from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template, g, session, redirect, url_for
from flask_cors import CORS
from database import init_db, get_db
from auth import hash_password, verify_password, create_token, token_required
import json
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from flask_dance.contrib.google import make_google_blueprint, google
from triage import analyze_scam_message
# Content Imports
from phishing_content import PHISHING_QUESTIONS
from digital_arrest_scam import DIGITAL_ARREST_SCENARIO
from contact_content import GOVT_CONTACTS
from malicious_app_content import APP_QUESTIONS
from learning_content import LEARNING_MODULES
from translations import TRANSLATIONS

app = Flask(__name__)
CORS(app)
app.secret_key = 'cyberfit-secret-key-123' # Required for sessions
# ============ GOOGLE OAUTH SETUP ============
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # For local testing only
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# You must get these from console.cloud.google.com
GOOGLE_CLIENT_ID = "920919631814-8l0rned731rugtncho568fevfm2akjjb.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

google_bp = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    redirect_to="google_authorized",
    scope = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
],

reprompt_select_account=True
)
app.register_blueprint(google_bp, url_prefix="/login")

# ============ EMAIL OTP SENDER ============
# Replace with your actual Gmail and App Password
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_16_letter_app_password" 

def send_email_otp(receiver_email, otp):
    msg = MIMEText(f"Welcome to CyberFit!\n\nYour verification code is: {otp}\n\nThis code expires in 10 minutes.")
    msg['Subject'] = 'CyberFit - Your Verification Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

with app.app_context():
    init_db()

# ============ TRANSLATIONS & CONTEXT ============
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in TRANSLATIONS:
        session['lang'] = lang
    return redirect(request.referrer or '/dashboard')

@app.context_processor
def inject_translations():
    current_lang = session.get('lang')
    show_popup = False
    if not current_lang:
        current_lang = 'en'
        show_popup = True
    return dict(
        t=TRANSLATIONS[current_lang], 
        current_lang=current_lang, 
        show_lang_popup=show_popup
    )


# ============ BASIC ROUTES ============
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'CyberFit backend is running',
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/db-check')
def db_check():
    conn = get_db()
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        return jsonify({'status': 'ok', 'tables': [t['name'] for t in tables]})
    finally:
        conn.close()


# ============ AUTH ROUTES ============
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not name or not email or not password:
        return jsonify({'error': 'name, email, and password are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Invalid email format'}), 400

    conn = get_db()
    try:
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            return jsonify({'error': 'Email already registered'}), 409

        password_hash = hash_password(password)
        cur = conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        conn.commit()
        user_id = cur.lastrowid
        token = create_token(user_id, email)
        session['user_id'] = user_id

        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {'id': user_id, 'name': name, 'email': email}
        }), 201
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400

    conn = get_db()
    try:
        user = conn.execute(
            'SELECT id, name, email, password_hash FROM users WHERE email = ?', (email,)
        ).fetchone()

        if user['password_hash'] == 'OAUTH_USER_NO_PASSWORD':
            return jsonify({'error': 'This account was created with Google. Please use "Continue with Google".'}), 401

        if not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid password. Please try again.'}), 401
        token = create_token(user['id'], user['email'])
        session['user_id'] = user['id']
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {'id': user['id'], 'name': user['name'], 'email': user['email']}
        })
    finally:
        conn.close()

@app.route('/api/auth/me')
@token_required
def me():
    conn = get_db()
    try:
        user = conn.execute(
            'SELECT id, name, email, language, created_at FROM users WHERE id = ?', (g.user_id,)
        ).fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': dict(user)})
    finally:
        conn.close()


# ============ PAGES & MODULES ============
@app.route('/test')
def test_page():
    return render_template('auth_test.html')

@app.route('/phishing')
def phishing_page():
    return render_template('phishing.html')

@app.route('/digital-arrest')
def digital_arrest_page():
    return render_template('digital_arrest.html')

@app.route('/malicious-app')
def malicious_app_page():
    return render_template('malicious_app.html')

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', contacts=GOVT_CONTACTS)


# ============ DASHBOARD & SURVEY ============
@app.route('/')
def home():
    is_logged_in = 'user_id' in session
    return render_template('home.html', is_logged_in=is_logged_in)

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/api/dashboard')
@token_required
def api_dashboard():
    conn = get_db()
    try:
        # MAKE SURE TO SELECT difficulty_level HERE
        user = conn.execute(
            'SELECT name, difficulty_level FROM users WHERE id = ?', (g.user_id,)
        ).fetchone()
        
        attempts = conn.execute(
            'SELECT module_type, score, attempted_at FROM attempts '
            'WHERE user_id = ? ORDER BY attempted_at ASC', (g.user_id,)
        ).fetchall()

        attempts_list = [dict(a) for a in attempts]
        module_scores = {}
        for a in attempts_list:
            module_scores[a['module_type']] = a['score']
        
        overall_score = int(sum(module_scores.values()) / len(module_scores)) if module_scores else 0

        return jsonify({
            'user_name': user['name'] if user else 'User',
            'difficulty_level': user['difficulty_level'] if user else 'unassessed',
            'overall_score': overall_score,
            'modules_completed': len(module_scores),
            'attempts': attempts_list
        })
    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.clear() # This clears the user_id AND the language
    return redirect('/test')

@app.route('/survey')
def survey_page():
    return render_template('survey.html')

@app.route('/api/survey/submit', methods=['POST'])
@token_required
def survey_submit():
    data = request.get_json(silent=True) or {}
    level = data.get('level', 'beginner')
    
    conn = get_db()
    try:
        conn.execute('UPDATE users SET difficulty_level = ? WHERE id = ?', (level, g.user_id))
        conn.commit()
    finally:
        conn.close()
        
    return jsonify({'status': 'ok', 'level': level})

@app.route('/learning')
def learning_page():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/test')

    conn = get_db()
    try:
        user = conn.execute('SELECT difficulty_level FROM users WHERE id = ?', (user_id,)).fetchone()
        level = user['difficulty_level'] if user else 'unassessed'
    finally:
        conn.close()

    # If they haven't taken the survey, redirect them!
    if level == 'unassessed':
        return redirect('/survey')

    lang = session.get('lang', 'en')

    tailored_modules = {}
    for module_key, tiers in LEARNING_MODULES.items():
        tailored_modules[module_key] = tiers.get(level, tiers['beginner'])[lang]

    return render_template('learning.html', modules=tailored_modules, user_level=level)

@app.route('/learn/<module_key>')
def learn_module(module_key):
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/test')

    conn = get_db()
    try:
        user = conn.execute('SELECT difficulty_level FROM users WHERE id = ?', (user_id,)).fetchone()
        level = user['difficulty_level'] if user and user['difficulty_level'] != 'unassessed' else 'beginner'
    finally:
        conn.close()

    lang = session.get('lang', 'en')
    
    if module_key not in LEARNING_MODULES:
        return redirect('/learning')

    # Get the specific module data
    module_data = LEARNING_MODULES[module_key].get(level, LEARNING_MODULES[module_key]['beginner'])[lang]

    return render_template('learn_module.html', module=module_data, module_key=module_key, user_level=level)


# ============ API ENDPOINTS FOR MODULES ============

@app.route('/api/phishing/questions')
@token_required
def phishing_questions():
    sanitized = [{
        'id': q['id'], 'sender_name': q['sender_name'], 'sender_email': q['sender_email'],
        'subject': q['subject'], 'body': q['body'],
    } for q in PHISHING_QUESTIONS]
    return jsonify({'questions': sanitized})

@app.route('/api/phishing/submit', methods=['POST'])
@token_required
def phishing_submit():
    data = request.get_json(silent=True) or {}
    answers = data.get('answers', [])
    if len(answers) != len(PHISHING_QUESTIONS):
        return jsonify({'error': 'Please answer all questions'}), 400

    answer_map = {a['id']: a['choice'] for a in answers if 'id' in a and 'choice' in a}
    results = []
    correct_count = 0
    for q in PHISHING_QUESTIONS:
        user_choice = answer_map.get(q['id'], '')
        is_correct = user_choice == q['answer']
        if is_correct: correct_count += 1
        results.append({
            'id': q['id'], 'user_choice': user_choice, 'correct_answer': q['answer'],
            'is_correct': is_correct, 'red_flags': q['red_flags'], 'explanation': q['explanation'],
        })

    score = int((correct_count / len(PHISHING_QUESTIONS)) * 100)
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO attempts (user_id, module_type, score, answers_json) VALUES (?, ?, ?, ?)',
            (g.user_id, 'phishing', score, json.dumps(answer_map))
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({'score': score, 'correct_count': correct_count, 'total': len(PHISHING_QUESTIONS), 'results': results})

@app.route('/api/digital-arrest/scenario')
@token_required
def digital_arrest_scenario():
    return jsonify(DIGITAL_ARREST_SCENARIO)

@app.route('/api/digital-arrest/submit', methods=['POST'])
@token_required
def digital_arrest_submit():
    data = request.get_json(silent=True) or {}
    score = int(data.get('score', 0))
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO attempts (user_id, module_type, score, answers_json) VALUES (?, ?, ?, ?)',
            (g.user_id, 'digital_arrest', score, json.dumps({'completed': True}))
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({'status': 'ok'})

@app.route('/api/malicious-app/questions')
@token_required
def malicious_app_questions():
    sanitized = [{
        'id': q['id'], 'app_name': q['app_name'], 'developer': q['developer'],
        'icon': q['icon'], 'description': q['description'], 'permissions': q['permissions'],
        'answer': q['answer'], 'red_flags': q['red_flags'], 'explanation': q['explanation']
    } for q in APP_QUESTIONS]
    return jsonify({'questions': sanitized})

@app.route('/api/malicious-app/submit', methods=['POST'])
@token_required
def malicious_app_submit():
    data = request.get_json(silent=True) or {}
    answers = data.get('answers', [])
    answer_map = {a['id']: a['choice'] for a in answers if 'id' in a and 'choice' in a}
    results = []
    correct_count = 0
    for q in APP_QUESTIONS:
        user_choice = answer_map.get(q['id'], '')
        is_correct = user_choice == q['answer']
        if is_correct: correct_count += 1
        results.append({
            'id': q['id'], 'user_choice': user_choice, 'correct_answer': q['answer'],
            'is_correct': is_correct, 'explanation': q['explanation']
        })

    score = int((correct_count / len(APP_QUESTIONS)) * 100)
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO attempts (user_id, module_type, score, answers_json) VALUES (?, ?, ?, ?)',
            (g.user_id, 'malicious_app', score, json.dumps(answer_map))
        )
        conn.commit()
    finally:
        conn.close()
    return jsonify({'score': score, 'results': results})


# ============ GOOGLE LOGIN & OTP FLOW ============

@app.route('/google_callback')
def google_authorized():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v1/userinfo")
    if not resp.ok:
        return "Failed to fetch user info", 400
        
    user_info = resp.json()
    email = user_info['email']
    name = user_info.get('name', 'User')
    google_id = user_info['id']

    conn = get_db()
    try:
        user = conn.execute('SELECT * FROM users WHERE email = ? OR google_id = ?', (email, google_id)).fetchone()
        
        if user and user['is_verified']:
            # Returning verified user -> Log in directly
            token = create_token(user['id'], user['email'])
            session['user_id'] = user['id']
            return redirect(f'/dashboard?token={token}') 
        
        else:
            # New user OR unverified user -> Generate OTP
            otp = str(random.randint(100000, 999999))
            expiry = datetime.now() + timedelta(minutes=10)
            
            if user:
                # Update existing unverified user
                conn.execute('UPDATE users SET otp_code = ?, otp_expiry = ? WHERE id = ?', (otp, expiry, user['id']))
                user_id = user['id']
            else:
                # Create new user
                cur = conn.execute('INSERT INTO users (name, email, google_id, is_verified, otp_code, otp_expiry) VALUES (?, ?, ?, 0, ?, ?)', 
                                   (name, email, google_id, otp, expiry))
                user_id = cur.lastrowid
            conn.commit()
            
            # Send OTP (Print to console for testing)
            print(f"\n=== 🚨 MOCK EMAIL SENT TO {email} ===")
            print(f"YOUR OTP IS: {otp}")
            print("=======================================\n")
            
            return redirect(f'/verify-email?user_id={user_id}')
    finally:
        conn.close()


@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    user_id = request.args.get('user_id')
    
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        
        conn = get_db()
        try:
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            
            if not user or user['otp_code'] != entered_otp:
                return "❌ Invalid OTP. Please try again.", 400
            
            # Check expiry
            expiry = datetime.strptime(user['otp_expiry'], '%Y-%m-%d %H:%M:%S.%f')
            if datetime.now() > expiry:
                return "❌ OTP Expired. Please log in again.", 400
                
            # Mark verified
            conn.execute('UPDATE users SET is_verified = 1, otp_code = NULL WHERE id = ?', (user_id,))
            conn.commit()
            
            # Log them in
            token = create_token(user['id'], user['email'])
            session['user_id'] = user['id']
            return redirect(f'/dashboard?token={token}') 
        finally:
            conn.close()

    # Simple form to enter OTP (You can style this beautifully)
    return '''
        <div style="font-family: sans-serif; text-align: center; margin-top: 100px;">
            <h2>Check Your Email</h2>
            <p>We sent a 6-digit code to your email address.</p>
            <form method="POST">
                <input type="text" name="otp" placeholder="Enter OTP" style="padding: 10px; font-size: 18px; letter-spacing: 5px; text-align: center;" required>
                <br><br>
                <button type="submit" style="padding: 10px 20px; background: #1a237e; color: white; border: none; border-radius: 5px;">Verify</button>
            </form>
        </div>
    '''

# ============ REPORTING ============
@app.route('/api/report-1930', methods=['POST'])
@token_required
def generate_report():
    data = request.get_json(silent=True) or {}
    scam_type = data.get('scam_type', 'Unknown')
    description = data.get('description', 'No additional details provided.')

    report_text = f"""--- NATIONAL CYBER CRIME REPORTING PORTAL (MOCK) ---
To: 1930 / cybercrime.gov.in
Date: {datetime.now().strftime('%d-%b-%Y')}

SUBJECT: Report of {scam_type}

DESCRIPTION OF INCIDENT:
{description}

SUSPECT DETAILS:
[If available, enter phone number, email, or UPI ID here]

I request the authorities to take immediate action to prevent financial loss and track the perpetrators.
--- END OF REPORT ---"""

    return jsonify({'report_text': report_text})

@app.route('/triage')
def triage_page():
    return render_template('triage.html')

@app.route('/api/triage/analyze', methods=['POST'])
@token_required
def analyze_text():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    result = analyze_scam_message(text)
    return jsonify(result)

@app.route('/report')
def report_page():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)