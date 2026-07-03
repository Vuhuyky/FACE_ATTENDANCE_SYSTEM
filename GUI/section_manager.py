import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys

from database.connection import get_connection


# ====================================================
# Load Sections
# ====================================================

def load_sections():

    for row in tree.get_children():
        tree.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            cs.id,

            c.course_code,

            c.course_name,

            cs.section_name,

            cs.room

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

    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )


# ====================================================
# Add
# ====================================================

def add_section():

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.add_section"
        ]
    )


# ====================================================
# Edit
# ====================================================

def edit_section():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a section."
        )

        return

    values = tree.item(
        selected[0]
    )["values"]

    section_id = str(values[0])

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.edit_section",
            section_id
        ]
    )


# ====================================================
# Delete
# ====================================================

def delete_section():

    selected = tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a section."
        )

        return

    values = tree.item(
        selected[0]
    )["values"]

    section_id = values[0]

    answer = messagebox.askyesno(
        "Confirm",
        "Delete this section?"
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
            "Section deleted."
        )

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
    "Section Manager"
)

root.geometry(
    "850x500"
)

root.resizable(
    False,
    False
)


# ====================================================
# Buttons
# ====================================================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)

tk.Button(
    button_frame,
    text="Add",
    width=12,
    command=add_section
).pack(
    side=tk.LEFT,
    padx=5
)

tk.Button(
    button_frame,
    text="Edit",
    width=12,
    command=edit_section
).pack(
    side=tk.LEFT,
    padx=5
)

tk.Button(
    button_frame,
    text="Delete",
    width=12,
    command=delete_section
).pack(
    side=tk.LEFT,
    padx=5
)

tk.Button(
    button_frame,
    text="Refresh",
    width=12,
    command=load_sections
).pack(
    side=tk.LEFT,
    padx=5
)


# ====================================================
# Treeview
# ====================================================

tree = ttk.Treeview(

    root,

    columns=(

        "ID",
        "Course Code",
        "Course Name",
        "Section",
        "Room"

    ),

    show="headings",

    height=18

)

tree.heading(
    "ID",
    text="ID"
)

tree.heading(
    "Course Code",
    text="Course Code"
)

tree.heading(
    "Course Name",
    text="Course Name"
)

tree.heading(
    "Section",
    text="Section"
)

tree.heading(
    "Room",
    text="Room"
)

tree.column(
    "ID",
    width=60,
    anchor="center"
)

tree.column(
    "Course Code",
    width=120,
    anchor="center"
)

tree.column(
    "Course Name",
    width=240
)

tree.column(
    "Section",
    width=180,
    anchor="center"
)

tree.column(
    "Room",
    width=120,
    anchor="center"
)

tree.pack(
    padx=15,
    pady=15,
    fill="both",
    expand=True
)

load_sections()

root.mainloop()