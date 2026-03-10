import tkinter as tk
from tkinter import ttk
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Database
# =========================

conn = sqlite3.connect("data_analysis.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
id INTEGER PRIMARY KEY AUTOINCREMENT,
month TEXT,
value INTEGER
)
""")

conn.commit()

# =========================
# Insert Data
# =========================

def add_data():
    month = month_entry.get()
    value = value_entry.get()

    cursor.execute("INSERT INTO sales(month,value) VALUES (?,?)",(month,value))
    conn.commit()

    month_entry.delete(0,tk.END)
    value_entry.delete(0,tk.END)

    show_data()


# =========================
# Show Data
# =========================

def show_data():

    for row in table.get_children():
        table.delete(row)

    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()

    for r in rows:
        table.insert("",tk.END,values=r)


# =========================
# Get Data for Analysis
# =========================

def get_values():

    cursor.execute("SELECT value FROM sales")
    rows = cursor.fetchall()

    values = np.array([r[0] for r in rows])

    return values


# =========================
# Charts
# =========================

def bar_chart():

    cursor.execute("SELECT month,value FROM sales")
    rows = cursor.fetchall()

    months = [r[0] for r in rows]
    values = np.array([r[1] for r in rows])

    plt.bar(months,values,color="#ff8fab")
    plt.title("Sales Bar Chart")
    plt.show()


def line_chart():

    cursor.execute("SELECT month,value FROM sales")
    rows = cursor.fetchall()

    months = [r[0] for r in rows]
    values = np.array([r[1] for r in rows])

    plt.plot(months,values,marker="o",color="#cdb4db")
    plt.title("Sales Line Chart")
    plt.show()


def pie_chart():

    cursor.execute("SELECT month,value FROM sales")
    rows = cursor.fetchall()

    months = [r[0] for r in rows]
    values = np.array([r[1] for r in rows])

    plt.pie(values,labels=months,autopct="%1.1f%%")
    plt.title("Sales Distribution")
    plt.show()


# =========================
# Statistics
# =========================

def analyze():

    values = get_values()

    if len(values)==0:
        result_label.config(text="No Data")
        return

    mean = np.mean(values)
    total = np.sum(values)
    max_val = np.max(values)
    min_val = np.min(values)

    result_label.config(
        text=f"Mean = {mean:.2f}   Total = {total}   Max = {max_val}   Min = {min_val}"
    )


# =========================
# GUI
# =========================

root = tk.Tk()
root.title("Data Analysis Program")
root.geometry("750x500")
root.config(bg="#f8edeb")

title = tk.Label(root,text="Data Analysis Dashboard",
font=("Arial",18,"bold"),bg="#f8edeb",fg="#6d6875")

title.pack(pady=10)


# Frame Inputs
frame = tk.Frame(root,bg="#f8edeb")
frame.pack()

tk.Label(frame,text="Month",bg="#f8edeb").grid(row=0,column=0,padx=10)
month_entry = tk.Entry(frame)
month_entry.grid(row=0,column=1)

tk.Label(frame,text="Value",bg="#f8edeb").grid(row=0,column=2,padx=10)
value_entry = tk.Entry(frame)
value_entry.grid(row=0,column=3)

tk.Button(frame,text="Add Data",
bg="#ffb4a2",
command=add_data).grid(row=0,column=4,padx=10)


# Table
table = ttk.Treeview(root,columns=("ID","Month","Value"),show="headings")
table.heading("ID",text="ID")
table.heading("Month",text="Month")
table.heading("Value",text="Value")

table.pack(pady=20)


# Buttons
btn_frame = tk.Frame(root,bg="#f8edeb")
btn_frame.pack()

tk.Button(btn_frame,text="Bar Chart",
bg="#ffc8dd",width=12,command=bar_chart).grid(row=0,column=0,padx=10)

tk.Button(btn_frame,text="Line Chart",
bg="#cdb4db",width=12,command=line_chart).grid(row=0,column=1,padx=10)

tk.Button(btn_frame,text="Pie Chart",
bg="#bde0fe",width=12,command=pie_chart).grid(row=0,column=2,padx=10)

tk.Button(btn_frame,text="Analyze Data",
bg="#a2d2ff",width=12,command=analyze).grid(row=0,column=3,padx=10)


result_label = tk.Label(root,text="",
font=("Arial",12,"bold"),bg="#f8edeb",fg="#6d6875")

result_label.pack(pady=20)

show_data()

root.mainloop()
