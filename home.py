import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, VERTICAL
from PIL import Image, ImageTk
import sqlite3
from hashlib import sha256
from datetime import datetime

# Database setup
conn = sqlite3.connect('cps.db')
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
cursor.execute('''
CREATE TABLE IF NOT EXISTS tenancy_mapping (
    tennancy_mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    tenant_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS service_mapping (
    service_mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    last_serviced_date TEXT,
    next_service_date TEXT,
    FOREIGN KEY (service_id) REFERENCES services(service_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
)
''')
# Function to clear all data
def clear_data():
    clear_data_sql = """
        DELETE FROM properties;
        DELETE FROM landlords;
        DELETE FROM tenants;
        DELETE FROM tenancy_mapping;
        DELETE FROM services;
        DELETE FROM service_mapping;
        """
    cursor.executescript(clear_data_sql)
    conn.commit()
    messagebox.showinfo("Success", "All data has been cleared successfully.")

# Function to populate reference data
def populate_reference_data():
    ref_data_sql = """
        INSERT INTO properties (property_id, property_name, landlord_name, next_available_date) VALUES (1, 'The Grand Old Mansion', 'Mr. Rich', '2023-01-01');
        INSERT INTO properties (property_id, property_name, landlord_name, next_available_date) VALUES (2, 'Spacious Townhouse', 'Mrs. Gentle', '2023-02-01');
        INSERT INTO properties (property_id, property_name, landlord_name, next_available_date) VALUES (3, 'Cozy Cottage', 'Mr. Tall', '2023-03-01');

        INSERT INTO landlords (landlord_id, landlord_name, gender, age) VALUES (1, 'Mr. Rich', 'Male', 50);
        INSERT INTO landlords (landlord_id, landlord_name, gender, age) VALUES (2, 'Mrs. Gentle', 'Female', 45);
        INSERT INTO landlords (landlord_id, landlord_name, gender, age) VALUES (3, 'Mr. Tall', 'Male', 60);

        INSERT INTO tenants (tenant_id, tenant_name, gender, age) VALUES (1, 'Dr. Drew', 'Female', 30);
        INSERT INTO tenants (tenant_id, tenant_name, gender, age) VALUES (2, 'Rev. Pettifer', 'Male', 25);
        INSERT INTO tenants (tenant_id, tenant_name, gender, age) VALUES (3, 'Sir Humble', 'Male', 35);

        INSERT INTO tenancy_mapping (tennancy_mapping_id, property_id, tenant_id, start_date, end_date) VALUES (1, 1, 1, '2022-01-01 00:00:00', '2023-12-31 00:00:00');
        INSERT INTO tenancy_mapping (tennancy_mapping_id, property_id, tenant_id, start_date, end_date) VALUES (2, 2, 2, '2022-02-01 00:00:00', '2023-11-31 00:00:00');
        INSERT INTO tenancy_mapping (tennancy_mapping_id, property_id, tenant_id, start_date, end_date) VALUES (3, 3, 3, '2022-03-01 00:00:00', '2023-10-31 00:00:00');

        INSERT INTO services (service_id, service_name) VALUES (1, 'Heating Inspection');
        INSERT INTO services (service_id, service_name) VALUES (2, 'Boiler Service');
        INSERT INTO services (service_id, service_name) VALUES (3, 'Electircal Inspection');

        INSERT INTO service_mapping (service_mapping_id, service_id, property_id, last_serviced_date, next_service_date) VALUES (1, 1, 1, '2022-01-01 00:00:00', '2022-07-01 00:00:00');
        INSERT INTO service_mapping (service_mapping_id, service_id, property_id, last_serviced_date, next_service_date) VALUES (2, 2, 2, '2022-02-01 00:00:00', '2022-08-01 00:00:00');
        INSERT INTO service_mapping (service_mapping_id, service_id, property_id, last_serviced_date, next_service_date) VALUES (3, 3, 3, '2022-03-01 00:00:00', '2022-09-01 00:00:00');
        """
    cursor.executescript(ref_data_sql)
    conn.commit()
    messagebox.showinfo("Success", "Reference data has been populated successfully.")

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def login():
    global username, password
    username = username_entry.get()
    password = password_entry.get()

    # Check if the user is trying to log in as the admin
    if username == "admin" and password == "admin":
        # Clear the login screen
        for widget in root.winfo_children():
            widget.destroy()

        # Show the admin screen
        show_admin_screen()
        return

    # Check if either field is empty or contains only whitespace
    if not username or not password or ' ' in username or ' ' in password:
        messagebox.showerror("Error", "Username and password cannot be empty or contain whitespace.")
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
    admin_label = tk.Label(root, text="Admin Management Screen", font=("Helvetica", 24), bg='#3652AD')
    admin_label.pack(pady=20)

    # Add some sample text
    sample_text = "This is the admin screen, use this to view and add records not available to standard users"
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

    # Create a button to display tenancy records
    display_tenants_button = ttk.Button(root, text="Display Tenancy Records", command=display_tenancy_records)
    display_tenants_button.pack(pady=(10, 0))

    # Create a button to display service records
    display_services_button = ttk.Button(root, text="Display Service Records", command=display_service_records)
    display_services_button.pack(pady=(10, 0))

    # Create a button to display service mapping records
    display_services_button = ttk.Button(root, text="Display Service Mapping Records", command=display_service_mapping_records)
    display_services_button.pack(pady=(10, 0))

    # Create a button to add a new property
    add_property_button = ttk.Button(root, text="Add Property", command=add_property)
    add_property_button.pack(pady=(10, 0))

    # Create a button to add a new landlord
    add_landlord_button = ttk.Button(root, text="Add Landlord", command=add_landlord)
    add_landlord_button.pack(pady=(10, 0))

    # Create a button to add a new tenant
    add_tenant_button = ttk.Button(root, text="Add Tenant", command=add_tenant)
    add_tenant_button.pack(pady=(10, 0))

    # Create a button to add a new tenant
    add_service_button = ttk.Button(root, text="Add Sevice", command=add_service)
    add_service_button.pack(pady=(10, 0))

    # Create buttons to populate reference data
    populate_data_button = ttk.Button(root, text="Populate Reference Data", command=populate_reference_data)
    populate_data_button.pack(pady=(10, 0))

    # Create buttons to clear data
    clear_data_button = ttk.Button(root, text="Clear Data", command=clear_data)
    clear_data_button.pack(pady=(10, 0))


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

