from peewee import BaseModel, CharField, IntegerField,TextField,BooleanField,BlobField,ForeignKeyField,DateTimeField,TimeField,DecimalField,JSONField
import time
from uploadergenius.utils.tools import  generate_unique_hash
from uploadergenius.server.models import BaseModel,db
from uploadergenius.server.models.proxy_model import ProxyModel
from uploadergenius.utils.customid import CustomID
# https://whoer.net
class IPAddress(BaseModel):
    hostname = CharField(null=True)
    reversed = CharField(null=True)
    mail_server = CharField(null=True)
    ip_range = CharField(default="154.84.1.0 - 154.84.1.255")
    isp = CharField(default="Multacom Corporation")
    organization = CharField(default="Multacom Corporation")
    as_organization = CharField(default="YISP B.V.")
    as_number = IntegerField(default=58073)
# Sample data entry
IPAddress.create(
    hostname=None,
    reversed=None,
    mail_server=None,
    ip_range="154.84.1.0 - 154.84.1.255",
    isp="Multacom Corporation",
    organization="Multacom Corporation",
    as_organization="YISP B.V.",
    as_number=58073
)



class Navigator(BaseModel):
    vendor_sub = CharField()
    product_sub = CharField()
    vendor = CharField()
    max_touch_points = IntegerField()
    pdf_viewer_enabled = BooleanField()
    hardware_concurrency = IntegerField()
    cookie_enabled = BooleanField()
    app_code_name = CharField()
    app_name = CharField()
    app_version = CharField()
    platform = CharField()
    product = CharField()
    user_agent = TextField()
    language = CharField()
    on_line = BooleanField()
    webdriver = BooleanField()
    device_memory = IntegerField()
Navigator.create(
    vendor_sub="20030107",
    product_sub="20030107",
    vendor="Google Inc.",
    max_touch_points=0,
    pdf_viewer_enabled=True,
    hardware_concurrency=8,
    cookie_enabled=True,
    app_code_name="Mozilla",
    app_name="Netscape",
    app_version="5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    platform="MacIntel",
    product="Gecko",
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    language="zh-CN",
    on_line=True,
    webdriver=False,
    device_memory=8
)

class Plugin(BaseModel):
    pdf_viewer = CharField()
    chrome_pdf_viewer = CharField()
    chromium_pdf_viewer = CharField()
    microsoft_edge_pdf_viewer = CharField()
    webkit_builtin_pdf = CharField()
# Sample data entry
Plugin.create(
    pdf_viewer="internal-pdf-viewer",
    chrome_pdf_viewer="internal-pdf-viewer",
    chromium_pdf_viewer="internal-pdf-viewer",
    microsoft_edge_pdf_viewer="internal-pdf-viewer",
    webkit_builtin_pdf="internal-pdf-viewer"
)


class TimeInfo(BaseModel):
    timezone = CharField()
    local_time = DateTimeField()
    system_time = DateTimeField()
    utc_time = DateTimeField()
    gmt_time = DateTimeField()
    daylight_saving_time = BooleanField()
    sunrise_time = TimeField()
    sunset_time = TimeField()


# Sample data entry
TimeInfo.create(
    timezone="Asia/Shanghai",
    local_time="2023-10-16 15:48:55",
    system_time="2023-10-16 21:52:08",
    utc_time="2023-10-16 13:48:55",
    gmt_time="2023-10-16 13:48:55",
    daylight_saving_time=True,
    sunrise_time="08:07:12",
    sunset_time="18:44:48"
)

class Location(BaseModel):
    country = CharField()
    country_code=CharField()
    continent = CharField()
    continent_code = CharField()
    region = CharField()
    subdivision_code = CharField()
    city = CharField()
    as_organization = CharField()
    as_number = IntegerField()
    zone = CharField()
    latitude = DecimalField(max_digits=10, decimal_places=6)
    longitude = DecimalField(max_digits=10, decimal_places=6)
    map_url = TextField()
Location.create(
    country="China",
    country_code="CN",
    continent="Asia",
    continent_code="AS",
    region="Guangdong",
    subdivision_code="GD",
    city="Foshan",
    as_organization="YISP B.V.",
    as_number=58073,
    zone="Asia/Shanghai",
    latitude=23.0261,
    longitude=113.1371,
    map_url="https://example.com/map"
)
class ScriptInfo(BaseModel):
    javascript = CharField()
    flash = CharField()
    java = CharField()
    activex = CharField()
    webrtc = CharField()
    vbscript = CharField()
    adblock = CharField()
