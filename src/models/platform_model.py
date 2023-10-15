from peewee import Model, CharField, TextField,IntegerField,BlobField
from src.models import BaseModel,db

class PLATFORM_TYPE:
    YOUTUBE = 1
    TIKTOK = 2

    PLATFORM_TYPE_TEXT = [
        (YOUTUBE, "youtube"),
        (TIKTOK, "other"),
    ]

class PlatformModel(BaseModel):
    id = BlobField(primary_key=True)    
    name = IntegerField()
    type= IntegerField(default=PLATFORM_TYPE.YOUTUBE)
    server = TextField(default=None)
    inserted_at = IntegerField(null=True)

    class Meta:
        db_table = db
#     class Meta:
#         database = your_database_instance  # Replace with your actual database connection

# # Assuming you have a database connection already set up
# # db = your_database_connection

# # Connect the model to your database
# Account.bind(db)

# # Create the tables if they don't exist
# Account.create_table()