def display_service_records():
    # Fetch all service records from the database
    cursor.execute('SELECT * FROM services')
    services = cursor.fetchall()

    # Create a new window to display the service records
    display_services_window = tk.Toplevel(root)
    display_services_window.title("Service Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(display_services_window, columns=("ID", "Service Name"), show="headings")
    treeview.pack(expand=True, fill='both')

    # Define the columns
    treeview.heading("ID", text="ID")
    treeview.heading("Service Name", text="Service Name")

    # Insert the records into the treeview
    for service in services:
        treeview.insert("", "end", values=service)

    # Function to close the records window
    def close_display_services_window():
        display_services_window.destroy()

    # Add a close button to the records window
    close_button = ttk.Button(display_services_window, text="Close", command=close_display_services_window)
    close_button.pack(pady=(10, 0))

def display_service_mapping_records():
    # Fetch all service mapping records from the database
    cursor.execute('SELECT * FROM service_mapping')
    service_mappings = cursor.fetchall()

    # Create a new window to display the service mapping records
    display_service_mappings_window = tk.Toplevel(root)
    display_service_mappings_window.title("Service Mapping Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(display_service_mappings_window, columns=("ID", "Service ID", "Property ID", "Last Serviced Date", "Next Service Date"), show="headings")
    treeview.pack(expand=True, fill='both')

    # Define the columns
    treeview.heading("ID", text="ID")
    treeview.heading("Service ID", text="Service ID")
    treeview.heading("Property ID", text="Property ID")
    treeview.heading("Last Serviced Date", text="Last Serviced Date")
    treeview.heading("Next Service Date", text="Next Service Date")

    # Insert the records into the treeview
    for service_mapping in service_mappings:
        treeview.insert("", "end", values=service_mapping)

    # Function to close the records window
    def close_display_service_mappings_window():
        display_service_mappings_window.destroy()

    # Add a close button to the records window
    close_button = ttk.Button(display_service_mappings_window, text="Close", command=close_display_service_mappings_window)
    close_button.pack(pady=(10, 0))

def display_tenancy_records():
    # Fetch all tenancy records from the database
    cursor.execute('SELECT * FROM tenancy_mapping')
    tenancies = cursor.fetchall()

    # Create a new window to display the tenancy records
    display_tenancy_window = tk.Toplevel(root)
    display_tenancy_window.title("Tenancy Records")

    # Create a treeview to display the records
    treeview = ttk.Treeview(display_tenancy_window, columns=("ID", "Property ID", "Tenant ID", "Start Date", "End Date"), show="headings")
    treeview.pack(expand=True, fill='both')

    # Define the columns
    treeview.heading("ID", text="ID")
    treeview.heading("Property ID", text="Service ID")
    treeview.heading("Tenant ID", text="Property ID")
    treeview.heading("Start Date", text="Last Serviced Date")
    treeview.heading("End Date", text="Next Service Date")

    # Insert the records into the treeview
    for tenancy in tenancies:
        treeview.insert("", "end", values=tenancy)

    # Function to close the records window
    def close_display_tenancy_window():
        display_tenancy_window.destroy()

    # Add a close button to the records window
    close_button = ttk.Button(display_tenancy_window, text="Close", command=close_display_tenancy_window)
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
        next_available_date = next_available_date_entry.get()

        # Validate the input
        if not property_name or not landlord_name or not next_available_date:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            # Convert the next_available_date string to a datetime object
            next_available_date = datetime.strptime(next_available_date, "%Y-%m-%d")
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

def add_service():
    # Create a new window for adding a service
    add_service_window = tk.Toplevel(root)
    add_service_window.title("Add Service")

    # Create entry fields for service name
    service_name_label = ttk.Label(add_service_window, text="Service Name:")
    service_name_label.pack(pady=(10, 5))
    service_name_entry = ttk.Entry(add_service_window)
    service_name_entry.pack(pady=(0, 10))

    # Function to add the tenant to the database
    def submit_service():
        service_name = service_name_entry.get()

        # Validate the input
        if not service_name:
            messagebox.showerror("Error", "Service name field is required.")
            return

        # Insert the tenant into the database
        cursor.execute('INSERT INTO services (service_name) VALUES (?)',
                       (service_name,))
        conn.commit()

        # Close the add tenant window
        add_service_window.destroy()

    # Create a submit button
    submit_button = ttk.Button(add_service_window, text="Submit", command=submit_service)
    submit_button.pack(pady=(10, 0))


def show_welcome_screen(username):
    # Clear the login screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create welcome screen
    welcome_label = tk.Label(root, text=f"Welcome, {username}!", font=("Helvetica", 24), bg='#3652AD')
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

    # Create a button to view tenancies
    view_tenancies_button = ttk.Button(button_frame, text="View Tenancies", command=show_tenancies_screen)
    view_tenancies_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    # Create a button to add a new tenancy
    add_tenancy_button = ttk.Button(button_frame, text="Add Tenancy", command=add_tenancy)
    add_tenancy_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    # Add a button to view service mappings
    view_service_mappings_button = ttk.Button(button_frame, text="View Service Mappings", command=show_service_mappings_screen)
    view_service_mappings_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    # Add the add_service button to the admin screen
    add_service_mapping_button = ttk.Button(button_frame, text="Add Service Mapping", command=add_service_mapping)
    add_service_mapping_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    if username == 'admin':
        # Create the back to admin screen button
        back_button = ttk.Button(root, text="Admin", command=lambda: show_admin_screen())
        back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-100, y=10)

    # Create the logout button
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)


