import tkinter as tk
from src.constants import height,width,window_size
from src.log import logger
from src.utils import showinfomsg,find_key
from src.customid import CustomID
from src.models.youtube_video_model import YoutubeVideoModel
from src.models.platform_model import PLATFORM_TYPE
from src.models.upload_setting_model import UploadSettingModel
from src.models.account_model import AccountModel
from src.models.account_model import *
from datetime import datetime,date,timedelta

def bulkImportUsers(frame):

    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    #缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0,1), weight=1)

    newWindow.title('user bulk import')
    newWindow.grid_rowconfigure(0, weight=1)
    newWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    newWindow.grid_columnconfigure(1, weight=2)
    
    account_frame_left = tk.Frame(newWindow, height = height)
    account_frame_left.grid(row=0,column=0,sticky="nsew")
    account_frame_right = tk.Frame(newWindow, height = height)
    account_frame_right.grid(row=0,column=1,sticky="nsew") 
    accountView(account_frame_right)


    ttkframe=account_frame_left

    lbl15 = tk.Label(ttkframe, text='input account info with \\n separator')
    lbl15.grid(row=0,column=0, sticky=tk.W)
    

        
    
    
    
    from tkinter.scrolledtext import ScrolledText
    textfield = ScrolledText(ttkframe, wrap=tk.WORD)
    textfield.grid(row = 1, column = 0, columnspan = 5, padx=14, pady=15)
    textfield.bind_all("<Control-c>",_copy)
    accountfilepath=tk.StringVar()
    
    b_choose_proxy=tk.Button(ttkframe,text="load  from file",command=lambda: threading.Thread(target=select_file('',variable=accountfilepath,)).start() )
    b_choose_proxy.grid(row=2,column=0, sticky=tk.W)

    
    b_save_user=tk.Button(ttkframe,text="save user",command=lambda: threading.Thread(target=bulksaveUser(accountfilepath.get())).start() )
    b_save_user.grid(row = 10, column = 0, columnspan = 3, padx=14, pady=15)    
def bulksaveUser(accountfilepath):
    print(accountfilepath)
def saveUser(platform,username,password,proxy,cookies,linkaccounts=None):

    if platform is None:
        logger.error('please choose a platform')
        showinfomsg(message='please choose a platform first')
    if username is None:
        logger.error('please provide  a username')
        showinfomsg(message='please provide  a username')

    else:    
        if password is None:
            logger.debug('you dont provide password')        
            if cookies is None:
                logger.error('please provide a cookie file without  password')     
                showinfomsg(message='please provide a cookie file without  password')

        # Define a list of proxy IDs associated with the account
        proxy_ids = proxy
        # [1, 2, 3]  # Replace with the actual IDs of the proxies

        # Serialize the list of proxy IDs to JSON
        # proxy_ids_json = json.dumps(proxy_ids)
        user_data=           {
            'platform': platform,
            'username': username,
            'password': password,
            'cookies': cookies,
            'proxy': proxy_ids
        }
        # Create the user and associate the proxy IDs
        userid = AccountModel.add_account(user_data)

        if userid:

            if linkaccounts !=None:
                accounts=eval(linkaccounts)
                for key,value in enumerate(accounts):
                    if len(value.split(','))!=0:
                        for id in  value.split(','):
                            r=AccountRelationship.add_AccountRelationship_by_username(main_username=userid,otherusername=id)
                            if r:
                                print(f'bind {id} to {username} as side account')
            showinfomsg(message='this account added ok')
        else:

            showinfomsg(message='this account added failed')

    

def find_key(input_dict, value):
    if type(input_dict)==list:
        input_dict=dict(input_dict)
    result = "None"
    for key,val in input_dict.items():
        if val == value:
            result = key
    return result
