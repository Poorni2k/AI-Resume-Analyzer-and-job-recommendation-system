import sqlite3

DB_NAME = "users.db"


# ================= CREATE TABLES ================= #
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    # RESUME HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        resume_name TEXT,
        ats_score INTEGER,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")


# ================= ADD ADMIN USER ================= #
def create_admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, ("admin", "admin123", "admin"))

    conn.commit()
    conn.close()
    print("Admin ensured")


# ================= ADD ROLE COLUMN (SAFE MIGRATION) ================= #
def add_role_column():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        print("Role column added")
    except:
        print("Role column already exists")

    conn.commit()
    conn.close()


# ================= MAIN RUN ================= #
if __name__ == "__main__":
    init_db()
    add_role_column()
    create_admin()