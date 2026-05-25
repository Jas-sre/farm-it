import tkinter as tk
from tkinter import messagebox
from db import execute_query,fetch_all

def open_registration_window():
    window = tk.Toplevel()
    window.title("Register")
    window.geometry("600x700")

    tk.Label(window, text="Register As", font=("Arial", 20, "bold")).pack(pady=30)
    role_var = tk.StringVar(value="farmer")
    tk.Radiobutton(window, text="Farmer", variable=role_var, value="farmer").pack(pady=10)
    tk.Radiobutton(window, text="Customer", variable=role_var, value="customer").pack(pady=10)

    entries = {}
    fields = ["Username", "Password", "Name"]
    for field in fields:
        tk.Label(window, text=field).pack()
        entry = tk.Entry(window)
        entry.pack()
        entries[field.lower()] = entry

    additional = {
        "farmer": ["Product (with price)", "Contact", "Tag", "Location"],
        "customer": []
    }
    additional_entries = {}
    dynamic_frame = tk.Frame(window)
    dynamic_frame.pack(pady=30)

    def update_form():
        for widget in dynamic_frame.winfo_children():
            widget.destroy()
        additional_entries.clear()
        for field in additional[role_var.get()]:
            tk.Label(dynamic_frame, text=field).pack()
            entry = tk.Entry(dynamic_frame)
            entry.pack()
            additional_entries[field.lower()] = entry

    role_var.trace("w", lambda *args: update_form())
    update_form()

    def register():
        username = entries["username"].get().strip()
        password = entries["password"].get().strip()
        name = entries["name"].get().strip()
        role = role_var.get()

        if not (username and password and name):
            messagebox.showerror("Error", "Please fill all basic fields")
            return

        if role == "farmer":
            product = additional_entries["product (with price)"].get().strip()
            contact = additional_entries["contact"].get().strip()
            tag = additional_entries["tag"].get().strip()
            location = additional_entries["location"].get().strip()

            if not all([product, contact, tag, location]):
                    messagebox.showerror("Error", "Please fill all farmer fields")
                    
            if not username or not password or not name:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            existing = fetch_all("SELECT * FROM farmers WHERE username=%s", (username,))
            if existing:
                messagebox.showerror("Registration Failed", "Username already exists!")
                return
            
            query = "INSERT INTO farmers (username, password, name, product, contact, tag, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (username, password, name, product, contact, tag, location)
        else:
            existing = fetch_all("SELECT * FROM customers WHERE username=%s", (username,))
            if existing:
                messagebox.showerror("Registration Failed", "Username already exists!")
                return
            
            query = "INSERT INTO customers (username, password, name) VALUES (%s, %s, %s)"
            values = (username, password, name)

        try:
            execute_query(query, values)
            messagebox.showinfo("Success", f"{role.capitalize()} registered successfully")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(window, text="Register", bg="#4CAF50", fg="white", command=register).pack(pady=30)
