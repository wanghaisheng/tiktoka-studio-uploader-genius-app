from peewee import Model, TextField, BooleanField, IntegerField,BlobField
class PLATFORM:
    YOUTUBE = 1
    TIKTOK = 2

    PLATFORM_TEXT = [
        (YOUTUBE, "youtube"),
        (TIKTOK, "other"),
    ]

class BROWSER_TYPE:

    CHROMIUM = 'chromium'
    FIREFOX = 'firefox'
    WEBKIT = 'webkit'

    BROWSER_TYPE_TEXT = [
        (CHROMIUM, "Chromium"),
        (FIREFOX, "Firefox"),
        (WEBKIT, "WebKit"),
    ]

    
class UploadSettingModel(BaseModel):
    id = BlobField(primary_key=True)    
    proxy_option = TextField()
    timeout = IntegerField(default=200000)
    is_open_browser = BooleanField(default=True)
    is_debug = BooleanField(default=True)
    platform = IntegerField(default=PLATFORM.YOUTUBE)
    username = TextField()
    password = TextField()
    browser_type = IntegerField()
    channel_cookie_path = TextField()
    is_record_video = BooleanField(default=True)

    class Meta:
        db_table = db


