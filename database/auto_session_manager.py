import sqlite3

from datetime import datetime


def auto_session_manager():

    now = datetime.now()

    weekday = now.weekday()

    current_time = now.strftime(
        "%H:%M"
    )

    print(
        f"[AUTO] weekday={weekday}"
    )

    print(
        f"[AUTO] current_time={current_time}"
    )

    conn = sqlite3.connect(
        "attendance.db"
    )
    import os

    print(
        "[AUTO] DB FILE =",
        os.path.abspath("attendance.db")
    )
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            section_id,
            start_time,
            end_time
        FROM schedules
        WHERE weekday = ?
        """,
        (
            weekday,
        )
    )

    schedules = cursor.fetchall()
    print(
        "[AUTO] RAW SCHEDULES =",
        schedules
    )

    print(
        f"[AUTO] schedules={len(schedules)}"
    )

    for schedule in schedules:

        schedule_id = schedule[0]

        section_id = schedule[1]

        start_time = schedule[2]

        end_time = schedule[3]

        print(
            f"[AUTO] checking "
            f"section={section_id} "
            f"{start_time}-{end_time}"
        )

        # ==========================
        # HẾT GIỜ HỌC
        # ==========================

        if current_time > end_time:

            cursor.execute(
                """
                UPDATE attendance_sessions
                SET is_active = 0
                WHERE section_id = ?
                AND is_active = 1
                """,
                (
                    section_id,
                )
            )

            if cursor.rowcount > 0:

                print(
                    f"[AUTO CLOSE] "
                    f"Section {section_id}"
                )

                conn.commit()

        # ==========================
        # ĐANG TRONG GIỜ HỌC
        # ==========================

        elif start_time <= current_time <= end_time:

            cursor.execute(
                """
                SELECT id
                FROM attendance_sessions
                WHERE section_id = ?
                AND is_active = 1
                LIMIT 1
                """,
                (
                    section_id,
                )
            )

            session = cursor.fetchone()

            if not session:

                today = (
                    now.date()
                    .isoformat()
                )

                cursor.execute(
                    """
                    INSERT INTO
                    attendance_sessions
                    (
                        section_id,
                        session_date,
                        start_time,
                        end_time,
                        is_active
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, 1
                    )
                    """,
                    (
                        section_id,
                        today,
                        start_time,
                        end_time
                    )
                )

                conn.commit()

                print(
                    f"[AUTO OPEN] "
                    f"Section {section_id}"
                )

            else:

                print(
                    f"[AUTO] "
                    f"Session already active "
                    f"for section "
                    f"{section_id}"
                )

    conn.close()