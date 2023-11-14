from peewee import TextField, BlobField, BooleanField,IntegerField,ForeignKeyField
from playhouse.shortcuts import model_to_dict

import time
from src.customid import CustomID
from src.models.youtube_video_model import YoutubeVideoModel
from src.models.platform_model import PLATFORM_TYPE
from src.models.upload_setting_model import UploadSettingModel
from src.models.account_model import AccountModel
from src.models.task_model import *
from datetime import datetime,date,timedelta
import tkinter as tk
from src.constants import height,width,window_size
from src.log import logger
from src.utils import showinfomsg,find_key,askokcancelmsg
from pathlib import Path,PureWindowsPath,PurePath
import asyncio
def queryTasks(frame=None,canvas=None,tab_headers=None,username=None,platform=None,status=None,video_title=None,schedule_at=None,video_id=None,pageno=None,pagecount=None,ids=None,sortby="Add DATE ASC"):
    if pageno is None:
        pageno=1
    if pagecount is None:
        pagecount=50
    if  username is not None and 'input' in username:
        username=None
    if username==''  or username is None:
        username=None
    if  schedule_at is not None and 'input' in schedule_at:
        schedule_at=None            
    if schedule_at=='' or schedule_at is None:
        schedule_at=None           
    if  video_id is not None and 'input' in video_id:
        video_id=None            
    if video_id=='' or video_id is None:
        video_id=None           
    if  video_title is not None and 'input' in video_title:
        video_title=None            
    if video_title=='' or video_title is None:
        video_title=None            
    if  platform is not None and 'choose' in platform:
        platform=None            
    if platform=='' or platform is None:
        platform=None        
    elif type(platform)==str:
        print('======',platform)
        print(f'query tasks for  platform:{platform} {find_key(PLATFORM_TYPE.PLATFORM_TYPE_TEXT, platform)} ')

        platform=find_key(PLATFORM_TYPE.PLATFORM_TYPE_TEXT, platform)

        if type(status)==str:
            try:
                print(f'query tasks for status:{status} {getattr(TASK_STATUS, status.upper())} ')

                status=getattr(TASK_STATUS, status.upper())
            except:
                logger.info('you input status is invalid :{status},we use default 2')
                status=0

    if sortby=='':
        sortby="Add DATE ASC"
    elif sortby  in list(dict(SORT_BY_TYPE.SORT_BY_TYPE_TEXT).keys()):
        pass
    elif  sortby is not None and 'choose' in sortby:
        sortby=None             
    elif type(sortby)==str:
        print(f'query tasks for sortby: {sortby} {find_key(SORT_BY_TYPE.SORT_BY_TYPE_TEXT, sortby.upper())} ')

        sortby=find_key(SORT_BY_TYPE.SORT_BY_TYPE_TEXT, sortby.upper())

        # sortby=find_key(SORT_BY_TYPE.SORT_BY_TYPE_TEXT,sortby)
        # if row.type in dict(TASK_STATUS.TASK_STATUS_TEXT).values():
            
        #     ptype=getattr(dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT),row.type)
        #     ptype=dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[ptype]
        #     print(f"{getattr(dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT),row.type)}")
        # if row.status in dict(TASK_STATUS.TASK_STATUS_TEXT).values():
        #     status=getattr(dict(TASK_STATUS.TASK_STATUS_TEXT),row.status)

        #     print(f"{getattr(dict(TASK_STATUS.TASK_STATUS_TEXT),row.status)}")        

    task_rows,counts=TaskModel.filter_tasks(status=status,schedule_at=schedule_at,platform=platform,video_title=video_title,video_id=video_id,username=username,pagecount=pagecount,pageno=pageno,ids=ids,sortby=sortby) 
    if task_rows is None or len(task_rows)==0:
        showinfomsg(message=f"try to add tasks  first",parent=frame,DURATION=500)    

    else:                
        logger.debug(f'we found {counts} record matching ')
        # showinfomsg(message=f'we found {counts} record matching',DURATION=500)
        
        print(f'try to clear existing result frame  {len(frame.winfo_children())} ')

        try:
            print(frame.winfo_children())
            frame.winfo_children()


            if len(frame.winfo_children())>0:
                for widget in frame.winfo_children():
                    widget.destroy()      

        except:
            print('there is no result frame  at all')    
        l_totalcount = tk.Label(frame, text=f'total:{counts} per page:{pagecount} current page: {pageno}')
        l_totalcount.grid(row = 3, column = 0,sticky='w')            
        i=0
        task_data=[]
        # tab_headers=None
        pagebuttons=[]
        if counts>pagecount:

            pages=counts/pagecount
            pages=int(pages)
            for i in range(pages):
                # 这里如果没有lambda x=i 的话 后面的i+1 一直是1
                pagebutton= tk.Button(frame, text=str(i+1), padx = 0, pady = 0,
                                command = lambda x=i:queryTasks(canvas=canvas,frame=frame,status=status,schedule_at=schedule_at,platform=platform,
                                                video_title=video_title,video_id=video_id,username=username,pagecount=pagecount,pageno=x+1,ids=ids,sortby=sortby) )
                

                pagebutton.grid(row=3, column=i+1,sticky=tk.NW)
                pagebuttons.append(pagebutton)
            # Create a frame for the canvas and scrollbar(s).

        else:
            pagebutton= tk.Button(frame, text=str(1), padx = 0, pady = 0,
                                command = lambda x=0:queryTasks(canvas=canvas,frame=frame,status=status,schedule_at=schedule_at,platform=platform,
                                                video_title=video_title,video_id=video_id,username=username,pagecount=pagecount,pageno=x+1,ids=ids,sortby=sortby) )
                

            pagebutton.grid(row=3, column=1,sticky=tk.NW)
        print(f'prepare row data to render:{task_rows}')
        for row in task_rows:
            print('row data',row)
            print('platform',row.platform,dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[row.platform])


            p_value=row.platform
            if type(row.platform)!=int:
                p_value=100
            task={
                "id":CustomID(custom_id=row.id).to_hex(),
                "platform":dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[p_value],
                "prorioty":row.prorioty,
                "username":row.username,
                "status":dict(TASK_STATUS.TASK_STATUS_TEXT)[row.status],
                "schedule_at":row.video.release_date,
                "proxy":row.proxy,
                "video title":row.video.video_title,
                "uploaded_at":datetime.fromtimestamp(row.uploaded_at).strftime("%Y-%m-%d %H:%M:%S") if row.uploaded_at else None, 

                "inserted_at":datetime.fromtimestamp(row.inserted_at).strftime("%Y-%m-%d %H:%M:%S")  
            }
            if list(task.keys())!=tab_headers:
                tab_headers=list(task.keys())

            task_data.append(task)
        print(f'end to prepare row data to render:{task_data}')
        # print(f'try to clear existing rows in the tabular ')
        # if canvas is not None:
        #     try:
        #         canvas.winfo_children
        #         print('+++++++++++++++++',len(canvas.winfo_children()))
        #         if len(canvas.winfo_children())>0:
        #             for widget in canvas.winfo_children():
        #                 widget.destroy()      

        #     except:
        #         print('there is no rows in the tabular at all')
        # else:
        #     print('there is no tabular at all')
        tab_headers.append('operation')
        tab_headers.append('operation')
        tab_headers.append('operation')

        print(f'show header and rows based on query {tab_headers}\n{task_data}')
        refreshTaskcanvas(canvas=canvas,frame=frame,headers=tab_headers,datas=[])

        refreshTaskcanvas(canvas=canvas,frame=frame,headers=tab_headers,datas=task_data)
    
        print(f'end to show header and rows based on query {tab_headers}\n{task_data}')

        logger.debug(f'Task search and display finished')
                    
