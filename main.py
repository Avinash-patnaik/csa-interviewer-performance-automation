import tkinter as tk
from tkinter import messagebox, font
from src.reader import get_latest_file, rename_file

class MailerGUI:
    def __init__(self, root):
        self.root = root 
        self.root.title("CSA Interviewer Performance Automation")
        self.root.geometry("400x200")

        # Set custom font
        title_font = font.Font(family="Helvetica", size=16, weight="bold")

        # Heading 
        tk.Label(root, text="CSA Interviewer Performance Automation", font=title_font).pack(pady=20)
        tk.Label(root, text="Click the button below to send performance emails").pack(pady=10)

        # Send Emails Button
        tk.Button(root, text="FOLCAPI", width=25, height=2,
                  bg="#22b10f", command=lambda: self.start_process("FOLCAPI")).pack(pady=10)
    
        tk.Button(root, text="SPESE", width=25, height=2,
                  bg="#153ceb", command=lambda: self.start_process("SPESE")).pack(pady=10)