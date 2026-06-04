import sqlite3

conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()

cursor.execute("""
ALTER TABLE students
ADD COLUMN face_embedding TEXT
""")

conn.commit()

conn.close()

print("Column added successfully")