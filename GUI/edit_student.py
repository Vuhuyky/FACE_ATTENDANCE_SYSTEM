import tkinter as tk
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
        "Student Code not found."
    )

    exit()

student_code = sys.argv[1]


# =====================================================
# Load Student
# =====================================================

def load_student():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            student_code,
            full_name,
            email

        FROM students

        WHERE student_code = ?
        """,
        (
            student_code,
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row


# =====================================================
# Update Student
# =====================================================

def update_student(
    old_student_code,
    new_student_code,
    full_name,
    email
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students

        SET

            student_code = ?,
            full_name = ?,
            email = ?

        WHERE student_code = ?
        """,
        (
            new_student_code,
            full_name,
            email,
            old_student_code
        )
    )

    conn.commit()

    conn.close()


# =====================================================
# Save
# =====================================================

def save_student():

    new_student_code = entry_code.get().strip()

    full_name = entry_name.get().strip()

    email = entry_email.get().strip()

    if (

        not new_student_code

        or

        not full_name

    ):

        messagebox.showerror(
            "Error",
            "Student Code and Name are required."
        )

        return

    try:

        update_student(

            student_code,

            new_student_code,

            full_name,

            email

        )

        messagebox.showinfo(
            "Success",
            "Student updated successfully."
        )

        root.destroy()

    except sqlite3.IntegrityError:

        messagebox.showwarning(
            "Duplicate",
            "Student Code already exists."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =====================================================
# Load Data
# =====================================================

student = load_student()

if student is None:

    messagebox.showerror(
        "Error",
        "Student not found."
    )

    exit()


# =====================================================
# Window
# =====================================================

root = tk.Tk()

root.title("Edit Student")

root.geometry("420x260")

root.resizable(False, False)


# =====================================================
# Student Code
# =====================================================

tk.Label(
    root,
    text="Student Code"
).pack(
    pady=(20,5)
)

entry_code = tk.Entry(
    root,
    width=40
)

entry_code.pack()

entry_code.insert(
    0,
    student[0]
)


# =====================================================
# Full Name
# =====================================================

tk.Label(
    root,
    text="Full Name"
).pack(
    pady=(15,5)
)

entry_name = tk.Entry(
    root,
    width=40
)

entry_name.pack()

entry_name.insert(
    0,
    student[1]
)


# =====================================================
# Email
# =====================================================

tk.Label(
    root,
    text="Email"
).pack(
    pady=(15,5)
)

entry_email = tk.Entry(
    root,
    width=40
)

entry_email.pack()

entry_email.insert(
    0,
    "" if student[2] is None else student[2]
)


# =====================================================
# Button
# =====================================================

tk.Button(
    root,
    text="Update Student",
    width=18,
    command=save_student
).pack(
    pady=25
)

root.mainloop()