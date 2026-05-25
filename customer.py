import tkinter as tk
from tkinter import messagebox, ttk
from db import fetch_all, execute_query
import os
from PIL import Image,ImageTk

def open_customer_interface():
    login_window = tk.Toplevel()
    image = Image.open(r"loginbg.jpg")
    image = image.resize((500,500), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(login_window, image=bg_image)
    bg_label.image = bg_image  
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_window.title("Customer Login")
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

        result = fetch_all("SELECT * FROM customers WHERE username=%s AND password=%s", (username, password))
        if result:
            login_window.destroy()
            show_customer_dashboard(result[0])
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login_window, text="Login", command=login).pack(pady=30)

def show_customer_dashboard(customer):
    window = tk.Toplevel()
    window.title(f"Customer Dashboard - {customer['name']}")
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

    browse_tab = ttk.Frame(notebook)
    wishlist_tab = ttk.Frame(notebook)
    notebook.add(browse_tab, text="Browse Products")
    notebook.add(wishlist_tab, text="My Wishlist")

    search_frame = tk.Frame(browse_tab)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search: ").grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1, padx=5)

    result_frame = tk.Frame(browse_tab)
    result_frame.pack(fill=tk.BOTH, expand=True)

    columns = ["ID", "Username", "Name", "Product", "Contact", "Tag", "Location"]
    tree = ttk.Treeview(result_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True)

    def display_results(results):
        for row in tree.get_children():
            tree.delete(row)
        for f in results:
            tree.insert("", "end", values=(
                f.get("id"), f.get("username"), f.get("name"), f.get("product"),
                f.get("contact"), f.get("tag"), f.get("location")
            ))

    def search():
        q = search_entry.get().strip().lower()
        results = fetch_all("""
            SELECT * FROM farmers
            WHERE LOWER(tag) LIKE %s OR LOWER(location) LIKE %s OR LOWER(product) LIKE %s
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))
        display_results(results)

    def view_selected():
        selected = tree.selection()
        if not selected:
            tk.Label(info_window, text= "Please select a farmer", font=("Arial", 12)).pack(pady=5)
            return

        row = tree.item(selected[0])['values']
        info_window = tk.Toplevel(window)
        info_window.title("Farmer Info")
        info_window.geometry("400x300")

        fields = tree["columns"]
        for i, field in enumerate(fields):
            tk.Label(info_window, text=f"{field.capitalize()}: {row[i]}", font=("Arial", 12)).pack(pady=5)

    def save_to_wishlist():
        selected = tree.selection()
        if not selected:
            tk.Label(info_window, text="Please select a farmer", font=("Arial", 12)).pack(pady=5)
            return
        
        row = tree.item(selected[0])['values']
        info_window = tk.Toplevel(window)
        info_window.title("WishList Info")
        info_window.geometry("350x100")

        farmer_id = row[0]
        customer_id = customer['id']
        existing = fetch_all("SELECT * FROM wishlist WHERE customer_id=%s AND farmer_id=%s", (customer_id, farmer_id))
        if existing:
            tk.Label(info_window, text=f"{row[2]}'s product is already in your wishlist.", font=("Arial", 12)).pack(pady=5)
        else:
            execute_query("INSERT INTO wishlist (customer_id, farmer_id) VALUES (%s, %s)", (customer_id, farmer_id))
            tk.Label(info_window, text= f"{row[2]}'s product is added to your wishlist.", font=("Arial", 12)).pack(pady=5)
            load_wishlist()

    action_frame = tk.Frame(browse_tab)
    action_frame.pack(pady=5)
    tk.Button(action_frame, text="View Selected", command=view_selected, bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(action_frame, text="Save to Wishlist", command=save_to_wishlist, bg="green", fg="white").pack(side=tk.LEFT, padx=5)

    tk.Button(search_frame, text="Search", command=search).grid(row=0, column=2, padx=5)
    display_results(fetch_all("SELECT * FROM farmers"))

    wishlist_tree = ttk.Treeview(wishlist_tab, columns=columns, show="headings")
    for col in columns:
        wishlist_tree.heading(col, text=col)
        wishlist_tree.column(col, width=120)
    wishlist_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_wishlist():
        for row in wishlist_tree.get_children():
            wishlist_tree.delete(row)
        results = fetch_all("""
            SELECT f.* FROM farmers f
            JOIN wishlist w ON f.id = w.farmer_id
            WHERE w.customer_id = %s
        """, (customer['id'],))
        for f in results:
            wishlist_tree.insert("", "end", values=(
                f.get("id"), f.get("username"), f.get("name"), f.get("product"),
                f.get("contact"), f.get("tag"), f.get("location")
            ))

    load_wishlist()

    def remove_from_wishlist():
        selected = wishlist_tree.selection()
        if not selected:
            tk.Label(info_window, text= "Please select a farmer", font=("Arial", 12)).pack(pady=5)
            return
        row = wishlist_tree.item(selected[0])['values']
        info_window = tk.Toplevel(window)
        info_window.title("Wishlist info")
        info_window.geometry("350x100")
        farmer_id = row[0]
        customer_id = customer['id']

        execute_query("DELETE FROM wishlist WHERE customer_id=%s AND farmer_id=%s", (customer_id, farmer_id))
        tk.Label(info_window, text= f"{row[2]}'s product removed from wishlist.", font=("Arial", 12)).pack(pady=5)
        load_wishlist()

    tk.Button(wishlist_tab, text="Remove from Wishlist", command=remove_from_wishlist, bg="red", fg="white").pack(pady=5)