# Sample data entry
ScriptInfo.create(
    javascript="enabled",
    flash="disabled",
    java="disabled",
    activex="disabled",
    webrtc="enabled",
    vbscript="disabled",
    adblock="disabled"
)

class InteractiveDetection(BaseModel):
    INTERACTIVE_DETECTION = CharField()
    RUN_TESTS = CharField()
    IP_ADDRESS = CharField()
    ISO = CharField()
    FLASH = CharField()
    WEBRTC = CharField()
    JAVA_TCP = CharField()
    JAVA_UDP = CharField()
    JAVA_SYSTEM = CharField()
    DNS = JSONField()  # Treat DNS as a JSON field
    BROWSER = CharField()
    
    # https://pixelscan.net/ip
class ProxyResults(BaseModel):
    Proxy_detection = BooleanField()
    Rotating_proxy_detection = BooleanField()
    MTU_fingerprint_NMAP = IntegerField()
    MTU_fingerprint = CharField()
# Populate the data
data = [
    { "Proxy_detection": False, "Rotating_proxy_detection": False, "MTU_fingerprint_NMAP": 0, "MTU_fingerprint": 
"DSL(1452"}
    # Add more data as needed...
]
class OSDetection(BaseModel):
    OS = CharField()
    Detected_OS = CharField()
    TCP_IP_OS_NMAP = CharField()
    TCP_IP_OS = CharField()
data = [
    {"OS": "Mac OS", "Detected_OS": "Mac OS", "TCP_IP_OS_NMAP": "N/A", "TCP_IP_OS": "Mac OS X (generic fuzzy)"},
    # Add more data as needed...
]

# https://www.astrill.com/vpn-leak-test
# Define the basemodel
class astrillDNSServer(BaseModel):
    IP = CharField()
    ISP = CharField()
    COUNTRY = CharField()
        # You are using DNS servers from different country and belonging to different ISP.

# Populate the data
data = [
    {"IP": "74.125.186.202", "ISP": "Google LLC", "COUNTRY": "United States"},
    {"IP": "172.69.133.123", "ISP": "CloudFlare Inc.", "COUNTRY": "United States"},
    {"IP": "112.25.12.136", "ISP": "China Mobile Communications Corporation", "COUNTRY": "China"},
    {"IP": "112.25.12.139", "ISP": "China Mobile Communications Corporation", "COUNTRY": "China"},
    {"IP": "112.25.12.149", "ISP": "China Mobile Communications Corporation", "COUNTRY": "China"},
    # Add more data as needed...
]
    
# Define the basemodel
class astrillLeakDetection(BaseModel):
    IPv6_leaked = CharField()
    Java_status = CharField()
    Flash_status = CharField()
    WebRTC_status = CharField()
    DNS_Leak_status = CharField()
    
# Populate the data
data = [
    {"IPv6_leaked": "2a02:2a38:1:2796:ec4:7aff:fe81:77bai", 
     "Java_status": "Java is:disabled",
     "Flash_status": "Flash is: disabled",
     "WebRTC_status": "WebRTC revealed IP: no IP",
     "DNS_Leak_status": "HTTP Headers revealed: no info"}
    # Add more data as needed...
]

# Define the basemodel
class WhoerResult(BaseModel):
    ISP = CharField()
    Hostname = CharField()
    OS = CharField()
    Browser = CharField()
    Hide_DNS = CharField()
    Proxy = CharField()
    Anonymizer = CharField()
    Blacklist = CharField()
    LANGUAGE = CharField()
    FLAG = CharField()
    IP = CharField()
    WEBRTC = CharField()
    JAVASCRIPT = CharField()
    FLASH = CharField()
    ACTIVEX = CharField()
    JAVA = CharField()
    COOKIES = CharField()



# Populate the data
data = [
    {
        "ISP": "Peg Tech", 
        "Hostname": "N/A", 
        "OS": "Mac OS X", 
        "Browser": "Chrome 117.0", 
        "Hide_DNS": "172.69.133.5410  United States", 
        "Proxy": "No", 
        "Anonymizer": "No", 
        "Blacklist": "No", 
        "LANGUAGE": "flag-cn.svgCN", 
        "FLAG": "flag-cn.svg", 
        "IP": "154.84.1.216", 
        "WEBRTC": "Enabled", 
        "JAVASCRIPT": "Enabled", 
        "FLASH": "Disabled", 
        "ACTIVEX": "Disabled", 
        "JAVA": "Disabled", 
        "COOKIES": "Enabled"
    }
    # Add more data as needed...
]

