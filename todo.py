import tkinter as tk
from tkinter import messagebox
import json
import os


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = "tasks.json"

BG_COLOR = "#F4F6FA"
WHITE = "#FFFFFF"

PRIMARY = "#4F46E5"
PRIMARY_DARK = "#3730A3"

GREEN = "#10B981"
GREEN_DARK = "#059669"

BLUE = "#3B82F6"
BLUE_DARK = "#2563EB"

PURPLE = "#8B5CF6"
PURPLE_DARK = "#7C3AED"

RED = "#EF4444"
RED_DARK = "#DC2626"

ORANGE = "#F59E0B"
ORANGE_DARK = "#D97706"

TEXT = "#111827"
GRAY = "#6B7280"
LIGHT_GRAY = "#F9FAFB"
BORDER = "#E5E7EB"


# ============================================================
# SAVE TASKS
# ============================================================

def save_tasks():

    tasks = []

    for i in range(task_listbox.size()):

        task = task_listbox.get(i)

        if task.startswith("✓ "):

            tasks.append({
                "text": task[2:],
                "completed": True
            })

        else:

            tasks.append({
                "text": task,
                "completed": False
            })

    try:

        with open(DATA_FILE, "w", encoding="utf-8") as file:

            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            f"Could not save tasks.\n\n{error}"
        )


# ============================================================
# LOAD TASKS
# ============================================================

def load_tasks():

    if not os.path.exists(DATA_FILE):
        return

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            tasks = json.load(file)

        for task in tasks:

            text = task.get("text", "")
            completed = task.get("completed", False)

            if not text:
                continue

            if completed:

                task_listbox.insert(
                    tk.END,
                    "✓ " + text
                )

            else:

                task_listbox.insert(
                    tk.END,
                    text
                )

    except Exception:

        pass


# ============================================================
# UPDATE STATISTICS
# ============================================================

def update_statistics():

    total = task_listbox.size()

    completed = 0

    for i in range(total):

        task = task_listbox.get(i)

        if task.startswith("✓ "):

            completed += 1

    pending = total - completed

    total_label.config(
        text=f"Total: {total}"
    )

    pending_label.config(
        text=f"Pending: {pending}"
    )

    completed_label.config(
        text=f"Completed: {completed}"
    )


# ============================================================
# CREATE TASK
# ============================================================

def create_task():

    task = task_entry.get().strip()

    if task == "":

        messagebox.showwarning(
            "Create Task",
            "Please enter a task."
        )

        task_entry.focus()

        return

    task_listbox.insert(
        tk.END,
        task
    )

    task_entry.delete(
        0,
        tk.END
    )

    save_tasks()

    update_statistics()

    task_entry.focus()


# ============================================================
# SELECT TASK
# ============================================================

def select_task(event=None):

    selected = task_listbox.curselection()

    if not selected:
        return

    index = selected[0]

    task = task_listbox.get(index)

    # Remove completed symbol
    if task.startswith("✓ "):

        task = task[2:]

    task_entry.delete(
        0,
        tk.END
    )

    task_entry.insert(
        0,
        task
    )

    task_entry.focus()

    task_entry.icursor(tk.END)


# ============================================================
# UPDATE TASK
# ============================================================

def update_task():

    selected = task_listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Update Task",
            "Please select a task from the list first."
        )

        return

    new_task = task_entry.get().strip()

    if new_task == "":

        messagebox.showwarning(
            "Update Task",
            "Please enter the updated task."
        )

        task_entry.focus()

        return

    index = selected[0]

    old_task = task_listbox.get(index)

    completed = old_task.startswith("✓ ")

    if completed:

        new_task = "✓ " + new_task

    task_listbox.delete(index)

    task_listbox.insert(
        index,
        new_task
    )

    task_listbox.selection_set(index)

    task_listbox.activate(index)

    task_entry.delete(
        0,
        tk.END
    )

    save_tasks()

    update_statistics()

    task_entry.focus()


