import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys

from database.connection import get_connection

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

        ORDER BY

            cs.section_name,
            s.weekday,
            s.start_time
        """
    )

    rows = cursor.fetchall()
    weekday_map = {

        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"

    }

    conn.close()

    for row in rows:

        schedule_tree.insert(
            "",
            tk.END,
            values=(
                row[0],
                row[1],
                weekday_map.get(
                    row[2],
                    row[2]
                ),
                row[3],
                row[4]
            )
        )

root = tk.Tk()

root.title(
    "Schedule Manager"
)

root.geometry(
    "760x500"
)

schedule_tree = ttk.Treeview(

    root,

    columns=(

        "ID",
        "Section",
        "Day",
        "Start",
        "End"

    ),

    show="headings",

    height=15

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
    "Day",
    text="Day"
)

schedule_tree.heading(
    "Start",
    text="Start Time"
)

schedule_tree.heading(
    "End",
    text="End Time"
)

schedule_tree.column(
    "ID",
    width=50,
    anchor="center"
)

schedule_tree.column(
    "Section",
    width=170
)

schedule_tree.column(
    "Day",
    width=120
)

schedule_tree.column(
    "Start",
    width=120,
    anchor="center"
)

schedule_tree.column(
    "End",
    width=120,
    anchor="center"
)

schedule_tree.pack(
    padx=15,
    pady=20,
    fill="both",
    expand=True
)

load_schedules()

root.mainloop()