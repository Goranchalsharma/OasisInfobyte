import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

FILE_NAME = 'bmi_data.csv'
if not os.path.exists(FILE_NAME):
    pd.DataFrame(columns=['Name', 'Date', 'Weight', 'Height', 'BMI']).to_csv(FILE_NAME, index=False)

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100
        bmi = round(weight / (height ** 2), 2)
        bmi_result.set(f"BMI: {bmi}")
        
        save_data(user_name.get(), weight, height * 100, bmi)
        
        if bmi < 18.5:
            messagebox.showinfo("Result", f"Your BMI is {bmi} (Underweight)")
        elif 18.5 <= bmi < 24.9:
            messagebox.showinfo("Result", f"Your BMI is {bmi} (Normal weight)")
        elif 25 <= bmi < 29.9:
            messagebox.showinfo("Result", f"Your BMI is {bmi} (Overweight)")
        else:
            messagebox.showinfo("Result", f"Your BMI is {bmi} (Obese)")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and height")

def save_data(name, weight, height, bmi):
    date = datetime.now().strftime("%Y-%m-%d")
    data = {'Name': name, 'Date': date, 'Weight': weight, 'Height': height, 'BMI': bmi}
    
    df = pd.DataFrame([data])
    df.to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False)

def view_history():
    try:
        df = pd.read_csv(FILE_NAME)
        user_df = df[df['Name'] == user_name.get()]
        if not user_df.empty:
            history_window = tk.Toplevel(root)
            history_window.title("BMI History")
            history_window.geometry("400x250")
            
            cols = list(user_df.columns)
            tree = ttk.Treeview(history_window, columns=cols, show='headings')
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.grid(row=0, column=0)
            
            for index, row in user_df.iterrows():
                tree.insert("", "end", values=list(row))
            
        else:
            messagebox.showinfo("No Data", "No historical data found for this user.")
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No data found. Please calculate BMI first.")

def show_bmi_trend():
    try:
        df = pd.read_csv(FILE_NAME)
        user_df = df[df['Name'] == user_name.get()]
        
        if not user_df.empty:
            plt.plot(user_df['Date'], user_df['BMI'], marker='o', color='blue')
            plt.title(f"BMI Trend for {user_name.get()}")
            plt.xlabel("Date")
            plt.ylabel("BMI")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No Data", "No data found to display a trend.")
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No data found. Please calculate BMI first.")

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("300x250")
root.configure(bg="#F5F5DC")

user_name = tk.StringVar()
weight_entry = tk.StringVar()
height_entry = tk.StringVar()
bmi_result = tk.StringVar()

pad_options = {'padx': 10, 'pady': 5}
bold_font = ("Arial", 12, "bold")

tk.Label(root, font=bold_font, text="Name:", fg="#023020", bg="#F5F5DC").grid(row=0, column=0, **pad_options)
tk.Entry(root, font=bold_font, fg="#FFFFFF", bg="#5C4033", textvariable=user_name).grid(row=0, column=1, **pad_options)

tk.Label(root, font=bold_font, text="Weight (kg):", fg="#023020", bg="#F5F5DC").grid(row=1, column=0, **pad_options)
tk.Entry(root, font=bold_font, fg="#FFFFFF", bg="#5C4033", textvariable=weight_entry).grid(row=1, column=1, **pad_options)

tk.Label(root, font=bold_font, text="Height (cm):", fg="#023020", bg="#F5F5DC").grid(row=2, column=0, **pad_options)
tk.Entry(root, font=bold_font, fg="#FFFFFF", bg="#5C4033", textvariable=height_entry).grid(row=2, column=1, **pad_options)

tk.Button(root, text="Calculate BMI", command=calculate_bmi, fg="#d34f00", font=bold_font).grid(row=3, column=0, columnspan=2, **pad_options)

tk.Label(root, textvariable=bmi_result, bg="#D3D3D3", fg="#023020" , font=bold_font).grid(row=4, column=0, columnspan=2, **pad_options)

tk.Button(root, text="View History", command=view_history, fg="#d34f00", font=bold_font).grid(row=5, column=0, columnspan=2, **pad_options)

tk.Button(root, text="Show BMI Trend", command=show_bmi_trend, fg="#d34f00", font=bold_font).grid(row=6, column=0, columnspan=2, **pad_options)

root.mainloop()
