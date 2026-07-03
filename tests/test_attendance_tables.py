import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

print("\nATTENDANCE SESSIONS\n")

cursor.execute("""
SELECT *
FROM attendance_sessions
""")

for row in cursor.fetchall():

    print(row)

print("\nATTENDANCE RECORDS\n")

cursor.execute("""
SELECT *
FROM attendance_records
""")

for row in cursor.fetchall():

    print(row)

conn.close()