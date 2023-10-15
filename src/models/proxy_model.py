import time
import config
from src.customid import CustomID
from sqlalchemy import create_engine, text
from sqlalchemy.orm.session import sessionmaker

from src.database import dbsession_test,dbsession_pro,Base
from sqlalchemy import Column, Integer, String,LargeBinary,Text,Boolean,Enum

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


class ProxyModel(Base):
    __tablename__ = 'proxymodel'
    id = Column(LargeBinary, primary_key=True)
    inserted_at = Column(Integer, nullable=True)
    proxy_protocol = Column(Enum(*[item[0] for item in PROXY_PROTOCOL.PROXY_PROTOCOL_TEXT]))
    proxy_provider_type = Column(Enum(*[item[1] for item in PROXY_PROVIDER_TYPE.PROXY_PROVIDER_TYPE_TEXT]))
    proxy_host = Column(String, nullable=True)
    proxy_port = Column(Integer, nullable=True)
    proxy_username = Column(String, nullable=True)
    proxy_password = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    city = Column(String, nullable=True)
    tags = Column(Text, nullable=True)
    status = Column(Integer, default=2)
    proxy_validate_network_type = Column(String, nullable=True)
    proxy_validate_server = Column(Text, nullable=True)
    proxy_validate_results = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False)
    unique_hash = Column(Text, unique=True, nullable=True, default=None)