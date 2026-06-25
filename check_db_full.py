import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

print("=== USERS TABLE ===")
cursor.execute("PRAGMA table_info(users)")
print(cursor.fetchall())

print("\n=== RESUME HISTORY DATA ===")
cursor.execute("SELECT * FROM resume_history")
print(cursor.fetchall())

conn.close()