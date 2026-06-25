import sqlite3


def get_session_section(session_id):

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT section_id
        FROM attendance_sessions
        WHERE id = ?
        """,
        (session_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None