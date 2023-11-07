from peewee import TextField, BlobField, BooleanField,IntegerField,ForeignKeyField
from playhouse.shortcuts import model_to_dict

import time
from src.customid import CustomID
from src.models.youtube_video_model import YoutubeVideoModel
from src.models.platform_model import PLATFORM_TYPE
from src.models.upload_setting_model import UploadSettingModel
from src.models.account_model import AccountModel
from src.models.task_model import *
from src.models.proxy_model import *
from datetime import datetime,date,timedelta
import tkinter as tk
from src.constants import height,width,window_size
from src.log import logger
from src.utils import showinfomsg
from src.utils import showinfomsg,find_key,askokcancelmsg
from pathlib import Path,PureWindowsPath,PurePath
import asyncio
def check_selected_row(rowid):
    
    print('check proxy whether valid and its city country')
    result=ProxyModel.get_proxy_by_id(id=rowid)
    # if len(results)>0:
    #     showinfomsg(f'there are {len(results)} proxy to be validated')
    #     for proxy in results:
    #         proxy_string=(
    #                     f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
    #                     if proxy.proxy_username
    #                     else f"{proxy.proxy_host}:{proxy.proxy_port}"
    #                 )
    #         http_proxy=f"socks5://{proxy_string}"
    #         https_proxy=f"socks5://{proxy_string}"

    #         check=CheckIP(http_proxy=http_proxy,https_proxy=https_proxy)
    #         ip=check.check_api64ipify()
    #         print('check_api64ipify',ip)
    #         asp=check.check_asn_type()
    #         print('asp',asp)
    #         dnscountry=check.check_dns_country(ip)
    #         print('dnscountry',dnscountry)

    #         ipcountry=check.check_ip_coutry(ip)
    #         print('ipcountry',ipcountry)


def queryProxy(linkProxy=None,platform=None,frame=None,canvas=None,tab_headers=None,state=None,city=None,status=None,country=None,tags=None,network_type=None,pageno=None,pagecount=None,ids=None,sortby="Add DATE ASC",mode='query'):

    if status=='valid':
        status=1
    elif status=='invalid':
        status=0
    else:
        status=2        
    if city=='':
        city=None
    if country=='':
        country=None  
    if tags=='':
        tags=None      
    if state=='':
        state=None
    if network_type=='':
        network_type=None 
    if city is not None:
        city=city.lower()
    if country is not None:

        country=country.lower()
    if tags is not None:

        tags=tags.lower()

    db_rows=  ProxyModel.filter_proxies(city=city,country=country,tags=tags,status=status,state=state,network_type=network_type)
    # Extract account names and set them as options in the account dropdown
    if db_rows is None or len(db_rows)==0:
        # langlist.delete(0,tk.END)
        showinfomsg(message=f"try to add proxy first",parent=frame)    

    else:                
        logger.debug(f'we found {len(db_rows)} record matching ')

        # langlist.delete(0,tk.END)
        i=0
        proxy_data=[]
        for row in db_rows:
            proxy={
                "id":CustomID(custom_id=row.id).to_hex(),
                "provider": dict(PROXY_PROVIDER_TYPE.PROXY_PROVIDER_TYPE_TEXT)[row.proxy_provider_type],
                "protocol":row.proxy_protocol,
                "host":row.proxy_host,
                "port":row.proxy_port,                    
                "username":row.proxy_username,
                "pass":row.proxy_password,
                "country":row.country,
                "state":row.state,
                "city":row.city,                    
                "tags":row.tags,                    
                "status":row.status,                    
                "validate_results":row.proxy_validate_results,
                "is_deleted":row.is_deleted   ,
                "inserted_at":datetime.fromtimestamp(row.inserted_at).strftime("%Y-%m-%d %H:%M:%S")
            }
            proxy_data.append(proxy)
            print(proxy.keys())
        print(f'show header and rows based on query {tab_headers}\n{proxy_data}')
        refreshProxycanvas(canvas=canvas,frame=frame,headers=tab_headers,datas=[],mode=mode,linkProxy=linkProxy,platform=platform)

        refreshProxycanvas(canvas=canvas,frame=frame,headers=tab_headers,datas=proxy_data,mode=mode,linkProxy=linkProxy,platform=platform)
    



        print(f'end to show header and rows based on query {tab_headers}\n{proxy_data}')

        logger.debug(f'Proxy search and display finished')
                

                    
