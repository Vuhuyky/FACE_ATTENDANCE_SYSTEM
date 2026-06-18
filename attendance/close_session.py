import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute(
    """
    UPDATE attendance_sessions
    SET is_active = 0
    WHERE is_active = 1
    """
)

conn.commit()

print(
    f"Closed {cursor.rowcount} session(s)"
)

conn.close()