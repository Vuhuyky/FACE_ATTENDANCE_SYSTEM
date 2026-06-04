import sqlite3

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

enrollments = [

    (1, 1),  # Vu Huy Ky -> KTPM01

    (2, 1),  # Nguyen Thanh Hai -> KTPM01

    (3, 1)   # Nguyen Van C -> KTPM01

]

for enrollment in enrollments:

    cursor.execute(
        """
        INSERT OR IGNORE INTO enrollments
        (
            student_id,
            section_id
        )
        VALUES
        (
            ?, ?
        )
        """,
        enrollment
    )

conn.commit()

conn.close()

print(
    "Enrollments inserted"
)