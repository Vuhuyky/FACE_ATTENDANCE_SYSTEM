import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database.connection import get_connection


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
# Insert
# =====================================================

def insert_enrollment(
    student_id,
    section_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO enrollments(

            student_id,
            section_id

        )

        VALUES(

            ?,
            ?

        )
        """,
        (
            student_id,
            section_id
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

        insert_enrollment(

            student_id,

            section_id

        )

        messagebox.showinfo(

            "Success",

            "Enrollment created."

        )

        root.destroy()

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


# =====================================================
# Window
# =====================================================

root = tk.Tk()

root.title("Add Enrollment")

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


# =====================================================
# Button
# =====================================================

tk.Button(

    root,

    text="Save",

    width=18,

    command=save_enrollment

).pack(

    pady=30

)

root.mainloop()