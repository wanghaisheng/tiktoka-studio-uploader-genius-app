from peewee import Model, CharField, TextField,IntegerField,ForeignKeyField,BlobField
from src.models import BaseModel,db

class AccountModel(Model):
    id = BlobField(primary_key=True)    
    platform = TextField()
    username = TextField()
    
    password = TextField()  # Assuming passwords might be long, use TextField
    cookies = TextField()   # Same for cookies
    proxy = TextField()
    inserted_at = IntegerField(null=True)


    class Meta:
        db_table = db

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


