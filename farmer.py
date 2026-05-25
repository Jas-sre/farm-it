import tkinter as tk
from tkinter import messagebox
from db import fetch_all, execute_query
import os
from PIL import Image,ImageTk

def open_farmer_interface():
    login_window = tk.Toplevel()
    image = Image.open(r"loginbg.jpg")
    image = image.resize((500,500), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(login_window, image=bg_image)
    bg_label.image = bg_image  
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_window.title("Farmer Login")
    login_window.geometry("500x500")

    tk.Label(login_window, text="Username",font=("Helvetica", 20)).pack(pady=50)
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    
    tk.Label(login_window, text="Password",font=("Helvetica", 20)).pack(pady=50)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    
    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        result = fetch_all("SELECT * FROM farmers WHERE username=%s AND password=%s", (username, password))
        if result:
            login_window.destroy()
            show_farmer_info(result[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(login_window, text="Login", command=login).pack(pady=30)

def show_farmer_info(farmer):
    window = tk.Toplevel()
    window.title("Farmer Dashboard")
    window.attributes('-fullscreen',True)
    
    image = Image.open(r"farmerbg.jpg")
    image = image.resize((1600,900), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.image = bg_image  
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Button(window, text="Home", command=lambda: [window.destroy(), os.system("python main.py")], bg="orange", fg="white", font=("Arial", 12)).pack(pady=10)


    fields = ["product", "contact", "tag", "location"]
    entries = {}

    for field in fields:
        tk.Label(window, text=f"{field.capitalize()}",font=("Helvetica", 20)).pack(pady=20)
        entry = tk.Entry(window, width=30)
        entry.insert(0, farmer.get(field, ""))
        entry.pack()
        entries[field] = entry

    def update_info():
        info_window = tk.Toplevel(window)
        info_window.title("Wishlist info")
        info_window.geometry("350x100")
        updates = {f: entries[f].get().strip() for f in fields}
        query = "UPDATE farmers SET product=%s, contact=%s, tag=%s, location=%s WHERE id=%s"
        execute_query(query, (updates["product"], updates["contact"], updates["tag"], updates["location"], farmer["id"]))
        tk.Label(info_window, text= "Information updated.", font=("Arial", 12)).pack(pady=5)

    tk.Button(window, text="Update Info", command=update_info,font=("Helvetica", 20),bg="#4CAF50", fg="white").pack(pady=30)

