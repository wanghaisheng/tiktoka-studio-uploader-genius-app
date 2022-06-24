from cProfile import label
from re import L
import tkinter as tk
from tkinter import BOTTOM, font
from turtle import bgcolor, width
from matplotlib.font_manager import FontProperties
import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import csv
from tkinter import mainloop, ttk
import customtkinter as ctk

def main():
    file_name = file_name_input()

    if file_name.endswith(".csv"):
        pass
    else:
        file_name = file_name + ".csv"

    #opening the file name entered by the user
    with open(file_name,"r") as data:
        data = csv.reader(data)

        #creating an empty list to store the data from the file
        file = []
        for _ in data:
            file.append(_)

    #creating a dataframe from the file
    df = pd.DataFrame(data = file[1:] , columns = file[0])
    df = df.astype({"SP" : float ,
                    "Total_PnL" : float ,
                    "sales" : float})

    #removing unwanted columnss
    del df["s_no"]

    #viewing the dataframe in another window
    df_viewer(df,file_name)
    confirmation()


    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    #creating buttons for all the columns that are floats
    top = ctk.CTk()
    top.geometry("500x400")

    frame_label = ctk.CTkFrame(top)
    frame_label.pack(padx = 10 , pady = 10)
    #the big frame
    label_top = ctk.CTkLabel(frame_label,
                    text = "Choose the axis of the graph you want to plot : ",
                    text_font = ("Garamond" , 15))
    label_top.pack(padx = 10, pady = 10)


    #X axis stuff

    framex = ctk.CTkFrame(top)
    framex.pack(padx = 10 , pady = 10)

    #Func for x axis input
    def input_x(text):
        text_entry_x.set(text)

    #widgets for x axis input
    text_entry_x = tk.StringVar()

    #frame

    label_x = ctk.CTkLabel(framex,
                        text = "X - Axis : ",
                        text_font=("Gramond" , 10))
    label_x.grid(column = 1 , row = 3 , padx = 10 , pady = (10,0))
    #entry box
    e_x = ctk.CTkEntry(framex,
                    textvariable= text_entry_x,
                    text_font=("Garamond" , 15))
    e_x.grid(column = 2 , row = 3  , padx = 10 , pady = (10,0) )

    #creating buttons for x axis

    button_x_sales = ctk.CTkButton(framex,
                                text = "Sales",
                                text_font=("Garamond",12),
                                command = lambda: input_x("sales"))

    button_x_sales.grid(column = 1, row = 6 , pady = 15 , padx = 10)

    button_x_sp = ctk.CTkButton(framex,
                            text = "SP",
                            text_font=("Garamond",12),
                            command = lambda: input_x("SP"))

    button_x_sp.grid(column = 2, row = 6,pady = 15 , padx = 10)

    button_x_pnl = ctk.CTkButton(framex,
                                text = "Total PnL",
                                text_font=("Garamond",12),
                                command = lambda: input_x("Total_PnL"))

    button_x_pnl.grid(column = 3, row = 6 , pady=15 , padx = 10)



    ##y axis stuff
    framey = ctk.CTkFrame(top)
    framey.pack(padx = 10, pady = 10)
    #func for y axis input
    def input_y(text):
        text_entry_y.set(text)

    #widgets for y axis input
    text_entry_y = tk.StringVar()

    #label
    label_y = ctk.CTkLabel(framey,
                        text = "Y - Axis : ",
                        text_font=("Gramond" , 10))
    label_y.grid(column = 1 , row = 3 , padx = 10 , pady = (10,0))

    #entry box
    e_y = ctk.CTkEntry(framey,
                    textvariable= text_entry_y,
                    text_font=("Garamond" , 15))
    e_y.grid(column = 2 , row = 3  , padx = 10 , pady = (10,0) )


    #creating buttons for y axis input
    button_y_sales = ctk.CTkButton(framey,
                                text = "Sales",
                                text_font=("Garamond",12),
                                command = lambda: input_y("sales"))

    button_y_sales.grid(column = 1, row = 6 , pady = 15 , padx = 10)

    button_y_sp = ctk.CTkButton(framey,
                            text = "SP",
                            text_font=("Garamond",12),
                            command = lambda: input_y("SP"))

    button_y_sp.grid(column = 2, row = 6,pady = 15 , padx = 10)

    button_y_pnl = ctk.CTkButton(framey,
                                text = "Total PnL",
                                text_font=("Garamond",12),
                                command = lambda: input_y("Total_PnL"))

    button_y_pnl.grid(column = 3, row = 6 , pady=15 , padx = 10)

    frame_plot = ctk.CTkFrame(top)
    frame_plot.pack(padx = 10 , pady = 10)
    #plot button
    plot_button = ctk.CTkButton(frame_plot,
                            text = "Plot",
                            text_font = ("Garamond",12),
                            command = lambda : plotter(df,text_entry_x.get(),text_entry_y.get()))
    plot_button.pack(padx = 10 , pady = 10)
    top.mainloop()

