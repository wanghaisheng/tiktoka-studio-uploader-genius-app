from peewee import Model, CharField, IntegerField,TextField,BooleanField,BlobField,ForeignKeyField
import time
import config
from src.models import BaseModel,db
from src.models.account_model import AccountModel
from src.customid import CustomID

class PROXY_STATUS:
    VALID = 0
    INVALID = 1
    UNCHEKCED = 2

    PROXY_STATUS_TEXT = [
        (VALID, "VALID"),
        (INVALID, "INVALID"),
        (UNCHEKCED, "UNCHEKCED"),
    ]
    
    
class IP_TYPE:
    IPv4 = 1
    IPv6 = 2

    IP_TYPE_TEXT = [
        (IPv4, "IPv4"),
        (IPv6, "IPv6")
    ]
class IP_SOURCE_TYPE:
    mobile = 1
    residential  = 2
    datacenter  = 3

    IP_SOURCE_TYPE_TEXT = [
        (mobile, "mobile"),
        (residential, "residential"),
        (datacenter, "datacenter"),

    ]



class PROXY_PROTOCOL:
    HTTP = 'http'
    HTTPS = 'https'
    SOCKS5 = 'socks5'

    PROXY_PROTOCOL_TEXT = [
        (HTTP, "http"),
        (HTTPS, "https"),
        (SOCKS5, "socks5"),
    ]

class PROXY_PROVIDER_TYPE:
    CUSTOM =0
    BRIGHT_DATA = 1
    IP_FOXY = 2
    IP_IDEA = 3
    OXYLABS = 4
    KOOKEEY = 5
    IPIP_GO = 6
    IPFLY = 7
    NETNUT = 8
    PROXY_302 = 9
    IP007 = 10
    LUNA_PROXY = 11
    S5_PROXY = 12
    PIA_S5_PROXY = 13

    PROXY_PROVIDER_TYPE_TEXT = [
        (CUSTOM, "custom"),
        (BRIGHT_DATA, "BrightData"),
        (IP_FOXY, "IPFoxy"),
        (IP_IDEA, "IPIDEA"),
        (OXYLABS, "Oxylabs"),
        (KOOKEEY, "kookeey"),
        (IPIP_GO, "ipipgo"),
        (IPFLY, "IPFLY"),
        (NETNUT, "netnut"),
        (PROXY_302, "Proxy302"),
        (IP007, "IP007"),
        (LUNA_PROXY, "LunaProxy"),
        (S5_PROXY, "922S5 Proxy"),
        (PIA_S5_PROXY, "PIA S5 Proxy"),
    ]


