import tkinter as tk
from tkinter import ttk, messagebox

class Util:
    @staticmethod
    def get_button(window, text, command, width=20):
        return ttk.Button(
            window,
            text=text,
            command=command,
            width=width
        )

    @staticmethod
    def get_img_label(window):
        label = ttk.Label(window)
        label.pack(fill=tk.BOTH, expand=True)
        return label

    @staticmethod
    def get_text_label(window, text, font_size=12):
        return ttk.Label(
            window,
            text=text,
            font=("Helvetica", font_size),  # Use font_size parameter
            justify="left"
        )

    @staticmethod
    def get_entry_text(window):
        return ttk.Entry(
            window,
            font=("Helvetica", 12),
            width=30
        )

    @staticmethod
    def msg_box(title, description):
        messagebox.showinfo(title, description)
