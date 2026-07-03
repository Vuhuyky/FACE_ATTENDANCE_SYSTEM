import sqlite3

from utils import (
    json_to_embedding
)

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
student_code,
full_name,
face_embedding
FROM students
WHERE face_embedding IS NOT NULL
""")

rows = cursor.fetchall()

students = []

for row in rows:

    students.append(
        (
            row[0],
            row[1],
            json_to_embedding(
                row[2]
            )
        )
    )

conn.close()

print(
    f"Loaded {len(students)} students"
)

for student in students:

    print(
        student[0],
        student[1],
        student[2].shape
    )