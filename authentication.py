# authentication.py
from database import conn, cursor, hash_password
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def login(username_entry, password_entry, root):
    username = username_entry.get()
    password = hash_password(password_entry.get())

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    if user:
        # Clear the login screen
        for widget in root.winfo_children():
            widget.destroy()

        # Create welcome screen
        welcome_label = tk.Label(root, text=f"Welcome, {username}!")
        welcome_label.pack(pady=20)

        # Button to show/hide the image
        show_image_button = tk.Button(root, text="Show Image", command=lambda: toggle_image(root))
        show_image_button.pack()
        show_image_button.image_visible = False  # Initialize the image state

        logout_button = tk.Button(root, text="Logout", command=lambda: logout(root))
        logout_button.pack()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def logout(root):
    # Clear the welcome screen
    for widget in root.winfo_children():
        widget.destroy()

def register(username_entry, password_entry, root):
    username = username_entry.get()
    password = hash_password(password_entry.get())

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

def toggle_image(root):
    # Assuming you have an image file named 'image.png' in the same directory as your script
    image_path = 'test.png'
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Check if the image label already exists
    if hasattr(root, 'image_label'):
        # If the image is visible, hide it
        if root.image_visible:
            root.image_label.pack_forget()
            show_image_button.config(text="Show Image")
            root.image_visible = False
        # If the image is hidden, show it
        else:
            root.image_label.pack()
            show_image_button.config(text="Hide Image")
            root.image_visible = True
    else:
        # If the image label doesn't exist, create it and show it
        root.image_label = tk.Label(root, image=photo)
        root.image_label.image = photo  # Keep a reference to avoid garbage collection
        root.image_label.pack()
        root.image_visible = True



# Guard to prevent code from being executed when the module is imported
if __name__ == "__main__":
    # Placeholder for testing the functions
    print("This script is being run directly.")
    # You can add code here to test the functions if needed