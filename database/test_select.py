import sqlite3

conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(students)")

columns = cursor.fetchall()

for col in columns:
    print(col)

conn.close()