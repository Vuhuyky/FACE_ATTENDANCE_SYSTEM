import sqlite3

from datetime import date


conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

today = date.today().isoformat()

# ==========================
# Kiểm tra đã có session hôm nay chưa
# ==========================

cursor.execute(
    """
    SELECT id
    FROM attendance_sessions
    WHERE section_id = ?
    AND session_date = ?
    """,
    (
        1,
        today
    )
)

session = cursor.fetchone()

if session:

    print(
        f"Session already exists: {session[0]}"
    )

else:

    cursor.execute(
        """
        INSERT INTO attendance_sessions
        (
            section_id,
            session_date,
            start_time
        )
        VALUES
        (
            ?, ?, ?
        )
        """,
        (
            1,
            today,
            "07:00:00"
        )
    )

    conn.commit()

    print(
        "Session created!"
    )

conn.close()