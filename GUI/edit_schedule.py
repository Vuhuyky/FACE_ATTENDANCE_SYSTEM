import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys

from database.connection import get_connection


if len(sys.argv) < 2:

    print(
        "Schedule ID not found."
    )

    exit()

schedule_id = int(
    sys.argv[1]
)
def load_sections():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            section_name
        FROM course_sections
        ORDER BY section_name
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
def load_schedule():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            section_id,

            weekday,

            start_time,

            end_time

        FROM schedules

        WHERE id = ?
        """,
        (
            schedule_id,
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row
def update_schedule(
    schedule_id,
    section_id,
    weekday,
    start_time,
    end_time
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE schedules

        SET

            section_id = ?,

            weekday = ?,

            start_time = ?,

            end_time = ?

        WHERE id = ?
        """,
        (
            section_id,
            weekday,
            start_time,
            end_time,
            schedule_id
        )
    )

    conn.commit()

    conn.close()

# ====================================================
# Load Data
# ====================================================

sections = load_sections()

schedule = load_schedule()

section_id = schedule[0]

weekday = schedule[1]

start_time = schedule[2]

end_time = schedule[3]

# ====================================================
# Window
# ====================================================

root = tk.Tk()

root.title(
    "Edit Schedule"
)

root.geometry(
    "420x350"
)

root.resizable(
    False,
    False
)
# ====================================================
# Section
# ====================================================

tk.Label(
    root,
    text="Section"
).pack(
    pady=(15,5)
)

combo_section = ttk.Combobox(
    root,
    width=35,
    state="readonly"
)

combo_section["values"] = [

    f"{row[0]} - {row[1]}"

    for row in sections

]

combo_section.pack()

for index, row in enumerate(sections):

    if row[0] == section_id:

        combo_section.current(index)

        break

# ====================================================
# Weekday
# ====================================================

tk.Label(
    root,
    text="Weekday"
).pack(
    pady=(15,5)
)

combo_weekday = ttk.Combobox(
    root,
    width=35,
    state="readonly"
)

combo_weekday["values"] = [

    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"

]

combo_weekday.current(
    weekday - 1
)

combo_weekday.pack()

# ====================================================
# Start Time
# ====================================================

tk.Label(
    root,
    text="Start Time"
).pack(
    pady=(15,5)
)

start_frame = tk.Frame(root)

start_frame.pack()

start_hour, start_minute = start_time.split(":")

combo_start_hour = ttk.Combobox(
    start_frame,
    width=5,
    state="readonly"
)

combo_start_hour["values"] = [

    f"{i:02d}"

    for i in range(24)

]

combo_start_hour.set(
    start_hour
)

combo_start_hour.pack(
    side=tk.LEFT
)

tk.Label(
    start_frame,
    text=":"
).pack(
    side=tk.LEFT,
    padx=5
)

combo_start_minute = ttk.Combobox(
    start_frame,
    width=5,
    state="readonly"
)

combo_start_minute["values"] = [

    "00",
    "15",
    "30",
    "45"

]

combo_start_minute.set(
    start_minute
)

combo_start_minute.pack(
    side=tk.LEFT
)

# ====================================================
# End Time
# ====================================================

tk.Label(
    root,
    text="End Time"
).pack(
    pady=(15,5)
)

end_frame = tk.Frame(root)

end_frame.pack()

end_hour, end_minute = end_time.split(":")

combo_end_hour = ttk.Combobox(
    end_frame,
    width=5,
    state="readonly"
)

combo_end_hour["values"] = [

    f"{i:02d}"

    for i in range(24)

]

combo_end_hour.set(
    end_hour
)

combo_end_hour.pack(
    side=tk.LEFT
)

tk.Label(
    end_frame,
    text=":"
).pack(
    side=tk.LEFT,
    padx=5
)

combo_end_minute = ttk.Combobox(
    end_frame,
    width=5,
    state="readonly"
)

combo_end_minute["values"] = [

    "00",
    "15",
    "30",
    "45"

]

combo_end_minute.set(
    end_minute
)

combo_end_minute.pack(
    side=tk.LEFT
)

# ====================================================
# Save
# ====================================================

def save_schedule():

    section_text = combo_section.get()

    weekday_text = combo_weekday.get()

    section_id = int(
        section_text.split(" - ")[0]
    )

    weekday_map = {

        "Monday":1,
        "Tuesday":2,
        "Wednesday":3,
        "Thursday":4,
        "Friday":5,
        "Saturday":6,
        "Sunday":7

    }

    weekday = weekday_map[
        weekday_text
    ]

    start_time = (
        combo_start_hour.get()
        + ":"
        + combo_start_minute.get()
    )

    end_time = (
        combo_end_hour.get()
        + ":"
        + combo_end_minute.get()
    )

    if end_time <= start_time:

        messagebox.showerror(
            "Error",
            "End time must be later than Start time."
        )

        return

    try:

        update_schedule(

            schedule_id,

            section_id,

            weekday,

            start_time,

            end_time

        )

        messagebox.showinfo(
            "Success",
            "Schedule updated successfully."
        )

        root.destroy()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

# ====================================================
# Button
# ====================================================

tk.Button(

    root,

    text="Update Schedule",

    width=20,

    command=save_schedule

).pack(

    pady=25

)

root.mainloop()

