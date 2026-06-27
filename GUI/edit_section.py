import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
from database.connection import get_connection

if len(sys.argv) < 2:

    print(
        "Section ID not found."
    )

    exit()
section_id = int(
    sys.argv[1]
)

def load_courses():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            course_code,
            course_name
        FROM courses
        ORDER BY course_code
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

def load_section():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            course_id,
            section_name,
            room

        FROM course_sections

        WHERE id = ?
        """,
        (
            section_id,
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row

def update_section(
    section_id,
    course_id,
    section_name,
    room
):
    
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE course_sections

        SET
            course_id = ?,
            section_name = ?,
            room = ?

        WHERE id = ?
        """,
        (
            course_id,
            section_name,
            room,
            section_id
        )
    )

    conn.commit()

    conn.close()
# ====================================================
# Save
# ====================================================

def save_section():

    course_text = combo_course.get().strip()

    section_name = entry_section.get().strip()

    room = entry_room.get().strip()

    if (
        not course_text
        or not section_name
        or not room
    ):

        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )

        return

    course_id = int(
        course_text.split(" - ")[0]
    )

    try:

        update_section(
            section_id,
            course_id,
            section_name,
            room
        )

        messagebox.showinfo(
            "Success",
            "Section updated successfully."
        )

        root.destroy()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
# ====================================================
# Load Data
# ====================================================

courses = load_courses()

section = load_section()

course_id = section[0]

old_section_name = section[1]

old_room = section[2]


# ====================================================
# Window
# ====================================================

root = tk.Tk()

root.title(
    "Edit Section"
)

root.geometry(
    "420x300"
)

root.resizable(
    False,
    False
)


# ====================================================
# Course
# ====================================================

tk.Label(
    root,
    text="Course"
).pack(
    pady=(15, 5)
)

combo_course = ttk.Combobox(
    root,
    width=35,
    state="readonly"
)

combo_course["values"] = [

    f"{row[0]} - {row[1]} ({row[2]})"

    for row in courses

]

combo_course.pack()

for index, row in enumerate(courses):

    if row[0] == course_id:

        combo_course.current(index)

        break


# ====================================================
# Section Name
# ====================================================

tk.Label(
    root,
    text="Section Name"
).pack(
    pady=(15, 5)
)

entry_section = tk.Entry(
    root,
    width=40
)

entry_section.pack()

entry_section.insert(
    0,
    old_section_name
)


# ====================================================
# Room
# ====================================================

tk.Label(
    root,
    text="Room"
).pack(
    pady=(15, 5)
)

entry_room = tk.Entry(
    root,
    width=40
)

entry_room.pack()

entry_room.insert(
    0,
    old_room
)


# ====================================================
# Button
# ====================================================

tk.Button(
    root,
    text="Update Section",
    width=20,
    command=save_section
).pack(
    pady=25
)

root.mainloop()