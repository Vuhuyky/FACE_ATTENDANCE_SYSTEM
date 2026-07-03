from database.connection import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT
id,
weekday,
section_id,
start_time,
end_time
FROM schedules
""")

for row in cursor.fetchall():
    print(row)

conn.close()