def show_properties_screen():
    # Clear the properties screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a list to hold the selected properties for comparison
    selected_properties = []

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

    # Function to handle the comparison button press
    def compare_properties(property_details):
        nonlocal selected_properties

        # Add the property to the list of selected properties
        selected_properties.append(property_details)

        # If two properties are selected, show the comparison screen
        if len(selected_properties) == 2:
            show_comparison_screen(selected_properties)
            # Reset the list of selected properties
            selected_properties = []


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

        # Create a button to compare the property
        compare_button = ttk.Button(content_inside_canvas, text="Compare", command=lambda p=property_details: compare_properties(p))
        compare_button.grid(row=i, column=2, sticky='w')  # Align to the right


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

# Function to show the comparison screen
def show_comparison_screen(properties):
    # Clear the comparison screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for the comparison screen
    comparison_label = tk.Label(root, text="Comparison:", font=("Helvetica", 24), bg='#3652AD')
    comparison_label.pack(pady=20)

    # Create a frame for the property details
    content_frame = tk.Frame(root, bg='#3652AD')
    content_frame.pack(expand=True, fill='both')

    # Display the selected properties side by side
    for i, prop in enumerate(properties):
        # Create a label for the text block
        text_label = tk.Label(content_frame, text=prop, font=("Helvetica", 14), bg='#3652AD', wraplength=400, pady=5)
        text_label.grid(row=3, column=i, sticky='nsew')  # Two columns, properties show in order of selection

        content_frame.grid_columnconfigure(i, weight=1)


    # Create the back to properties screen button
    back_button = ttk.Button(root, text="Back to Properties", command=show_properties_screen)
    back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-190, y=10)

    # Create the back to welcome screen button
    back_button = ttk.Button(root, text="Home", command=lambda: show_welcome_screen(username))
    back_button.place(relx=1.0, rely=0.0, anchor='ne', x=-100, y=10)

    # Create the logout button after packing the property list
    logout_button = ttk.Button(root, text="Logout", command=logout)
    logout_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)


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


