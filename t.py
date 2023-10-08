import tkinter as tk

# Create a global variable for mode
mode = None

def policyOptionCallBack(*args):
    global mode

    mode_value = mode.get()

    if mode_value in [3, 4, 5]:
        l_dailycount.grid()
        l_start_publish_date.grid()
        e_start_publish_date.grid()
        logger.info('Show offset elements')
    else:
        l_dailycount.grid_remove()
        l_start_publish_date.grid_remove()
        e_start_publish_date.grid_remove()
        logger.info('Hide offset elements')

# Create the main tkinter window and frame
root = tk.Tk()
frame = tk.Frame(root)

# Rest of your code...

mode = tk.IntVar()
mode.set(3)
mode.trace_add('write', policyOptionCallBack)

# Rest of your code...

root.mainloop()
