import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

print("=== TABLE CHECK ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

print("\n=== RESUME HISTORY DATA ===")
cursor.execute("SELECT * FROM resume_history")
print(cursor.fetchall())

conn.close()
