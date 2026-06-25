import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

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

print("resume_history table ready")