import sqlite3

def get_latest_session():

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM attendance_sessions
        ORDER BY id DESC
        LIMIT 1
        """
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        return result[0]

    return None

def attendance_report(
    session_id=None
):
    if session_id is None:

        session_id = get_latest_session()

        if session_id is None:

            print(
                "No session found"
            )

            return
        
    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    # =====================================
    # Lấy section của session
    # =====================================

    cursor.execute(
        """
        SELECT
            section_id,
            session_date
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

    session_date = result[1]

    # =====================================
    # Lấy thông tin môn học
    # =====================================

    cursor.execute(
        """
        SELECT
            c.course_name,
            cs.section_name
        FROM course_sections cs

        JOIN courses c
        ON cs.course_id = c.id

        WHERE cs.id = ?
        """,
        (section_id,)
    )

    course_info = cursor.fetchone()

    if not course_info:

        print(
            "Course information not found"
        )

        conn.close()

        return

    course_name = course_info[0]

    section_name = course_info[1]

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
    # Attendance Rate
    # =====================================

    attendance_rate = 0

    if len(all_students) > 0:

        attendance_rate = (
            len(present_students)
            / len(all_students)
        ) * 100

    # =====================================
    # Header
    # =====================================

    print()

    print("=" * 60)

    print(
        f"COURSE : {course_name}"
    )

    print(
        f"SECTION: {section_name}"
    )

    print(
        f"SESSION: {session_id}"
    )

    print(
        f"DATE   : {session_date}"
    )

    print("=" * 60)

    print()

    # =====================================
    # Present
    # =====================================

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
        f"Present : {len(present_students)}"
    )

    print(
        f"Absent  : {absent_count}"
    )

    print(
        f"Total   : {len(all_students)}"
    )

    print()

    print(
        f"Attendance Rate : "
        f"{attendance_rate:.2f}%"
    )

    print("=" * 60)


if __name__ == "__main__":

    attendance_report()