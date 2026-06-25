import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# add role column safely
try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("Role column added successfully")
except Exception as e:
    print("Already exists or error:", e)

conn.commit()
conn.close()