def refreshProxycanvas(linkProxy=None,canvas=None,frame=None,headers=None,datas=None,mode=None,platform=None):

    print(f'try to clear existing rows in the tabular {len(frame.winfo_children())} ')

    try:
        print(canvas.winfo_children())
        canvas.winfo_children()


        if len(canvas.winfo_children())>0:
            for widget in canvas.winfo_children():
                widget.destroy()      

    except:
        print('there is no rows in the tabular at all')
        
    print('start to render tabular rows')
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame, bg='Yellow')
    canvas.grid(row=0, column=0)
    print(f'currrent accountvas is {canvas}')    
    canvas=canvas
    print(f'set canvas to {canvas}')
    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    # Create a horizontal scrollbar linked to the canvas.
    hsbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    hsbar.grid(row=1, column=0, sticky=tk.EW)
    canvas.configure(xscrollcommand=hsbar.set)

    # Create a frame on the canvas to contain the grid of buttons.
    buttons_frame = tk.Frame(canvas)
    

    
    ROWS_DISP = len(datas)+1 # Number of rows to display.
    COLS_DISP = len(headers)+1  # Number of columns to display.
    COLS=len(headers)+1
    
    
    ROWS=len(datas)+1
    



    # Add the buttons to the frame.
    add_buttons = [tk.Button() for j in range(ROWS+1)] 
    del_buttons = [tk.Button() for j in range(ROWS+1)] 
    bind_buttons = [tk.Button() for j in range(ROWS+1)] 
    unbind_buttons = [tk.Button() for j in range(ROWS+1)] 

    # set table header
    print('start to set table header')


    for j,h in enumerate(headers):
        label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                            activebackground= 'orange', text=h)
        label.grid(row=0, column=j, sticky='news')                    
        if h=='operation':
            button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='operation')
            button.grid(row=0, column=j, sticky='news')
            button.config(state=tk.DISABLED)

            # delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
            #                     activebackground= 'orange', text='operation')
            # delete_button.grid(row=0, column=j, sticky='news')
    print('start to set table data')
    if datas and datas!=[]:
        
        for i,row in enumerate(datas):
            i=i+1
            for j in range(0,len(headers)):
                
                if headers[j]!='operation':
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=row[headers[j]])
                    label.grid(row=i ,column=j, sticky='news')         


            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row_proxy(rowid=datas[x]['id'],name='account'))
            add_buttons[i].grid(row=i, column=len(headers)-4, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row_proxy(rowid=datas[x]['id'],name='account'))
            del_buttons[i].grid(row=i, column=len(headers)-3, sticky='news')
            if mode!='query':
                bind_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='bind',command=lambda x=i-1 :bind_selected_row_proxy(selected_platform=platform,linkProxy=linkProxy,rowid=datas[x]['id'],frame=frame))
                bind_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')


                unbind_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='unbind',command=lambda x=i-1 :unbind_selected_row_proxy(selected_platform=platform,linkProxy=linkProxy,rowid=datas[x]['id'],frame=frame))
                unbind_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')
    # Create canvas window to hold the buttons_frame.
    canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)
    buttons_frame.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.
    w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
    print('=before==',COLS,COLS_DISP,ROWS,ROWS_DISP)
    widthratio=1
    height_ratio=0.7
    for i in range(5,COLS_DISP):
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

        if dw>int( width*widthratio):
            COLS=i-1
    for i in range(5,ROWS_DISP):
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)                
        if dh>int( height*height_ratio):
            ROWS=i-1

    print('=after==',COLS,COLS_DISP,ROWS,ROWS_DISP)
    dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

    if dw>int( width*widthratio):
        dw=int( width*widthratio)
    if dh>int( height*height_ratio):
        dh=int( height*height_ratio)
        print('use parent frame widht')
    canvas.configure(scrollregion=bbox, width=dw, height=dh)
    print('end to render tabular rows')

