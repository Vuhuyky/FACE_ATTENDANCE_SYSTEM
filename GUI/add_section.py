import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database.connection import get_connection


# ====================================================
# Load Courses
# ====================================================

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

    courses = cursor.fetchall()

    conn.close()

    return courses


# ====================================================
# Add Section
# ====================================================

def add_section():

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

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO course_sections
            (
                course_id,
                section_name,
                room
            )
            VALUES
            (
                ?, ?, ?
            )
            """,
            (
                course_id,
                section_name,
                room
            )
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Section added successfully."
        )

        entry_section.delete(
            0,
            tk.END
        )

        entry_room.delete(
            0,
            tk.END
        )

        combo_course.current(0)

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
    "Add Section"
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

courses = load_courses()

combo_course["values"] = [

    f"{row[0]} - {row[1]} ({row[2]})"

    for row in courses

]

if courses:

    combo_course.current(0)

combo_course.pack()


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


# ====================================================
# Button
# ====================================================

tk.Button(
    root,
    text="Add Section",
    width=20,
    command=add_section
).pack(
    pady=25
)


root.mainloop()