from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template, g
from flask_cors import CORS
from database import init_db, get_db
from auth import hash_password, verify_password, create_token, token_required
import json
from phishing_content import PHISHING_QUESTIONS
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


if __name__ == '__main__':
    app.run(debug=True, port=3000)