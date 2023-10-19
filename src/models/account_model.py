from peewee import Model, BooleanField, TextField,IntegerField,ForeignKeyField,BlobField
from src.models import BaseModel,db
import config
import time
from src.customid import CustomID

class AccountModel(BaseModel):
    id = BlobField(primary_key=True)    
    platform = IntegerField()
    username = TextField()
    password = TextField()  
    cookies = TextField()   
    proxy = TextField()
    inserted_at = IntegerField(null=True)
    is_deleted = BooleanField(default=False)  # Flag if the account is deleted
    unique_hash = TextField(index=True, unique=True, null=True, default=None)  # Unique hash for the account

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
            account.insert_date = int(time.time())  # Update insert_date
            account.unique_hash=unique_hash
            # proxy.id = CustomID().to_bin()

            account.save()
            return True
            
        else:
            return False

    @classmethod
    def get_account_by_id(cls, account_id):
        return cls.get_or_none(cls.id == account_id)

    @classmethod
    def update_account(cls, account_id, **kwargs):
        try:
            account = cls.get(cls.id == account_id)
            for key, value in kwargs.items():
                setattr(account, key, value)
            account.save()
            return account
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_account(cls, account_id):
        try:
            account = cls.get(cls.id == account_id)
            account.delete_instance()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def filter_accounts(cls, platform=None, username=None, proxy=None):
        query = cls.select()

        if platform is not None:
            query = query.where(cls.platform == platform)

        if username is not None:
            query = query.where(cls.username == username)

        if proxy is not None:
            query = query.where(cls.proxy == proxy)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_account = proxy.account  # This will fetch the associated Account

        try:
            result = list(query)
            
        except AccountModel.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result



class AccountRelationship(Model):
    account = ForeignKeyField(AccountModel, backref='backup_relationships')
    backup_account = ForeignKeyField(AccountModel, backref='main_account_relationships')

    class Meta:
        db_table = db
# # Assuming you have a database connection already set up
# # db = your_database_connection

# # Connect the model to your database
# Account.bind(db)

# # Create the tables if they don't exist
# Account.create_table()