# Define the basemodel
class PixelResult(BaseModel):
    Hostname = CharField()
    ISP = CharField()
    Static_IP_Score = DecimalField(max_digits=5, decimal_places=2)
    User_Type_By_IP = CharField()
    IP_Location = CharField()
    IP_Address_Clean = BooleanField()
    IP_Blacklisted = CharField()
    Timezone_From_Javascript = CharField()
    Time_From_Javascript = CharField()
    Time_From_IP = CharField()
    Daylight_Savings_Time = BooleanField()
    Detected_OS = CharField()
    TCP_IP_OS_NMAP = CharField()
    TCP_IP_OS = CharField()
    Geolocation_IP = CharField()
    Geolocation_API = CharField()



# Populate the data
data = [
    {
        "Hostname": "N/A",
        "ISP": "China Mobile",
        "Static_IP_Score": 11.3,
        "User_Type_By_IP": "residential",
        "IP_Location": "China/Xi'an",
        "IP_Address_Clean": True,
        "IP_Blacklisted": "IP is blacklisted in 8 databases",
        "Timezone_From_Javascript": "Asia/Shanghai",
        "Time_From_Javascript": "Mon Oct 16 2023 22:53:33 GMT+0800 (中国标准时间)",
        "Time_From_IP": "Mon Oct 16 2023 22:53:36 GMT+0800",
        "Daylight_Savings_Time": False,
        "Detected_OS": "Mac OS",
        "TCP_IP_OS_NMAP": "N/A",
        "TCP_IP_OS": "N/A",
        "Geolocation_IP": "34.3287, 109.0337",
        "Geolocation_API": "Geo API check was blocked."
    }
    # Add more data as needed...
]
    
    
# https://browserleaks.com/ip


# Define the basemodel
class browserleakscomIPInformation(BaseModel):
    IP_address = CharField()
    Hostname = CharField()
    Country = CharField()
    State_Region = CharField()
    City = CharField()
    ISP = CharField()
    Organization = CharField()
    Network = CharField()
    Usage_Type = CharField()
    Timezone = CharField()
    Local_Time = CharField()
    Coordinates = CharField()
    IPv6_Address = CharField()
    WebRTC_Local_IP = CharField()
    WebRTC_Public_IP = CharField()
    OS = CharField()
    Link = CharField()
    MTU = IntegerField()
    Distance = IntegerField()
    TLS_JA3_Hash = CharField()
    HTTP2_Akamai_Hash = CharField()
    HTTP_Headers = TextField()
    Tor_Relay = BooleanField()
    Source_Registry = CharField()
    Net_Range = CharField()
    CIDR = CharField()
    Name = CharField()
    Handle = CharField()
    Net_Type = CharField()
    Registration_Date = CharField()
    Last_Changed_Date = CharField()
    Description = TextField()
    Full_Name = CharField()
    Entity_Roles = CharField()
    Email = CharField()
    Telephone = CharField()
    Address = TextField()
    Remarks = TextField()


class browserleakscomWebRTCLeakTest(BaseModel):
    # ... (previous fields)
    WebRTC_RTCPeerConnection = BooleanField()
    WebRTC_RTCDataChannel = BooleanField()
    WebRTC_Leak_Test_Result = CharField()
    WebRTC_Local_IP = CharField()
    WebRTC_Public_IP = CharField()
    WebRTC_Remote_IPv4 = CharField()
    WebRTC_Remote_IPv6 = CharField()

# Your Remote IP
# IPv4 Address	111.18.153.195
# IPv6 Address	-
# WebRTC Support Detection
# RTCPeerConnection	✔True
# RTCDataChannel	✔True
# Your WebRTC IP
# WebRTC Leak Test	✔No Local IP Leak
# !WebRTC IP doesn't match your Remote IP
# Local IP Address	-
# Public IP Address	

# 154.84.1.216

# 140.238.28.22

