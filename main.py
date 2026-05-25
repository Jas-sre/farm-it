import tkinter as tk
from admin import open_admin_dashboard
from customer import open_customer_interface
from farmer import open_farmer_interface
from register import open_registration_window
from PIL import Image,ImageTk
import os,sys

def main():
    root = tk.Tk()
    image = Image.open(r"bg.jpeg")
    image = image.resize((1550,1020), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.image = bg_image  
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.title("Farm-It | Login")
    root.attributes('-fullscreen',True)
    root.configure(bg="#f0fff0")
    
    tk.Label(root, text="Welcome to Farm-It", font=("Helvetica", 50, "bold"), bg="#228B22",fg="#FFFFFF").pack(pady=90)

    tk.Button(root, text="Admin Login", width=25, font=("Helvetica", 20), bg="#4CAF50", fg="white", command=open_admin_dashboard).pack(pady=30)
    tk.Button(root, text="Customer Login", width=25, font=("Helvetica", 20), bg="#2196F3", fg="white", command=open_customer_interface).pack(pady=30)
    tk.Button(root, text="Farmer Login", width=25, font=("Helvetica", 20), bg="#FF9800", fg="white", command=open_farmer_interface).pack(pady=30)
    tk.Button(root, text="Register", width=25, font=("Helvetica", 20), bg="#9C27B0", fg="white", command=open_registration_window).pack(pady=30)
    tk.Button(root, text="Exit", width=25, font=("Helvetica", 20),bg="#f44336", fg="white", command=root.destroy).pack(pady=5)

    root.mainloop()


main()
