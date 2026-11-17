from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template, g
from flask_cors import CORS
from database import init_db, get_db
from auth import hash_password, verify_password, create_token, token_required
import json
from phishing_content import PHISHING_QUESTIONS
from digital_arrest_scam import DIGITAL_ARREST_SCENARIO
from contact_content import GOVT_CONTACTS
from malicious_app_content import APP_QUESTIONS
from learning_content import LEARNING_MODULES
app = Flask(__name__)
CORS(app)

with app.app_context():
    init_db()


# ============ BASIC ROUTES (from Milestone 1) ============

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
        return jsonify({
            'status': 'ok',
            'tables': [t['name'] for t in tables]
        })
    finally:
        conn.close()


# ============ AUTH ROUTES (Milestone 2) ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    # Validation
    if not name or not email or not password:
        return jsonify({'error': 'name, email, and password are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Invalid email format'}), 400

    conn = get_db()
    try:
        existing = conn.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        ).fetchone()
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
            'SELECT id, name, email, password_hash FROM users WHERE email = ?',
            (email,)
        ).fetchone()

        if not user or not verify_password(password, user['password_hash']):
            # Same error for "no such user" and "wrong password" — prevents email enumeration
            return jsonify({'error': 'Invalid email or password'}), 401

        token = create_token(user['id'], user['email'])
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        })
    finally:
        conn.close()


@app.route('/api/auth/me')
@token_required
def me():
    conn = get_db()
    try:
        user = conn.execute(
            'SELECT id, name, email, language, created_at '
            'FROM users WHERE id = ?', (g.user_id,)
        ).fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': dict(user)})
    finally:
        conn.close()


# ============ TEST PAGE (Milestone 2) ============

@app.route('/test')
def test_page():
    return render_template('auth_test.html')

# ============ PHISHING MODULE (Milestone 3) ============

@app.route('/api/phishing/questions')
@token_required
def phishing_questions():
    """Return questions WITHOUT the answers (to prevent cheating)."""
    sanitized = [{
        'id': q['id'],
        'sender_name': q['sender_name'],
        'sender_email': q['sender_email'],
        'subject': q['subject'],
        'body': q['body'],
    } for q in PHISHING_QUESTIONS]
    return jsonify({'questions': sanitized})


@app.route('/api/phishing/submit', methods=['POST'])
@token_required
def phishing_submit():
    """Score the answers and save the attempt."""
    data = request.get_json(silent=True) or {}
    answers = data.get('answers', [])

    if len(answers) != len(PHISHING_QUESTIONS):
        return jsonify({'error': 'Please answer all questions before submitting'}), 400

    answer_map = {a['id']: a['choice'] for a in answers if 'id' in a and 'choice' in a}

    results = []
    correct_count = 0
    for q in PHISHING_QUESTIONS:
        user_choice = answer_map.get(q['id'], '')
        is_correct = user_choice == q['answer']
        if is_correct:
            correct_count += 1
        results.append({
            'id': q['id'],
            'user_choice': user_choice,
            'correct_answer': q['answer'],
            'is_correct': is_correct,
            'red_flags': q['red_flags'],
            'explanation': q['explanation'],
        })

    score = int((correct_count / len(PHISHING_QUESTIONS)) * 100)

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO attempts (user_id, module_type, score, answers_json) '
            'VALUES (?, ?, ?, ?)',
            (g.user_id, 'phishing', score, json.dumps(answer_map))
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify({
        'score': score,
        'correct_count': correct_count,
        'total': len(PHISHING_QUESTIONS),
        'results': results,
    })


@app.route('/phishing')
def phishing_page():
    return render_template('phishing.html')

@app.route('/api/debug/attempts')
def debug_attempts():
    conn = get_db()
    try:
        rows = conn.execute('SELECT * FROM attempts ORDER BY id DESC LIMIT 5').fetchall()
        return jsonify({'attempts': [dict(r) for r in rows]})
    finally:
        conn.close()

# ============ DIGITAL ARREST MODULE (Milestone 4) ============

@app.route('/api/digital-arrest/scenario')
@token_required
def digital_arrest_scenario():
    # Returns the full scenario. 
    # Note: In a high-security production app, you'd hide the 'is_correct' flags 
    # and evaluate server-side. For this UI experience, client-side is smoother.
    return jsonify(DIGITAL_ARREST_SCENARIO)


@app.route('/api/digital-arrest/submit', methods=['POST'])
@token_required
def digital_arrest_submit():
    data = request.get_json(silent=True) or {}
    score = int(data.get('score', 0))

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO attempts (user_id, module_type, score, answers_json) '
            'VALUES (?, ?, ?, ?)',
            (g.user_id, 'digital_arrest', score, json.dumps({'completed': True}))
        )
        conn.commit()
    finally:
        conn.close()

    return jsonify({'status': 'ok'})


@app.route('/digital-arrest')
def digital_arrest_page():
    return render_template('digital_arrest.html')

# ============ DASHBOARD & REPORTING (Milestone 5) ============

@app.route('/')
def home():
    """Redirect root to dashboard."""
    from flask import redirect, url_for
    return redirect('/dashboard')


@app.route('/api/dashboard')
@token_required
def api_dashboard():
    conn = get_db()
    try:
        # Get user info
        user = conn.execute(
            'SELECT name FROM users WHERE id = ?', (g.user_id,)
        ).fetchone()
        
        # Get all attempts for this user (newest first)
        attempts = conn.execute(
            'SELECT module_type, score, attempted_at FROM attempts '
            'WHERE user_id = ? ORDER BY attempted_at ASC', (g.user_id,)
        ).fetchall()

        attempts_list = [dict(a) for a in attempts]
        
        # Calculate overall Risk Reflex Score (average of latest attempt per module)
        module_scores = {}
        for a in attempts_list:
            module_scores[a['module_type']] = a['score']  # latest overwrites older
        
        overall_score = int(sum(module_scores.values()) / len(module_scores)) if module_scores else 0

        return jsonify({
            'user_name': user['name'] if user else 'User',
            'overall_score': overall_score,
            'modules_completed': len(module_scores),
            'attempts': attempts_list
        })
    finally:
        conn.close()


@app.route('/api/report-1930', methods=['POST'])
@token_required
def generate_report():
    data = request.get_json(silent=True) or {}
    scam_type = data.get('scam_type', 'Unknown')
    description = data.get('description', 'No additional details provided.')

    # Generate a pre-filled complaint template
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


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# ============ EMERGENCY CONTACTS (New Feature) ============

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', contacts=GOVT_CONTACTS)

# ============ MALICIOUS APP MODULE (Milestone 6) ============

@app.route('/api/malicious-app/questions')
@token_required
def malicious_app_questions():
    # For this specific UI, we must send the explanation data so the client 
    # can show immediate feedback on click.
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


@app.route('/malicious-app')
def malicious_app_page():
    return render_template('malicious_app.html')

# ============ LEARNING CENTER (New Pre-requisite) ============

@app.route('/learning')
def learning_page():
    return render_template('learning.html', modules=LEARNING_MODULES)


if __name__ == '__main__':
    app.run(debug=True, port=3000)