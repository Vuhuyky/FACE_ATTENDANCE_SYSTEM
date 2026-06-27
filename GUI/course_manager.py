import sqlite3

import tkinter as tk

import subprocess
import sys

from tkinter import ttk
from tkinter import messagebox

from tkinter import simpledialog

from database.connection import get_connection
# ====================================================
# Database
# ====================================================

DB_NAME = "attendance.db"


# ====================================================
# Load Courses
# ====================================================

def load_courses():

    for row in course_tree.get_children():

        course_tree.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            course_code,
            course_name
        FROM courses

        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        course_tree.insert(
            "",
            tk.END,
            values=row
        )

# ====================================================
# Add Course
# ====================================================

def add_course():

    course_code = simpledialog.askstring(
        "Course Code",
        "Enter course code:"
    )

    if not course_code:
        return

    course_name = simpledialog.askstring(
        "Course Name",
        "Enter course name:"
    )

    if not course_name:
        return

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO courses
            (
                course_code,
                course_name
            )
            VALUES
            (
                ?, ?
            )
            """,
            (
                course_code,
                course_name
            )
        )

        conn.commit()

        load_courses()

        messagebox.showinfo(
            "Success",
            "Course added successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()
        
# ====================================================
# Edit Course
# ====================================================

def edit_course():

    selected = course_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a course."
        )

        return

    values = course_tree.item(
        selected[0],
        "values"
    )

    course_id = values[0]

    old_code = values[1]

    old_name = values[2]

    new_code = simpledialog.askstring(
        "Edit Course",
        "Course Code:",
        initialvalue=old_code
    )

    if not new_code:

        return

    new_name = simpledialog.askstring(
        "Edit Course",
        "Course Name:",
        initialvalue=old_name
    )

    if not new_name:

        return

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            UPDATE courses
            SET
                course_code = ?,
                course_name = ?
            WHERE id = ?
            """,
            (
                new_code,
                new_name,
                course_id
            )
        )

        conn.commit()

        load_courses()

        load_sections()

        load_schedules()

        messagebox.showinfo(
            "Success",
            "Course updated successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()

def delete_course():

    selected = course_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a course."
        )

        return

    values = course_tree.item(
        selected[0],
        "values"
    )

    course_id = values[0]

    answer = messagebox.askyesno(
        "Delete",
        "Delete this course?\n\nThis action cannot be undone."
    )

    if not answer:

        return

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM courses
            WHERE id = ?
            """,
            (course_id,)
        )

        conn.commit()

        load_courses()

        load_sections()

        messagebox.showinfo(
            "Success",
            "Course deleted successfully."
        )
    except sqlite3.IntegrityError:

        messagebox.showwarning(
            "Cannot Delete",
            "This course is being used by one or more sections."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()

# ====================================================
# Load Sections
# ====================================================

def load_sections():

    for row in section_tree.get_children():

        section_tree.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            cs.id,

            c.course_code,

            cs.section_name,

            cs.room

        FROM course_sections cs

        JOIN courses c
        ON cs.course_id = c.id

        ORDER BY cs.id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        section_tree.insert(
            "",
            tk.END,
            values=row
        )

def open_add_section():

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.add_section"
        ]
    )
def edit_section():

    selected = section_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a section."
        )

        return

    values = section_tree.item(
        selected[0],
        "values"
    )

    section_id = values[0]

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.edit_section",
            str(section_id)
        ]
    )
def delete_section():

    selected = section_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a section."
        )

        return

    values = section_tree.item(
        selected[0],
        "values"
    )

    section_id = values[0]

    section_name = values[2]

    answer = messagebox.askyesno(
        "Confirm Delete",
        f"Delete section '{section_name}' ?"
    )

    if not answer:

        return

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM course_sections
            WHERE id = ?
            """,
            (
                section_id,
            )
        )

        conn.commit()

        load_sections()

        messagebox.showinfo(
            "Success",
            "Section deleted successfully."
        )

    except sqlite3.IntegrityError:

        messagebox.showwarning(
            "Cannot Delete",
            "Students are enrolled in this section."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()

# ====================================================
# Load Schedule
# ====================================================

def load_schedules():

    for row in schedule_tree.get_children():

        schedule_tree.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            s.id,

            cs.section_name,

            s.weekday,

            s.start_time,

            s.end_time

        FROM schedules s

        JOIN course_sections cs
        ON s.section_id = cs.id

        ORDER BY s.id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    weekday_name = {

        0: "Monday",

        1: "Tuesday",

        2: "Wednesday",

        3: "Thursday",

        4: "Friday",

        5: "Saturday",

        6: "Sunday"

    }

    for row in rows:

        schedule_tree.insert(

            "",

            tk.END,

            values=(

                row[0],

                row[1],

                weekday_name[row[2]],

                row[3],

                row[4]

            )
        )


# ====================================================
# Window
# ====================================================

root = tk.Tk()

root.title(
    "Course Manager"
)

root.geometry(
    "1400x950"
)
root.minsize(
    1200,
    850
)
root.resizable(
    False,
    False
)


# ====================================================
# COURSE FRAME
# ====================================================

course_frame = tk.LabelFrame(

    root,

    text="Courses",

    padx=10,

    pady=10

)

course_frame.pack(

    fill="x",

    padx=10,

    pady=10

)


course_tree = ttk.Treeview(

    course_frame,

    columns=(

        "ID",

        "Code",

        "Name"

    ),

    show="headings",

    height=6

)

course_tree.heading(
    "ID",
    text="ID"
)

course_tree.heading(
    "Code",
    text="Course Code"
)

course_tree.heading(
    "Name",
    text="Course Name"
)

course_tree.column(
    "ID",
    width=60
)

course_tree.column(
    "Code",
    width=220,
    stretch=True
)

course_tree.column(
    "Name",
    width=400
)

course_tree.pack(
    fill="x"
)


# ====================================================
# SECTION FRAME
# ====================================================

section_frame = tk.LabelFrame(

    root,

    text="Sections",

    padx=10,

    pady=10

)

section_frame.pack(

    fill="x",

    padx=10,

    pady=10

)


section_tree = ttk.Treeview(

    section_frame,

    columns=(

        "ID",

        "Course",

        "Section",

        "Room"

    ),

    show="headings",

    height=6

)

section_tree.heading(
    "ID",
    text="ID"
)

section_tree.heading(
    "Course",
    text="Course"
)

section_tree.heading(
    "Section",
    text="Section"
)

section_tree.heading(
    "Room",
    text="Room"
)

section_tree.column(
    "ID",
    width=60
)

section_tree.column(
    "Course",
    width=120
)

section_tree.column(
    "Section",
    width=150
)

section_tree.column(
    "Room",
    width=120
)

section_tree.pack(
    fill="x"
)


# ====================================================
# SCHEDULE FRAME
# ====================================================

schedule_frame = tk.LabelFrame(

    root,

    text="Schedules",

    padx=10,

    pady=10

)

schedule_frame.pack(

    fill="both",

    expand=True,

    padx=10,

    pady=10

)


schedule_tree = ttk.Treeview(

    schedule_frame,

    columns=(

        "ID",

        "Section",

        "Weekday",

        "Start",

        "End"

    ),

    show="headings",

    height=10

)

schedule_tree.heading(
    "ID",
    text="ID"
)

schedule_tree.heading(
    "Section",
    text="Section"
)

schedule_tree.heading(
    "Weekday",
    text="Weekday"
)

schedule_tree.heading(
    "Start",
    text="Start"
)

schedule_tree.heading(
    "End",
    text="End"
)

schedule_tree.column(
    "ID",
    width=60
)

schedule_tree.column(
    "Section",
    width=120
)

schedule_tree.column(
    "Weekday",
    width=120
)

schedule_tree.column(
    "Start",
    width=120
)

schedule_tree.column(
    "End",
    width=120
)

schedule_tree.pack(
    fill="both",
    expand=True
)

# ====================================================
# BUTTON FRAME
# ====================================================

button_frame = tk.Frame(
    root
)

button_frame.pack(
    pady=10
)


# ====================================================
# COURSE BUTTONS
# ====================================================

course_button_frame = tk.LabelFrame(
    button_frame,
    text="Course"
)

course_button_frame.grid(
    row=0,
    column=0,
    padx=10
)


btn_add_course = tk.Button(
    course_button_frame,
    text="Add",
    width=12,
    command=add_course
)

btn_add_course.pack(
    pady=5
)


btn_edit_course = tk.Button(
    course_button_frame,
    text="Edit",
    width=12,
    command=edit_course
)

btn_edit_course.pack(
    pady=5
)


btn_delete_course = tk.Button(
    course_button_frame,
    text="Delete",
    width=12,
    command=delete_course
)

btn_delete_course.pack(
    pady=5
)


# ====================================================
# SECTION BUTTONS
# ====================================================

section_button_frame = tk.LabelFrame(
    button_frame,
    text="Section"
)

section_button_frame.grid(
    row=0,
    column=1,
    padx=10
)


btn_add_section = tk.Button(
    section_button_frame,
    text="Add",
    width=12,
    command=open_add_section
)

btn_add_section.pack(
    pady=5
)


btn_edit_section = tk.Button(
    section_button_frame,
    text="Edit",
    width=12,
    command=edit_section
)

btn_edit_section.pack(
    pady=5
)


btn_delete_section = tk.Button(
    section_button_frame,
    text="Delete",
    width=12,
    command=delete_section
)

btn_delete_section.pack(
    pady=5
)


# ====================================================
# SCHEDULE BUTTONS
# ====================================================

schedule_button_frame = tk.LabelFrame(
    button_frame,
    text="Schedule"
)

schedule_button_frame.grid(
    row=0,
    column=2,
    padx=10
)


btn_add_schedule = tk.Button(
    schedule_button_frame,
    text="Add",
    width=12
)

btn_add_schedule.pack(
    pady=5
)


btn_edit_schedule = tk.Button(
    schedule_button_frame,
    text="Edit",
    width=12
)

btn_edit_schedule.pack(
    pady=5
)


btn_delete_schedule = tk.Button(
    schedule_button_frame,
    text="Delete",
    width=12
)

btn_delete_schedule.pack(
    pady=5
)
# ====================================================
# Initial Load
# ====================================================

load_courses()

load_sections()

load_schedules()


root.mainloop()