def show_tenancies_screen():
    # Clear the tenants screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for the tenants screen
    tenants_label = tk.Label(root, text="Tenancies:", font=("Helvetica", 24), bg='#3652AD')
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

    # Fetch tenancy records from the database
    cursor.execute('SELECT property_id, tenant_id, start_date, end_date FROM tenancy_mapping')
    tenancies = cursor.fetchall()

    # Display tenants on the screen
    for i, tenancy in enumerate(tenancies):
        property_id, tenant_id, start_date, end_date = tenancy

        try:
            # Convert the start_date string to a datetime object
            start_date = datetime.strptime(start_date.split(' ')[0], "%Y-%m-%d")
            end_date = datetime.strptime(end_date.split(' ')[0], "%Y-%m-%d")
        # Format the start_date to be more readable
            formatted_start_date = start_date.strftime("%B %d, %Y")
            formatted_end_date = end_date.strftime("%B %d, %Y")
        except ValueError:
            # Handle the case where the date format is incorrect
            formatted_date = "Invalid Date Format"

        # Create a formatted string for the tenancy details
        tenancy_details = f"Property Id: {property_id}\nTenant ID: {tenant_id}\nStart Date: {formatted_start_date}\nEnd Date: {formatted_end_date}"

        # Create a label for the text block
        text_label = tk.Label(content_inside_canvas, text=tenancy_details, font=("Helvetica", 14), bg='#3652AD', wraplength=400)
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

