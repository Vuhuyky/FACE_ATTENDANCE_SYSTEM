import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT *
    FROM attendance_sessions
    """
)

for row in cursor.fetchall():

    print(row)

conn.close()