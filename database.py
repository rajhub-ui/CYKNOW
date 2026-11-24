import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    """Connects to the Neon PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # This makes the rows behave like dictionaries (like sqlite3.Row did)
    conn.cursor_factory = psycopg2.extras.RealDictCursor 
    return conn

def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password_hash TEXT,
                google_id TEXT UNIQUE,
                language TEXT DEFAULT 'en',
                difficulty_level TEXT DEFAULT 'unassessed',
                is_verified INTEGER DEFAULT 0,
                otp_code TEXT,
                otp_expiry TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS attempts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                module_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                answers_json TEXT,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS link_checks (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                url TEXT NOT NULL,
                verdict TEXT NOT NULL,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                scam_type TEXT NOT NULL,
                description TEXT,
                reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # --- SELF-HEALING MIGRATIONS ---
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users';
        """)
        columns = [row['column_name'] for row in cursor.fetchall()]
        
        if 'difficulty_level' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN difficulty_level TEXT DEFAULT 'unassessed'")
            
        if 'google_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN google_id TEXT UNIQUE")
            
        if 'is_verified' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
            
        if 'otp_code' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN otp_code TEXT")
            
        if 'otp_expiry' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN otp_expiry TIMESTAMP")

        if 'phone' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT UNIQUE")

        conn.commit()
        print('✅ PostgreSQL Database initialized successfully')
    except Exception as e:
        print(f"Error initializing DB: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()