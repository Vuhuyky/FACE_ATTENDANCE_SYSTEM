import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
student_code,
full_name,
LENGTH(face_embedding)
FROM students
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()