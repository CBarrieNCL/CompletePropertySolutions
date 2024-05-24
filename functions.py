# from PIL import Image, ImageTk
# import tkinter as tk
#
#
# def toggle_image(root):
#     show_image_button = root.show_image_button
#     if show_image_button.image_visible:
#         # Hide the image by destroying any Label widgets with an image
#         for widget in root.winfo_children():
#             if isinstance(widget, tk.Label) and widget.cget('image') is not None:
#                 widget.destroy()
#         show_image_button.config(text="Show Image")
#     else:
#         # Show the image
#         image = Image.open("test.png")  # Replace with the path to your image
#         photo = ImageTk.PhotoImage(image)
#         image_label = tk.Label(root, image=photo)
#         image_label.image = photo  # Keep a reference to avoid garbage collection
#         image_label.pack(pady=20)
#         show_image_button.config(text="Hide Image")  # Change button text to "Hide Image"
#     show_image_button.image_visible = not show_image_button.image_visible
