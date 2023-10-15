from peewee import *
from src.models.proxy_model import *

db = SqliteDatabase('debug.db')
grandma = ProxyModel.select()

# grandma = ProxyModel.select().where(ProxyModel.status == 2).get()
print(grandma)