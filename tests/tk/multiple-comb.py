import tkinter as tk
from tkinter import *
from tkinter import ttk 
from tkscrolledframe import ScrolledFrame #https://github.com/bmjcode/tkScrolledFrame
# for installation pip install tkScrolledFrame





class Picker(ttk.Frame):

    def __init__(self, master=None,
                 values=[],
                 entry_wid=None,
                 command=None,
                 entlarge_fonction=None, 
                 borderwidth=1, 
                 relief="solid",
                 font=('Arial, 11')):

        self._selected_item = None
        self._values = values
        self._entry_wid = entry_wid
        self._command = command
        if type(entlarge_fonction).__name__!='NoneType':
            self.entlarge_fonction=entlarge_fonction
        else:
            self.entlarge_fonction= lambda : 1
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#ffffff')
        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief, style='Custom.TFrame')
        self.bind("<Button-3>", lambda event : self.entlarge_fonction())
        self.bind("<FocusIn>", lambda event:self.event_generate('<<PickerFocusIn>>'))
        self.bind("<FocusOut>", lambda event:self.event_generate('<<PickerFocusOut>>'))
        # search field
        self.searchfield=ttk.Entry(self , font=font)
        self.searchfield.pack(fill=X)
        self.searchfield.insert(END, 'Search')
        self.searchfield.bind("<Button-1>", lambda event : self.clear_search_field())
        self.searchfield.bind("<Button-3>", lambda event : self.entlarge_fonction())
        self.searchfield.bind('<KeyRelease>',lambda event : self.update_checkbutton_list())


        

        self.scrolledframe=ScrolledFrame(self)
        self.scrolledframe.pack(fill=BOTH)
        self.scrolledframe.bind_arrow_keys(self)
        self.scrolledframe.bind_scroll_wheel(self)
        self.frame = self.scrolledframe.display_widget(Frame)
        
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#ffffff')

        #checkbutton frame
        self.check_buttonFrame=ttk.Frame(self.frame, style='Custom.TFrame')
        self.check_buttonFrame.pack(fill=BOTH)



        self.dict_checkbutton = {}
        self.dict_intvar_item = {}
        self.selected_value=[]
        self.create_check_button()



    @property
    def selection(self):
        return self.selected_value
    def set_value(self, new_values):
        if type(new_values).__name__=='list':
            self.selected_value=[]
            self._values=new_values
        else:
            raise('ValueError')


    def create_check_button(self, values=None):
        self.dict_checkbutton = {}
        self.dict_intvar_item = {}
        if type(values).__name__=='NoneType':
            values=self._values

        # first clear my frame
        for widget in self.check_buttonFrame.winfo_children():
            widget.destroy()

        for index,item in enumerate(values):

            self.dict_intvar_item[item] = tk.IntVar()
            self.dict_checkbutton[item] = ttk.Checkbutton(self.check_buttonFrame, 
                                                          text = item, 
                                                          variable=self.dict_intvar_item[item],
                                                          command=lambda selected=item : self.check_box_select(selected))
            self.dict_checkbutton[item].grid(row=index, column=0, sticky=tk.NSEW)
            self.dict_checkbutton[item].bind("<Button-3>", lambda e : self.entlarge_fonction())
            if item not in self.selected_value:
                self.dict_intvar_item[item].set(0)
            else:
                self.dict_intvar_item[item].set(1)

    def check_box_select(self, selected_value=None):
        for keys in self.dict_intvar_item.keys():
            if self.dict_intvar_item[keys].get()!=0:
                if keys not in self.selected_value:
                    self.selected_value.append(keys)
            else:
                if keys in self.selected_value:
                    self.selected_value.remove(keys)
        try:
            self._command(selected_value)
        except Exception as e:
            print(e)



    def clear_search_field(self):
        self.searchfield.delete(0, END)
        self.update_checkbutton_list()
    
    def update_checkbutton_list(self):
        
        search_value=self.searchfield.get()

        update_values=[]

        if search_value!='':
            for item in self._values:
                if search_value.lower() in str(item).lower():
                    update_values.append(item)
        else:
            update_values=self._values.copy()

        self.create_check_button(update_values)


