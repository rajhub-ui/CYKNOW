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
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                language TEXT DEFAULT 'en',
                difficulty_level TEXT DEFAULT 'unassessed',
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
        
        # --- SELF-HEALING SCRIPT ---
        # This checks if your old database is missing the new column, and adds it automatically
        cursor = conn.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'difficulty_level' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN difficulty_level TEXT DEFAULT 'unassessed'")
            print('✅ Upgraded existing database: Added difficulty_level column')

        conn.commit()
        print('✅ Database initialized successfully')
    finally:
        conn.close()

# Run directly to init the DB manually (useful for testing)
if __name__ == '__main__':
    init_db()