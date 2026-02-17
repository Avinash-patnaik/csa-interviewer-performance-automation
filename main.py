import os
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
        
    def start_process(self, mode):

        folder_path = f"data/{mode}/"

        target_file = get_latest_file(folder_path)

        if not target_file:
            messagebox.showwarning("No File", f"No new files found in {folder_path}")
            return

        # 3. Confirmation Dialog
        if messagebox.askyesno("Confirm", f"Process latest file: {os.path.basename(target_file)}?"):
            try:
                # --- START PIPELINE ---
                # df = load_excel(target_file)
                # status = run_mailer_logic(df, mode)
                # -----------------------
                
                # 4. Rename file after success
                new_name = rename_file(target_file)
                messagebox.showinfo("Success", f"Emails sent! File renamed to: {new_name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MailerGUI(root)
    root.mainloop()