class Combopicker(ttk.Combobox, Picker):
    def __init__(self, master, 
                 values= [] ,
                 entryvar=None, 
                 entrywidth=25, 
                 entrystyle=None, 
                 font=('Arial, 16'),
                 command=None):

        if entryvar is not None:
            self.entry_var = entryvar
        else:
            self.entry_var = tk.StringVar()
        self.entrywidth=entrywidth

        if  type(command).__name__=='NoneType':
            self.command= lambda : 1
        else:
            self.command = command

        entry_config = {}
        if entrywidth is not None:
            entry_config["width"] = entrywidth

        if entrystyle is not None:
            entry_config["style"] = entrystyle

        ttk.Combobox.__init__(self, master, 
                              textvariable=self.entry_var, 
                              **entry_config, 
                              state = "readonly", font=font)
        self.unbind_class("TCombobox", "<Button-1>")
        self.unbind_class("TCombobox", "<Double-1>")
        self.unbind_class("TCombobox", "<Triple-1>")
        self.unbind_class("TCombobox","<<ComboboxSelected>>")


        self._is_menuoptions_visible = False

        self.picker_frame = Picker(self.winfo_toplevel(), 
                                   values=values,
                                   entry_wid = self.entry_var,
                                   entlarge_fonction=self.entlarge,
                                   command=self._on_selected_check)

        self.bind_all("<1>", self._on_click, "+")

        self.bind("<Escape>", lambda event: self.hide_picker())

        # get widget size

        self.expand_var=False




    def set_value(self, new_value):
        self.picker_frame.set_value(new_value)
    
    def get(self):
        return self.picker_frame.selection
    
    def entlarge(self):
        if self.expand_var==False:
            self.config(width=80)
            self.picker_frame.place(in_=self, relx=0, rely=1, relwidth=1, height=300 )
            self.expand_var=True
        else:
            self.config(width=self.entrywidth)
            self.picker_frame.place(in_=self, relx=0, rely=1, relwidth=1, height=150 )
            self.expand_var=False

    def _on_selected_check(self, SELECTED):
        ''' add selected values on entry'''
        values=self.picker_frame.selection.copy()
        if len(values)!=0:
            values=str(values)[1:len(str(values))-1] # transform my list to string and remove []
            self.entry_var.set(values)
        self.command()

    def _on_click(self, event):
        str_widget = str(event.widget)

        if str_widget == str(self):
            if not self._is_menuoptions_visible:
                self.show_picker()
            else:
                try:
                    self.hide_picker()
                except:
                    pass
        else:
            if not str_widget.startswith(str(self.picker_frame)) and self._is_menuoptions_visible:
                self.hide_picker()

    def show_picker(self):
        if not self._is_menuoptions_visible:
            self.picker_frame.place(in_=self, relx=0, rely=1, relwidth=1, height=150 )
            self.picker_frame.lift()
        self._is_menuoptions_visible = True

    def hide_picker(self):
        if self._is_menuoptions_visible:
            self.picker_frame.place_forget()

        self._is_menuoptions_visible = False




if __name__ == "__main__":


    root = Tk()
    root.geometry("500x600")

    main =Frame(root, pady =15, padx=15,)
    main.pack(expand=True, fill="both")

    data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emma', 'Frank', 'Grace', 'Henry', 'Isabel', 'Jack'],
            'Gender': ['F', 'M', 'M', 'M', 'F', 'M', 'F', 'M', 'F', 'M'],
            'Age': [24, 32, 18, 47, 29, 53, 41, 19, 37, 28]}
    def print_selection():
        print('click')
        for key in combobox.keys():
            print(key, combobox[key].get())
    
    combobox={}
    
    counter=0
    for key in data.keys():
        Label(main, text=key).grid(row=counter, column= 0)
        combobox[key]=Combopicker(main, values=list(set(data[key])) , command=lambda :print_selection())
        combobox[key].grid(row=counter, column= 1)
        counter+=1



    root.mainloop()