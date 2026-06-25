import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM schedules
""")

rows = cursor.fetchall()

print(rows)

conn.close()