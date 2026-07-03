import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    student_code,
    full_name
FROM students
""")

for row in cursor.fetchall():

    print(row)

conn.close()