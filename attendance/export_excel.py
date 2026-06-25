import sqlite3

from openpyxl import Workbook


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


def export_session_to_excel(
    session_id=None,
    output_file="attendance_report.xlsx"
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
    # Session info
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

    session = cursor.fetchone()

    if not session:

        print(
            "Session not found"
        )

        conn.close()

        return

    section_id = session[0]

    session_date = session[1]

    # =====================================
    # Course info
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

    course_name = course_info[0]

    section_name = course_info[1]

    # =====================================
    # All students
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
    # Present students
    # =====================================

    cursor.execute(
        """
        SELECT
            ar.student_id,
            ar.first_seen_time
        FROM attendance_records ar

        WHERE ar.session_id = ?
        """,
        (session_id,)
    )

    attendance_rows = cursor.fetchall()

    conn.close()

    # =====================================
    # Convert to dictionary
    # =====================================

    attendance_dict = {}

    for row in attendance_rows:

        attendance_dict[row[0]] = row[1]

    # =====================================
    # Excel
    # =====================================

    wb = Workbook()

    ws = wb.active

    ws.title = "Attendance"

    ws.append(
        [
            "Course",
            course_name
        ]
    )

    ws.append(
        [
            "Section",
            section_name
        ]
    )

    ws.append(
        [
            "Date",
            session_date
        ]
    )

    ws.append([])

    ws.append(
        [
            "Student Code",
            "Full Name",
            "Check In Time",
            "Status"
        ]
    )

    present_count = 0

    absent_count = 0

    for student in all_students:

        student_id = student[0]

        student_code = student[1]

        full_name = student[2]

        if student_id in attendance_dict:

            present_count += 1

            ws.append(
                [
                    student_code,
                    full_name,
                    attendance_dict[student_id],
                    "Present"
                ]
            )

        else:

            absent_count += 1

            ws.append(
                [
                    student_code,
                    full_name,
                    "-",
                    "Absent"
                ]
            )

    ws.append([])

    ws.append(
        [
            "Present",
            present_count
        ]
    )

    ws.append(
        [
            "Absent",
            absent_count
        ]
    )

    ws.append(
        [
            "Total",
            len(all_students)
        ]
    )

    attendance_rate = 0

    if len(all_students) > 0:

        attendance_rate = (
            present_count
            / len(all_students)
        ) * 100

    ws.append(
        [
            "Attendance Rate",
            f"{attendance_rate:.2f}%"
        ]
    )

    wb.save(
        output_file
    )

    print(
        f"Excel exported: {output_file}"
    )


if __name__ == "__main__":

    export_session_to_excel()