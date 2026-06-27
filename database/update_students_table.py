import sqlite3
from database.connection import get_connection
conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
ALTER TABLE students
ADD COLUMN face_embedding TEXT
""")

conn.commit()

conn.close()

print("Column added successfully")