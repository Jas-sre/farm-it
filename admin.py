import tkinter as tk
from tkinter import ttk, messagebox
from db import fetch_all, execute_query
import os
from PIL import Image,ImageTk

def open_admin_dashboard():
    login = tk.Toplevel()
    image = Image.open(r"loginbg.jpg")
    image = image.resize((500,500), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(login, image=bg_image)
    bg_label.image = bg_image  
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    login.title("Admin Login")
    login.geometry("500x500")

    tk.Label(login, text="Username",font=("Helvetica", 20)).pack(pady=50)
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Password",font=("Helvetica", 20)).pack(pady=50)
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def authenticate():
        user = username_entry.get()
        pw = password_entry.get()
        result = fetch_all("SELECT * FROM admins WHERE username=%s AND password=%s", (user, pw))
        if result:
            login.destroy()
            show_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login, text="Login", command=authenticate).pack(pady=30)

def show_admin_dashboard():
    window = tk.Toplevel()
    window.title("Admin Dashboard")
    window.attributes('-fullscreen',True)
    
    tk.Button(window, text="Home", command=lambda: [window.destroy(), os.system("python main.py")], bg="orange", fg="white", font=("Arial", 12)).pack(pady=10)

    style = ttk.Style()
    style.theme_use("default")

# Change Treeview background
    style.configure("Treeview",
    background="#e8f5e9",     # light green
    foreground="black",
    rowheight=25,
    fieldbackground="#e8f5e9")

# Change selected row highlight color
    style.map("Treeview",
    background=[("selected", "#a5d6a7")])

    notebook = ttk.Notebook(window)
    notebook.pack(fill=tk.BOTH, expand=True)
        
    farmer_tab = ttk.Frame(notebook)
    customer_tab = ttk.Frame(notebook)
    notebook.add(farmer_tab, text="Farmers")
    notebook.add(customer_tab, text="Customers")

    def load_table(tab, query, delete_query, update_query=None):
        for widget in tab.winfo_children():
            widget.destroy()

        data = fetch_all(query)
        cols = list(data[0].keys()) if data else []

        tree = ttk.Treeview(tab, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for row in data:
            tree.insert("", "end", iid=row['id'], values=tuple(row.values()))
        tree.pack(fill=tk.BOTH, expand=True)

        def delete_selected():
            selected = tree.selection()
            for sel in selected:
                execute_query(delete_query, (int(sel),))
            load_all()

        def edit_selected():
            selected = tree.selection()
            if not selected:
                return
            row = tree.item(selected[0])['values']
            edit_window = tk.Toplevel()
            edit_window.title("Edit Entry")
            entries = []
            for i, col in enumerate(cols):
                tk.Label(edit_window, text=col).pack()
                e = tk.Entry(edit_window)
                e.insert(0, row[i])
                e.pack()
                entries.append(e)

            def save_changes():
                values = [e.get() for e in entries[1:]]  # skip id
                values.append(entries[0].get())  # id last
                execute_query(update_query, tuple(values))
                edit_window.destroy()
                load_all()

            tk.Button(edit_window, text="Save", command=save_changes).pack()

        if update_query:
            tk.Button(tab, text="Edit Selected", command=edit_selected, bg="blue", fg="white").pack(pady=5)
        tk.Button(tab, text="Delete Selected", command=delete_selected, bg="red", fg="white").pack(pady=5)

    def load_all():
        load_table(farmer_tab, "SELECT * FROM farmers", "DELETE FROM farmers WHERE id = %s", "UPDATE farmers SET username=%s, password=%s, name=%s, product=%s, contact=%s, tag=%s, location=%s WHERE id=%s")
        load_table(customer_tab, "SELECT * FROM customers", "DELETE FROM customers WHERE id = %s")

    load_all()
