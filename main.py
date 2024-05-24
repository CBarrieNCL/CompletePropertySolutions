# main.py
import tkinter as tk
from gui import create_login_screen

def main():
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


    # Create login screen
    create_login_screen(root)

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()