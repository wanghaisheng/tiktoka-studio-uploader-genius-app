# Python program demonstrating Multiple selection
# in Listbox widget with a scrollbar


from tkinter import *

window = Tk()
window.title('Multiple selection')

# for scrolling vertically
yscrollbar = Scrollbar(window)
yscrollbar.pack(side = RIGHT, fill = Y)

label = Label(window,
			text = "Select the languages below : ",
			font = ("Times New Roman", 10),
			padx = 10, pady = 10)
label.pack()
langlist = Listbox(window, selectmode = "multiple",
			yscrollcommand = yscrollbar.set)

# Widget expands horizontally and
# vertically by assigning both to
# fill option
langlist.pack(padx = 10, pady = 10,
		expand = YES, fill = "both")

x =["C", "C++", "C#", "Java", "Python",
	"R", "Go", "Ruby", "JavaScript", "Swift",
	"SQL", "Perl", "XML"]

def CurSelet(event):
    listbox = event.widget
    # values = [listbox.get(idx) for idx in listbox.curselection()]
    
    # print( ', '.join(values))
    selection=listbox.curselection()
    # picked = listbox.get(selection[1])
    print(type(selection),list(selection))
    
langlist.bind('<<ListboxSelect>>',CurSelet)

for each_item in range(len(x)):
	
	langlist.insert(END, x[each_item])
	print('-',type(x[each_item]),type(each_item))
	langlist.itemconfig(each_item, bg = "lime")

# Attach listbox to vertical scrollbar
# yscrollbar.config(command = list.yview)
window.mainloop()
