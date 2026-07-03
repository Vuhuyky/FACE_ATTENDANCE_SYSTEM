import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import sys

from database.connection import get_connection


# =====================================================
# Check Argument
# =====================================================

if len(sys.argv) < 2:

    messagebox.showerror(
        "Error",
        "Enrollment ID not found."
    )

    exit()

enrollment_id = int(
    sys.argv[1]
)


# =====================================================
# Load Students
# =====================================================

def load_students():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            id,
            student_code,
            full_name

        FROM students

        ORDER BY student_code
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================================
# Load Sections
# =====================================================

def load_sections():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            cs.id,

            c.course_code,

            cs.section_name

        FROM course_sections cs

        JOIN courses c

        ON cs.course_id = c.id

        ORDER BY

            c.course_code,
            cs.section_name
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================================
# Load Current Enrollment
# =====================================================

def load_enrollment():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            student_id,
            section_id

        FROM enrollments

        WHERE id = ?
        """,
        (
            enrollment_id,
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row


# =====================================================
# Update
# =====================================================

def update_enrollment(
    student_id,
    section_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE enrollments

        SET

            student_id = ?,
            section_id = ?

        WHERE id = ?
        """,
        (
            student_id,
            section_id,
            enrollment_id
        )
    )

    conn.commit()

    conn.close()


# =====================================================
# Save
# =====================================================

def save_enrollment():

    if (

        not combo_student.get()

        or

        not combo_section.get()

    ):

        messagebox.showerror(
            "Error",
            "Please select student and section."
        )

        return

    student_id = int(
        combo_student.get().split(" - ")[0]
    )

    section_id = int(
        combo_section.get().split(" - ")[0]
    )

    try:

        update_enrollment(
            student_id,
            section_id
        )

        messagebox.showinfo(
            "Success",
            "Enrollment updated successfully."
        )

        root.destroy()

    except sqlite3.IntegrityError:

        messagebox.showwarning(
            "Duplicate",
            "This student is already enrolled in this section."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =====================================================
# Load Data
# =====================================================

students = load_students()

sections = load_sections()

current = load_enrollment()

student_id = current[0]

section_id = current[1]


# =====================================================
# Window
# =====================================================

root = tk.Tk()

root.title("Edit Enrollment")

root.geometry("450x260")

root.resizable(False, False)


# =====================================================
# Student
# =====================================================

tk.Label(
    root,
    text="Student"
).pack(
    pady=(20,5)
)

combo_student = ttk.Combobox(
    root,
    width=40,
    state="readonly"
)

combo_student["values"] = [

    f"{row[0]} - {row[1]} ({row[2]})"

    for row in students

]

combo_student.pack()

for i, row in enumerate(students):

    if row[0] == student_id:

        combo_student.current(i)

        break


# =====================================================
# Section
# =====================================================

tk.Label(
    root,
    text="Section"
).pack(
    pady=(20,5)
)

combo_section = ttk.Combobox(
    root,
    width=40,
    state="readonly"
)

combo_section["values"] = [

    f"{row[0]} - {row[1]} ({row[2]})"

    for row in sections

]

combo_section.pack()

for i, row in enumerate(sections):

    if row[0] == section_id:

        combo_section.current(i)

        break


# =====================================================
# Button
# =====================================================

tk.Button(
    root,
    text="Update",
    width=18,
    command=save_enrollment
).pack(
    pady=30
)

root.mainloop()