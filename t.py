from peewee import *
db = SqliteDatabase('people.db')

db.connect()
class PROXY_STATUS:
    VALID = 0
    INVALID = 1
    UNCHEKCED = 2

    PROXY_PROTOCOL_TEXT = [
        (VALID, "VALID"),
        (INVALID, "INVALID"),
        (UNCHEKCED, "UNCHEKCED"),
    ]
    
    
class PROXY_PROTOCOL:
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    SOCKS5 = 'SOCKS5'

    PROXY_PROTOCOL_TEXT = [
        (HTTP, "HTTP"),
        (HTTPS, "HTTPS"),
        (SOCKS5, "SOCKS5"),
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


class ProxyModel(Model):
    id = IntegerField(primary_key=True)    
    inserted_at = IntegerField(null=True)    
    # Proxy Protocol (HTTP/HTTPS/SOCKS5)
    proxy_protocol = IntegerField(choices=PROXY_PROTOCOL)
    
    # Proxy Type
    proxy_provider_type = IntegerField(default=PROXY_PROVIDER_TYPE.CUSTOM,null=True)
    
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
    

    
    tags = TextField(null=True)
    status = IntegerField(default=PROXY_STATUS.UNCHEKCED)

    # Proxy network
    proxy_validate_network_type = CharField(null=True)
    proxy_validate_server = TextField(null=True)
    #json保存多个核对结果 核对服务器url：核对结果json字符串
    proxy_validate_results = TextField(null=True)
    is_deleted = BooleanField(default=False)  # Add a field to flag if video is deleted
    unique_hash = TextField(index=True, unique=True, null=True, default=None)  # Add this line

    class Meta:
        database = db # This model uses the "people.db" database.

    def filter_proxies(country=None, state=None, city=None, tags=None, status=None, network_type=None):
        query = ProxyModel.select()
        print('===',country,state,city,tags,status,network_type)
        
        if country is not None:
            query = query.where(ProxyModel.country == country)

        if state is not None:
            query = query.where(ProxyModel.state == state)

        if city is not None:
            query = query.where(ProxyModel.city == city)

        if tags is not None:
            query = query.where(ProxyModel.tags == tags)

        if status is not None:
            query = query.where(ProxyModel.status == status)

        if network_type is not None:
            query = query.where(ProxyModel.proxy_validate_network_type == network_type)
        try:
            result = list(query)
            
        except ProxyModel.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result


        
db.create_tables([ProxyModel])


proxy_data = {
    'proxy_protocol': 'socks5',
    'proxy_provider_type': 0,
    'proxy_host': '127.0.0.1',
    'proxy_port': '1080',
    'proxy_username': None,
    'proxy_password': None,
    'ip_address': '127.0.0.1',
    'country': None,
    'tags': 'youtube',
    'status': 2,
    'proxy_validate_network_type': None,
    'proxy_validate_server': None,
    'proxy_validate_results': None,
                }
# ProxyModel.add_proxy(proxy_data=proxy_data)
t1 = ProxyModel.create(id= 1,proxy_protocol='socks5',proxy_host='127.0.0.0', proxy_port='1080', status=0)
t12 = ProxyModel.create(id= 2,proxy_protocol='socks5',proxy_host='127.0.0.1', proxy_port='1080', status=1)
t13 = ProxyModel.create(id= 3,proxy_protocol='socks5',proxy_host='127.0.0.2', proxy_port='1080', status=2)
t2 = ProxyModel.create(id= 4,proxy_protocol='socks5',proxy_host='127.0.0.2', proxy_port='1082', status=1)
t3 = ProxyModel.create(id= 5,proxy_protocol='socks5',proxy_host='127.0.0.3', proxy_port='1083', status=2)

for person in ProxyModel.select():
    print(person.proxy_host,person.proxy_port,person.status)
# give 3 result
for person in ProxyModel.filter_proxies(status=2):
    print(person.proxy_host,person.proxy_port,person.status)