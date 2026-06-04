import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM course_sections
""")

rows = cursor.fetchall()

for row in rows:

    print(row)

conn.close()