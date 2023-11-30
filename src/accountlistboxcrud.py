def chooseAccountsView_listbox(newWindow,parentchooseaccounts):
    chooseAccountsWindow = tk.Toplevel(newWindow)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title('Choose associated accounts in which platform')
    account_var = tk.StringVar()

    # chooseAccountsWindow.grid_columnconfigure(0, weight=1)
    # frame_canvas.grid_columnconfigure(1, weight=1)    


    # Create a label for the platform dropdown
    platform_label = ttk.Label(chooseAccountsWindow, text="Select Platform:")
    platform_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    # Create a Combobox for the platform selection
    platform_var = tk.StringVar()
    platform_var.set("choose one:")    

    def db_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows]

        platform_combo['values'] = platform_names

    def db_refresh(event):
        platform_combo['values'] = db_values()
    platform_combo = ttk.Combobox(chooseAccountsWindow, textvariable=platform_var)
    platform_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
    platform_combo.bind('<FocusIn>', lambda event: db_refresh(event))
    platform_combo['values'] = db_values()

    # platform_combo.configure(values=platform_rows)
    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(chooseAccountsWindow)
    frame_canvas.grid(row=4, column=0,columnspan=10, pady=(5, 0), sticky='nw')
    frame_canvas.grid_columnconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(1, weight=1)    
    # frame_canvas.grid_rowconfigure(0, weight=1)
    # frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    # frame_canvas.grid_propagate(False)     
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame_canvas, bg='Yellow')
    canvas.grid(row=0, column=0)
    canvas.grid_columnconfigure(0, weight=1)
    canvas.grid_columnconfigure(1, weight=1)    
    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    # Create a horizontal scrollbar linked to the canvas.
    hsbar = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL, command=canvas.xview)
    hsbar.grid(row=1, column=0, sticky=tk.EW)
    canvas.configure(xscrollcommand=hsbar.set)
    # for scrolling vertically

    langlist_frame = tk.Frame(frame_canvas)

    
    langlist = tk.Listbox(langlist_frame, selectmode = "multiple",
                xscrollcommand=hsbar.set,
                yscrollcommand = vsbar.set)
    # langlist.pack(padx = 10, pady = 10,
    #         expand = tk.YES, 
    #         fill = "both")
    langlist.grid(row=0,column=0,sticky='nswe')
        # Create canvas window to hold the buttons_frame.
    canvas.create_window((0,0), window=langlist_frame, anchor=tk.NW)

    langlist_frame.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.

    canvas.configure(scrollregion=bbox
                    #  , width=dw, height=dh
                     )
    
    btn6= tk.Button(chooseAccountsWindow, text="remove selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=remove_selected_row).start())     
    btn6.grid(row=5,column=0, sticky=tk.W)
    Tooltip(btn6, text='if you want remove any from selected user' , wraplength=200)
    lbl16 = tk.Label(chooseAccountsWindow, text='selected user')
    lbl16.grid(row=8,column=0, sticky=tk.W)
    txt16 = tk.Entry(chooseAccountsWindow,textvariable=account_var,width=int(int(window_size.split('x')[-1])/5))
    txt16.insert(0,'')
    txt16.grid(row=8,column=1, 
            #    width=width,
               columnspan=4,
            #    rowspan=3,
               sticky='nswe')    
    def on_platform_selected(event):
        selected_platform = platform_var.get()
        # Clear the current selection in the account dropdown

        if selected_platform:


            platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
            platform_names = [dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows]
            print('platforms options are',platform_names)

            # Extract platform names and set them as options in the platform dropdown
            if platform_rows is None:
                platform_combo["values"]=[]
                button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

            else:
                logger.debug(f'query results of existing platforms is {platform_names}')

                if  len(platform_names)==0:
                    platform_combo["values"]=[]
                    button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                    button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
                    
                else:

                    # Execute a query to retrieve accounts based on the selected platform
                    platform_combo["values"]=platform_names
                    for platform in platform_names:
                        
                        if tmp['accountlinkaccount'].has_key(platform):
                            logger.debug(f'you have cached  this platform {platform}')
                        else:
                            tmp['accountlinkaccount'][platform]=''
                    
                    account_rows=AccountModel.filter_accounts(platform=getattr(PLATFORM_TYPE, selected_platform.upper()))
                    print(f'query accounts for {selected_platform} {getattr(PLATFORM_TYPE, selected_platform.upper())} ')
                    # Extract account names and set them as options in the account dropdown
                    if account_rows is None or len(account_rows)==0:
                        langlist.delete(0,tk.END)
                        showinfomsg(message=f"try to add accounts for {selected_platform} first",parent=chooseAccountsWindow)    

                    else:                
                        account_names = [row.username for row in account_rows]
                        logger.debug(f'we found {len(account_names)} record matching ')

                        langlist.delete(0,tk.END)
                        i=0
                        for row in account_names:

                            langlist.insert(tk.END, row)
                            langlist.itemconfig(int(i), bg = "lime")                        

    # Bind the platform selection event to the on_platform_selected function
    platform_combo.bind("<<ComboboxSelected>>", on_platform_selected)


    # Create a label for the account dropdown
    account_label = ttk.Label(chooseAccountsWindow, text="Select Account(one or many):")
    account_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)


    # Initialize the platform dropdown by calling the event handler
    # on_platform_selected(None)

    
    def remove_selected_row():
        selected_accounts=tmp['accountlinkaccount']['selected']
        show_str=account_var.get()

        print('you want to remove these selected proxy',selected_accounts)
        if len(selected_accounts)==0:

            showinfomsg(message='you have not selected  proxy at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:
            existingaccounts=tmp['accountlinkaccount'][platform_var.get()].split(',')            
            logger.debug(f'you want to remove this selected proxy {selected_accounts} from existing: {existingaccounts}')

            for item in selected_accounts:

                if item in existingaccounts:
                    existingaccounts.remove(item)


                    logger.debug(f'this proxy {item} removed success')
                    showinfomsg(message=f'this proxy {item} removed success',parent=chooseAccountsWindow)    
                else:
                    logger.debug(f'you cannot remove this proxy {item}, not added before')
                    showinfomsg(message=f'this proxy {item} not added before',parent=chooseAccountsWindow)    
            logger.debug(f'end to remove,reset proxystr {existingaccounts}')
            tmp['accountlinkaccount'][platform_var.get()]= ','.join(item for item in existingaccounts if item is not None and item != "")
        show_str=str(tmp['accountlinkaccount'])
        if tmp['accountlinkaccount'].has_key('selected'):
            new=dict(tmp['accountlinkaccount'])
            new.pop('selected')
            show_str=str(new)
        account_var.set(show_str)
        parentchooseaccounts.set(show_str)

    def add_selected_accounts(event):
        listbox = event.widget
        values = [listbox.get(idx).split(':')[0] for idx in listbox.curselection()]
        selected_platform = platform_var.get()
        print('----------',type(tmp['accountlinkaccount']),type(values))
        tmp['accountlinkaccount']['selected']=values
        existingaccounts=tmp['accountlinkaccount'][platform_var.get()].split(',')
        # (youtube:y1,y2),(tiktok:t1:t2)
        show_str=account_var.get()
        if len(list(values))==0:
            logger.debug('you have not selected  proxiess at all.choose one or more')
            showinfomsg(message='you have not selected  proxiess at all.choose one or more',parent=chooseAccountsWindow)    
        
        elif values==existingaccounts:
            logger.debug('you have not selected new proxiess at all')
            showinfomsg(message='you have not selected new proxiess at all',parent=chooseAccountsWindow)    
        
        else:
            for item in values:
                if item in existingaccounts:
                    logger.debug(f'this proxy {item} added before')                   
                    showinfomsg(message=f'this proxiess {item} added before',parent=chooseAccountsWindow)    

                else:
                    existingaccounts.append(item)
                    logger.debug(f'this proxy {item} added successS')
                    showinfomsg(message=f'this proxy {item} added success',parent=chooseAccountsWindow)    
            tmp['accountlinkaccount'][platform_var.get()]= ','.join(item for item in existingaccounts if item is not None and item != "")

        show_str=str(tmp['accountlinkaccount'])
        if tmp['accountlinkaccount'].has_key('selected'):
            new=dict(tmp['accountlinkaccount'])
            new.pop('selected')
            show_str=str(new)

        account_var.set(show_str)
        parentchooseaccounts.set(show_str)
    langlist.bind('<<ListboxSelect>>',add_selected_accounts)   