def refreshTaskcanvas(canvas=None,frame=None,headers=None,datas=None):

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
    print(f'currrent taskvas is {canvas}')    
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
    upload_buttons = [tk.Button() for j in range(ROWS+1)] 

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
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row_task(rowid=datas[x]['id'],name='task'))
            add_buttons[i].grid(row=i, column=len(headers)-3, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row_task(rowid=datas[x]['id'],name='task'))
            del_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')

            upload_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='upload',command=lambda x=i-1 :upload_selected_row_task(rowid=datas[x]['id'],frame=frame,status=datas[x]['status'],platform=datas[x]['platform']))
            upload_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')

    # Create canvas window to hold the buttons_frame.
    canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)
    buttons_frame.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.
    w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
    print('=before==',COLS,COLS_DISP,ROWS,ROWS_DISP)

    for i in range(5,COLS_DISP):
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

        if dw>int( width*1.2):
            COLS=i-1
    for i in range(5,ROWS_DISP):
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)                
        if dh>int( height*0.7):
            ROWS=i-1

    print('=after==',COLS,COLS_DISP,ROWS,ROWS_DISP)
    dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

    if dw>int( width*1.2):
        dw=int( width*1.2)
    if dh>int( height*0.7):
        dh=int( height*0.7)
        print('use parent frame widht')
    canvas.configure(scrollregion=bbox, width=dw, height=dh)
    print('end to render tabular rows')

def remove_selected_row_task(rowid,frame=None,name=None,func=None):



    print(f'you want to remove these selected {name}',rowid)
    if rowid==0:

        showinfomsg(message=f'you have not selected  {name} at all.choose one or more',parent=frame)      
    
    else:


        if rowid :
            rowid_bin=CustomID(custom_id=rowid).to_bin()
            result=TaskModel.update_task(id=rowid_bin,is_deleted=True)
            # result=func(id=rowid,is_deleted=True)

            if result:
                logger.debug(f'this {name}: {rowid} removed success')
                showinfomsg(message=f'this {name}: {rowid} removed success',parent=frame)    
            else:
                logger.debug(f'you cannot remove this {name} {rowid}, not added before')
                showinfomsg(message=f'this {name}: {rowid} not added before',parent=frame)    
        logger.debug(f'end to remove,reset {name} {rowid}')

