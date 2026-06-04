import sqlite3

from datetime import date


def get_current_session():

    today = date.today().isoformat()

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM attendance_sessions
        WHERE session_date = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            today,
        )
    )

    session = cursor.fetchone()

    conn.close()

    if session:

        return session[0]

    return None