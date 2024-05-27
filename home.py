import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, VERTICAL
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256

# Database setup
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
conn.commit()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def login():
    username = username_entry.get()
    password = hash_password(password_entry.get())

    # Check if the user is trying to log in as the admin
    if username == "admin" and password == hash_password("admin"):
        # Clear the login screen
        for widget in root.winfo_children():
            widget.destroy()

        # Show the admin screen
        show_admin_screen()
        return

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    if user:
        # Clear the login screen
        for widget in root.winfo_children():
            widget.destroy()

        # Show the welcome screen
        show_welcome_screen(username)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# def show_admin_screen():
#     # Create admin screen
#     admin_label = tk.Label(root, text="Welcome, Admin!", font=("Helvetica", 24), bg='#3652AD')
#     admin_label.pack(pady=20)
#
#     # Add some sample text
#     text_label = tk.Label(root, text="This is the admin screen with some sample text.", font=("Helvetica", 14), bg='#3652AD')
#     text_label.pack(pady=(30, 0))  # Add padding to the top
#
#     # Create the logout button after packing the property list
#     logout_button = ttk.Button(root, text="Logout", command=logout)
#     logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

def show_admin_screen():
    # Clear the root window
    for widget in root.winfo_children():
        widget.destroy()

    # Create admin screen
    admin_label = tk.Label(root, text="Welcome, Admin!", font=("Helvetica", 24), bg='#3652AD')
    admin_label.pack(pady=20)

    # Add some sample text
    sample_text = "This is the admin screen with some sample text."
    text_label = tk.Label(root, text=sample_text, font=("Helvetica", 14), bg='#3652AD', wraplength=400)
    text_label.pack(pady=(20, 0))  # Add padding to the top

    # Create a button to display all user records
    display_records_button = ttk.Button(root, text="Display User Records", command=display_user_records)
    display_records_button.pack(pady=(10, 0))

    # Create the logout button
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)


def display_user_records():
    # Fetch all user records from the database
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # Create a new window to display the user records
    records_window = tk.Toplevel(root)
    records_window.title("User Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(records_window, columns=("ID", "Username", "Password"), show="headings")
    treeview.pack(expand=True, fill='both')

    # Define the columns
    treeview.heading("ID", text="ID")
    treeview.heading("Username", text="Username")
    treeview.heading("Password", text="Password")

    # Insert the records into the treeview
    for user in users:
        treeview.insert("", "end", values=user)

    # Function to close the records window
    def close_records_window():
        records_window.destroy()

    # Add a close button to the records window
    close_button = ttk.Button(records_window, text="Close", command=close_records_window)
    close_button.pack(pady=(10, 0))

def show_welcome_screen(username):
    # Create welcome screen
    welcome_label = tk.Label(root, text=f"Welcome, {username.capitalize()}!", font=("Helvetica", 24), bg='#3652AD')
    welcome_label.pack(pady=20)

    # Create a frame for the images and text
    content_frame = tk.Frame(root, bg='#3652AD')
    content_frame.pack(expand=True, fill='both')

    # Create a canvas to hold the content and scrollbar
    canvas = tk.Canvas(content_frame, bg='#3652AD')
    canvas.pack(side='left', fill='both', expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(content_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Bind the mouse wheel events to the canvas
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))

    # Create a frame inside the canvas for the content
    content_inside_canvas = tk.Frame(canvas, bg='#3652AD')

    # Add the content frame to the canvas
    canvas.create_window((0, 0), window=content_inside_canvas, anchor='nw')

    # Load and display images with text blocks
    images_info = [
        {"path": "test.png", "text": "This is the first image with some text."},
        {"path": "test.png", "text": "This is the second image with some more text."},
        {"path": "test.png", "text": "This is the third image with even more text."},
        {"path": "test.png", "text": "This is the fourth image with even more text."},
        {"path": "test.png", "text": "This is the fifth image with even more text."},
        {"path": "test.png", "text": "This is the sixth image with even more text."}
    ]

    for i, info in enumerate(images_info):
        # Load the image
        image = Image.open(info["path"])

        # Calculate the desired height based on a percentage of the screen height
        desired_height = int(root.winfo_screenheight() * 0.2)  # 20% of the screen height
        aspect_ratio = image.width / image.height
        new_width = int(aspect_ratio * desired_height)
        image = image.resize((new_width, desired_height), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image)

        # Create a label for the image
        image_label = tk.Label(content_inside_canvas, image=photo, bg='#3652AD')
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.grid(row=i, column=0, padx=(0, 20), sticky='w')  # Add padding to the left

        # Create a label for the text block
        text_label = tk.Label(content_inside_canvas, text=info["text"], font=("Helvetica", 14), bg='#3652AD', wraplength=400)
        text_label.grid(row=i, column=1, sticky='w')  # Align to the left and wrap the text

    # Create the logout button after packing the property list
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    # Function to update the scrollregion of the canvas
    def on_content_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    # Bind the configure event to the content frame
    content_inside_canvas.bind('<Configure>', on_content_configure)



def logout():
    # Clear the welcome screen
    for widget in root.winfo_children():
        widget.destroy()

    # Show the login screen again
    create_login_screen()

def register():
    username = username_entry.get()
    password = hash_password(password_entry.get())

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

def create_login_screen():
    global username_entry, password_entry

    # Add padding to the main frame
    main_frame = tk.Frame(root, bg='#3652AD')
    main_frame.pack(expand=True, fill='both')

    # Create and pack the widgets with padding and alignment
    username_label = tk.Label(main_frame, text="Username:", bg='#3652AD')
    username_label.pack(pady=(20, 5))  # Add vertical padding

    username_entry = tk.Entry(main_frame)
    username_entry.pack(pady=5)  # Add vertical padding

    password_label = tk.Label(main_frame, text="Password:", bg='#3652AD')
    password_label.pack(pady=(5, 20))  # Add vertical padding

    password_entry = tk.Entry(main_frame, show="*")
    password_entry.pack(pady=(5, 20))  # Add vertical padding

    # Create a frame for the buttons
    button_frame = tk.Frame(main_frame, bg='#3652AD')
    button_frame.pack(pady=(5, 20))  # Add vertical padding

    # Use ttk.Button instead of tk.Button
    login_button = ttk.Button(button_frame, text="Login", command=login)
    login_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    register_button = ttk.Button(button_frame, text="Register", command=register)
    register_button.pack(side='left', padx=(10, 0))  # Add horizontal padding

# GUI setup
root = tk.Tk()
root.title("Login Screen")

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to the screen size
root.geometry(f"{screen_width}x{screen_height}")

# Set the background color of the window to 3652AD
root.configure(bg='#3652AD')

ttk.Style().theme_use('alt')

# Create login screen
create_login_screen()

root.mainloop()

# Close the database connection
conn.close()