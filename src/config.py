import hashlib
import binascii
import json
from src.customid import  CustomID

class SQLSerialGenerator:
    def __init__(self, val=b''):
        if isinstance(val, str):
            val = binascii.unhexlify(val)
        self.val = val

    def to_bin(self):
        return self.val
# 被数据库所使用的两个ID，短ID与长ID
POST_ID_GENERATOR = SQLSerialGenerator  # 代表SQL自动生成
LONG_ID_GENERATOR = CustomID    
def generate_unique_hash(data):
    if type(data)==dict:
        data=json.dumps(data)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
def append_id(values):
    """
    若有ID生成器，那么向values中添加生成出的值，若生成器为SQL Serial，则什么都不做
    :param values:
    :return:
    """
    if LONG_ID_GENERATOR != SQLSerialGenerator:
        values['id'] = CustomID().to_bin()

