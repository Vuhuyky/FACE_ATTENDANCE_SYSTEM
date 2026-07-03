import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database.connection import get_connection


# ====================================================
# Load Sections
# ====================================================

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


# ====================================================
# Add Schedule
# ====================================================

def add_schedule():

    section_text = combo_section.get().strip()

    weekday_text = combo_weekday.get().strip()

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
    if (
        not section_text
        or not weekday_text
        or not start_time
        or not end_time
    ):

        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )

        return

    section_id = int(
        section_text.split(" - ")[0]
    )

    weekday_map = {

        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7

    }

    weekday = weekday_map[
        weekday_text
    ]

    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*)

        FROM schedules

        WHERE

            section_id = ?

            AND weekday = ?

            AND start_time = ?

            AND end_time = ?
        """,
        (
            section_id,
            weekday,
            start_time,
            end_time
        )
    )

    if cursor.fetchone()[0] > 0:

        messagebox.showwarning(
            "Duplicate",
            "This schedule already exists."
        )

        conn.close()

        return
    
    cursor.execute(
        """
        SELECT

            start_time,
            end_time

        FROM schedules

        WHERE

            section_id = ?

            AND weekday = ?
        """,
        (
            section_id,
            weekday
        )
    )

    existing = cursor.fetchall()

    for row in existing:

        old_start = row[0]

        old_end = row[1]

        if (
            start_time < old_end
            and end_time > old_start
        ):

            messagebox.showerror(
                "Schedule Conflict",
                "Time overlaps with another schedule."
            )

            conn.close()

            return                              
    try:

        cursor.execute(
            """
            INSERT INTO schedules
            (
                section_id,
                weekday,
                start_time,
                end_time
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                section_id,
                weekday,
                start_time,
                end_time
            )
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Schedule added successfully."
        )

        root.destroy()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()


# ====================================================
# Window
# ====================================================

root = tk.Tk()

root.title(
    "Add Schedule"
)

root.geometry(
    "420x320"
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
    pady=(15, 5)
)

combo_section = ttk.Combobox(
    root,
    width=35,
    state="readonly"
)

sections = load_sections()

combo_section["values"] = [

    f"{row[0]} - {row[1]}"

    for row in sections

]

combo_section.pack()


# ====================================================
# Weekday
# ====================================================

tk.Label(
    root,
    text="Weekday"
).pack(
    pady=(15, 5)
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

combo_start_hour = ttk.Combobox(
    start_frame,
    width=5,
    state="readonly"
)

combo_start_hour["values"] = [

    f"{i:02d}"

    for i in range(24)

]

combo_start_hour.current(7)

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

combo_start_minute.current(0)

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

combo_end_hour = ttk.Combobox(
    end_frame,
    width=5,
    state="readonly"
)

combo_end_hour["values"] = [

    f"{i:02d}"

    for i in range(24)

]

combo_end_hour.current(9)

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

combo_end_minute.current(0)

combo_end_minute.pack(
    side=tk.LEFT
)


# ====================================================
# Button
# ====================================================

tk.Button(
    root,
    text="Add Schedule",
    width=20,
    command=add_schedule
).pack(
    pady=25
)

root.mainloop()