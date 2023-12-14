from peewee import Model, BooleanField, TextField,IntegerField,ForeignKeyField,BlobField
from uploadergenius.server.models import BaseModel,db
from uploadergenius.utils.tools import generate_unique_hash
import time
from uploadergenius.utils.customid import CustomID
from uploadergenius.server.models.platform_model import PLATFORM_TYPE

class AccountModel(BaseModel):
    id = BlobField(primary_key=True)    
    platform= IntegerField(default=PLATFORM_TYPE.YOUTUBE)
    username = TextField()
    password = TextField(null=True)  
    cookie_local_path = TextField(null=True)   
    profile_local_path = TextField(null=True)   

    cookie_content = TextField(null=True)   
    proxy = TextField(null=True)
    inserted_at = IntegerField(null=True)
    is_deleted = BooleanField(default=False)  # Flag if the account is deleted
    unique_hash = TextField(index=True,unique=True, null=True, default=None)  # Unique hash for the account
    link_accounts = TextField(null=True)  

    # class Meta:
    #     db_table = db
    @classmethod

    def add_account(cls,account_data):
        unique_hash =generate_unique_hash(

        account_data
            )

        # Check if an account with the same unique hash already exists
        existing_account = cls.get_or_none(cls.unique_hash == unique_hash)

        if existing_account is None:
            account = AccountModel(**account_data)
            account.inserted_at = int(time.time())  # Update insert_date
            account.unique_hash=unique_hash
            account.id = CustomID().to_bin()
            account.is_deleted=False
            account.save(force_insert=True) 
            return account
            
        else:
            return existing_account
    @classmethod

    def get_account_by_id(cls, id):
        
        return cls.get_or_none(cls.id == id)
    @classmethod

    def get_active_account_by_id(cls, id):
        return cls.get_or_none(cls.id == id,cls.is_deleted==False)    
    @classmethod

    def get_account_by_username(cls, username):
        return cls.get_or_none(cls.username == username)
    @classmethod
    
    def update_account(cls, id,account_data=None, **kwargs):
        try:
            account = cls.get_or_none(cls.id == id)
            print('before modify',account,account.is_deleted)
            if account_data:
                account = AccountModel(**account_data)
                print('after modify',account,account.is_deleted)


            else:
                for key, value in kwargs.items():
                    # 由于entry获取的都是字符串变量值，对于bool型，需要手动转换
                    if key=='is_deleted':
                        print('is deleted',type(value))
                        if value=='0':
                            value=False
                        elif value=='1':
                            value=True
                    setattr(account, key, value)
                    
                print('after modify',account,account.is_deleted)
            account.inserted_at = int(time.time())  # Update insert_date

            account.save() 
            print('update success')
            return account
        except cls.DoesNotExist:
            return None

    def delete_account(cls, id):
        try:
            account = cls.get(cls.id == id)
            account.delete_instance()
            return True
        except cls.DoesNotExist:
            return False
    @classmethod
    def filter_accounts(cls, platform=None, username=None,cookie_local_path=None, cookie_content=None,proxy=None,inserted_at=None,is_deleted=False,pageno=None,pagecount=None,start=None,end=None,data=None,ids=None,sortby=None):
        query = cls.select()
        
        print('platform',platform)
        print('username',username)

        if is_deleted is None or type(is_deleted) !=bool:
            is_deleted=False
        if is_deleted:
            query = query.where(cls.is_deleted == is_deleted)


        if username is not None and username!='':
            query = query.where(cls.username == username)

        if platform is not None:
            if platform in dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT).keys():
                query=query.where(cls.platform==platform)
            else:
                print(f'there is no support for platform value yet:{platform}')

        if proxy is not None and proxy !='':
            query = query.where(cls.proxy == proxy)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_account = proxy.account  # This will fetch the associated Account

        try:
            print('==total record counts===',len(list(query)),list(query))
            for i in list(query):
                print(i.platform)
            print('==per page counts===',pagecount)
            print('==page number===',pageno)

            counts=len(list(query))
            if pageno:
                
                query=query.paginate(pageno, pagecount)
                print(f'==current pagi  {pageno} record counts===',len(list(query)))

            elif start and type(start)==int and type(start)==int:
                startpage=start/pagecount
                # and start<end                   
                # endpage=end/pagecount
                query=query.paginate(startpage, pagecount)
                print(f'==current pagi start {start} record counts===',len(list(query)))

            else:
                if pageno==None and start is None and end is None:
                    print(f'grab all records matching filters:{list(query)}')

            print('before return result=========')
            for i in list(query):
                print(i.platform)
                
            return list(query),counts

            
        except cls.DoesNotExist:
            query = None  # Set a default value or perform any other action

            return query,None



