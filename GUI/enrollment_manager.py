import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys

from database.connection import get_connection


# =====================================================
# Load Enrollment
# =====================================================

def load_enrollments():

    for row in enrollment_tree.get_children():

        enrollment_tree.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            e.id,

            s.student_code,

            s.full_name,

            c.course_code,

            cs.section_name

        FROM enrollments e

        JOIN students s

        ON e.student_id = s.id

        JOIN course_sections cs

        ON e.section_id = cs.id

        JOIN courses c

        ON cs.course_id = c.id

        ORDER BY

            s.student_code
        """
    )

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        enrollment_tree.insert(
            "",
            tk.END,
            values=row
        )


# =====================================================
# Add
# =====================================================

def open_add_enrollment():

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.add_enrollment"
        ]
    )


# =====================================================
# Edit
# =====================================================

def edit_enrollment():

    selected = enrollment_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select an enrollment."
        )

        return

    enrollment_id = enrollment_tree.item(
        selected[0],
        "values"
    )[0]

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.edit_enrollment",
            str(enrollment_id)
        ]
    )


# =====================================================
# Delete
# =====================================================

def delete_enrollment():

    selected = enrollment_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select an enrollment."
        )

        return

    enrollment_id = enrollment_tree.item(
        selected[0],
        "values"
    )[0]

    answer = messagebox.askyesno(
        "Delete",
        "Delete this enrollment?"
    )

    if not answer:

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM enrollments

        WHERE id = ?
        """,
        (
            enrollment_id,
        )
    )

    conn.commit()

    conn.close()

    load_enrollments()


# =====================================================
# Window
# =====================================================

root = tk.Tk()

root.title(
    "Enrollment Manager"
)

root.geometry(
    "900x550"
)

root.resizable(
    False,
    False
)


# =====================================================
# Buttons
# =====================================================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)

tk.Button(
    button_frame,
    text="Add",
    width=12,
    command=open_add_enrollment
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    button_frame,
    text="Edit",
    width=12,
    command=edit_enrollment
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    button_frame,
    text="Delete",
    width=12,
    command=delete_enrollment
).grid(
    row=0,
    column=2,
    padx=5
)

tk.Button(
    button_frame,
    text="Refresh",
    width=12,
    command=load_enrollments
).grid(
    row=0,
    column=3,
    padx=5
)


# =====================================================
# Table
# =====================================================

enrollment_tree = ttk.Treeview(

    root,

    columns=(

        "ID",
        "Student Code",
        "Full Name",
        "Course",
        "Section"

    ),

    show="headings",

    height=18

)

for col in (

    "ID",
    "Student Code",
    "Full Name",
    "Course",
    "Section"

):

    enrollment_tree.heading(
        col,
        text=col
    )

enrollment_tree.column(
    "ID",
    width=60,
    anchor="center"
)

enrollment_tree.column(
    "Student Code",
    width=120,
    anchor="center"
)

enrollment_tree.column(
    "Full Name",
    width=250
)

enrollment_tree.column(
    "Course",
    width=120,
    anchor="center"
)

enrollment_tree.column(
    "Section",
    width=150,
    anchor="center"
)

enrollment_tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

load_enrollments()

root.mainloop()