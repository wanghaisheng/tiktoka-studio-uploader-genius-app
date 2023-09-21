import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Resizable Frames with Notebook and Log Console")

    # Create a PanedWindow widget (vertical)
    paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
    paned_window.pack(expand=True, fill="both")

    # Create the frame for the notebook
    frame1 = ttk.Frame(paned_window)
    paned_window.add(frame1)

    # Create the frame for the log console with a custom style
    custom_style = ttk.Style()
    custom_style.configure("Log.TFrame", background="blue")
    frame2 = ttk.Frame(paned_window, style="Log.TFrame")
    paned_window.add(frame2)

    # Set the initial size of the notebook frame (4/5 of total height)
    paned_window.paneconfig(frame2, minsize=0.6)  # Adjust minsize as needed

    # Add a ttk.Notebook with 4 tabs to the notebook frame
    notebook = ttk.Notebook(frame1)
    notebook.grid(row=0, column=0, sticky="nsew")
    frame1.grid_rowconfigure(0, weight=1)
    frame1.grid_columnconfigure(0, weight=1)

    # Create four tabs (pages) for the notebook
    for i in range(1, 5):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=f"Tab {i}")

    # Create a log console (ScrolledText) in the log console frame

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)


    
    log_console = ScrolledText(frame2, wrap=tk.WORD, width=40, height=2)
    log_console.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    # Function to log a message
    def log_message(message):
        log_console.insert(tk.END, message + "\n")
        log_console.see(tk.END)  # Scroll to the end

    # Example: Log a message
    log_message("This is a log message.")

    # Start the tkinter main loop
    root.mainloop()

# Create the GUI
create_gui()
