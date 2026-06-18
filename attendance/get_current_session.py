import sqlite3


def get_current_session():

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM attendance_sessions
        WHERE is_active = 1
        LIMIT 1
        """
    )

    session = cursor.fetchone()

    conn.close()

    if session:

        return session[0]

    return None