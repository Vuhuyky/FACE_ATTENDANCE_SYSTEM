import sqlite3

from datetime import datetime


def mark_attendance(
    session_id,
    student_id
):
    """
    Điểm danh sinh viên
    """

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    # ==========================
    # Kiểm tra đã điểm danh chưa
    # ==========================

    cursor.execute(
        """
        SELECT id
        FROM attendance_records
        WHERE session_id = ?
        AND student_id = ?
        """,
        (
            session_id,
            student_id
        )
    )

    record = cursor.fetchone()

    if record:

        conn.close()

        return False

    # ==========================
    # Chưa điểm danh
    # => INSERT
    # ==========================

    current_time = (
        datetime.now()
        .strftime("%H:%M:%S")
    )

    cursor.execute(
        """
        INSERT INTO attendance_records
        (
            session_id,
            student_id,
            first_seen_time,
            status
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """,
        (
            session_id,
            student_id,
            current_time,
            "Present"
        )
    )

    conn.commit()

    conn.close()

    return True