# Function to display service mappings
def show_service_mappings_screen():
    # Clear the service mappings screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a label for the service mappings screen
    service_mappings_label = tk.Label(root, text="Service Mappings:", font=("Helvetica", 24), bg='#3652AD')
    service_mappings_label.pack(pady=20)

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

    # Fetch service mappings from the database
    cursor.execute('''
        SELECT sm.service_mapping_id, s.service_name, p.property_name, sm.last_serviced_date, sm.next_service_date
        FROM service_mapping sm
        JOIN services s ON sm.service_id = s.service_id
        JOIN properties p ON sm.property_id = p.property_id
    ''')
    service_mappings = cursor.fetchall()

    # Display service mappings on the screen
    for i, mapping in enumerate(service_mappings):
        mapping_id, service_name, property_name, last_serviced_date, next_service_date = mapping

        try:
            # Convert the start_date string to a datetime object
            last_serviced_date = datetime.strptime(last_serviced_date.split(' ')[0], "%Y-%m-%d")
            next_service_date = datetime.strptime(next_service_date.split(' ')[0], "%Y-%m-%d")
            # Format the start_date to be more readable
            formatted_last_serviced_date = last_serviced_date.strftime("%B %d, %Y")
            formatted_next_service_date = next_service_date.strftime("%B %d, %Y")
        except ValueError:
            # Handle the case where the date format is incorrect
            formatted_date = "Invalid Date Format"

        # Create a formatted string for the service mapping details
        mapping_details = f"Service: {service_name}\nProperty: {property_name}\nLast Serviced: {formatted_last_serviced_date}\nNext Service: {formatted_next_service_date}"

        # Create a label for the text block
        text_label = tk.Label(content_inside_canvas, text=mapping_details, font=("Helvetica", 14), bg='#3652AD', wraplength=400)
        text_label.pack(pady=(0, 20))  # Align to the top and wrap the text

        # Create an edit button for each mapping
        edit_button = ttk.Button(content_inside_canvas, text="Edit", command=lambda m_id=mapping_id: edit_service_mapping(m_id))
        edit_button.pack(pady=(0, 20))  # Align to the top and wrap the text

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


def add_tenancy():
    # Create a new window for adding a tenancy
    add_tenancy_window = tk.Toplevel(root)
    add_tenancy_window.title("Add Tenancy")

    # Fetch property IDs from the database
    cursor.execute('SELECT property_id FROM properties')
    property_ids = cursor.fetchall()

    # Create a dropdown for property IDs
    property_id_label = ttk.Label(add_tenancy_window, text="Property ID:")
    property_id_label.pack(pady=(10, 5))
    property_id_dropdown = ttk.Combobox(add_tenancy_window, values=[str(row[0]) for row in property_ids], state='readonly')
    property_id_dropdown.pack(pady=(0, 10))

    # Fetch tenant IDs from the database
    cursor.execute('SELECT tenant_id FROM tenants')
    tenant_ids = cursor.fetchall()

    # Create a dropdown for tenant IDs
    tenant_id_label = ttk.Label(add_tenancy_window, text="Tenant ID:")
    tenant_id_label.pack(pady=(0, 5))
    tenant_id_dropdown = ttk.Combobox(add_tenancy_window, values=[str(row[0]) for row in tenant_ids], state='readonly')
    tenant_id_dropdown.pack(pady=(0, 10))

    # Create entry fields for start date and end date
    start_date_label = ttk.Label(add_tenancy_window, text="Start Date (YYYY-MM-DD):")
    start_date_label.pack(pady=(0, 5))
    start_date_entry = ttk.Entry(add_tenancy_window)
    start_date_entry.pack(pady=(0, 10))

    end_date_label = ttk.Label(add_tenancy_window, text="End Date (YYYY-MM-DD):")
    end_date_label.pack(pady=(0, 5))
    end_date_entry = ttk.Entry(add_tenancy_window)
    end_date_entry.pack(pady=(0, 10))

    # Function to add the tenancy to the database
    def submit_tenancy():
        property_id = property_id_dropdown.get()
        tenant_id = tenant_id_dropdown.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # Validate the input
        if not property_id or not tenant_id or not start_date:
            messagebox.showerror("Error", "Property ID, Tenant ID, and Start Date are required.")
            return

        try:
            # Convert the start and end dates to date objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        except ValueError:
            messagebox.showerror("Error", "Dates must be in the format YYYY-MM-DD.")
            return

        # Insert the tenancy into the database
        cursor.execute('''
            INSERT INTO tenancy_mapping (property_id, tenant_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
        ''', (property_id, tenant_id, start_date, end_date))
        conn.commit()

        # Close the add tenancy window
        add_tenancy_window.destroy()

    # Create a submit button
    submit_button = ttk.Button(add_tenancy_window, text="Submit", command=submit_tenancy)
    submit_button.pack(pady=(10, 0))

