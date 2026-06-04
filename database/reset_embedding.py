import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
UPDATE students
SET face_embedding = NULL
""")

conn.commit()

conn.close()

print(
    "All embeddings reset"
)