
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from openpyxl import Workbook

# ---------------- DATABASE ---------------- #

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        grade TEXT
        )
        """)
        self.conn.commit()

    def add(self,name,age,grade):
        self.cur.execute(
        "INSERT INTO students(name,age,grade) VALUES(?,?,?)",
        (name,age,grade))
        self.conn.commit()

    def delete(self,id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    def update(self,id,name,age,grade):
        self.cur.execute(
        "UPDATE students SET name=?,age=?,grade=? WHERE id=?",
        (name,age,grade,id))
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM students")
        return self.cur.fetchall()

# ---------------- APP ---------------- #

class App:

    def __init__(self,root):

        self.db = Database()

        root.title("Student Management System")
        root.geometry("700x500")
        root.config(bg="#f5f6fa")

        # ---------- FRAME INPUT ---------- #

        frame = tk.Frame(root,bg="#ffffff",padx=10,pady=10)
        frame.pack(pady=10)

        tk.Label(frame,text="Name",bg="#ffffff").grid(row=0,column=0)
        tk.Label(frame,text="Age",bg="#ffffff").grid(row=1,column=0)
        tk.Label(frame,text="Grade",bg="#ffffff").grid(row=2,column=0)

        self.name = tk.Entry(frame)
        self.age = tk.Entry(frame)
        self.grade = tk.Entry(frame)

        self.name.grid(row=0,column=1)
        self.age.grid(row=1,column=1)
        self.grade.grid(row=2,column=1)

        # ---------- BUTTON FRAME ---------- #

        btn_frame = tk.Frame(root,bg="#f5f6fa")
        btn_frame.pack(pady=10)

        self.add_btn = tk.Button(btn_frame,text="➕ Add",width=12,command=self.add_student)
        self.update_btn = tk.Button(btn_frame,text="✏ Update",width=12,command=self.update_student)
        self.delete_btn = tk.Button(btn_frame,text="🗑 Delete",width=12,command=self.delete_student)
        self.export_btn = tk.Button(btn_frame,text="📁 Export Excel",width=15,command=self.export_excel)

        self.add_btn.grid(row=0,column=0,padx=5)
        self.update_btn.grid(row=0,column=1,padx=5)
        self.delete_btn.grid(row=0,column=2,padx=5)
        self.export_btn.grid(row=0,column=3,padx=5)

        # ---------- SIMPLE BUTTON ANIMATION ---------- #

        for btn in [self.add_btn,self.update_btn,self.delete_btn,self.export_btn]:

            btn.bind("<Enter>",lambda e,b=btn: b.config(bg="#dfe6e9"))
            btn.bind("<Leave>",lambda e,b=btn: b.config(bg="SystemButtonFace"))

        # ---------- TABLE ---------- #

        table_frame = tk.Frame(root)
        table_frame.pack()

        self.table = ttk.Treeview(
        table_frame,
        columns=("ID","Name","Age","Grade"),
        show="headings",
        height=10)

        self.table.heading("ID",text="ID")
        self.table.heading("Name",text="Name")
        self.table.heading("Age",text="Age")
        self.table.heading("Grade",text="Grade")

        self.table.column("ID",width=50)
        self.table.column("Name",width=200)
        self.table.column("Age",width=100)
        self.table.column("Grade",width=100)

        self.table.pack()

        self.table.bind("<<TreeviewSelect>>",self.select_student)

        self.load_data()

    # ---------- FUNCTIONS ---------- #

    def load_data(self):

        for row in self.table.get_children():
            self.table.delete(row)

        for student in self.db.fetch():
            self.table.insert("",tk.END,values=student)

    def add_student(self):

        self.db.add(
        self.name.get(),
        self.age.get(),
        self.grade.get())

        self.load_data()

    def delete_student(self):

        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected,"values")

        self.db.delete(data[0])

        self.load_data()

    def update_student(self):

        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected,"values")

        self.db.update(
        data[0],
        self.name.get(),
        self.age.get(),
        self.grade.get())

        self.load_data()

    def select_student(self,event):

        selected = self.table.focus()

        if not selected:
            return

        data = self.table.item(selected,"values")

        self.name.delete(0,tk.END)
        self.age.delete(0,tk.END)
        self.grade.delete(0,tk.END)

        self.name.insert(0,data[1])
        self.age.insert(0,data[2])
        self.grade.insert(0,data[3])

    def export_excel(self):

        wb = Workbook()
        ws = wb.active

        ws.append(["ID","Name","Age","Grade"])

        for student in self.db.fetch():
            ws.append(student)

        wb.save("students.xlsx")

        messagebox.showinfo("Success","Exported to students.xlsx")

# ---------------- RUN ---------------- #

root = tk.Tk()
app = App(root)
root.mainloop()