def button_plot(df,x,y,kind):
    try:
        df.plot(x = x,
                y = y,
                kind = kind)
        mp.show()
    except ValueError:
        top = ctk.CTk()
        top.geometry("500x200")

        frame = ctk.CTkFrame(top)
        frame.pack(padx = 10 , pady = 10)

        label = ctk.CTkLabel(frame,
                             text = "One of the input fields contains negative values.",
                             text_font = ("Garamond" , 15))
        label.pack(padx = 10 , pady = 10)
        
        label2 = ctk.CTkLabel(frame,
                             text = "Pie Chart does not support negative values.",
                             text_font = ("Garamond" , 15))
        label2.pack(padx = 10 , pady = 10)

        frame_buttons = ctk.CTkFrame(top)
        frame_buttons.pack(padx = 10 , pady = 10)

        buttonc = ctk.CTkButton(frame_buttons,
                                text = "Continue",
                                text_font=("Garamond Bold" , 12),
                                command = lambda:top.destroy())
        buttonc.grid(column = 0 , row = 1 , padx = 10 , pady = 10)
        
        buttonc = ctk.CTkButton(frame_buttons,
                                text = "Exit App",
                                text_font=("Garamond Bold" , 12),
                                command = lambda: quit())
        buttonc.grid(column = 1 , row = 1, padx = 10 , pady = 10)
        top.mainloop()

def plotter(df,x,y):
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    top = ctk.CTk()
    top.geometry("400x250")
    top.title("Graph Options")
    #the big frame
    framel = ctk.CTkFrame(top)
    framel.pack(padx = 10 , pady = 10)

    label = ctk.CTkLabel(framel,
                        text = "Choose the type of graph you want : ",
                        text_font= ("Garamond" , 15))
    label.pack(padx = 10 , pady = 10)

    #frame for buttons
    frame_button  = ctk.CTkFrame(top)
    frame_button.pack(padx = 10, pady = 10)

    button_bar = ctk.CTkButton(frame_button,
                            text = "Bar Graph",
                            text_font = ("Garamond Bold" ,  ),
                            height = 40,
                            command = lambda : button_plot(df,x,y,"bar"))
    button_bar.grid(column = 1,row = 1,padx = (15,0) ,  pady = (15,0))

    button_line = ctk.CTkButton(frame_button,
                            text = "Line Chart",
                            text_font = ("Garamond Bold" ,  ),
                            height = 40,
                            command = lambda :  button_plot(df,x,y,"line"))
    button_line.grid(column = 2,row = 1,padx = 15 ,  pady =(15,0))

    button_pie = ctk.CTkButton(frame_button,
                            text = "Pie Chart",
                            text_font = ("Garamond Bold" ,  ),
                            height = 40,
                            command = lambda :  button_plot(df,x,y,"pie"))
    button_pie.grid(column = 1,row = 2,padx = (15,0) ,  pady = 15)

    button_hist = ctk.CTkButton(frame_button,
                            text = "Histogram",
                            text_font = ("Garamond Bold" ,  ),
                            height = 40,
                            command = lambda :  button_plot(df,x,y,"hist"))
    button_hist.grid(column = 2, row = 2,padx = 15  ,  pady = 15)

    top.mainloop()
        