def newaccountView(frame):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    #缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0,1), weight=1)

    newWindow.title('user bulk import')
    newWindow.grid_rowconfigure(0, weight=1)
    newWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    newWindow.grid_columnconfigure(1, weight=2)
    
    account_frame_left = tk.Frame(newWindow, height = height)
    account_frame_left.grid(row=0,column=0,sticky="nsew")
    account_frame_right = tk.Frame(newWindow, height = height)
    account_frame_right.grid(row=0,column=1,sticky="nsew") 
    accountView(account_frame_right)


    ttkframe=account_frame_left
    global proxy_option_account,channel_cookie_user

    channel_cookie_user= tk.StringVar()
    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()


    l_platform = tk.Label(ttkframe, text=settings[locale]['l_platform']
                          )
    # l_platform.place(x=10, y=90)
    l_platform.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15)    

    socialplatform = tk.StringVar()
    socialplatform_box = ttk.Combobox(ttkframe, textvariable=socialplatform)


    def socialplatformdb_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)


        platform_names = [dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows]

        socialplatform_box['values'] = platform_names

    def socialplatformdb_refresh(event):
        socialplatform_box['values'] = socialplatformdb_values()

    socialplatform_box['values'] = socialplatformdb_values()



    def socialplatformOptionCallBack(*args):
        print(socialplatform.get())
        print(socialplatform_box.current())

    socialplatform.set("Select From Platforms")
    socialplatform.trace('w', socialplatformOptionCallBack)
    socialplatform_box.bind('<FocusIn>', lambda event: socialplatformdb_refresh(event))


    # socialplatform_box.config(values =platform_names)
    socialplatform_box.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15)    



    l_username = tk.Label(ttkframe, text=settings[locale]['username']
                          )
    # l_username.place(x=10, y=150)
    l_username.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15)    

    e_username = tk.Entry(ttkframe, width=int(width*0.01), textvariable=username)
    # e_username.place(x=10, y=180)
    e_username.grid(row = 2, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    




    l_password = tk.Label(ttkframe, text=settings[locale]['password']
                          )
    e_password = tk.Entry(ttkframe, width=int(width*0.01), textvariable=password)

    l_password.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15)    
    e_password.grid(row = 3, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    

    linkAccounts=tk.StringVar()


    l_linkAccounts = tk.Label(ttkframe, text=settings[locale]['linkAccounts']
                          )
    e_linkAccounts = tk.Entry(ttkframe, width=int(width*0.01), textvariable=linkAccounts)

    l_linkAccounts.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15)    
    e_linkAccounts.grid(row = 4, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')   

    b_choose_account=tk.Button(ttkframe,text="Link",command=lambda: threading.Thread(target=lambda:chooseAccountsView(ttkframe,linkAccounts)).start() )
    Tooltip(b_choose_account, text='if you want to associate any account as the backup accounts' , wraplength=200)

    b_choose_account.grid(row = 4, column = 9, columnspan = 2, padx=14, pady=15)    
    l_proxy_option = tk.Label(ttkframe, text=settings[locale]['proxySetting']
                              )
    
    l_proxy_option.grid(row = 5, column = 0, columnspan = 3, padx=14, pady=15)    

    e_proxy_option = tk.Entry(ttkframe, textvariable=proxy_option_account)
    e_proxy_option.grid(row = 5, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    

    b_choose_proxy=tk.Button(ttkframe,text="Link",command=lambda: threading.Thread(target=chooseProxies(ttkframe,username.get(),proxy_option_account)).start() )
    
    b_choose_proxy.grid(row = 5, column = 9, columnspan = 2, padx=14, pady=15)    




    l_channel_cookie = tk.Label(ttkframe, text='cookies' 
                                # settings[locale]['select_cookie_file']
                                )
    # l_channel_cookie.place(x=10, y=330)
    l_channel_cookie.grid(row = 6, column = 0, columnspan = 3, padx=14, pady=15)    

    e_channel_cookie = tk.Entry(ttkframe, textvariable=channel_cookie_user)
    # e_channel_cookie.place(x=10, y=360)
    e_channel_cookie.grid(row = 6, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    

    b_channel_cookie=tk.Button(ttkframe,text="Select",command=lambda: threading.Thread(target=select_file('select cookie file for account',channel_cookie_user,cached=None)).start() )
    # b_channel_cookie.place(x=10, y=390)    
    b_channel_cookie.grid(row = 6, column = 9, columnspan = 2, padx=14, pady=15)    

    
    b_channel_cookie_gen=tk.Button(ttkframe,text="pull",command=auto_gen_cookie_file)
    # b_channel_cookie_gen.place(x=100, y=390)    
    b_channel_cookie_gen.grid(row = 6, column = 12, columnspan = 2, padx=14, pady=15)    
 
    
    b_save_user=tk.Button(ttkframe,text="save user",command=lambda: threading.Thread(target=saveUser(socialplatform.get(),username.get(),password.get(),proxy_option_account.get(),channel_cookie_user.get(),linkAccounts.get())).start() )
    b_save_user.grid(row = 10, column = 0, columnspan = 3, padx=14, pady=15)    

def accountView(frame,mode='query'):



    operation_frame = tk.Frame(frame,  bd=1, relief=tk.FLAT)
    operation_frame.grid(row=1, column=0,sticky=tk.NW)

    b_new_users=tk.Button(operation_frame,text="New account",command=lambda: threading.Thread(target=newaccountView(frame)).start() )
    b_new_users.grid(row = 0, column = 0,  padx=14, pady=15)    

    b_bulk_import_users=tk.Button(operation_frame,text="bulk import",command=lambda: threading.Thread(target=bulkImportUsers(frame)).start() )
    # b_bulk_import_users.place(x=10, y=450)    
    b_bulk_import_users.grid(row = 0, column = 1,  padx=14, pady=15)    
    
    hints='bulk pull sessionid and cookies'

    b_bulk_pull_cookies=tk.Button(operation_frame,text=hints,command=lambda: threading.Thread(target=bulkImportUsers(frame)).start() )
    # b_bulk_import_users.place(x=10, y=450)    
    b_bulk_pull_cookies.grid(row = 0, column = 2,padx=14, pady=15)     
    

    global q_username_account,latest_user_conditions_user,q_platform_account
    q_username_account = tk.StringVar()
    q_platform_account = tk.StringVar()



    query_frame = tk.Frame(frame,  bd=1, relief=tk.FLAT)
    query_frame.grid(row=0, column=0,sticky=tk.NW)
    latest_user_conditions_user=tk.StringVar()
    lbl15 = tk.Label(query_frame, text='By username.')
    # lbl15.place(x=430, y=15, anchor=tk.NE)
    lbl15.grid(row = 0, column = 0, padx=14, pady=15,sticky='w')    
    txt15 = tk.Entry(query_frame, width=11,textvariable=q_platform_account)
    txt15.insert(0,'')
    txt15.grid(row = 1, column = 0, padx=14, pady=15,sticky='w')    


    lb18 = tk.Label(query_frame, text='By platform.')
    lb18.grid(row=0,column=1, sticky=tk.W)


    q_platform = tk.StringVar()
    q_platform_accountbox = ttk.Combobox(query_frame, textvariable=q_platform)

    def q_platformb_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows]

        q_platform_accountbox['values'] = platform_names

    def q_platformdb_refresh(event):
        q_platform_accountbox['values'] = q_platformb_values()

    q_platform_accountbox['values'] = q_platformb_values()


    def q_platformOptionCallBack(*args):
        print(q_platform.get())
        print(q_platform_accountbox.current())

    q_platform.set("Select From Platforms")
    q_platform.trace('w', q_platformOptionCallBack)


    q_platform_accountbox['values'] = q_platformb_values()

    q_platform_accountbox.bind('<FocusIn>', lambda event: q_platformdb_refresh(event))    
    q_platform_accountbox.grid(row = 1, column = 1, padx=14, pady=15,sticky='w')    







    btn5= tk.Button(query_frame, text="Reset", padx = 0, pady = 0,command = lambda:(q_platform.set(''),q_platform_account.set('')))
    btn5.grid(row=1,column=5, sticky=tk.W)    




    
    result_frame = tk.Frame(frame,  bd=1, relief=tk.FLAT)
    result_frame.grid(row=3, column=0,sticky=tk.NW)

    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)
    result_frame.grid_columnconfigure(1, weight=1)
    
    tab_headers=['id','platform','username','pass','is_deleted','proxy','inserted_at']


    tab_headers.append('operation')
    tab_headers.append('operation')
    tab_headers.append('operation')
    tab_headers.append('operation')



    refreshAccountcanvas(canvas=None,frame=result_frame,headers=tab_headers,datas=[])

    
    # txt15.place(x=580, y=15, anchor=tk.NE)
    btn5= tk.Button(query_frame, text="Get Info", command = lambda:queryAccounts(frame=result_frame,canvas=None,tab_headers=tab_headers,username=q_username_account.get(),platform=q_platform.get(),linkAccounts=None) )
    # btn5.place(x=800, y=15, anchor=tk.NE)    

    btn5.grid(row = 1, column =3, padx=14, pady=15)    

    