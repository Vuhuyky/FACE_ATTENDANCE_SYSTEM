import sqlite3
from database.connection import get_connection
conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_code TEXT UNIQUE NOT NULL,

    full_name TEXT NOT NULL,

    email TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_code TEXT UNIQUE NOT NULL,

    course_name TEXT NOT NULL

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS course_sections (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    course_id INTEGER NOT NULL,

    section_name TEXT NOT NULL,

    room TEXT,

    FOREIGN KEY(course_id)
    REFERENCES courses(id)

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id INTEGER NOT NULL,

    section_id INTEGER NOT NULL,

    FOREIGN KEY(student_id)
    REFERENCES students(id),

    FOREIGN KEY(section_id)
    REFERENCES course_sections(id),

    UNIQUE(student_id, section_id)

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance_sessions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    section_id INTEGER NOT NULL,

    session_date DATE NOT NULL,

    start_time TIME,

    end_time TIME,

    FOREIGN KEY(section_id)
    REFERENCES course_sections(id)

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance_records (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    session_id INTEGER NOT NULL,

    student_id INTEGER NOT NULL,

    first_seen_time TIME,

    status TEXT NOT NULL,

    FOREIGN KEY(session_id)
    REFERENCES attendance_sessions(id),

    FOREIGN KEY(student_id)
    REFERENCES students(id),

    UNIQUE(session_id, student_id)

)
""")

conn.commit()

print("Students table created successfully")
print("Courses table created successfully")
print("Course sections table created successfully")
print("Enrollments table created successfully")
print("Attendance sessions table created successfully")
print("Attendance records table created successfully")
conn.close()