def upload_selected_row_task(rowid,frame=None,status=None,platform=None):



    print('you want to upload this task',rowid)
    if rowid==0:

        showinfomsg(message='you have not selected  task at all.choose one or more',parent=frame)      
    
    else:
        if status=='success':
            askokcancelmsg(message='this video is been uploaded before',parent=frame)    
        if platform!='youtube':
            showinfomsg(message='this platform not supported yet',parent=frame)      
        else:
            if status=='success':
                askokcancelmsg(message='this video is been uploaded before',parent=frame)    
            if rowid :
                rowid_bin=CustomID(custom_id=rowid).to_bin()
                task_rows,counts=TaskModel.filter_tasks(id=rowid_bin,is_deleted=False)

                if counts>0:
                    logger.debug(f'this task {rowid} start to upload')
                    setting=None
                    video=None


                    for row in task_rows:
                        print('platform',row.platform,dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[row.platform])
                        uploadsetting=model_to_dict(row.setting)
                        uploadsetting.pop('id')
                        uploadsetting.pop('inserted_at')
                        uploadsetting.pop('account')
                        uploadsetting.pop('is_deleted')
                        uploadsetting.pop('platform')
                        uploadsetting['logger']=logger
                        proxy=row.setting.account.proxy
                        if proxy:
                            uploadsetting['proxy_option']='socks5:127.0.0.1:1080'

                        video=model_to_dict(row.video)
                        video.pop('id')
                        video.pop('unique_hash')
                        video.pop('inserted_at')
                        video.pop('is_deleted')


                        videoid= asyncio.run(uploadTask(video=video,uploadsetting=uploadsetting,account=row.setting.account))
                        if videoid:


                            showinfomsg(message=f'this task {rowid} upload success',parent=frame)    
                else:
                    logger.debug(f'you cannot upload this task {rowid}, not added before')
                    showinfomsg(message=f'this task {rowid} not added before',parent=frame)    
        logger.debug(f'end to upload,reset task {rowid}')
def update_selected_row_task(rowid,frame=None,name=None,func=None):
    # showinfomsg(message='not supported yet',parent=chooseAccountsWindow)    
    editsWindow = tk.Toplevel(frame)
    editsWindow.geometry(window_size)
    editsWindow.title('Edit and update task and related setting,video info ')
    rowid_bin=CustomID(custom_id=rowid).to_bin()

    taskresult=TaskModel.get(id=rowid_bin)
    taskresult = model_to_dict(taskresult)


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

    tmptask=taskresult
    # tmptask.pop('video')
    # tmptask.pop('setting')
    print('taskresult\n',taskresult)
    print('video\n',taskresult.get('video'))
    print('setting\n',taskresult.get('setting'))
    newtaskresult,serialno,cols,lastindex=renderelements(lastindex=0,i=1,result=tmptask,column=0,disableelements=['id','inserted_at','uploaded_at','video','setting'],title='task data')
    newvideoresult={}
    newsettingresult={}
    newaccountresult={}
    # print('======================',serialno,cols,lastindex)

    if taskresult.get('video'):
        print('video is associated to task',serialno,cols,lastindex)

        newvideoresult,serialno,cols,lastindex=renderelements(lastindex=lastindex,i=1,result=taskresult.get('video'),column=cols,disableelements=['id','inserted_at','unique_hash'],title='video data')
    if taskresult.get('setting'):
        print('setting is associated to task',serialno,cols,lastindex)

        newsettingresult,serialno,cols,lastindex=renderelements(lastindex=lastindex,i=1,result=taskresult.get('setting'),column=cols,disableelements=['id','inserted_at','account'],title='setting data',fenlie=False)
        if taskresult.get('setting').get('account') :
            print('account is associated to setting',serialno,cols,lastindex)

            newaccountresult,serialno,cols,lastindex=renderelements(lastindex=lastindex,i=serialno,result=taskresult.get('setting').get('account'),column=cols-2,disableelements=['id','inserted_at','unique_hash'],title='account data')

    btn5= tk.Button(editsWindow, text="save && update", padx = 0, pady = 0,command = lambda:update_task_video(id=rowid_bin,newvideoresult=newvideoresult,newsettingresult=newsettingresult,newaccountresult=newaccountresult,newtaskresult=newtaskresult))
    btn5.grid(row=0,column=cols+1, rowspan=2,sticky=tk.W)    


def update_task_video(newvideoresult=None,newsettingresult=None,newaccountresult=None,newtaskresult=None,id=id):
    if newvideoresult==None and newsettingresult==None and newaccountresult==None and newtaskresult==None:
        showinfomsg(message='you have not make any changes')
    else:
        result=TaskModel.update_task(**newtaskresult,id=id,taskdata=None,videodata=newvideoresult,settingdata=newsettingresult,accountdata=newaccountresult)    
        if result:
            showinfomsg(message='changes have been updated')
        else:
            showinfomsg(message='changes update failed')