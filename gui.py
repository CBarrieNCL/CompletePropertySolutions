# gui.py
import tkinter as tk
from tkinter import ttk
from authentication import login, register

# Create a style for the buttons
style = ttk.Style()
style.configure('Custom.TButton', font=('Helvetica', 14), foreground='black', background='white', highlightbackground='black', highlightcolor='black', padding=0, relief='flat', highlightthickness=0)

# Create login screen
def create_login_screen(root):
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
    login_button = ttk.Button(button_frame, text="Login", command=lambda: login(username_entry, password_entry, root), style='Custom.TButton')
    login_button.pack(side='left', padx=(0, 10))  # Add horizontal padding

    register_button = ttk.Button(button_frame, text="Register", command=lambda: register(username_entry, password_entry, root), style='Custom.TButton')
    register_button.pack(side='left', padx=(10, 0))  # Add horizontal padding

# This guard ensures that the create_login_screen function is not called when the file is imported as a module
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Screen")
    root.configure(bg='#3652AD')
    create_login_screen(root)
    root.mainloop()