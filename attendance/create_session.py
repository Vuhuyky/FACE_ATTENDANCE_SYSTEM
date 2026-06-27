import sqlite3

from datetime import date
from database.connection import get_connection

today = date.today().isoformat()

conn = get_connection()

cursor = conn.cursor()

# ==========================
# Tắt tất cả session cũ
# ==========================

cursor.execute(
    """
    UPDATE attendance_sessions
    SET is_active = 0
    """
)

# ==========================
# Tạo session mới
# ==========================

cursor.execute(
    """
    INSERT INTO attendance_sessions
    (
        section_id,
        session_date,
        start_time,
        end_time,
        is_active
    )
    VALUES
    (
        ?, ?, ?, ?, ?
    )
    """,
    (
        1,
        today,
        "07:00:00",
        "23:59:59",
        1
    )
)

conn.commit()

print(
    f"Created Session ID = "
    f"{cursor.lastrowid}"
)

conn.close()