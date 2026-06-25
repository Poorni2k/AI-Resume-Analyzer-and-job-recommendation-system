import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM resume_history")
rows = cursor.fetchall()

print(rows)

conn.close()