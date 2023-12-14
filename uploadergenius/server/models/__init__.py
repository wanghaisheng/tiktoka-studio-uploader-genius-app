import time,re
import hashlib
import binascii

# peewee 配置

from peewee import *
from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import (SqliteExtDatabase)
from i18n_json import i18n_json

# asyncpg 配置
# https://github.com/fy0/Icarus

# TODO: 连接池
asyncpg_conn = None
mode='debug'

DATABASE_URI=f'{mode}.sqlite3'
# DATABASE_URI = f'sqlite:///{mode}.sqlite3'

def connect(db_uri):

    db = SqliteExtDatabase(db_uri
                        , regexp_function=True
                        # ,
        #                 pragmas={
        # 'journal_mode': 'wal',  # WAL-mode.
        # 'cache_size': -64 * 1000,  # 64MB cache.
        # 'synchronous': 0}
                        )  # Let the OS manage syncing.
    return db




db = connect(DATABASE_URI)
@db.func()
def regexp(expr, s):
    return re.search(expr, s) is not None

class CITextField(TextField):
    field_type = 'CITEXT'


class SerialField(IntegerField):
    field_type = 'SERIAL'


class INETField(TextField):
    # 临时解决方案，peewee 的 custom field 有点问题
    field_type = 'inet'


class MyTimestampField(BigIntegerField):
    pass

class SORT_BY_TYPE:
    ASC = 0
    DESC = 1
    SORT_BY_TYPE_TEXT = [
        (ASC, "Add DATE ASC"),
        (DESC, "Add DATE DESC")
    ]

class BaseModel(Model):
    class Meta:
        database = db

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
