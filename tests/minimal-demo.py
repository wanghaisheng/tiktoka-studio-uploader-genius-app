import logging,os,queue
import tkinter as tk
from tkinter import OptionMenu, filedialog,ttk
import tkinter.scrolledtext as ScrolledText
import pyperclip as clip
from pystray import MenuItem as item
import pystray
from PIL import Image

#https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/ 
# thanks for this great  guy sharing

logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')        

# Add the handler to logger

logger = logging.getLogger()      


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)
        


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame,root):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText.ScrolledText(frame, state='disabled', height=12)
        
        self.scrolled_text.bind_all("<Control-c>",self.copy)



        # Bind right-click event to show context menu
        self.scrolled_text.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Clear All Text", command=self.clear_text)
            
        self.scrolled_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)
    def clear_text(self):

        self.scrolled_text.configure(state='normal')  # Enable text widget
        self.scrolled_text.delete(1.0, tk.END)  # Delete all text
        self.scrolled_text.configure(state='disabled')  # Disable text widget again
    # Create a right-click context menu
    def show_context_menu(self,event):
        self.context_menu.post(event.x_root, event.y_root)


    def copy(self,event):
        try:
            string = event.widget.selection_get()
            clip.copy(string)
        except:
            pass
    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)
class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.max_length = 250


    def emit(self, record):
        msg = self.format(record)
        if len(msg) > self.max_length:
            lines = []
            while len(msg) > self.max_length:
                lines.append(msg[:self.max_length])
                msg = msg[self.max_length:]
            lines.append(msg)
            msg= '\n'.join(lines)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


def docView(frame,ttkframe,lang):
  
    
    
    locale_tkstudio = tk.StringVar()


    l_lang = tk.Label(ttkframe, text='chooseLang')
    l_lang.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15)    


    def locale_tkstudioOptionCallBack(*args):
        print(locale_tkstudio.get())
        print(locale_tkstudio_box.current())
        changeDisplayLang(locale_tkstudio.get())

    locale_tkstudio.set("Select From Langs")
    locale_tkstudio.trace('w', locale_tkstudioOptionCallBack)


    locale_tkstudio_box = ttk.Combobox(ttkframe, textvariable=locale_tkstudio)
    locale_tkstudio_box.config(values =('en', 'zh'))
    locale_tkstudio_box.grid(row = 4, column = 1, columnspan = 3, padx=14, pady=15)    

    
    
    
def render(root,window,log_frame,lang):
    global doc_frame
    tab_control = ttk.Notebook(window)
    
    doc_frame = ttk.Frame(tab_control)
    doc_frame.grid_rowconfigure(0, weight=1)
    doc_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    doc_frame.columnconfigure((0,1), weight=1)
    
    doc_frame_left = tk.Frame(doc_frame)
    doc_frame_left.grid(row=0,column=0,sticky="nsew")
    doc_frame_right = tk.Frame(doc_frame)
    doc_frame_right.grid(row=0,column=1,sticky="nsew") 




    if lang=='en':
        print('1111')
        tab_control.add(doc_frame, text='help')
    else:
        tab_control.add(doc_frame, text='帮助')
        print('222')

    docView(doc_frame_left,doc_frame_right,lang)

    account_frame = ttk.Frame(tab_control)
    account_frame.grid_rowconfigure(0, weight=1)
    account_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    account_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    account_frame.columnconfigure((0,1), weight=1)
    
    account_frame_left = tk.Frame(account_frame, height = 240)
    account_frame_left.grid(row=0,column=0,sticky="nsew")
    account_frame_right = tk.Frame(account_frame, height = 240)
    account_frame_right.grid(row=0,column=1,sticky="nsew") 
    tab_control.add(account_frame, text='demo')
    docView(account_frame_right,account_frame_left,lang)

    # tab_control.pack(expand=1, fill='both')
    tab_control.grid(row=0,column=0)






    Cascade_button = tk.Menubutton(window)
    # Cascade_button.pack(side=tk.LEFT, padx="2m")
 
     # the primary pulldown
    Cascade_button.menu = tk.Menu(Cascade_button)
 
     # this is the menu that cascades from the primary pulldown....
    Cascade_button.menu.choices = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.choices.add_command(label='zh',command=lambda:changeDisplayLang('zh'))
    Cascade_button.menu.choices.add_command(label='en',command=lambda:changeDisplayLang('en'))
    Cascade_button.menu.add_cascade(label= 'langs',
                                    
                                     menu=Cascade_button.menu.choices)    
    


    menubar = tk.Menu(window)

    menubar.add_cascade(label='settings', menu=Cascade_button.menu)    





def start(lang):

    global ROOT_DIR
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    global root,paned_window,log_frame,mainwindow,st

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    # Create a PanedWindow widget (vertical)
    paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
    paned_window.pack(expand=True, fill="both")

    # Configure weights for mainwindow and log_frame
    paned_window.grid_rowconfigure(0, weight=5)
    paned_window.grid_rowconfigure(1, weight=1)

    # Create the frame for the notebook
    mainwindow = ttk.Frame(paned_window)
    paned_window.add(mainwindow)
    mainwindow.grid_rowconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(0, weight=1)


    


    log_frame =tk.Frame(paned_window)
    paned_window.add(log_frame)

    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)


    st =ConsoleUi(log_frame,root)



    render(root,mainwindow,log_frame,lang)
    root.update_idletasks()

# # Set the initial size of the notebook frame (4/5 of total height)
    mainwindow_initial_percentage = 5 / 6  

    # Calculate the initial height of mainwindow based on the percentage
    initial_height = int(float(root.winfo_height()) * mainwindow_initial_percentage)
    mainwindow.config(height=initial_height)

def quit_window(icon, item):
    icon.stop()
    root.destroy()

def show_window(icon, item):
    icon.stop()
    root.after(0,root.deiconify)

def withdraw_window():  
    root.withdraw()
    image = Image.open("assets/icon.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run_detached()
def changeDisplayLang(lang):

    mainwindow.destroy()
    # try:
        # st.destroy()
    # del st
    log_frame.destroy()
    paned_window.destroy()
    # root.quit()    
    # del text_handler
    start(lang)
    logger.info(f'switch lang to locale:{lang}')
    
    root.mainloop()

if __name__ == '__main__':
    global root,st
    root = tk.Tk()
    start('en')
    root.protocol('WM_DELETE_WINDOW', withdraw_window)
    
    root.mainloop()

