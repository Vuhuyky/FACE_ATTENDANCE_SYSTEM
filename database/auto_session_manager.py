import os

from datetime import datetime

from database.connection import get_connection


def auto_session_manager():

    now = datetime.now()

    weekday = now.weekday() + 1

    current_time = now.strftime(
        "%H:%M"
    )

    print(
        f"[AUTO] weekday={weekday}"
    )

    print(
        f"[AUTO] current_time={current_time}"
    )

    conn = get_connection()

    print(
        "[AUTO] DB FILE =",
        os.path.abspath("attendance.db")
    )

    cursor = conn.cursor()

    # ==================================================
    # BƯỚC 1 - ĐÓNG CÁC PHIÊN ĐIỂM DANH QUÁ GIỜ
    # --------------------------------------------------
    # Đoạn này sẽ kiểm tra TẤT CẢ các phiên hiện đang hoạt động
    # và so sánh thời gian thực tế của nó (ngày_phiên + giờ_kết_thúc)
    # với thời gian hiện tại - bất kể hôm nay là thứ mấy trong tuần.
    #
    # Phiên bản cũ chỉ đóng các phiên thuộc về lịch trình của 
    # thứ (ngày trong tuần) ngày HÔM NAY. Điều đó có nghĩa là một phiên 
    # bị bỏ quên không đóng khi hết giờ (ví dụ: không ai bật ứng dụng 
    # vào đúng thời điểm kết thúc lớp) sẽ không bao giờ được đóng một khi
    # lịch đã chuyển sang một thứ khác trong tuần, bởi vì dòng lịch trình 
    # đó đơn giản là không được ngó ngàng tới nữa cho đến khi đúng thứ đó
    # của tuần sau quay trở lại.
    # ==================================================

    cursor.execute(
        """
        SELECT
            id,
            session_date,
            end_time
        FROM attendance_sessions
        WHERE is_active = 1
        """
    )

    active_sessions = cursor.fetchall()

    for session_id, session_date, end_time in active_sessions:

        try:

            session_end = datetime.strptime(
                f"{session_date} {end_time}",
                "%Y-%m-%d %H:%M"
            )

        except (TypeError, ValueError) as error:

            print(
                f"[AUTO] Skipping session {session_id}: "
                f"could not parse date/time ({error})"
            )

            continue

        if now > session_end:

            cursor.execute(
                """
                UPDATE attendance_sessions
                SET is_active = 0
                WHERE id = ?
                """,
                (
                    session_id,
                )
            )

            print(
                f"[AUTO CLOSE] Session {session_id} "
                f"(was due {session_end})"
            )

    conn.commit()

# ==================================================
# BƯỚC 2 - MỞ CÁC PHIÊN ĐIỂM DANH THEO LỊCH TRÌNH HÔM NAY
# --------------------------------------------------
# Giữ nguyên: chỉ có lịch trình của thứ (ngày trong tuần)
# ngày hôm nay mới có giá trị để quyết định xem một phiên 
# MỚI có nên được mở vào ngay thời điểm này hay không.
# ==================================================

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

        if start_time <= current_time <= end_time:

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