class AccountRelationship(BaseModel):
    id = BlobField(primary_key=True)    
    
    account = ForeignKeyField(AccountModel, backref='backup_relationships')
    backup_account = ForeignKeyField(AccountModel, backref='main_account_relationships')
    inserted_at = IntegerField(null=True)
    is_deleted = BooleanField(default=False)  # Flag if the account is deleted
    @classmethod

    def add_AccountRelationship_by_main_id(cls,main_id,otherid):
        new=AccountRelationship()

        if AccountModel.get_by_id(main_id)==None:
            return False
        elif AccountModel.get_by_id(otherid)==None:
            return False
        else:
            if len(cls.filter_AccountRelationship(main_id=main_id,otherid=otherid))>0:
                print('bind record is exsit now')
            else:
                if AccountModel.get_by_id(main_id):
                    new.account=AccountModel.get_by_id(main_id)
                if AccountModel.get_by_id(otherid):
                    new.backup_account=AccountModel.get_by_id(otherid)       

                new.inserted_at = int(time.time())  # Update insert_date
                new.id = CustomID().to_bin()
                new.is_deleted=False

                new.save(force_insert=True) 
                return True
    @classmethod

    def add_AccountRelationship_by_username(cls,main_username,otherusername):
        new=AccountRelationship()

        if AccountModel.get_account_by_username(main_username)==None:
            return False
        elif AccountModel.get_account_by_username(otherusername)==None:
            return False
        else:
            id=None
            otherid=None
            if AccountModel.get_account_by_username(otherusername):
                id=AccountModel.get_account_by_username(otherusername).id
            if AccountModel.get_account_by_username(otherusername):
                otherid=AccountModel.get_by_id(otherusername).id
                   
            cls.add_AccountRelationship_by_id(id=id,otherid=otherid)
            return True        
    @classmethod

    def get_AccountRelationship_by_id(cls, id):
        if AccountRelationship.get_by_id(id):
            
            return cls.get_or_none(cls.account == AccountRelationship.get_by_id(id))
    @classmethod
    def filter_AccountRelationship(cls, main_id=None, otherid=None,inserted_at=None,is_deleted=False,pageno=None,pagecount=None,start=None,end=None,data=None,ids=None,sortby=None):
        query = cls.select()
        if is_deleted is not None and is_deleted!='':
            query = query.where(cls.is_deleted == is_deleted)


        if main_id is not None and main_id!='':
            query = query.where(cls.account == main_id)


        if otherid is not None and otherid !='':
            query = query.where(cls.backup_account == otherid)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_account = proxy.account  # This will fetch the associated Account

        try:
            print('==total record counts===',len(list(query)),list(query))
            # for i in list(query):
            #     print(i.id)
            print('==per page counts===',pagecount)
            print('==page number===',pageno)

            counts=len(list(query))
            if pageno:
                
                query=query.paginate(pageno, pagecount)
                print(f'==current pagi  {pageno} record counts===',len(list(query)))

            elif start and type(start)==int and type(start)==int:
                startpage=start/pagecount
                # and start<end                   
                # endpage=end/pagecount
                query=query.paginate(startpage, pagecount)
                print(f'==current pagi start {start} record counts===',len(list(query)))

            else:
                if pageno==None and start is None and end is None:
                    print(f'grab all records matching filters:{list(query)}')

            print('before return result=========')
            # for i in list(query):
            #     print(i.id)
                
            return list(query),counts

            
        except cls.DoesNotExist:
            query = None  # Set a default value or perform any other action

            return query,None