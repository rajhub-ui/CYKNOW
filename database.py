import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'cyberfit.db')


def get_db():
    """Open a connection with foreign keys enabled and dict-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    try:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                module_type TEXT NOT NULL,
                score INTEGER NOT NULL,
                answers_json TEXT,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS link_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                url TEXT NOT NULL,
                verdict TEXT NOT NULL,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                scam_type TEXT NOT NULL,
                description TEXT,
                reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')
        
        # --- SELF-HEALING MIGRATIONS ---
        cursor = conn.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'difficulty_level' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN difficulty_level TEXT DEFAULT 'unassessed'")
            print('✅ Upgraded DB: Added difficulty_level')
            
        # NOTE: We add the column without UNIQUE here, then create a UNIQUE INDEX below
        if 'google_id' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN google_id TEXT")
            print('✅ Upgraded DB: Added google_id')
            
        if 'is_verified' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
            print('✅ Upgraded DB: Added is_verified')
            
        if 'otp_code' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN otp_code TEXT")
            print('✅ Upgraded DB: Added otp_code')
            
        if 'otp_expiry' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN otp_expiry TIMESTAMP")
            print('✅ Upgraded DB: Added otp_expiry')

        if 'phone' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN phone TEXT")
            print('✅ Upgraded DB: Added phone')

        # Add unique indexes safely for existing tables
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id)")
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")

        conn.commit()
        print('✅ Database initialized successfully')
    finally:
        conn.close()

# Run directly to init the DB manually (useful for testing)
if __name__ == '__main__':
    init_db()