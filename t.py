import os
import tkinter as tk
import sys
# Assuming this is your root directory path
if sys.platform=='darwin':
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

iconfilename="assets/icon.ico"

# Icon file name
# iconfilename = "assets/images.png"

# Create the full path to the icon file
iconfile = os.path.join(ROOT_DIR, iconfilename)

# Create a Tkinter root window
root = tk.Tk()


# Set the icon for the window
root.iconbitmap(iconfile)

# Rest of your Tkinter code...

# Start the Tkinter event loop
root.mainloop()
