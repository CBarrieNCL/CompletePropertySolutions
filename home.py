import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, VERTICAL
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256
from datetime import datetime

# Database setup
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS properties (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_name TEXT NOT NULL,
    landlord_name TEXT NOT NULL,
    next_available_date TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS landlords (
    landlord_id INTEGER PRIMARY KEY AUTOINCREMENT,
    landlord_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')
conn.commit()

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def login():
    global username, password
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

    # Create a button to display property records
    display_properties_button = ttk.Button(root, text="Display Property Records", command=display_property_records)
    display_properties_button.pack(pady=(10, 0))

    # Create a button to display landlord records
    display_landlords_button = ttk.Button(root, text="Display Landlord Records", command=display_landlord_records)
    display_landlords_button.pack(pady=(10, 0))

    # Create a button to display tenant records
    display_tenants_button = ttk.Button(root, text="Display Tenant Records", command=display_tenant_records)
    display_tenants_button.pack(pady=(10, 0))

    # Create a button to add a new property
    add_property_button = ttk.Button(root, text="Add Property", command=add_property)
    add_property_button.pack(pady=(10, 0))

    # Create a button to add a new landlord
    add_landlord_button = ttk.Button(root, text="Add Landlord", command=add_landlord)
    add_landlord_button.pack(pady=(10, 0))

    # Create a button to add a new tenant
    add_tenant_button = ttk.Button(root, text="Add Tenant", command=add_tenant)
    add_tenant_button.pack(pady=(10, 0))

    # Create the back to welcome screen button
    back_button = ttk.Button(root, text="Home", command=lambda: show_welcome_screen(username))
    back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-100, y=10)

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

def display_property_records():
    # Retrieve all property records from the database
    cursor.execute('SELECT * FROM properties')
    properties = cursor.fetchall()

    # Create a new window to display the property records
    display_properties_window = tk.Toplevel(root)
    display_properties_window.title("Property Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(display_properties_window, columns=("ID", "Property Name", "Landlord Name", "Next Available Date"), show="headings")
    treeview.pack(fill='both', expand=True)

    # Define column headings
    treeview.heading("ID", text="ID")
    treeview.heading("Property Name", text="Property Name")
    treeview.heading("Landlord Name", text="Landlord Name")
    treeview.heading("Next Available Date", text="Next Available Date")

    # Insert property records into the treeview
    for prop in properties:
        treeview.insert("", "end", values=prop)

    # Function to close the display properties window
    def close_window():
        display_properties_window.destroy()

    # Create a close button
    close_button = ttk.Button(display_properties_window, text="Close", command=close_window)
    close_button.pack(pady=(10, 0))

def display_landlord_records():
    # Fetch landlord records from the database
    cursor.execute('SELECT * FROM landlords')
    landlords = cursor.fetchall()

    # Create a new window to display the landlord records
    display_landlords_window = tk.Toplevel(root)
    display_landlords_window.title("Landlord Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(display_landlords_window, columns=("ID", "Landlord Name", "Gender", "Age"), show="headings")
    treeview.pack(fill='both', expand=True)

    # Define column headings
    treeview.heading("ID", text="ID")
    treeview.heading("Landlord Name", text="Landlord Name")
    treeview.heading("Gender", text="Gender")
    treeview.heading("Age", text="Age")

    # Insert landlord records into the treeview
    for landlord in landlords:
        treeview.insert("", "end", values=landlord)

    # Function to close the display landlords window
    def close_window():
        display_landlords_window.destroy()

    # Create a close button
    close_button = ttk.Button(display_landlords_window, text="Close", command=close_window)
    close_button.pack(pady=(10, 0))

def display_tenant_records():
    # Fetch tenant records from the database
    cursor.execute('SELECT * FROM tenants')
    tenants = cursor.fetchall()

    # Create a new window to display the tenant records
    display_tenants_window = tk.Toplevel(root)
    display_tenants_window.title("Tenant Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(display_tenants_window, columns=("ID", "Tenant Name", "Gender", "Age"), show="headings")
    treeview.pack(fill='both', expand=True)

    # Define column headings
    treeview.heading("ID", text="ID")
    treeview.heading("Tenant Name", text="Tenant Name")
    treeview.heading("Gender", text="Gender")
    treeview.heading("Age", text="Age")

    # Insert tenant records into the treeview
    for tenant in tenants:
        treeview.insert("", "end", values=tenant)

    # Function to close the display tenants window
    def close_window():
        display_tenants_window.destroy()

    # Create a close button
    close_button = ttk.Button(display_tenants_window, text="Close", command=close_window)
    close_button.pack(pady=(10, 0))

def add_property():
    # Create a new window for adding a property
    add_property_window = tk.Toplevel(root)
    add_property_window.title("Add Property")

    # Create entry fields for property name, landlord name, and next available date
    property_name_label = ttk.Label(add_property_window, text="Property Name:")
    property_name_label.pack(pady=(10, 5))
    property_name_entry = ttk.Entry(add_property_window)
    property_name_entry.pack(pady=(0, 10))

    landlord_name_label = ttk.Label(add_property_window, text="Landlord Name:")
    landlord_name_label.pack(pady=(0, 5))
    landlord_name_entry = ttk.Entry(add_property_window)
    landlord_name_entry.pack(pady=(0, 10))

    next_available_date_label = ttk.Label(add_property_window, text="Next Available Date (YYYY-MM-DD):")
    next_available_date_label.pack(pady=(0, 5))
    next_available_date_entry = ttk.Entry(add_property_window)
    next_available_date_entry.pack(pady=(0, 10))

    # Function to add the property to the database
    def submit_property():
        property_name = property_name_entry.get()
        landlord_name = landlord_name_entry.get()
        next_available_date_str = next_available_date_entry.get()

        # Validate the input
        if not property_name or not landlord_name or not next_available_date_str:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            # Convert the next_available_date string to a datetime object
            next_available_date = datetime.strptime(next_available_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Insert the property into the database
        cursor.execute('INSERT INTO properties (property_name, landlord_name, next_available_date) VALUES (?, ?, ?)',
                       (property_name, landlord_name, next_available_date))
        conn.commit()

        # Close the add property window
        add_property_window.destroy()

    # Create a submit button
    submit_button = ttk.Button(add_property_window, text="Submit", command=submit_property)
    submit_button.pack(pady=(10, 0))

def add_landlord():
    # Create a new window for adding a landlord
    add_landlord_window = tk.Toplevel(root)
    add_landlord_window.title("Add Landlord")

    # Create entry fields for landlord name, gender, and age
    landlord_name_label = ttk.Label(add_landlord_window, text="Landlord Name:")
    landlord_name_label.pack(pady=(10, 5))
    landlord_name_entry = ttk.Entry(add_landlord_window)
    landlord_name_entry.pack(pady=(0, 10))

    gender_label = ttk.Label(add_landlord_window, text="Gender (M/F/O):")
    gender_label.pack(pady=(0, 5))
    gender_entry = ttk.Entry(add_landlord_window)
    gender_entry.pack(pady=(0, 10))

    age_label = ttk.Label(add_landlord_window, text="Age:")
    age_label.pack(pady=(0, 5))
    age_entry = ttk.Entry(add_landlord_window)
    age_entry.pack(pady=(0, 10))

    # Function to add the landlord to the database
    def submit_landlord():
        landlord_name = landlord_name_entry.get()
        gender = gender_entry.get().upper()  # Convert to uppercase to allow for case-insensitive input
        age = age_entry.get()

        # Validate the input
        if not landlord_name or not gender or not age:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate gender input
        if gender not in ['M', 'F', 'O']:
            messagebox.showerror("Error", "Gender must be 'M', 'F', or 'O'.")
            return

        try:
            # Convert the age to an integer
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        # Insert the landlord into the database
        cursor.execute('INSERT INTO landlords (landlord_name, gender, age) VALUES (?, ?, ?)',
                       (landlord_name, gender, age))
        conn.commit()

        # Close the add landlord window
        add_landlord_window.destroy()

    # Create a submit button
    submit_button = ttk.Button(add_landlord_window, text="Submit", command=submit_landlord)
    submit_button.pack(pady=(10, 0))

def add_tenant():
    # Create a new window for adding a tenant
    add_tenant_window = tk.Toplevel(root)
    add_tenant_window.title("Add Tenant")

    # Create entry fields for tenant name, gender, and age
    tenant_name_label = ttk.Label(add_tenant_window, text="Tenant Name:")
    tenant_name_label.pack(pady=(10, 5))
    tenant_name_entry = ttk.Entry(add_tenant_window)
    tenant_name_entry.pack(pady=(0, 10))

    gender_label = ttk.Label(add_tenant_window, text="Gender (M/F/O):")
    gender_label.pack(pady=(0, 5))
    gender_entry = ttk.Entry(add_tenant_window)
    gender_entry.pack(pady=(0, 10))

    age_label = ttk.Label(add_tenant_window, text="Age:")
    age_label.pack(pady=(0, 5))
    age_entry = ttk.Entry(add_tenant_window)
    age_entry.pack(pady=(0, 10))

    # Function to add the tenant to the database
    def submit_tenant():
        tenant_name = tenant_name_entry.get()
        gender = gender_entry.get().upper()  # Convert to uppercase to allow for case-insensitive input
        age = age_entry.get()

        # Validate the input
        if not tenant_name or not gender or not age:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate gender input
        if gender not in ['M', 'F', 'O']:
            messagebox.showerror("Error", "Gender must be 'M', 'F', or 'O'.")
            return

        try:
            # Convert the age to an integer
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        # Insert the tenant into the database
        cursor.execute('INSERT INTO tenants (tenant_name, gender, age) VALUES (?, ?, ?)',
                       (tenant_name, gender, age))
        conn.commit()

        # Close the add tenant window
        add_tenant_window.destroy()

    # Create a submit button
    submit_button = ttk.Button(add_tenant_window, text="Submit", command=submit_tenant)
    submit_button.pack(pady=(10, 0))


def show_welcome_screen(username):
    # Clear the login screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create welcome screen
    welcome_label = tk.Label(root, text=f"Welcome, {username.capitalize()}!", font=("Helvetica", 24), bg='#3652AD')
    welcome_label.pack(pady=20)

    # Create a frame for the buttons
    button_frame = tk.Frame(root, bg='#3652AD')
    button_frame.pack(pady=(5, 20))  # Add vertical padding

    # Create the "View Properties" button
    view_properties_button = ttk.Button(button_frame, text="View Properties", command=show_properties_screen)
    view_properties_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    # Create the "View Landlords" button
    view_landlords_button = ttk.Button(button_frame, text="View Landlords", command=show_landlords_screen)
    view_landlords_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    # Create the "View Tenants" button
    view_tenants_button = ttk.Button(button_frame, text="View Tenants", command=show_tenants_screen)
    view_tenants_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    # Create the logout button
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)


def show_properties_screen():
    # Clear the properties screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for the properties screen
    properties_label = tk.Label(root, text="Properties:", font=("Helvetica", 24), bg='#3652AD')
    properties_label.pack(pady=20)

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

    # Fetch properties from the database
    cursor.execute('SELECT property_name, landlord_name, next_available_date FROM properties')
    properties = cursor.fetchall()

    # Display properties on the screen
    for i, prop in enumerate(properties):
        property_name, landlord_name, next_available_date = prop

        try:
            # Convert the next_available_date string to a datetime object
            next_available_date = datetime.strptime(next_available_date.split(' ')[0], "%Y-%m-%d")
            # Format the next_available_date to be more readable
            formatted_date = next_available_date.strftime("%B %d, %Y")
        except ValueError:
            # Handle the case where the date format is incorrect
            formatted_date = "Invalid Date Format"

        # Create a formatted string for the property details
        property_details = f"Property Name: {property_name}\nLandlord Name: {landlord_name}\nNext Available Date: {formatted_date}"

        # Create a label for the text block
        text_label = tk.Label(content_inside_canvas, text=property_details, font=("Helvetica", 14), bg='#3652AD', wraplength=400, pady=5)
        text_label.grid(row=i, column=1, sticky='w')  # Align to the left and wrap the text

    # Create the back to welcome screen button
    back_button = ttk.Button(root, text="Home", command=lambda: show_welcome_screen(username))
    back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-100, y=10)

    # Create the logout button after packing the property list
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    # Function to update the scrollregion of the canvas
    def on_content_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    # Bind the configure event to the content frame
    content_inside_canvas.bind('<Configure>', on_content_configure)

def show_landlords_screen():
    # Clear the properties screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for the properties screen
    properties_label = tk.Label(root, text="Landlords:", font=("Helvetica", 24), bg='#3652AD')
    properties_label.pack(pady=20)

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

    # Fetch landlords from the database
    cursor.execute('SELECT landlord_name, gender, age FROM landlords')
    landlords = cursor.fetchall()

    # Display landlords on the screen
    for i, landlord in enumerate(landlords):
        landlord_name, gender, age = landlord

        # Create a formatted string for the landlord details
        landlord_details = f"Name: {landlord_name}\nGender: {gender}\nAge: {age}"

        # Create a label for the text block
        text_label = tk.Label(content_inside_canvas, text=landlord_details, font=("Helvetica", 14), bg='#3652AD', wraplength=400)
        text_label.pack(pady=(0, 20))  # Align to the top and wrap the text

    # Create the back to welcome screen button
    back_button = ttk.Button(root, text="Home", command=lambda: show_welcome_screen(username))
    back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-100, y=10)

    # Create the logout button after packing the property list
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    # Function to update the scrollregion of the canvas
    def on_content_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    # Bind the configure event to the content frame
    content_inside_canvas.bind('<Configure>', on_content_configure)


def show_tenants_screen():
    # Clear the tenants screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for the tenants screen
    tenants_label = tk.Label(root, text="Tenants:", font=("Helvetica", 24), bg='#3652AD')
    tenants_label.pack(pady=20)

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

    # Fetch tenants from the database
    cursor.execute('SELECT tenant_name, gender, age FROM tenants')
    tenants = cursor.fetchall()

    # Display tenants on the screen
    for i, tenant in enumerate(tenants):
        tenant_name, gender, age = tenant

        # Create a formatted string for the tenant details
        tenant_details = f"Name: {tenant_name}\nGender: {gender}\nAge: {age}"

        # Create a label for the text block
        text_label = tk.Label(content_inside_canvas, text=tenant_details, font=("Helvetica", 14), bg='#3652AD', wraplength=400)
        text_label.pack(pady=(0, 20))  # Align to the top and wrap the text

    # Create the back to welcome screen button
    back_button = ttk.Button(root, text="Home", command=lambda: show_welcome_screen(username))
    back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-100, y=10)

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