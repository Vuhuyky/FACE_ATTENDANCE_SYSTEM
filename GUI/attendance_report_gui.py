import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from attendance.attendance_report import (
    get_all_sessions,
    get_attendance_report_data
)

from attendance.export_excel import (
    export_session_to_excel
)

# =====================================
# State
# =====================================

# Maps combobox display strings -> session_id
session_lookup = {}

current_report = None


# =====================================
# Load session list into the picker
# =====================================

def load_session_list():

    sessions = get_all_sessions()

    session_lookup.clear()

    display_values = []

    for session_id, course_name, section_name, session_date in sessions:

        label = (
            f"#{session_id} - {course_name} - "
            f"{section_name} - {session_date}"
        )

        session_lookup[label] = session_id

        display_values.append(label)

    combo_session["values"] = display_values

    if display_values:

        combo_session.current(0)

        load_report()

    else:

        combo_session.set("")

        clear_report_view()


# =====================================
# Clear the report view (no session)
# =====================================

def clear_report_view():

    global current_report

    current_report = None

    for row in tree.get_children():

        tree.delete(row)

    info_var.set(
        "No attendance sessions found."
    )

    summary_var.set("")


# =====================================
# Load & display the selected session
# =====================================

def load_report():

    global current_report

    label = combo_session.get()

    session_id = session_lookup.get(label)

    if session_id is None:

        clear_report_view()

        return

    report = get_attendance_report_data(session_id)

    current_report = report

    for row in tree.get_children():

        tree.delete(row)

    if report is None:

        info_var.set(
            "Session not found."
        )

        summary_var.set("")

        return

    info_var.set(
        f"Course: {report['course_name']}    "
        f"Section: {report['section_name']}    "
        f"Date: {report['session_date']}"
    )

    for _, code, name, first_seen in report["present_students"]:

        tree.insert(
            "",
            tk.END,
            values=(
                "Present",
                code,
                name,
                first_seen or ""
            ),
            tags=("present",)
        )

    for _, code, name in report["absent_students"]:

        tree.insert(
            "",
            tk.END,
            values=(
                "Absent",
                code,
                name,
                "-"
            ),
            tags=("absent",)
        )

    summary_var.set(
        f"Present: {report['present_count']}    "
        f"Absent: {report['absent_count']}    "
        f"Total: {report['total']}    "
        f"Attendance Rate: {report['attendance_rate']:.2f}%"
    )


# =====================================
# Export to Excel
# =====================================

def export_to_excel():

    if current_report is None:

        messagebox.showwarning(
            "Export",
            "No report loaded to export."
        )

        return

    default_name = (
        f"attendance_session_"
        f"{current_report['session_id']}.xlsx"
    )

    output_path = filedialog.asksaveasfilename(
        title="Save Attendance Report",
        defaultextension=".xlsx",
        initialfile=default_name,
        filetypes=[
            ("Excel Workbook", "*.xlsx")
        ]
    )

    if not output_path:

        return

    try:

        export_session_to_excel(
            session_id=current_report["session_id"],
            output_file=output_path
        )

        answer = messagebox.askyesno(
            "Export Complete",
            f"Report saved to:\n{output_path}\n\n"
            "Open the containing folder now?"
        )

        if answer:

            folder = os.path.dirname(
                os.path.abspath(output_path)
            )

            os.startfile(folder)

    except Exception as error:

        messagebox.showerror(
            "Export Failed",
            str(error)
        )


# =====================================
# Window
# =====================================

root = tk.Tk()

root.title(
    "Attendance Report"
)

root.geometry(
    "900x560"
)

tk.Label(
    root,
    text="ATTENDANCE REPORT",
    font=("Arial", 18, "bold")
).pack(
    pady=(15, 10)
)

# ====================================
# Session picker row
# ====================================

picker_frame = tk.Frame(root)

picker_frame.pack(
    fill="x",
    padx=15
)

tk.Label(
    picker_frame,
    text="Session:",
    font=("Arial", 10, "bold")
).pack(
    side="left"
)

combo_session = ttk.Combobox(
    picker_frame,
    width=60,
    state="readonly"
)

combo_session.pack(
    side="left",
    padx=10
)

combo_session.bind(
    "<<ComboboxSelected>>",
    lambda event: load_report()
)

tk.Button(
    picker_frame,
    text="Refresh",
    command=load_session_list
).pack(
    side="left",
    padx=5
)

tk.Button(
    picker_frame,
    text="Export to Excel",
    command=export_to_excel
).pack(
    side="right"
)

# ====================================
# Course / section / date info
# ====================================

info_var = tk.StringVar(
    value="Loading..."
)

tk.Label(
    root,
    textvariable=info_var,
    font=("Arial", 10)
).pack(
    pady=(12, 5),
    anchor="w",
    padx=15
)

# ====================================
# Table
# ====================================

columns = (
    "status",
    "code",
    "name",
    "time"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

tree.heading("status", text="Status")
tree.heading("code", text="Student Code")
tree.heading("name", text="Full Name")
tree.heading("time", text="Check-in Time")

tree.column("status", width=100, anchor="center")
tree.column("code", width=150, anchor="center")
tree.column("name", width=300, anchor="w")
tree.column("time", width=150, anchor="center")

tree.tag_configure(
    "present",
    background="#C6EFCE"
)

tree.tag_configure(
    "absent",
    background="#FFC7CE"
)

tree.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

# ====================================
# Summary
# ====================================

summary_var = tk.StringVar(
    value=""
)

tk.Label(
    root,
    textvariable=summary_var,
    font=("Arial", 11, "bold")
).pack(
    pady=(0, 15)
)

# ====================================
# Bottom buttons
# ====================================

bottom_frame = tk.Frame(root)

bottom_frame.pack(
    pady=(0, 15)
)

tk.Button(
    bottom_frame,
    text="Close",
    width=15,
    command=root.destroy
).pack()

load_session_list()

root.mainloop()