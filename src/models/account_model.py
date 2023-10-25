from peewee import Model, BooleanField, TextField,IntegerField,ForeignKeyField,BlobField
from src.models import BaseModel,db
import config
import time
from src.customid import CustomID

class AccountModel(BaseModel):
    id = BlobField(primary_key=True)    
    platform = IntegerField()
    username = TextField()
    password = TextField(null=True)  
    cookie_local_path = TextField(null=True)   
    cookie_content = TextField(null=True)   
    proxy = TextField(null=True)
    inserted_at = IntegerField(null=True)
    is_deleted = BooleanField(default=False)  # Flag if the account is deleted
    unique_hash = TextField(index=True,unique=True, null=True, default=None)  # Unique hash for the account

    # class Meta:
    #     db_table = db
    @classmethod

    def add_account(cls,account_data):
        unique_hash = config.generate_unique_hash(

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
    
    def update_account(cls, id,account_data, **kwargs):
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
    def filter_accounts(cls, platform=None, username=None, proxy=None,is_deleted=None):
        query = cls.select()
    
        if is_deleted is not None and is_deleted!='':
            query = query.where(cls.is_deleted == is_deleted)
        if platform is not None and platform !='':
            query = query.where(cls.platform == platform)

        if username is not None and username!='':
            query = query.where(cls.username == username)

        if proxy is not None and proxy !='':
            query = query.where(cls.proxy == proxy)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_account = proxy.account  # This will fetch the associated Account

        try:
            result = list(query)
            
        except AccountModel.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result



class AccountRelationship(BaseModel):
    account = ForeignKeyField(AccountModel, backref='backup_relationships')
    backup_account = ForeignKeyField(AccountModel, backref='main_account_relationships')

    @classmethod

    def add_AccountRelationship_by_id(cls,main_id,otherid):
        new=AccountRelationship()

        if AccountModel.get_by_id(main_id)==None:
            return False
        elif AccountModel.get_by_id(otherid)==None:
            return False
        else:
            if AccountModel.get_by_id(main_id):
                new.account=AccountModel.get_by_id(main_id)
            if AccountModel.get_by_id(otherid):
                new.backup_account=AccountModel.get_by_id(otherid)            
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

    def get_AccountRelationship_by_id(cls, account_id):
        if AccountModel.get_by_id(account_id):
            
            return cls.get_or_none(cls.account == AccountModel.get_by_id(account_id))
    @classmethod
    
    def get_AccountRelationship_by_username(cls, username):
        if AccountModel.get_account_by_username(username):
            
            return cls.get_or_none(cls.account == AccountModel.get_account_by_username(username))