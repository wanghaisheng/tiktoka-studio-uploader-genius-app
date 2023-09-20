import tkinter as tk

def resize_right_frame(event):
    # Get the new width of the root frame
    new_width = root.winfo_width()

    # Calculate the new width for the right frame
    right_frame_width = new_width - left_frame_width
    root.grid_columnconfigure(1, minsize=right_frame_width)

root = tk.Tk()
root.title("Resizable Frames")

# Create the left frame
left_frame = tk.Frame(root, bg="blue")
left_frame.grid(row=0, column=0, sticky="nsew")

# Create the right frame
right_frame = tk.Frame(root, bg="red")
right_frame.grid(row=0, column=1, sticky="nsew")

# Configure grid row and column weights
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)  # Right frame occupies twice the width

# Bind the window resize event to the resize_right_frame function
# root.bind("<Configure>", resize_right_frame)

# Get the initial width of the left frame
left_frame_width = left_frame.winfo_width()

root.mainloop()
