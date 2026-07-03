import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys

from database.connection import get_connection

def load_sessions():

    for row in session_tree.get_children():

        session_tree.delete(row)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            attendance_sessions.id,

            course_sections.section_name,

            attendance_sessions.session_date,

            attendance_sessions.start_time,

            attendance_sessions.end_time,

            attendance_sessions.is_active

        FROM attendance_sessions

        JOIN course_sections

        ON attendance_sessions.section_id = course_sections.id

        ORDER BY

            attendance_sessions.session_date DESC,

            attendance_sessions.start_time
        """
    )

    rows = cursor.fetchall()

    conn.close()

    for row in rows:

        status = "Open" if row[5] == 1 else "Closed"

        session_tree.insert(
            "",
            tk.END,
            values=(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                status
            )
        )

def create_session():

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "GUI.create_session"
        ]
    )
def open_session():

    selected = session_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a session."
        )

        return

    session_id = session_tree.item(
        selected[0],
        "values"
    )[0]

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE attendance_sessions

        SET is_active = 0
        """
    )

    cursor.execute(
        """
        UPDATE attendance_sessions

        SET is_active = 1

        WHERE id = ?
        """,
        (
            session_id,
        )
    )

    conn.commit()

    conn.close()

    load_sessions()

def close_session():

    selected = session_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a session."
        )

        return

    session_id = session_tree.item(
        selected[0],
        "values"
    )[0]

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE attendance_sessions

        SET is_active = 0

        WHERE id = ?
        """,
        (
            session_id,
        )
    )

    conn.commit()

    conn.close()

    load_sessions()

def delete_session():

    selected = session_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a session."
        )

        return

    session_id = session_tree.item(
        selected[0],
        "values"
    )[0]

    confirm = messagebox.askyesno(
        "Confirm",
        "Delete this session?"
    )

    if not confirm:

        return

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM attendance_sessions

            WHERE id = ?
            """,
            (
                session_id,
            )
        )

        conn.commit()

        load_sessions()

        messagebox.showinfo(
            "Success",
            "Session deleted successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        conn.close()
        

root = tk.Tk()

root.title(
    "Session Manager"
)

root.geometry(
    "900x550"
)

root.resizable(
    False,
    False
)

session_tree = ttk.Treeview(

    root,

    columns=(

        "ID",
        "Section",
        "Date",
        "Start",
        "End",
        "Status"

    ),

    show="headings",

    height=18

)

session_tree.heading(
    "ID",
    text="ID"
)

session_tree.heading(
    "Section",
    text="Section"
)

session_tree.heading(
    "Date",
    text="Date"
)

session_tree.heading(
    "Start",
    text="Start Time"
)

session_tree.heading(
    "End",
    text="End Time"
)

session_tree.heading(
    "Status",
    text="Status"
)

session_tree.column(
    "ID",
    width=50,
    anchor="center"
)

session_tree.column(
    "Section",
    width=180,
    anchor="center"
)

session_tree.column(
    "Date",
    width=120,
    anchor="center"
)

session_tree.column(
    "Start",
    width=120,
    anchor="center"
)

session_tree.column(
    "End",
    width=120,
    anchor="center"
)

session_tree.column(
    "Status",
    width=100,
    anchor="center"
)

session_tree.pack(
    padx=15,
    pady=15,
    fill="both",
    expand=True
)

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)

btn_create = tk.Button(

    button_frame,

    text="Create",

    width=12,

    command=create_session

)

btn_create.grid(
    row=0,
    column=0,
    padx=5
)
btn_open = tk.Button(

    button_frame,

    text="Open",

    width=12,

    command=open_session

)

btn_open.grid(
    row=0,
    column=1,
    padx=5
)
btn_close = tk.Button(

    button_frame,

    text="Close",

    width=12,

    command=close_session

)

btn_close.grid(
    row=0,
    column=2,
    padx=5
)
btn_delete = tk.Button(

    button_frame,

    text="Delete",

    width=12,

    command=delete_session

)

btn_delete.grid(
    row=0,
    column=3,
    padx=5
)
load_sessions()

root.mainloop()