# ============================================================
# COMPLETE TASK
# ============================================================

def complete_task():

    selected = task_listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Complete Task",
            "Please select a task first."
        )

        return

    index = selected[0]

    task = task_listbox.get(index)

    if task.startswith("✓ "):

        messagebox.showinfo(
            "Already Completed",
            "This task is already completed."
        )

        return

    task_listbox.delete(index)

    task_listbox.insert(
        index,
        "✓ " + task
    )

    task_listbox.selection_set(index)

    save_tasks()

    update_statistics()


# ============================================================
# DELETE TASK
# ============================================================

def delete_task():

    selected = task_listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Delete Task",
            "Please select a task first."
        )

        return

    index = selected[0]

    task = task_listbox.get(index)

    confirm = messagebox.askyesno(
        "Delete Task",
        f"Are you sure you want to delete:\n\n{task}"
    )

    if not confirm:
        return

    task_listbox.delete(index)

    task_entry.delete(
        0,
        tk.END
    )

    save_tasks()

    update_statistics()

    task_entry.focus()


# ============================================================
# CLEAR ALL TASKS
# ============================================================

def clear_all_tasks():

    if task_listbox.size() == 0:

        messagebox.showinfo(
            "Clear All",
            "There are no tasks to clear."
        )

        return

    confirm = messagebox.askyesno(
        "Clear All Tasks",
        "Are you sure you want to delete all tasks?"
    )

    if not confirm:
        return

    task_listbox.delete(
        0,
        tk.END
    )

    task_entry.delete(
        0,
        tk.END
    )

    save_tasks()

    update_statistics()

    task_entry.focus()


# ============================================================
# ENTER KEY
# ============================================================

def enter_key(event):

    create_task()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "My To-Do List"
)

root.geometry(
    "1200x800"
)

root.minsize(
    950,
    650
)

root.configure(
    bg=BG_COLOR
)

# Maximize window
try:

    root.state("zoomed")

except:

    pass


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=PRIMARY,
    height=115
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title = tk.Label(
    header,
    text="✓  My To-Do List",
    font=("Segoe UI", 30, "bold"),
    bg=PRIMARY,
    fg=WHITE
)

title.pack(
    pady=(20, 2)
)


subtitle = tk.Label(
    header,
    text="Create • Update • Complete • Track your tasks",
    font=("Segoe UI", 12),
    bg=PRIMARY,
    fg="#E0E7FF"
)

subtitle.pack()


# ============================================================
# MAIN CONTAINER
# ============================================================

main = tk.Frame(
    root,
    bg=BG_COLOR
)

main.pack(
    fill="both",
    expand=True,
    padx=55,
    pady=22
)


# ============================================================
# INPUT CARD
# ============================================================

input_card = tk.Frame(
    main,
    bg=WHITE
)

input_card.pack(
    fill="x",
    pady=(0, 15)
)


input_title = tk.Label(
    input_card,
    text="Task",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=TEXT
)

input_title.pack(
    anchor="w",
    padx=25,
    pady=(16, 2)
)


input_hint = tk.Label(
    input_card,
    text="Enter a new task or select an existing task to update it.",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=GRAY
)

input_hint.pack(
    anchor="w",
    padx=25
)


input_frame = tk.Frame(
    input_card,
    bg=WHITE
)

input_frame.pack(
    fill="x",
    padx=25,
    pady=15
)


task_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 14),
    bg=LIGHT_GRAY,
    fg=TEXT,
    relief="solid",
    bd=1
)

task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)

task_entry.bind(
    "<Return>",
    enter_key
)


# CREATE BUTTON

create_button = tk.Button(
    input_frame,
    text="+  Create Task",
    font=("Segoe UI", 10, "bold"),
    bg=GREEN,
    fg=WHITE,
    activebackground=GREEN_DARK,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=10,
    command=create_task
)

create_button.pack(
    side="left",
    padx=4
)


# UPDATE BUTTON

