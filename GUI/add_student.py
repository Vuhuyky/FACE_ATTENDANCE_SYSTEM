import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def load_sections():

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            section_name
        FROM course_sections
        ORDER BY id
        """
    )

    sections = cursor.fetchall()

    conn.close()

    return sections


def add_student():

    student_code = entry_code.get().strip()

    full_name = entry_name.get().strip()

    email = entry_email.get().strip()

    section_text = combo_section.get()

    if (
        not student_code
        or not full_name
        or not email
        or not section_text
    ):

        messagebox.showerror(
            "Error",
            "Please fill all fields"
        )

        return

    section_id = int(
        section_text.split(" - ")[0]
    )

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO students
            (
                student_code,
                full_name,
                email
            )
            VALUES
            (
                ?, ?, ?
            )
            """,
            (
                student_code,
                full_name,
                email
            )
        )

        student_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO enrollments
            (
                student_id,
                section_id
            )
            VALUES
            (
                ?, ?
            )
            """,
            (
                student_id,
                section_id
            )
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully"
        )

        entry_code.delete(
            0,
            tk.END
        )

        entry_name.delete(
            0,
            tk.END
        )

        entry_email.delete(
            0,
            tk.END
        )

        combo_section.set("")

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()


root = tk.Tk()

root.title(
    "Add Student"
)

root.geometry(
    "400x380"
)

# ==========================
# Student Code
# ==========================

tk.Label(
    root,
    text="Student Code"
).pack(
    pady=5
)

entry_code = tk.Entry(
    root,
    width=30
)

entry_code.pack()

# ==========================
# Full Name
# ==========================

tk.Label(
    root,
    text="Full Name"
).pack(
    pady=5
)

entry_name = tk.Entry(
    root,
    width=30
)

entry_name.pack()

# ==========================
# Email
# ==========================

tk.Label(
    root,
    text="Email"
).pack(
    pady=5
)

entry_email = tk.Entry(
    root,
    width=30
)

entry_email.pack()

# ==========================
# Section
# ==========================

tk.Label(
    root,
    text="Section"
).pack(
    pady=5
)

combo_section = ttk.Combobox(
    root,
    width=27,
    state="readonly"
)

sections = load_sections()

combo_section["values"] = [

    f"{row[0]} - {row[1]}"

    for row in sections
]

combo_section.pack()

# ==========================
# Button
# ==========================

tk.Button(
    root,
    text="Add Student",
    width=20,
    command=add_student
).pack(
    pady=20
)

root.mainloop()