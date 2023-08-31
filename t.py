'''Example of how to use the place() method to create a GUI layout'''
from tkinter import *

root  =  Tk()  # create root window
root.title("Basic GUI Layout with Place")
root.geometry("900x550")  # Set the starting size of the window
root.maxsize(900,  600)  # width x height
root.config(bg="skyblue")

# Create left and right frames
left_frame  =  Frame(root,  width=250,  height=500,  bg='grey')
left_frame.place(x=10,  y=10,  relx=0.01,  rely=0.01)

right_frame  =  Frame(root,  width=600,  height=500,  bg='grey')
right_frame.place(x=270,  y=10,  relx=0.01,  rely=0.01)

# Create frames and labels in left_frame
Label(left_frame,  text="Original Image").place(relx=0.5,  rely=0.05,  anchor=N)

image  =  PhotoImage(file="./assets/images.png")
original_image  =  image.subsample(3,3)

Label(left_frame,  image=original_image,  bg='grey').place(rely=0.15,  relwidth=1)
Label(right_frame,  image=image,  bg='grey').place(y=10,  relwidth=1,  relheight=1)

tool_bar  =  Frame(left_frame,  width=115,  height=185,  bg='lightgrey')
tool_bar.place(x=5,  rely=0.5)

filter_bar  =  Frame(left_frame,  width=115,  height=185,  bg='lightgrey')
filter_bar.place(x=130,  rely=0.5)

def clicked():
    '''if button is clicked, display message'''
    print("Clicked.")

# Example labels that serve as placeholders for other widgets
Label(tool_bar,  text="Tools",  relief=RAISED).place(in_=tool_bar,  relx=0.5,  anchor=N)
Label(filter_bar,  text="Filters",  relief=RAISED).place(in_=filter_bar,  relx=0.5,  anchor=N)

# # For now, when the buttons are clicked, they only call the clicked() method. We will add functionality later.
# Button(tool_bar,  text="Select", command=clicked).place(in_=tool_bar,  relx=0.5,  rely=0.20,  anchor=CENTER)
# Button(tool_bar,  text="Crop",  command=clicked).place(in_=tool_bar,  relx=0.5,  rely=0.35,  anchor=CENTER)
# Button(tool_bar,  text="Rotate &amp; Flip",  command=clicked).place(in_=tool_bar,  relx=0.5,  rely=0.50,  anchor=CENTER)
# Button(tool_bar,  text="Resize",  command=clicked).place(in_=tool_bar,  relx=0.5,  rely=0.65,  anchor=CENTER)
# Button(filter_bar,  text="Black &amp; White",  command=clicked).place(in_=filter_bar,  relx=0.5,  rely=0.20,  anchor=CENTER)

root.mainloop()