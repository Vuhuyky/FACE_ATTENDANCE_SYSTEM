import sqlite3


def attendance_report(
    session_id
):

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    # =====================================
    # Lấy section của session
    # =====================================

    cursor.execute(
        """
        SELECT section_id
        FROM attendance_sessions
        WHERE id = ?
        """,
        (session_id,)
    )

    result = cursor.fetchone()

    if not result:

        print(
            "Session not found"
        )

        conn.close()

        return

    section_id = result[0]

    # =====================================
    # Danh sách sinh viên thuộc lớp
    # =====================================

    cursor.execute(
        """
        SELECT
            s.id,
            s.student_code,
            s.full_name
        FROM students s

        JOIN enrollments e
        ON s.id = e.student_id

        WHERE e.section_id = ?
        """,
        (section_id,)
    )

    all_students = cursor.fetchall()

    # =====================================
    # Danh sách đã điểm danh
    # =====================================

    cursor.execute(
        """
        SELECT
            s.id,
            s.student_code,
            s.full_name,
            ar.first_seen_time
        FROM attendance_records ar

        JOIN students s
        ON ar.student_id = s.id

        WHERE ar.session_id = ?
        """,
        (session_id,)
    )

    present_students = cursor.fetchall()

    conn.close()

    # =====================================
    # Tạo set id đã điểm danh
    # =====================================

    present_ids = set()

    for row in present_students:

        present_ids.add(
            row[0]
        )

    # =====================================
    # Present
    # =====================================

    print()

    print("=" * 60)

    print(
        f"SESSION {session_id}"
    )

    print("=" * 60)

    print()

    print("PRESENT")

    print("-" * 60)

    for row in present_students:

        student_code = row[1]
        full_name = row[2]
        first_seen = row[3]

        print(
            f"✓ {student_code} | "
            f"{full_name} | "
            f"{first_seen}"
        )

    # =====================================
    # Absent
    # =====================================

    print()

    print("ABSENT")

    print("-" * 60)

    absent_count = 0

    for student in all_students:

        student_id = student[0]

        if student_id not in present_ids:

            absent_count += 1

            print(
                f"✗ {student[1]} | "
                f"{student[2]}"
            )

    # =====================================
    # Summary
    # =====================================

    print()

    print("=" * 60)

    print(
        f"Present: {len(present_students)}"
    )

    print(
        f"Absent : {absent_count}"
    )

    print(
        f"Total   : {len(all_students)}"
    )

    print("=" * 60)

if __name__ == "__main__":
    attendance_report(
        session_id=1
    )