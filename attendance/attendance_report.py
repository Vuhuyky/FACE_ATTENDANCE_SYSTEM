import sqlite3

from database.connection import get_connection

def get_latest_session():

    conn = get_connection()

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


def get_all_sessions():
    """
    Returns every session, newest first, as
    (session_id, course_name, section_name, session_date)
    tuples - used to populate the session picker in the
    Attendance Report GUI.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            s.id,
            c.course_name,
            cs.section_name,
            s.session_date
        FROM attendance_sessions s

        JOIN course_sections cs
        ON s.section_id = cs.id

        JOIN courses c
        ON cs.course_id = c.id

        ORDER BY s.id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_attendance_report_data(session_id=None):
    """
    Gathers everything needed for an attendance report into
    a single dict, without printing anything. Both the CLI
    report below and the GUI report / Excel export build on
    top of this, so the underlying queries only live in one
    place.

    Returns None if the session (or its course/section) can't
    be found.
    """

    if session_id is None:

        session_id = get_latest_session()

        if session_id is None:

            return None

    conn = get_connection()

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

        conn.close()

        return None

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

        conn.close()

        return None

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

        ORDER BY s.student_code
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

        ORDER BY s.student_code
        """,
        (session_id,)
    )

    present_students = cursor.fetchall()

    conn.close()

    # =====================================
    # Tạo set id đã điểm danh
    # =====================================

    present_ids = {
        row[0]
        for row in present_students
    }

    absent_students = [
        student
        for student in all_students
        if student[0] not in present_ids
    ]

    total = len(all_students)

    present_count = len(present_students)

    absent_count = len(absent_students)

    attendance_rate = (
        (present_count / total) * 100
        if total > 0 else 0
    )

    return {
        "session_id": session_id,
        "course_name": course_name,
        "section_name": section_name,
        "session_date": session_date,
        "present_students": present_students,   # (id, code, name, first_seen_time)
        "absent_students": absent_students,      # (id, code, name)
        "present_count": present_count,
        "absent_count": absent_count,
        "total": total,
        "attendance_rate": attendance_rate
    }


def attendance_report(
    session_id=None
):
    """
    CLI report - unchanged behaviour, now built on top of
    get_attendance_report_data() instead of duplicating the
    queries itself.
    """

    report = get_attendance_report_data(session_id)

    if report is None:

        print(
            "No session found"
            if session_id is None
            else "Session not found"
        )

        return

    # =====================================
    # Header
    # =====================================

    print()

    print("=" * 60)

    print(
        f"COURSE : {report['course_name']}"
    )

    print(
        f"SECTION: {report['section_name']}"
    )

    print(
        f"SESSION: {report['session_id']}"
    )

    print(
        f"DATE   : {report['session_date']}"
    )

    print("=" * 60)

    print()

    # =====================================
    # Present
    # =====================================

    print("PRESENT")

    print("-" * 60)

    for row in report["present_students"]:

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

    for student in report["absent_students"]:

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
        f"Present : {report['present_count']}"
    )

    print(
        f"Absent  : {report['absent_count']}"
    )

    print(
        f"Total   : {report['total']}"
    )

    print()

    print(
        f"Attendance Rate : "
        f"{report['attendance_rate']:.2f}%"
    )

    print("=" * 60)


if __name__ == "__main__":

    attendance_report()