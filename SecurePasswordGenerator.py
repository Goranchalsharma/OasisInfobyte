import tkinter as tk
from tkinter import messagebox
import pyperclip
import secrets
import string

class PasswordGeneratorApp:
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Secure Password Generator")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#e0f7fa")

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#e0f7fa")
        self.frame.pack(pady=20)
        
        self.title_label = tk.Label(self.frame, text="Password Generator", font=("Arial", 18, "bold"), bg="#e0f7fa", fg="#00008B")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.length_label = tk.Label(self.frame, text="Password Length(4-128):", font=("Arial", 12), bg="#e0f7fa", fg="#00008B")
        self.length_label.grid(row=1, column=0, sticky="e", pady=5, padx=5)

        self.length_var = tk.StringVar(value="")
        self.length_entry = tk.Entry(self.frame, textvariable=self.length_var, width=10, font=("Arial", 12), fg="#00008B", bg="#ffffff")
        self.length_entry.grid(row=1, column=1, sticky="w", pady=5, padx=5)

        self.uppercase_var = tk.BooleanVar(value=False)
        self.lowercase_var = tk.BooleanVar(value=False)
        self.digits_var = tk.BooleanVar(value=False)
        self.symbols_var = tk.BooleanVar(value=False)

        self.uppercase_check = tk.Checkbutton(self.frame, text="Include Uppercase", variable=self.uppercase_var, bg="#e0f7fa", fg="#4169E1", font=("Arial", 12))
        self.uppercase_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5, padx=5)

        self.lowercase_check = tk.Checkbutton(self.frame, text="Include Lowercase", variable=self.lowercase_var, bg="#e0f7fa", fg="#4169E1", font=("Arial", 12))
        self.lowercase_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=5, padx=5)

        self.digits_check = tk.Checkbutton(self.frame, text="Include Digits", variable=self.digits_var, bg="#e0f7fa", fg="#4169E1", font=("Arial", 12))
        self.digits_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=5, padx=5)

        self.symbols_check = tk.Checkbutton(self.frame, text="Include Symbols", variable=self.symbols_var, bg="#e0f7fa", fg="#4169E1", font=("Arial", 12))
        self.symbols_check.grid(row=5, column=0, columnspan=2, sticky="w", pady=5, padx=5)

        self.generate_btn = tk.Button(self.frame, text="Generate Password", command=self.generate_password, font=("Arial", 12, "bold"), bg="#00796b", fg="#4169E1", activebackground="#00796b", activeforeground="#ffffff")
        self.generate_btn.grid(row=6, column=0, columnspan=2, pady=10)

        self.password_entry = tk.Entry(self.frame, font=("Arial", 14), justify="center", width=25, show="*", fg="#00008B", bg="#ffffff")
        self.password_entry.grid(row=7, column=0, columnspan=2, pady=10)

        self.copy_btn = tk.Button(self.frame, text="Copy to Clipboard", command=self.copy_password, font=("Arial", 12, "bold"), bg="#00796b", fg="#4169E1", activebackground="#00796b", activeforeground="#ffffff")
        self.copy_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def validate_password_length(self):
        try:
            length = int(self.length_var.get())
            if not (4 <= length <= 128):
                raise ValueError("Password length must be between 4 and 128.")
            return length
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid password length between 4 and 128.")
            return None

    def generate_password(self):
        length = self.validate_password_length()
        if not length:
            return

        character_pool = ''
        if self.uppercase_var.get():
            character_pool += string.ascii_uppercase
        if self.lowercase_var.get():
            character_pool += string.ascii_lowercase
        if self.digits_var.get():
            character_pool += string.digits
        if self.symbols_var.get():
            character_pool += string.punctuation

        if not character_pool:
            messagebox.showerror("Selection Error", "At least one character set must be selected.")
            return

        password = ''.join(secrets.choice(character_pool) for _ in range(length))
        self.password_entry.delete(0, 'end')
        self.password_entry.insert('end', password)

    def copy_password(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")
        else:
            messagebox.showwarning("No Password", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