def remove_selected_row_proxy(rowid,frame=None,name=None,func=None):



    print(f'you want to remove these selected {name}',rowid)
    if rowid==0:

        showinfomsg(message=f'you have not selected  {name} at all.choose one or more',parent=frame)      
    
    else:


        if rowid :
            rowid_bin=CustomID(custom_id=rowid).to_bin()
            result=ProxyModel.update_proxy(id=rowid_bin,is_deleted=True)
            # result=func(id=rowid,is_deleted=True)

            if result:
                logger.debug(f'this {name}: {rowid} removed success')
                showinfomsg(message=f'this {name}: {rowid} removed success',parent=frame)    
            else:
                logger.debug(f'you cannot remove this {name} {rowid}, not added before')
                showinfomsg(message=f'this {name}: {rowid} not added before',parent=frame)    
        logger.debug(f'end to remove,reset {name} {rowid}')

def bind_selected_row_proxy(rowid,selected_platform=None,linkProxy=None,frame=None):

    existingaProxies=linkProxy.get().split(',')
    show_str=linkProxy.get()
    if rowid is None:
        logger.debug('you have not selected new proxies at all')
        showinfomsg(message='you have not selected new proxies at all',parent=frame)    
    
    else:
        if rowid in existingaProxies:
            logger.debug(f'this proxy {rowid} added before')                   
            showinfomsg(message=f'this proxiess {rowid} added before') 

        else:
            existingaProxies.append(rowid)
            logger.debug(f'this proxy {rowid} added successS')
            showinfomsg(message=f'this proxy {rowid} added successS')

            if show_str=='':
                show_str=rowid
            else:
                show_str= show_str+','+rowid

    linkProxy.set(show_str)

        
        
def unbind_selected_row_proxy(rowid,selected_platform=None,linkProxy=None,frame=None):
    existingaProxies=linkProxy.get().split(',')
    show_str=linkProxy.get()
    if rowid is None:
        logger.debug('you have not selected new proxies at all')
        showinfomsg(message='you have not selected new proxies at all',parent=frame)    
    
    else:
        logger.debug(f'you want to remove this selected proxy {rowid} from existing: {existingaProxies}')

        if rowid in existingaProxies==False:
            logger.debug(f'this proxy {rowid} has not added before')                   
            showinfomsg(message=f'this proxiess {rowid}  has not added before') 

        else:
            existingaProxies.remove(rowid)

            logger.debug(f'this proxy {rowid} removed success')
            showinfomsg(message=f'this proxy {rowid} removed success')
        show_str= ','.join(item for item in existingaProxies if item is not None and item != "")


    linkProxy.set(show_str)


        


