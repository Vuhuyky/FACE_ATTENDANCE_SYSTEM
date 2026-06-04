from attendance.get_current_session import (
    get_current_session
)

session_id = get_current_session()

print(
    "Current Session:",
    session_id
)