def add_service_mapping():
    # Create a new window for adding a service
    add_service_window = tk.Toplevel(root)
    add_service_window.title("Add Service")

    # Fetch service names from the database
    cursor.execute('SELECT service_name FROM services')
    service_names = cursor.fetchall()

    # Create a dropdown for service names
    service_name_label = ttk.Label(add_service_window, text="Service Name:")
    service_name_label.pack(pady=(10, 5))
    service_name_dropdown = ttk.Combobox(add_service_window, values=[row[0] for row in service_names], state='readonly')
    service_name_dropdown.pack(pady=(0, 10))

    # Fetch property IDs from the database
    cursor.execute('SELECT property_id FROM properties')
    property_ids = cursor.fetchall()

    # Create a dropdown for property IDs
    property_id_label = ttk.Label(add_service_window, text="Property ID:")
    property_id_label.pack(pady=(0, 5))
    property_id_dropdown = ttk.Combobox(add_service_window, values=[str(row[0]) for row in property_ids], state='readonly')
    property_id_dropdown.pack(pady=(0, 10))

    # Create entry fields for last serviced date and next service date
    last_serviced_date_label = ttk.Label(add_service_window, text="Last Serviced Date (YYYY-MM-DD):")
    last_serviced_date_label.pack(pady=(0, 5))
    last_serviced_date_entry = ttk.Entry(add_service_window)
    last_serviced_date_entry.pack(pady=(0, 10))

    next_service_date_label = ttk.Label(add_service_window, text="Next Service Date (YYYY-MM-DD):")
    next_service_date_label.pack(pady=(0, 5))
    next_service_date_entry = ttk.Entry(add_service_window)
    next_service_date_entry.pack(pady=(0, 10))

    # Function to add the service to the database
    def submit_service():
        service_name = service_name_dropdown.get()
        property_id = property_id_dropdown.get()
        last_serviced_date = last_serviced_date_entry.get()
        next_service_date = next_service_date_entry.get()

        # Validate the input
        if not service_name or not property_id or not last_serviced_date or not next_service_date:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            # Convert the last_serviced_date and next_service_date strings to date objects
            last_serviced_date = datetime.strptime(last_serviced_date, "%Y-%m-%d")
            next_service_date = datetime.strptime(next_service_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Dates must be in the format YYYY-MM-DD.")
            return

        # Insert the service into the database
        cursor.execute('''
            INSERT INTO service_mapping (service_id, property_id, last_serviced_date, next_service_date)
            SELECT s.service_id, ?, ?, ?
            FROM services s
            WHERE s.service_name = ?
        ''', (property_id, last_serviced_date, next_service_date, service_name))
        conn.commit()

        # Close the add service window
        add_service_window.destroy()

    # Create a submit button
    submit_button = ttk.Button(add_service_window, text="Submit", command=submit_service)
    submit_button.pack(pady=(10, 0))


def edit_service_mapping(mapping_id):
    # Create a new window for editing the service mapping
    edit_service_mapping_window = tk.Toplevel(root)
    edit_service_mapping_window.title("Edit Service Mapping")

    # Fetch the current service mapping details
    cursor.execute('''
        SELECT sm.service_id, sm.property_id, sm.last_serviced_date, sm.next_service_date, s.service_name, p.property_name
        FROM service_mapping sm 
        INNER JOIN services s ON sm.service_id = s.service_id
        INNER JOIN properties p ON sm.property_id == p.property_id
        WHERE sm.service_mapping_id = ?
    ''', (mapping_id,))
    current_mapping = cursor.fetchone()

    if not current_mapping:
        messagebox.showerror("Error", "Service mapping not found.")
        edit_service_mapping_window.destroy()
        return

    current_service_id, current_property_id, current_last_serviced_date, current_next_service_date, current_service_name, current_property_name = current_mapping

    # Fetch service names from the database
    cursor.execute('SELECT service_name FROM services')
    service_names = cursor.fetchall()

    # Create a dropdown for service names
    service_name_label = ttk.Label(edit_service_mapping_window, text="Service Name:")
    service_name_label.pack(pady=(10, 5))
    service_name_dropdown = ttk.Combobox(edit_service_mapping_window, values=[row[0] for row in service_names], state='readonly')
    service_name_dropdown.set(current_service_name)  # Set the current service name
    service_name_dropdown.pack(pady=(0, 10))

    # Fetch property IDs from the database
    cursor.execute('SELECT property_name FROM properties')
    property_names = cursor.fetchall()

    # Create a dropdown for property names
    property_name_label = ttk.Label(edit_service_mapping_window, text="Property:")
    property_name_label.pack(pady=(0, 5))
    property_name_dropdown = ttk.Combobox(edit_service_mapping_window, values=[str(row[0]) for row in property_names], state='readonly')
    property_name_dropdown.set(current_property_name)  # Set the current property name
    property_name_dropdown.pack(pady=(0, 10))

    # Create entry fields for last serviced date and next service date
    last_serviced_date_label = ttk.Label(edit_service_mapping_window, text="Last Serviced Date (YYYY-MM-DD):")
    last_serviced_date_label.pack(pady=(0, 5))
    last_serviced_date_entry = ttk.Entry(edit_service_mapping_window)
    last_serviced_date_entry.insert(0, current_last_serviced_date.split(' ')[0])  # Set the current last serviced date
    last_serviced_date_entry.pack(pady=(0, 10))

    next_service_date_label = ttk.Label(edit_service_mapping_window, text="Next Service Date (YYYY-MM-DD):")
    next_service_date_label.pack(pady=(0, 5))
    next_service_date_entry = ttk.Entry(edit_service_mapping_window)
    next_service_date_entry.insert(0, current_next_service_date.split(' ')[0])  # Set the current next service date
    next_service_date_entry.pack(pady=(0, 10))

    # Function to update the service mapping in the database
    def update_service_mapping():
        service_name = service_name_dropdown.get()
        property_name = property_name_dropdown.get()
        last_serviced_date = last_serviced_date_entry.get()
        next_service_date = next_service_date_entry.get()

        # Validate the input
        if not service_name or not property_name or not last_serviced_date or not next_service_date:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            # Convert the last_serviced_date and next_service_date strings to date objects
            last_serviced_date = datetime.strptime(last_serviced_date, "%Y-%m-%d")
            next_service_date = datetime.strptime(next_service_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Dates must be in the format YYYY-MM-DD.")
            return

        # Update the service mapping in the database
        cursor.execute('''
            UPDATE service_mapping
            SET service_id = (SELECT service_id FROM services WHERE service_name = ?),
                property_id = (SELECT property_id FROM properties WHERE property_name = ?),
                last_serviced_date = ?,
                next_service_date = ?
            WHERE service_mapping_id = ?
        ''', (service_name, property_name, last_serviced_date, next_service_date, mapping_id))
        conn.commit()  # Commit the transaction

        # Show a success message and close the window
        messagebox.showinfo("Success", "Service mapping updated successfully.")
        edit_service_mapping_window.destroy()

    # Add a button to save the changes
    save_button = ttk.Button(edit_service_mapping_window, text="Save Changes", command=update_service_mapping)
    save_button.pack(pady=(10, 10))

def logout():
    # Clear the welcome screen
    for widget in root.winfo_children():
        widget.destroy()

    # Show the login screen again
    create_login_screen()

def register():
    username = username_entry.get()
    password = password_entry.get()

    # Check if either field is empty or contains only whitespace
    if not username or not password or ' ' in username or ' ' in password:
        messagebox.showerror("Error", "Username and password cannot be empty or contain whitespace.")
        return
    elif username.lower() == 'admin':
        messagebox.showerror("Error", "Invalid Credentials")
        return
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
root.title("Complete Property Solutions")

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