class IPInfoResults(BaseModel):
    # ... (previous fields)
    Ip = CharField()
    
    City = CharField()
    Region = CharField()
    Country = CharField()
    Location = CharField()
    Organization_ASN = CharField()
    Organization_Name = CharField()
    Organization_Domain = CharField()
    Organization_Type = CharField()
    Timezone = CharField()
    ASN = CharField()
    ASN_Name = CharField()
    ASN_Domain = CharField()
    ASN_Route = CharField()
    ASN_Type = CharField()
    Privacy_VPN = BooleanField()
    Privacy_Proxy = BooleanField()
    Privacy_Tor = BooleanField()
    Privacy_Relay = BooleanField()
    Privacy_Hosting = BooleanField()
    Privacy_Service = CharField()
    Abuse_Address = TextField()
    Abuse_Country = CharField()
    Abuse_Email = CharField()
    Abuse_Name = CharField()
    Abuse_Network = CharField()
    Abuse_Phone = CharField()
# Populate the data
data = [
    {
        # ... (previous data)
        "City": "Zhanjiang",
        "Region": "Guangdong",
        "Country": "CN",
        "Location": "21.2339,110.3875",
        "Organization_ASN": "AS9808",
        "Organization_Name": "China Mobile Communications Group Co., Ltd.",
        "Organization_Domain": "10086.cn",
        "Organization_Type": "isp",
        "Timezone": "Asia/Shanghai",
        "ASN": "AS9808",
        "ASN_Name": "China Mobile Communications Group Co., Ltd.",
        "ASN_Domain": "10086.cn",
        "ASN_Route": "111.18.0.0/16",
        "ASN_Type": "isp",
        "Privacy_VPN": False,
        "Privacy_Proxy": False,
        "Privacy_Tor": False,
        "Privacy_Relay": False,
        "Privacy_Hosting": False,
        "Privacy_Service": "",
        "Abuse_Address": "China Mobile Communications Corporation, 29, Jinrong Ave., Xicheng District, Beijing, 100032",
        "Abuse_Country": "CN",
        "Abuse_Email": "abuse@chinamobile.com",
        "Abuse_Name": "ABUSE CHINAMOBILECN",
        "Abuse_Network": "111.0.0.0/10",
        "Abuse_Phone": "+000000000"
    }
    # Add more data as needed...
]
class WhoerCity():
    id = BlobField(primary_key=True)    
    proxy = ForeignKeyField(ProxyModel, backref='backup_relationships')
    data=JSONField(null=True)

# data={"city_name":null,"continent_code":"NA","continent_name":"North America","country_code":"US","country_name":"United States","european_union":0,"geoname":6252001,"latitude":37.751,"longitude":-97.822,"metro_code":null,"network":"198.2.192.0\/19","postal_code":null,"register_country_code":null,"register_country_name":null,"represent_country_code":null,"represent_country_name":null,"subdivision1_code":null,"subdivision1_name":null,"subdivision2_code":null,"subdivision2_name":null,"time_zone":"America\/Chicago"}{"city_name":null,"continent_code":"NA","continent_name":"North America","country_code":"US","country_name":"United States","european_union":0,"geoname":6252001,"latitude":37.751,"longitude":-97.822,"metro_code":null,"network":"198.2.192.0\/19","postal_code":null,"register_country_code":null,"register_country_name":null,"represent_country_code":null,"represent_country_name":null,"subdivision1_code":null,"subdivision1_name":null,"subdivision2_code":null,"subdivision2_name":null,"time_zone":"America\/Chicago"}
class WhoerIsp():
    id = BlobField(primary_key=True)    
    proxy = ForeignKeyField(ProxyModel, backref='backup_relationships')
    data=JSONField(null=True)

# {"as_number":21887,"as_organization":"FIBER-LOGIC","isp":"Fiber-logic","network":"64.64.224.0\/19","organization":"Fiber-logic"}


# https://whoer.net/v2/geoip2-isp

class AntiDetectResult(BaseModel):

# IPV4地址泄露
#住宅 vs服务器 黑名单
# 如何检查自己的 IP 是机房还是住宅 IP 呢，可以登录 ipinfo.io 看。网站是有可能检查你的运营商从而判断你的真实性的。
#hosting：false为住宅

# IPV6地址泄露

# DNS泄露

# WebRTC泄露

# HTTPHeader信息泄露
# 时间泄露
#端口泄露

#网速 https://mp.weixin.qq.com/s/lXqsrGQCJyPe_73450twVg
# 我在 whatleaks 里的指标还有一项是异常的，那就是 Ping 值。网络速度也会影响砍单与否。因为你的网络速度明显慢于那个城市访问目标网站的平均速度，于是目标网站把你当成是使用代理的人。这也就是为什么有些人用 VPS 下单可能成功概率高一点，因为 VPS 访问目标网站的速度很快。


    class Meta:
        database =db

