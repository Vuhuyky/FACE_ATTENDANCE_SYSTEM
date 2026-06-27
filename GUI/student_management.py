import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys

from database.connection import get_connection
# =====================================
# Load Student List
# =====================================

def load_students():

    for row in tree.get_children():

        tree.delete(row)

    
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            s.student_code,
            s.full_name,
            IFNULL(s.email, ''),
            cs.section_name
        FROM students s

        LEFT JOIN enrollments e
        ON s.id = e.student_id

        LEFT JOIN course_sections cs
        ON e.section_id = cs.id

        ORDER BY s.student_code
        """
    )

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )


# =====================================
# Open Add Student
# =====================================

def open_add_student():

    subprocess.Popen(
        [
            sys.executable,
            "GUI/add_student.py"
        ]
    )


# =====================================
# Delete Student
# =====================================

def delete_student():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a student."
        )

        return

    values = tree.item(
        selected[0]
    )["values"]

    student_code = values[0]

    answer = messagebox.askyesno(
        "Confirm",
        f"Delete student {student_code} ?"
    )

    if not answer:

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM students
        WHERE student_code=?
        """,
        (
            student_code,
        )
    )

    student = cursor.fetchone()

    if student:

        student_id = student[0]

        cursor.execute(
            """
            DELETE FROM enrollments
            WHERE student_id=?
            """,
            (
                student_id,
            )
        )

        cursor.execute(
            """
            DELETE FROM students
            WHERE id=?
            """,
            (
                student_id,
            )
        )

    conn.commit()

    conn.close()

    load_students()


# =====================================
# Register Face
# =====================================

def register_face():

    messagebox.showinfo(
        "Coming Soon",
        "Next step."
    )


# =====================================
# GUI
# =====================================

root = tk.Tk()

root.title(
    "Student Management"
)

root.geometry(
    "850x500"
)

columns = (
    "Student Code",
    "Full Name",
    "Email",
    "Section"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for col in columns:

    tree.heading(
        col,
        text=col
    )

    tree.column(
        col,
        width=180
    )

tree.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)

button_frame = tk.Frame(
    root
)

button_frame.pack(
    pady=10
)

tk.Button(
    button_frame,
    text="Refresh",
    width=15,
    command=load_students
).grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=open_add_student
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    command=delete_student
).grid(
    row=0,
    column=2,
    padx=5
)

tk.Button(
    button_frame,
    text="Register Face",
    width=15,
    command=register_face
).grid(
    row=0,
    column=3,
    padx=5
)

tk.Button(
    button_frame,
    text="Close",
    width=15,
    command=root.destroy
).grid(
    row=0,
    column=4,
    padx=5
)

load_students()

root.mainloop()