def update_selected_row_proxy(rowid,frame=None,name=None,func=None):
    # showinfomsg(message='not supported yet',parent=chooseAccountsWindow)    
    editsWindow = tk.Toplevel(frame)
    editsWindow.geometry(window_size)
    editsWindow.title('Edit and update account and related setting,video info ')
    rowid_bin=CustomID(custom_id=rowid).to_bin()

    accountresult=ProxyModel.get_proxy_by_id(id=rowid_bin)
    accountresult = model_to_dict(accountresult)

    def renderelements(i=1,column=0,result={},disableelements=['id','inserted_at','unique_hash'],title=None,lastindex=0,fenlie=True):
        rowkeys={}
        newresult={}
        rowlimit=22
        if lastindex==0:
            lastindex=0        
        label= tk.Label(editsWindow, padx=7, pady=7,bg="lightyellow", relief=tk.RIDGE,
                            activebackground= 'orange', text=title)
        label.grid(row=i ,column=column, sticky='news')    
        i=i+1

        for key,value in result.items():

            if i >rowlimit:
                i=1
                
                column=i%rowlimit+column+2
            # print('current key',key,value)
            if key=='id':
                value=CustomID(custom_id=value).to_hex()
            if key=='platform':
                value= dict( PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[value]
            if value==None:
                value=''                        
            if key=='inserted_at':
                value=datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")    
            if key=='video_local_path':
                print('value===',value)
                value=PurePath(value)
                print('value===',value)
                value=str(value)
                print('value===',value)
            if key=='thumbnail_local_path':
                print('value===',value)
                value=PurePath(value)
                print('value===',value)
                value=str(value)
                print('value===',value)                    


            if not  key  in disableelements:
            
                label= tk.Label(editsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text=key)
                label.grid(row=i ,column=column, sticky='news')         
                entry = tk.Entry(editsWindow)
        
                entry.insert(0, value)
                entry.grid(row=i ,column=column+1, sticky='news')   



                def callback(event):

                    x = event.widget.grid_info()['row']
                    y = event.widget.grid_info()['column']
                    index=int((int(y-1))*0.5)*rowlimit
                    index=int(index)+x-2
                    print(f'index  is {index},x {x} y-{y} column-{column}key- {rowkeys[index]}')

                    print(f'current input changes for {rowkeys[index]}',event.widget.get())   

                    newresult[rowkeys[index]]=event.widget.get()
                    if rowkeys[index]=='is_deleted':
                        # print('is deleted',type(event.widget.get()))
                        if event.widget.get()=='0':
                            value=False
                        elif event.widget.get()=='1':
                            value=True                        
                        newresult[rowkeys[index]]=value

                        print(f'============update row {rowkeys[index]} to',newresult)

                # variable.trace('w', lambda:setEnty())    
                entry.bind("<KeyRelease>", callback)
                i=i+1
                rowkeys[lastindex]=key
                print(f'set {lastindex} to -{key}')
                lastindex=lastindex+1

            elif  key  in ['account','video','setting','unique_hash']:
                print('ignore showing these elements')

            else:

                label = tk.Label(editsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text=key)
                label.grid(row=i ,column=column, sticky='news')         
                variable=tk.StringVar()
                variable.set(value)
                entry = tk.Entry(editsWindow,textvariable=variable)
                entry.grid(row=i ,column=column+1, sticky='news') 
                entry.config(state='disabled')
                i=i+1
                rowkeys[lastindex]=key
                print(f'set {lastindex} to -{key}')                
                lastindex=lastindex+1
        if fenlie==True:
            # print('is fenlie',lastindex)s
            if i<rowlimit:
                lastindex=rowlimit*(int(lastindex/rowlimit)+1)
        else:
            print('is not fenlie',lastindex)

        return newresult,i,column+2,lastindex

    tmpaccount=accountresult
    # tmpaccount.pop('video')
    # tmpaccount.pop('setting')
    print('accountresult\n',accountresult)
    print('link_accounts\n',accountresult.get('link_accounts'))
    newaccountresult,serialno,cols,lastindex=renderelements(lastindex=0,i=1,result=tmpaccount,column=0,disableelements=['id','inserted_at','uploaded_at','unique_hash','setting'],title='account data')
    newbackupaccountresult={}
    newsettingresult={}
    newaccountresult={}
    # print('======================',serialno,cols,lastindex)

    # if backupaccount_rows:
        # print('video is associated to account',serialno,cols,lastindex)

        # newvideoresult,serialno,cols,lastindex=renderelements(lastindex=lastindex,i=1,result=backupaccount_rows,column=cols,disableelements=['id','inserted_at','unique_hash'],title='link account data')
    # if accountresult.get('setting'):
    #     print('setting is associated to account',serialno,cols,lastindex)

    #     newsettingresult,serialno,cols,lastindex=renderelements(lastindex=lastindex,i=1,result=accountresult.get('setting'),column=cols,disableelements=['id','inserted_at','account'],title='setting data',fenlie=False)
    #     if accountresult.get('setting').get('account') :
    #         print('account is associated to setting',serialno,cols,lastindex)

    #         newaccountresult,serialno,cols,lastindex=renderelements(lastindex=lastindex,i=serialno,result=accountresult.get('setting').get('account'),column=cols-2,disableelements=['id','inserted_at','unique_hash'],title='account data')

    btn5= tk.Button(editsWindow, text="save && update", padx = 0, pady = 0,command = lambda:update_proxy(id=rowid_bin,newaccountresult=newaccountresult))
    btn5.grid(row=0,column=cols+1, rowspan=2,sticky=tk.W)    


def update_proxy(newaccountresult=None,id=id):
    if newaccountresult==None:
        showinfomsg(message='you have not make any changes')
    else:
        result=ProxyModel.update_proxy(**newaccountresult,id=id,accountdata=newaccountresult)     

        if result:
            showinfomsg(message='changes have been updated')
        else:
            showinfomsg(message='changes update failed')