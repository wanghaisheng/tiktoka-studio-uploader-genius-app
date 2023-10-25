# from peewee import Metadata

# class ThreadSafeDatabaseMetadata(Metadata):
#     def __init__(self, *args, **kwargs):
#         self._local = threading.local()
#         super(ThreadSafeDatabaseMetadata, self).__init__(*args, **kwargs)

#     def _get_db(self):
#         return getattr(self._local, 'database', self._database)
#     def _set_db(self, db):
#         self._local.database = self._database = db
#     database = property(_get_db, _set_db)

# class BaseModel(Model):
#     class Meta:
#         model_metadata_class = ThreadSafeDatabaseMetadata
        
from peewee import SqliteDatabase, ForeignKeyField, Model

class TableA(Model):
    pass

class TableB(Model):
    pass

class TableAB(Model):
    field1 = ForeignKeyField(TableA)
    field2 = ForeignKeyField(TableB)

master = SqliteDatabase(':memory:')
replica=SqliteDatabase(':memory:')
print('before', TableA._meta.database)
with master.bind_ctx([TableA, TableB]):
    print('inside A', TableA._meta.database)
print('after', TableA._meta.database)    
with replica.bind_ctx([TableA, TableB]):
    print('inside A', TableA._meta.database)
    
