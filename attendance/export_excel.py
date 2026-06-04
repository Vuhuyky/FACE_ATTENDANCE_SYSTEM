import sqlite3

from openpyxl import Workbook


def export_session_to_excel(
    session_id,
    output_file
):
    """
    Xuất danh sách điểm danh ra Excel
    """

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            s.student_code,
            s.full_name,
            ar.first_seen_time,
            ar.status
        FROM attendance_records ar

        JOIN students s
        ON ar.student_id = s.id

        WHERE ar.session_id = ?

        ORDER BY s.student_code
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    wb = Workbook()

    ws = wb.active

    ws.title = "Attendance"

    ws.append(
        [
            "Student Code",
            "Full Name",
            "Check In Time",
            "Status"
        ]
    )

    for row in rows:

        ws.append(row)

    wb.save(output_file)

    print(
        f"Excel exported: {output_file}"
    )