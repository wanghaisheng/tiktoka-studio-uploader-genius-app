import time
import hashlib
import binascii
import env
# peewee 配置

from peewee import *
from playhouse.shortcuts import model_to_dict
# asyncpg 配置
# https://github.com/fy0/Icarus

# TODO: 连接池
asyncpg_conn = None

# DATABASE_URI=f'{mode}.sqlite3'
# # DATABASE_URI = f'sqlite:///{mode}.sqlite3'

# def connect(db_uri):

#     db = SqliteDatabase(db_uri
#                         # , 
#         #                 pragmas={
#         # 'journal_mode': 'wal',  # WAL-mode.
#         # 'cache_size': -64 * 1000,  # 64MB cache.
#         # 'synchronous': 0}
#                         )  # Let the OS manage syncing.
#     return db


db = DatabaseProxy()

# db = connect(DATABASE_URI)


class CITextField(TextField):
    field_type = 'CITEXT'


class SerialField(IntegerField):
    field_type = 'SERIAL'


class INETField(TextField):
    # 临时解决方案，peewee 的 custom field 有点问题
    field_type = 'inet'


class MyTimestampField(BigIntegerField):
    pass




class BaseModel(Model):
    class Meta:
        if env.mode == 'production':
            database = env.config['prod']
        else:
            database = ThreadSafeDatabaseMetadata        


    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_by_pk(cls, value):
        try:
            return cls.get(cls._meta.primary_key == value)
        except cls.DoesNotExist:
            return

    @classmethod
    def exists_by_pk(cls, value):
        return cls.select().where(cls._meta.primary_key == value).exists()


def get_time():
    return int(time.time())


class StdModel(BaseModel):
    id = BlobField(primary_key=True)
    time = BigIntegerField(index=True, default=get_time)
    deleted_at = BigIntegerField(null=True, index=True)

    is_for_tests = BooleanField(default=False, help_text='单元测试专属账号，单元测试结束后删除')


class StdUserModel(StdModel):
    user_id =BlobField(index=True, null=True, help_text='创建者用户ID')
