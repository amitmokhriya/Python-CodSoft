import tkinter as tk
from tkinter import messagebox
import random
import string


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showwarning(
                "Invalid Length",
                "Password length should be at least 4 characters."
            )
            return

        characters = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(
            random.choice(characters) for _ in range(length)
        )

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )


def copy_password():
    password = password_entry.get()

    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard!"
        )
    else:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Password Generator")

# Initial window size
root.geometry("600x450")

# Minimum size
root.minsize(500, 400)

# Allow resizing
root.resizable(True, True)

root.configure(bg="#f4f6f8")


# =========================
# MAIN FRAME
# =========================

main_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

main_frame.pack(
    fill="both",
    expand=True
)


# =========================
# TITLE
# =========================

title = tk.Label(
    main_frame,
    text="🔐 Password Generator",
    font=("Arial", 26, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

title.pack(pady=(45, 10))


# =========================
# DESCRIPTION
# =========================

description = tk.Label(
    main_frame,
    text="Generate a strong and random password",
    font=("Arial", 13),
    bg="#f4f6f8",
    fg="#6b7280"
)

description.pack(pady=5)


# =========================
# LENGTH LABEL
# =========================

length_label = tk.Label(
    main_frame,
    text="Enter Password Length:",
    font=("Arial", 14, "bold"),
    bg="#f4f6f8",
    fg="#374151"
)

length_label.pack(pady=(30, 8))


# =========================
# LENGTH ENTRY
# =========================

length_entry = tk.Entry(
    main_frame,
    font=("Arial", 14),
    justify="center",
    width=20
)

length_entry.pack(pady=5)

length_entry.insert(0, "12")


# =========================
# GENERATE BUTTON
# =========================

generate_button = tk.Button(
    main_frame,
    text="Generate Password",
    font=("Arial", 13, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    padx=25,
    pady=10,
    cursor="hand2",
    command=generate_password
)

generate_button.pack(pady=25)


# =========================
# PASSWORD ENTRY
# =========================

password_entry = tk.Entry(
    main_frame,
    font=("Arial", 15),
    justify="center",
    width=40
)

password_entry.pack(pady=5)


# =========================
# COPY BUTTON
# =========================

copy_button = tk.Button(
    main_frame,
    text="📋 Copy Password",
    font=("Arial", 11, "bold"),
    bg="#10b981",
    fg="white",
    activebackground="#059669",
    activeforeground="white",
    padx=20,
    pady=9,
    cursor="hand2",
    command=copy_password
)

copy_button.pack(pady=18)


# =========================
# FOOTER
# =========================

footer = tk.Label(
    main_frame,
    text="Use a unique password for every account.",
    font=("Arial", 10),
    bg="#f4f6f8",
    fg="#6b7280"
)

footer.pack(pady=10)


# =========================
# START APPLICATION
# =========================

root.mainloop()