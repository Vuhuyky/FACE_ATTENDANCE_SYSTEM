import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
INSERT INTO course_sections
(
    course_id,
    section_name,
    room
)
VALUES
(
    ?, ?, ?
)
""",
(
    1,
    "KTPM01",
    "A101"
))

cursor.execute("""
INSERT INTO course_sections
(
    course_id,
    section_name,
    room
)
VALUES
(
    ?, ?, ?
)
""",
(
    2,
    "KTPM02",
    "A102"
))

conn.commit()

print("Sections inserted")

conn.close()