class ProxyModel(BaseModel):
    id = BlobField(primary_key=True)    
    inserted_at = IntegerField(null=True)    
    # Proxy Protocol (HTTP/HTTPS/SOCKS5)
    proxy_protocol = CharField(choices=PROXY_PROTOCOL)
    
    # Proxy provider Type
    proxy_provider_type = IntegerField(default=PROXY_PROVIDER_TYPE.CUSTOM)
    
    # Proxy Host
    proxy_host = CharField()
    
    # Proxy Port
    proxy_port = IntegerField()
    
    # Proxy Username
    proxy_username = CharField(null=True)
    
    # Proxy Password
    proxy_password = CharField(null=True)
    
    # IP Address
    ip_address = CharField(null=True)
    
    # Country/Region
    country = CharField(null=True)
    
    # State/Province
    state = CharField(null=True)
    
    # City
    city = CharField(null=True)
    
    ip_type = IntegerField(default=IP_TYPE.IPv4)
    network_type = IntegerField(default=IP_SOURCE_TYPE.datacenter)

    
    tags = TextField(null=True)
    status = IntegerField(default=PROXY_STATUS.UNCHEKCED)

    # Proxy network
    proxy_validate_server = TextField(null=True)
    #json保存多个核对结果 核对服务器url：核对结果json字符串
    proxy_validate_results = TextField(null=True)
    is_deleted = BooleanField(default=False)  # Add a field to flag if video is deleted
    unique_hash = TextField(index=True, unique=True, null=True, default=None)  # Add this line
    inserted_at = IntegerField(null=True)

    # class Meta:
    #     db_table = db


    @classmethod
    def add_proxy(cls,proxy_data):

        
        unique_hash = config.generate_unique_hash(proxy_data)

        # Check if a proxy with the same unique hash already exists
        existing_proxy = cls.select().where(cls.unique_hash == unique_hash).first()
        print(f'existing_proxy:{existing_proxy}')
        if existing_proxy is None:    
            proxy = cls(**proxy_data)
            proxy.inserted_at = int(time.time())  # Update insert_date
            proxy.unique_hash=unique_hash
            proxy.id = CustomID().to_bin()

            proxy.save(force_insert=True) 

            return proxy
        else:
            return cls.get_proxy_by_id(id=existing_proxy)
    # Read (Select) Proxy by ID
    @classmethod

    def get_proxy_by_id(cls,id):
        try:
            proxy = ProxyModel.get(ProxyModel.id ==id)
            return proxy
        except ProxyModel.DoesNotExist:
            return None

    # Update Proxy by ID
    @classmethod

    def update_proxy(cls,id,proxy_data=None,**kwargs):
        try:
            proxy = ProxyModel.get(ProxyModel.id ==id)
            if proxy_data:
                proxy = ProxyModel(**proxy_data)
                print('after modify',proxy,proxy.is_deleted)
            

            else:
                for key, value in kwargs.items():
                    # 由于entry获取的都是字符串变量值，对于bool型，需要手动转换
                    if key=='is_deleted':
                        print('is deleted',type(value))
                        if value=='0':
                            value=False
                        elif value=='1':
                            value=True
                    setattr(proxy, key, value)
                    
                print('after modify',proxy,proxy.is_deleted)
            proxy.inserted_at = int(time.time())  # Update insert_date

            proxy.save() 
            return proxy
        except ProxyModel.DoesNotExist:
            return None
    @classmethod

    # Delete (Soft Delete) Proxy by ID
    def delete_proxy(cls,id):
        try:
            proxy = ProxyModel.get(ProxyModel.id ==id)
            proxy.is_deleted = True
            
            proxy.save() 
            return True
        except ProxyModel.DoesNotExist:
            return False
    @classmethod
     
    # Assuming you have a list of proxy data named proxy_list
    def bulk_add_proxies(cls,proxy_list):
        inserted_proxies = []
        for proxy_data in proxy_list:
            # Calculate unique hash for the proxy
            unique_hash = config.generate_unique_hash(proxy_data)

            # Check if a proxy with the same unique hash already exists
            existing_proxy = ProxyModel.select().where(ProxyModel.unique_hash == unique_hash).first()

            if existing_proxy is None:
                # Create a new proxy
                proxy = ProxyModel(**proxy_data, unique_hash=unique_hash)
                proxy.inserted_at = int(time.time())
                proxy.save(force_insert=True) 
                inserted_proxies.append(proxy)

        return inserted_proxies

    @classmethod

    def filter_proxies(cls,country=None, state=None, city=None, tags=None, status=None, network_type=None,
                       pageno=None,pagecount=None,start=None,end=None,data=None,ids=None,sortby=None):
        query = cls.select()
        print('===',country,state,city,tags,status,network_type)

        # for person in cls.select():
        #     print(person)

        if country is not None and country!='':
            query = query.where(cls.country == country)

        if state is not None and state!='':
            query = query.where(cls.state == state)

        if city is not None and city!='':
            query = query.where(cls.city == city)

        if tags is not None and tags!='':
            query = query.where(cls.tags == tags)

        if status is not None and status!='':
            query = query.where(cls.status == status)

        if network_type is not None and network_type!='':
            query = query.where(cls.network_type == network_type)
        try:
            result = list(query)
            
        except cls.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result