update_button = tk.Button(
    input_frame,
    text="✎  Update Task",
    font=("Segoe UI", 10, "bold"),
    bg=PURPLE,
    fg=WHITE,
    activebackground=PURPLE_DARK,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=10,
    command=update_task
)

update_button.pack(
    side="left",
    padx=4
)


# ============================================================
# TASK CARD
# ============================================================

task_card = tk.Frame(
    main,
    bg=WHITE
)

task_card.pack(
    fill="both",
    expand=True
)


# ============================================================
# TASK HEADER
# ============================================================

task_header = tk.Frame(
    task_card,
    bg=WHITE
)

task_header.pack(
    fill="x",
    padx=25,
    pady=(15, 8)
)


task_title = tk.Label(
    task_header,
    text="Your Tasks",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=TEXT
)

task_title.pack(
    side="left"
)


instruction = tk.Label(
    task_header,
    text="Select a task to manage it",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=GRAY
)

instruction.pack(
    side="right"
)


# ============================================================
# TASK LIST
# ============================================================

list_frame = tk.Frame(
    task_card,
    bg=WHITE
)

list_frame.pack(
    fill="both",
    expand=True,
    padx=25
)


scrollbar = tk.Scrollbar(
    list_frame
)

scrollbar.pack(
    side="right",
    fill="y"
)


task_listbox = tk.Listbox(
    list_frame,
    font=("Segoe UI", 13),
    bg=LIGHT_GRAY,
    fg=TEXT,
    selectbackground=PRIMARY,
    selectforeground=WHITE,
    activestyle="none",
    relief="solid",
    bd=1,
    highlightthickness=0,
    height=7,
    yscrollcommand=scrollbar.set
)

task_listbox.pack(
    fill="both",
    expand=True
)


scrollbar.config(
    command=task_listbox.yview
)


task_listbox.bind(
    "<<ListboxSelect>>",
    select_task
)


# ============================================================
# ACTION BUTTON BAR
# ============================================================

action_bar = tk.Frame(
    task_card,
    bg=WHITE
)

action_bar.pack(
    fill="x",
    padx=25,
    pady=(12, 15)
)


# COMPLETE BUTTON

complete_button = tk.Button(
    action_bar,
    text="✓  Complete Task",
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE_DARK,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=9,
    command=complete_task
)

complete_button.pack(
    side="left",
    padx=(0, 8)
)


# DELETE BUTTON

delete_button = tk.Button(
    action_bar,
    text="✕  Delete Task",
    font=("Segoe UI", 10, "bold"),
    bg=RED,
    fg=WHITE,
    activebackground=RED_DARK,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=9,
    command=delete_task
)

delete_button.pack(
    side="left",
    padx=8
)


# CLEAR BUTTON

clear_button = tk.Button(
    action_bar,
    text="🗑  Clear All",
    font=("Segoe UI", 10, "bold"),
    bg=ORANGE,
    fg=WHITE,
    activebackground=ORANGE_DARK,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=9,
    command=clear_all_tasks
)

clear_button.pack(
    side="left",
    padx=8
)


# ============================================================
# STATISTICS
# ============================================================

stats_frame = tk.Frame(
    action_bar,
    bg=WHITE
)

stats_frame.pack(
    side="right"
)


total_label = tk.Label(
    stats_frame,
    text="Total: 0",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=PRIMARY
)

total_label.pack(
    side="left",
    padx=10
)


pending_label = tk.Label(
    stats_frame,
    text="Pending: 0",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=ORANGE_DARK
)

pending_label.pack(
    side="left",
    padx=10
)


completed_label = tk.Label(
    stats_frame,
    text="Completed: 0",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=GREEN_DARK
)

completed_label.pack(
    side="left",
    padx=10
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text="Python • Tkinter • To-Do List Application",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=GRAY
)

footer.pack(
    pady=(0, 8)
)


# ============================================================
# START APPLICATION
# ============================================================

load_tasks()

update_statistics()

task_entry.focus()


# ============================================================
# RUN
# ============================================================

root.mainloop()