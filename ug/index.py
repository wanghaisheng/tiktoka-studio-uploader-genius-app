import tkinter as tk
from tkinter import messagebox
import logging
import bcrypt  # Import the bcrypt library
from src.database import register_user,login_user,dbsession_pro
from main import start
# Dummy user data (replace with a database in a real application)
user_data = {}
# Logging configuration
logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')        

# Add the handler to logger

logger = logging.getLogger()         
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password(username, password):
    # Check if the username exists and verify the password
    if username in user_data and bcrypt.checkpw(password.encode(), user_data[username]):
        return True
    return False

def login():
    username = username_entry.get()
    password = password_entry.get()

    if verify_password(username, password):
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        start('en',root)

        # root.protocol('WM_DELETE_WINDOW', withdraw_window)
    
        root.mainloop()

    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def signup():
    username = username_entry.get()
    password = password_entry.get()

    if username in user_data:
        messagebox.showerror("Sign-up Failed", "Username already exists")
    else:
        hashed_password = hash_password(password)
        user_data[username] = hashed_password
        messagebox.showinfo("Sign-up Successful", "Account created successfully")

        # Register a user
        register_user(dbsession_pro, "john_doe", "password123", logger)

        # Login
        # login_user(session, "john_doe", "password123", logger)        

# Create the main application window
root = tk.Tk()
root.title("Login and Sign-up")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
global login_frame
login_frame = tk.Frame(root)
login_frame.grid(row=0,column=0,sticky="nsew")
# Username and password labels and entry widgets
username_label = tk.Label(login_frame, text="Username:")
username_entry = tk.Entry(login_frame)
password_label = tk.Label(login_frame, text="Password:")
password_entry = tk.Entry(login_frame, show="*")

# Login and Sign-up buttons
login_button = tk.Button(login_frame, text="Login", command=login)
signup_button = tk.Button(login_frame, text="Sign-up", command=signup)

# Place widgets using grid


username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry.grid(row=0, column=1, padx=10, pady=5)
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry.grid(row=1, column=1, padx=10, pady=5)
login_button.grid(row=2, column=0, columnspan=2, pady=10)
signup_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()
