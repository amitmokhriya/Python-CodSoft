import tkinter as tk


# ==============================
# Calculator Functions
# ==============================

def button_click(value):
    current = display_var.get()

    # Don't add anything after an error message
    if current in ["Invalid", "Cannot divide by zero"]:
        current = ""

    display_var.set(current + str(value))


def clear_display():
    display_var.set("")


def delete_last():
    current = display_var.get()

    if current in ["Invalid", "Cannot divide by zero"]:
        display_var.set("")
    else:
        display_var.set(current[:-1])


def calculate():
    expression = display_var.get()

    try:
        if not expression:
            return

        result = eval(expression)

        # Remove unnecessary .0 from integer results
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        display_var.set(str(result))

    except ZeroDivisionError:
        display_var.set("Cannot divide by zero")

    except Exception:
        display_var.set("Invalid")


# ==============================
# Main Window
# ==============================

root = tk.Tk()

root.title("Simple Calculator")

# Starting window size
root.geometry("400x600")

# Minimum size
root.minsize(350, 500)

# Allow maximize / minimize / resize
root.resizable(True, True)

# Background
root.configure(bg="#1e1e1e")


# ==============================
# Display
# ==============================

display_var = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Segoe UI", 28),
    justify="right",
    bd=0,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)

display.pack(
    padx=25,
    pady=30,
    fill="x",
    ipady=18
)


# ==============================
# Button Frame
# ==============================

button_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

button_frame.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


# Make rows and columns resize
for row in range(4):
    button_frame.rowconfigure(row, weight=1)

for column in range(4):
    button_frame.columnconfigure(column, weight=1)


# ==============================
# Calculator Buttons
# ==============================

buttons = [
    ("7", 0, 0),
    ("8", 0, 1),
    ("9", 0, 2),
    ("/", 0, 3),

    ("4", 1, 0),
    ("5", 1, 1),
    ("6", 1, 2),
    ("*", 1, 3),

    ("1", 2, 0),
    ("2", 2, 1),
    ("3", 2, 2),
    ("-", 2, 3),

    ("0", 3, 0),
    (".", 3, 1),
    ("+", 3, 2),
    ("=", 3, 3)
]


for text, row, column in buttons:

    if text == "=":
        command = calculate
        bg_color = "#27ae60"

    elif text in ["+", "-", "*", "/"]:
        command = lambda value=text: button_click(value)
        bg_color = "#f39c12"

    else:
        command = lambda value=text: button_click(value)
        bg_color = "#3a3a3a"

    button = tk.Button(
        button_frame,
        text=text,
        command=command,
        font=("Segoe UI", 18, "bold"),
        bg=bg_color,
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        bd=0
    )

    button.grid(
        row=row,
        column=column,
        padx=5,
        pady=5,
        sticky="nsew"
    )


# ==============================
# Bottom Buttons
# ==============================

bottom_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

bottom_frame.pack(
    padx=25,
    pady=20,
    fill="x"
)


clear_button = tk.Button(
    bottom_frame,
    text="CLEAR",
    command=clear_display,
    font=("Segoe UI", 13, "bold"),
    bg="#c0392b",
    fg="white",
    activebackground="#e74c3c",
    bd=0,
    height=2
)

clear_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)


delete_button = tk.Button(
    bottom_frame,
    text="DELETE",
    command=delete_last,
    font=("Segoe UI", 13, "bold"),
    bg="#555555",
    fg="white",
    activebackground="#666666",
    bd=0,
    height=2
)

delete_button.pack(
    side="right",
    fill="x",
    expand=True,
    padx=5
)


# ==============================
# Keyboard Support
# ==============================

root.bind("<Return>", lambda event: calculate())
root.bind("<Escape>", lambda event: clear_display())
root.bind("<BackSpace>", lambda event: delete_last())


# ==============================
# Start Application
# ==============================

root.mainloop()