import sqlite3

conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()

cursor.execute("""
DELETE FROM attendance_records
""")

conn.commit()

conn.close()

print("Attendance records cleared")