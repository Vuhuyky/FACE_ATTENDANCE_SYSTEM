import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import re
from database.connection import get_connection

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

def valid_time(time_text):

    pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"

    return re.match(
        pattern,
        time_text
    )

def save_session():

    section_text = combo_section.get().strip()

    session_date = date_entry.get()

    start_time = entry_start.get().strip()

    end_time = entry_end.get().strip()

    if not valid_time(start_time):

        messagebox.showerror(
            "Error",
            "Start Time must be HH:MM"
        )

        return

    if not valid_time(end_time):

        messagebox.showerror(
            "Error",
            "End Time must be HH:MM"
        )

        return
    if start_time >= end_time:

        messagebox.showerror(
            "Error",
            "End Time must be later than Start Time."
        )

        return

    if (

        not section_text

        or not session_date

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

    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id

        FROM attendance_sessions

        WHERE

            section_id = ?

        AND session_date = ?

        AND start_time = ?

        """
        ,
        (
            section_id,
            session_date,
            start_time
        )
    )

    if cursor.fetchone():

        messagebox.showerror(
            "Duplicate",
            "This session already exists."
        )

        conn.close()

        return

    try:

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

                ?, ?, ?, ?, 0

            )
            """,
            (
                section_id,
                session_date,
                start_time,
                end_time
            )
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Session created successfully."
        )

        root.destroy()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()

sections = load_sections()
root = tk.Tk()

root.title(
    "Create Session"
)

root.geometry(
    "420x360"
)

root.resizable(
    False,
    False
)
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

tk.Label(
    root,
    text="Session Date"
).pack(
    pady=(15,5)
)

date_entry = DateEntry(
    root,
    width=20,
    date_pattern="yyyy-mm-dd"
)

date_entry.pack()

tk.Label(
    root,
    text="Start Time (HH:MM)"
).pack(
    pady=(15,5)
)

entry_start = tk.Entry(
    root,
    width=25
)

entry_start.pack()

tk.Label(
    root,
    text="End Time (HH:MM)"
).pack(
    pady=(15,5)
)

entry_end = tk.Entry(
    root,
    width=25
)

entry_end.pack()

tk.Button(

    root,

    text="Create Session",

    width=20,

    command=save_session

).pack(
    pady=25
)

root.mainloop()
