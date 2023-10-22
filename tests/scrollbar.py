import tkinter as tk

LABEL_BG = 'light grey'
ROWS, COLS = 10, 8  # Size of grid.
ROWS_DISP = 3  # Number of rows to display.
COLS_DISP = 8  # Number of columns to display.


class HoverButton(tk.Button):
    """ Button that changes color to activebackground when mouse is over it. """

    def __init__(self, master, **kw):
        super().__init__(master=master, **kw)
        self.default_Background = self.cget('background')
        self.hover_Background = self.cget('activebackground')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.config(background=self.hover_Background)

    def on_leave(self, e):
        self.config(background=self.default_Background)


class MyApp(tk.Tk):
    def __init__(self, title='Sample App', *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title(title)
        self.configure(background='Gray')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master_frame = tk.Frame(self, bg='Light Blue', bd=3, relief=tk.RIDGE)
        master_frame.grid(sticky=tk.NSEW)
        master_frame.columnconfigure(0, weight=1)

        label1 = tk.Label(master_frame, text='Frame1 Contents', bg=LABEL_BG)
        label1.grid(row=0, column=0, pady=5, sticky=tk.NW)

        frame1 = tk.Frame(master_frame, bg='Green', bd=2, relief=tk.FLAT)
        frame1.grid(row=1, column=0, sticky=tk.NW)

        cb_var1 = tk.IntVar()
        checkbutton1 = tk.Checkbutton(frame1, text='StartCheckBox', variable=cb_var1)
        checkbutton1.grid(row=0, column=0, padx=0, pady=0)

        label2 = tk.Label(master_frame, text='Frame2 Contents', bg=LABEL_BG)
        label2.grid(row=2, column=0, pady=5, sticky=tk.NW)

        # Create a frame for the canvas and scrollbar(s).
        frame2 = tk.Frame(master_frame, bg='Red', bd=1, relief=tk.FLAT)
        frame2.grid(row=3, column=0, sticky=tk.NW)

        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_columnconfigure(1, weight=1)
        # Add a canvas in that frame.
        canvas = tk.Canvas(frame2, bg='Yellow')
        canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)
        
        def deleteRow(rowid):
            print('delete',rowid)
        
        def addRow(rowid):
            print('add',rowid)
        def refreshcanvas(ROWS,COLS):
            # Add the buttons to the frame.
            add_buttons = [tk.Button() for j in range(ROWS+1)] 
            del_buttons = [tk.Button() for j in range(ROWS+1)] 

            for i in range(1, ROWS+1):
                for j in range(1, COLS+1-2):
                    
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text='[%d, %d]' % (i, j))
                    label.grid(row=i, column=j, sticky='news')
                    print(f'add button in  {i} row')
                    if i ==1:
                        button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                            activebackground= 'orange', text='add')
                        button.grid(row=i, column=COLS+1-2, sticky='news')

                        delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                            activebackground= 'orange', text='delete')
                        delete_button.grid(row=i, column=COLS+1-1, sticky='news')
                    if i!=1:
                        add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                            activebackground= 'orange', text='add',command=lambda x=i  :addRow(rowid=x))
                        add_buttons[i].grid(row=i, column=COLS+1-2, sticky='news')

                        del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                            activebackground= 'orange', text='delete',command=lambda x=i :deleteRow(rowid=x))
                        del_buttons[i].grid(row=i, column=COLS+1-1, sticky='news')
                        
 
                        

            # Create canvas window to hold the buttons_frame.
            canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

            buttons_frame.update_idletasks()  # Needed to make bbox info available.
            bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

            # Define the scrollable region as entire canvas with only the desired
            # number of rows and columns displayed.
            w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
            canvas.configure(scrollregion=bbox, width=dw, height=dh)
        refreshcanvas(1,8)

        label3 = tk.Label(master_frame, text='Frame3 Contents', bg=LABEL_BG)
        label3.grid(row=4, column=0, pady=5, sticky=tk.NW)

        frame3 = tk.Frame(master_frame, bg='Blue', bd=2, relief=tk.FLAT)
        frame3.grid(row=5, column=0, sticky=tk.NW)

        cb_var2 = tk.IntVar()
        checkbutton2 = tk.Checkbutton(frame3, text='EndCheckBox', variable=cb_var2)
        checkbutton2.grid(row=0, column=0, padx=0, pady=0)
        
        changesize=tk.Button(frame3,text='change',command=lambda:refreshcanvas(10,8))
        changesize.grid(row=1, column=0, padx=0, pady=0)


if __name__ == '__main__':
    app = MyApp('Scrollable Canvas')
    app.mainloop()