def df_viewer(df,file_name):
    
    #creating a window to view the dataframe
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")

    top = ctk.CTk()
    top.geometry("800x700")
    top.title("Data View")
    
    
    #frame for the data on upper half of window
    frame_big = ctk.CTkFrame(top)
    frame_big.pack(padx=10,pady = 10)

    #frame for label of data view
    frame_label = ctk.CTkFrame(frame_big)
    frame_label.pack(padx = 10 , pady = 10, anchor="sw")
    #creating the label
    file_name = file_name.split(".")
    label1 = ctk.CTkLabel (frame_label,
                        text = f"Data From {file_name[0]} : ",
                        text_font=("Garamond" , 18))
    label1.pack(anchor="w",padx = 5 , pady = 5)

    #frame for the treeview
    frame_tv = ctk.CTkFrame(frame_big)
    frame_tv.pack(padx=10,pady=(0,10))
    #creating a treeview
    tv = ttk.Treeview(frame_tv)
    tv.pack(padx=15,pady = (15,0))

    frame_scroll = ctk.CTkFrame(frame_tv)
    frame_scroll.pack(padx = 15 , pady = (0,15) , fill="x")
    #creating the scroll bars
    treescrollx = tk.Scrollbar(frame_scroll,  
                                orient="horizontal",
                                command = tv.xview)
    treescrollx.pack(pady = 0, padx = 0 , fill = "x")

    #entering the data into treeview from dataframe
    tv["columns"] = list(df.columns)
    tv["show"] = "headings"

    #getting column headings
    for _ in tv["columns"]:
        tv.heading(_,text = _)
    df_rows = df.to_numpy().tolist()
    #getting rows
    for _ in df_rows:
        tv.insert("","end" , values = _)


    #big frame for the lower half
    frame_big2 = ctk.CTkFrame(top)
    frame_big2.pack(padx = 10, pady = 0,anchor="n")

    #frame for lower label
    frame_label2 = ctk.CTkFrame(frame_big2)
    frame_label2.pack(padx = 10, pady = 10 , anchor = "sw")
    #label
    label2  = ctk.CTkLabel(frame_label2,
                        text = "Some statistical measure derived from the data : ",
                        text_font = ("Garamond" , 15))
    label2.pack(padx = 5, pady = 5)

    #frame for treeview
    frame_tv2 = ctk.CTkFrame(frame_big2)
    frame_tv2.pack(padx = 10 , pady = (0,10))
    #treeview
    tv1 = ttk.Treeview(frame_tv2)
    tv1.pack(padx=15,pady = (15,0))

    #frame for scrollbar
    frame_scroll2 = ctk.CTkFrame(frame_tv2)
    frame_scroll2.pack(padx = 15 , pady = (0,15) , fill="x")
    #scrollbar
    treescrollx1 = tk.Scrollbar(frame_scroll2,
                                orient="horizontal",
                                command = tv1.xview)
    treescrollx1.pack(pady = 0, padx = 0 , fill = "x")


    #getting another dataframe with statistical measures of our data
    desc = df.describe()
    names = ["Count","Mean", "Std" , "Percentiles - Min%", "25%" , "50%" , "75%" , "Max"]
    desc.insert(loc=0 , column="Measures", value=names)

    #entering the values into tv1
    tv1["columns"] = list(desc.columns)
    for _ in tv1["columns"]:
        tv1.heading(_,text = _)
    desc_rows = desc.to_numpy().tolist()
    for _ in desc_rows:
        tv1.insert("" , "end" , values = _)

    top.mainloop()

def confirmation():
    def declined():
        top.destroy()
        main()
        
        quit()

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    top = ctk.CTk()
    top.geometry("300x200")

    frame = ctk.CTkFrame(top)
    frame.pack(padx = 10 , pady = 10)

    label = ctk.CTkLabel(frame ,
                         text = "Is the data gathered correct?",
                         text_font = ("Garamond",15))
    label.pack(padx = 10,pady = 10)

    buttonc = ctk.CTkButton(frame,
                            text = "Confirm",
                            text_font = ("Garamond Bold" , 12),
                            command = top.destroy)
    buttonc.pack(padx = 10 , pady = 10)

    buttond = ctk.CTkButton(frame,
                            text = "Decline",
                            text_font = ("Garamond Bold" , 12),
                            command = declined)
    buttond.pack(padx = 10 , pady = 10)

    top.mainloop()

def file_name_input():
    
    def store_input():
        file_name.set(e_txt.get())
        top.destroy()
    #creating the top window
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")

    top = ctk.CTk()
    top.geometry("400x200")

    frame = ctk.CTkFrame(top)
    frame.pack(padx = 10, pady = 10)
    

    #top.configure(bg = "#5cdb95")
    top.title("Data analysis")
    #creating the heading of the program
    head_lbl = ctk.CTkLabel(master = frame,
                        text = "Data Analysis",
                        justify = tk.CENTER,
                        text_font=("Roboto Medium", -20),
                        width = 10)
    head_lbl.pack(pady = 13 , padx = 10)
    #asking the user to input the name of the file
    second_lbl = ctk.CTkLabel(frame,
                          text = "Enter the name of the file you want to access : ",
                          text_font=("Roboto Medium", -12),
                          justify = tk.CENTER)
    second_lbl.pack(pady = 5, padx = 10)
    #creating the input box
    e_txt = ctk.CTkEntry(frame,
                         placeholder_text = "File Name",
                         text_font = ("Roboto Medium" , 10),
                         width = 200)
    e_txt.pack(pady = 10 , padx = 10)
    #creating a variable to store the file name in
    file_name = tk.StringVar()
    #creating the button to store the name of the file
    
    file_name_button = ctk.CTkButton(master=frame,
                                 text = "Enter",
                                 text_font = ("Roboto Medium", 10),
                                 fg_color=("gray75", "gray30"),
                                 command = store_input)

    file_name_button.pack(pady = 10,padx = 10)

    top.mainloop()
    return file_name.get()

main()
