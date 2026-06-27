import sqlite3
from database.connection import get_connection
conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
INSERT INTO courses
(
    course_code,
    course_name
)
VALUES
(
    ?,
    ?
)
""",
(
    "CV101",
    "Computer Vision"
))

cursor.execute("""
INSERT INTO courses
(
    course_code,
    course_name
)
VALUES
(
    ?,
    ?
)
""",
(
    "AI101",
    "Artificial Intelligence"
))

conn.commit()

print("Courses inserted")

conn.close()