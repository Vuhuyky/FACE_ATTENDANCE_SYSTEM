import sqlite3

conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()

# Sinh viên 1
cursor.execute("""
INSERT INTO students (student_code, full_name, email)
VALUES (?, ?, ?)
""", (
    "22010001",
    "Nguyen Van A",
    "a@example.com"
))

# Sinh viên 2
cursor.execute("""
INSERT INTO students (student_code, full_name, email)
VALUES (?, ?, ?)
""", (
    "22010002",
    "Nguyen Van B",
    "b@example.com"
))

# Sinh viên 3
cursor.execute("""
INSERT INTO students (student_code, full_name, email)
VALUES (?, ?, ?)
""", (
    "22010003",
    "Nguyen Van C",
    "c@example.com"
))

conn.commit()

print("Students inserted successfully")

conn.close()