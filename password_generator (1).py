#!/usr/bin/env python3
"""
Password Generator with GUI
A simple window app to generate passwords and copy them with one click.
"""

import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,.<>?/")

    if not pools:
        return None

    all_chars = "".join(pools)
    password_chars = [secrets.choice(pool) for pool in pools]
    remaining = length - len(password_chars)
    password_chars += [secrets.choice(all_chars) for _ in range(remaining)]
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def password_strength(password):
    score = 0
    score += len(password) >= 8
    score += len(password) >= 12
    score += len(password) >= 16
    score += any(c.islower() for c in password)
    score += any(c.isupper() for c in password)
    score += any(c.isdigit() for c in password)
    score += any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in password)

    if score <= 3:
        return "Weak"
    elif score <= 5:
        return "Moderate"
    else:
        return "Strong"


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        root.title("Password Generator")
        root.geometry("420x360")
        root.resizable(False, False)

        padding = {"padx": 15, "pady": 8}

        # Length
        ttk.Label(root, text="Password Length:").pack(anchor="w", **padding)
        self.length_var = tk.IntVar(value=16)
        length_frame = ttk.Frame(root)
        length_frame.pack(fill="x", padx=15)
        self.length_slider = ttk.Scale(
            length_frame, from_=4, to=64, orient="horizontal",
            variable=self.length_var, command=self._update_length_label
        )
        self.length_slider.pack(side="left", fill="x", expand=True)
        self.length_label = ttk.Label(length_frame, text="16", width=3)
        self.length_label.pack(side="left", padx=5)

        # Options
        options_frame = ttk.LabelFrame(root, text="Include")
        options_frame.pack(fill="x", padx=15, pady=10)

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.use_upper).pack(anchor="w", padx=10, pady=2)
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.use_lower).pack(anchor="w", padx=10, pady=2)
        ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.use_digits).pack(anchor="w", padx=10, pady=2)
        ttk.Checkbutton(options_frame, text="Symbols (!@#$...)", variable=self.use_symbols).pack(anchor="w", padx=10, pady=2)

        # Generate button
        ttk.Button(root, text="Generate Password", command=self.on_generate).pack(pady=10)

        # Result display
        result_frame = ttk.Frame(root)
        result_frame.pack(fill="x", padx=15)

        self.result_var = tk.StringVar(value="")
        self.result_entry = ttk.Entry(result_frame, textvariable=self.result_var, font=("Consolas", 12), state="readonly")
        self.result_entry.pack(side="left", fill="x", expand=True, ipady=4)

        ttk.Button(result_frame, text="Copy", command=self.on_copy).pack(side="left", padx=5)

        # Strength label
        self.strength_var = tk.StringVar(value="")
        self.strength_label = ttk.Label(root, textvariable=self.strength_var, font=("Segoe UI", 10, "bold"))
        self.strength_label.pack(pady=8)

        # Generate one on startup
        self.on_generate()

    def _update_length_label(self, event=None):
        self.length_label.config(text=str(int(self.length_var.get())))

    def on_generate(self):
        length = int(self.length_var.get())
        pwd = generate_password(
            length,
            self.use_upper.get(),
            self.use_lower.get(),
            self.use_digits.get(),
            self.use_symbols.get(),
        )
        if pwd is None:
            messagebox.showwarning("No character types selected", "Please select at least one character type.")
            return

        self.result_var.set(pwd)
        strength = password_strength(pwd)
        self.strength_var.set(f"Strength: {strength}")

        colors = {"Weak": "red", "Moderate": "orange", "Strong": "green"}
        self.strength_label.config(foreground=colors.get(strength, "black"))

    def on_copy(self):
        pwd = self.result_var.get()
        if not pwd:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.root.update()  # keeps clipboard content after window closes
        messagebox.showinfo("Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
    main()

    