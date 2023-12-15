import time,base64,os
import peewee
from peewee import *
from src.config import generate_unique_hash
from src.models import BaseModel,db
from src.customid import CustomID
import logging
from src.log import logger




class WAIT_POLICY:
    GO_NEXT_UPLOAD_SUCCESS = 1
    GO_NEXT_PROCESSING_SUCCESS = 2
    GO_NEXT_COPYRIGHT_CHECK_SUCCESS=3
    # Mapping of options to human-readable text
    WAIT_POLICY_TEXT = {
        GO_NEXT_UPLOAD_SUCCESS: "Go next after uploading success",
        GO_NEXT_PROCESSING_SUCCESS: "Go next after processing success",
        GO_NEXT_COPYRIGHT_CHECK_SUCCESS: "Go next after copyright check success"
    }

class PUBLISH_POLICY_TYPE:
    Private = 1
    Publish = 2
    Schedule=3
    Unlisted=4
    # Mapping of options to human-readable text
    Public_Premiere=5
    # Publish Policy Options
    PUBLISH_POLICY_TYPE_TEXT = {
        Private:"Private",
        Publish:"Publish",
        Schedule:"Schedule",
        Unlisted:"Unlisted",
        Public_Premiere:"Public & Premiere"
    }
class VIDEO_CATEGORIES_OPTIONS:
    AutosVehicles= 15
    Comedy= 1
    Education= 2
    Entertainment= 3
    FilmAnimation= 4
    Gaming= 5
    HowtoStyle= 6
    Music= 7
    NewsPolitics= 8
    NonprofitsActivism= 9
    PeopleBlogs= 10
    PetsAnimals= 11
    ScienceTechnology= 12
    Sports= 13
    TravelEvents= 14

    
    # VIDEO_LANGUAGE_TEXT = {v: k for k, v in VIDEO_LANGUAGE_OPTIONS.items()}
    VIDEO_CATEGORIES_OPTIONS_TEXT = {
        AutosVehicles: "Autos & Vehicles",
        Comedy: "Comedy",
        Education: "Education",
        Entertainment: "Entertainment",
        FilmAnimation: "Film & Animation",
        Gaming: "Gaming",
        HowtoStyle: "Howto & Style",
        Music: "Music",
        NewsPolitics: "News & Politics",
        NonprofitsActivism: "Nonprofits & Activism",
        PeopleBlogs: "People & Blogs",
        PetsAnimals: "Pets & Animals",
        ScienceTechnology: "Science & Technology",
        Sports: "Sports",
        TravelEvents: "Travel & Events"
    }
    
class VIDEO_SETTINGS:
    # Wait Policy options
    GO_NEXT_UPLOAD_SUCCESS = 0
    GO_NEXT_PROCESSING_SUCCESS = 1
    GO_NEXT_COPYRIGHT_CHECK_SUCCESS = 2

    # License Type options
    STANDARD_YOUTUBE_LICENSE = 0
    CREATIVE_COMMONS_ATTRIBUTION = 1

    # Shorts Remixing Type options
    ALLOW_VIDEO_AND_AUDIO_REMIXING = 0
    ALLOW_ONLY_AUDIO_REMIXING = 1
    DONT_ALLOW_REMIXING = 2

    # Comments Ratings Policy options
    ALLOW_ALL_COMMENTS = 0
    HOLD_POTENTIALLY_INAPPROPRIATE_COMMENTS = 1
    INCREASE_STRICTNESS = 2
    HOLD_ALL_COMMENTS_FOR_REVIEW = 3
    DISABLE_COMMENTS = 4


    LICENSE_TYPE_TEXT = {
        STANDARD_YOUTUBE_LICENSE: "Standard YouTube License",
        CREATIVE_COMMONS_ATTRIBUTION: "Creative Commons - Attribution"
    }

    SHORTS_REMIXING_TYPE_TEXT = {
        ALLOW_VIDEO_AND_AUDIO_REMIXING: "Allow video and audio remixing",
        ALLOW_ONLY_AUDIO_REMIXING: "Allow only audio remixing",
        DONT_ALLOW_REMIXING: "Don’t allow remixing"
    }

    COMMENTS_RATINGS_POLICY_TEXT = {
        ALLOW_ALL_COMMENTS: "Allow all comments",
        HOLD_POTENTIALLY_INAPPROPRIATE_COMMENTS: "Hold potentially inappropriate comments for review",
        INCREASE_STRICTNESS: "Increase strictness",
        HOLD_ALL_COMMENTS_FOR_REVIEW: "Hold all comments for review",
        DISABLE_COMMENTS: "Disable comments"
    }
    VIDEO_LANGUAGE_OPTIONS = [
        "None",
        "Not applicable",
        "Abkhazian",
        "Afar",
        "Afrikaans",
        "Akan",
        "Akkadian",
        "Albanian",
        "American Sign Language",
        "Amharic",
        "Arabic",
        "Aramaic",
        "Armenian",
        "Assamese",
        "Aymara",
        "Azerbaijani",
        "Bambara",
        "Bangla",
        "Bashkir",
        "Basque",
        "Belarusian",
        "Bhojpuri",
        "Bislama",
        "Bodo",
        "Bosnian",
        "Breton",
        "Bulgarian",
        "Burmese",
        "Cantonese",
        "Cantonese (Hong Kong)",
        "Catalan",
        "Cherokee",
        "Chinese",
        "Chinese (China)",
        "Chinese (Hong Kong)",
        "Chinese (Simplified)",
        "Chinese (Singapore)",
        "Chinese (Taiwan)",
        "Chinese (Traditional)",
        "Choctaw",
        "Coptic",
        "Corsican",
        "Cree",
        "Croatian",
        "Czech",
        "Danish",
        "Dogri",
        "Dutch",
        "Dutch (Belgium)",
        "Dutch (Netherlands)",
        "Dzongkha",
        "English",
        "English (Canada)",
        "English (India)",
        "English (Ireland)",
        "English (United Kingdom)",
        "English (United States)",
        "Esperanto",
        "Estonian",
        "Ewe",
        "Faroese",
        "Fijian",
        "Filipino",
        "Finnish",
        "French",
        "French (Belgium)",
        "French (Canada)",
        "French (France)",
        "French (Switzerland)",
        "Fula",
        "Galician",
        "Ganda",
        "Georgian",
        "German",
        "German (Austria)",
        "German (Germany)",
        "German (Switzerland)",
        "Greek",
        "Guarani",
        "Gujarati",
        "Gusii",
        "Haitian Creole",
        "Hakka Chinese",
        "Hakka Chinese (Taiwan)",
        "Haryanvi",
        "Hausa",
        "Hawaiian",
        "Hebrew",
        "Hindi",
        "Hindi (Latin)",
        "Hiri Motu",
        "Hungarian",
        "Icelandic",
        "Igbo",
        "Indonesian",
        "Interlingua",
        "Interlingue",
        "Inuktitut",
        "Inupiaq",
        "Irish",
        "Italian",
        "Japanese",
        "Javanese",
        "Kalaallisut",
        "Kalenjin",
        "Kamba",
        "Kannada",
        "Kashmiri",
        "Kazakh",
        "Khmer",
        "Kikuyu",
        "Kinyarwanda",
        "Klingon",
        "Konkani",
        "Korean",
        "Kurdish",
        "Kyrgyz",
        "Ladino",
        "Lao",
        "Latin",
        "Latvian",
        "Lingala",
        "Lithuanian",
        "Luba-Katanga",
        "Luo",
        "Luxembourgish",
        "Luyia",
        "Macedonian",
        "Maithili",
        "Malagasy",
        "Malay",
        "Malayalam",
        "Maltese",
        "Manipuri",
        "Māori",
        "Marathi",
        "Masai",
        "Meru",
        "Min Nan Chinese",
        "Min Nan Chinese (Taiwan)",
        "Mixe",
        "Mizo",
        "Mongolian",
        "Mongolian (Mongolian)",
        "Nauru",
        "Navajo",
        "Nepali",
        "Nigerian Pidgin",
        "North Ndebele",
        "Northern Sotho",
        "Norwegian",
        "Occitan",
        "Odia",
        "Oromo",
        "Papiamento",
        "Pashto",
        "Persian",
        "Persian (Afghanistan)",
        "Persian (Iran)",
        "Polish",
        "Portuguese",
        "Portuguese (Brazil)",
        "Portuguese (Portugal)",
        "Punjabi",
        "Quechua",
        "Romanian",
        "Romanian (Moldova)",
        "Romansh",
        "Rundi",
        "Russian",
        "Russian (Latin)",
        "Samoan",
        "Sango",
        "Sanskrit",
        "Santali",
        "Sardinian",
        "Scottish Gaelic",
        "Serbian",
        "Serbian (Cyrillic)",
        "Serbian (Latin)",
        "Serbo-Croatian",
        "Sherdukpen",
        "Shona",
        "Sicilian",
        "Sindhi",
        "Sinhala",
        "Slovak",
        "Slovenian",
        "Somali",
        "South Ndebele",
        "Southern Sotho",
        "Spanish",
        "Spanish (Latin America)",
        "Spanish (Mexico)",
        "Spanish (Spain)",
        "Spanish (United States)",
        "Sundanese",
        "Swahili",
        "Swati",
        "Swedish",
        "Tagalog",
        "Tajik",
        "Tamil",
        "Tatar",
        "Telugu",
        "Thai",
        "Tibetan",
        "Tigrinya",
        "Tok Pisin",
        "Toki Pona",
        "Tongan",
        "Tsonga",
        "Tswana",
        "Turkish",
        "Turkmen",
        "Twi",
        "Ukrainian",
        "Urdu",
        "Uyghur",
        "Uzbek",
        "Venda",
        "Vietnamese",
        "Volapük",
        "Võro",
        "Welsh",
        "Western Frisian",
        "Wolaytta",
        "Wolof",
        "Xhosa",
        "Yiddish",
        "Yoruba",
        "Zulu",
    ]

class ALTMeta(BaseModel):
    lang= TextField(null=True,default=None)
    title= TextField(null=True,default=None)
    description= TextField(null=True,default=None)
    subtitle_filepath= TextField(null=True,default=None)
    subtitle_name=  TextField(null=True,default=None)
    subtitle_format= TextField(null=True,default=None)
    subtitle_contents= TextField(null=True,default=None)


class YoutubeVideoModel(BaseModel):
    id = BlobField(primary_key=True)    
    video_id = TextField(null=True,default=None)
    
    video_local_path = TextField(null=True,default=None)
    video_title = TextField(null=True,default=None)
    video_description = TextField(null=True,default=None)
    thumbnail_local_path = TextField(null=True,default=None)
    publish_policy = IntegerField(default=0)
    is_age_restriction = BooleanField(default=True)
    is_paid_promotion = BooleanField(default=True)
    is_automatic_chapters = BooleanField(default=True)
    is_featured_place = BooleanField(default=True)
    video_language = TextField(null=True,default=None)
    captions_certification = IntegerField(default=0)
    video_film_date = TextField(null=True,default=None)
    video_film_location = TextField(null=True,default=None)
    license_type = IntegerField(default=0)
    is_allow_embedding = BooleanField(default=True)
    is_publish_to_subscriptions_feed_notify = BooleanField(default=True)
    shorts_remixing_type = IntegerField(default=0)
    is_show_howmany_likes = BooleanField(default=True)
    is_monetization_allowed = BooleanField(default=True)
    first_comment = TextField(null=True,default=None)
    alternate_infos = TextField(null=True,default=None)
    is_not_for_kid = BooleanField(default=True)
    categories = IntegerField(null=True)
    comments_ratings_policy = IntegerField(default=1)
    tags = TextField(null=True,default=None)
    release_date = TextField(null=True,default=None)
    release_date_hour = TextField(null=True,default=None)
    
    inserted_at = IntegerField(null=True)  # Updated field definition
    
    unique_hash = TextField(index=True, unique=True, null=True, default=None)  # Add this line
    is_deleted = BooleanField(default=False)  # Add a field to flag if video is deleted


    @classmethod

    # Assuming you have defined VideoModel as shown earlier
    def add_video(cls,video_data):
        try:
            unique_hash = generate_unique_hash(video_data)
            video_data['unique_hash'] = unique_hash
            existing_video = cls.select().where(cls.unique_hash == unique_hash).first()
            if existing_video is None:
                video = cls(**video_data)
                video.inserted_at = int(time.time())  # Update insert_date
                video.id=CustomID().to_bin()
                video.unique_hash=unique_hash
                video.save(force_insert=True) 
                return video
            else:
                return existing_video
        except Exception as e:
            logger.error(f'create video failure due to error:{e}')
            return None
    @classmethod
        
    # Assuming you have defined VideoModel as shown earlier
    def bulk_add_videos(video_data_list):
        inserted_videos = []
        for video_data in video_data_list:    
            try:
                unique_hash = generate_unique_hash(video_data)
                video_data['unique_hash'] = unique_hash
                
                video = YoutubeVideoModel(**video_data)
                video.inserted_at = int(time.time())  # Update insert_date
                
                video.save(force_insert=True) 
                inserted_videos.append(video)
                
                return video
            except Exception as e:
                return str(e)

        return inserted_videos        
    @classmethod

    def update_video(cls,id, video_data,**kwargs):
        try:
            video = cls.get_or_none(cls.id == id)
            print('before modify',video,video.is_deleted)
            if video_data:
                video = YoutubeVideoModel(**video_data)
                print('after modify',video,video.is_deleted)


            else:
                for key, value in kwargs.items():
                    # 由于entry获取的都是字符串变量值，对于bool型，需要手动转换
                    # if key=='is_deleted':
                    #     print('is deleted',type(value))
                    #     if value=='0':
                    #         value=False
                    #     elif value=='1':
                    #         value=True
                    setattr(video, key, value)
                    
                print('after modify',video,video.is_deleted)
            video.inserted_at = int(time.time())  # Update insert_date

            video.save() 
            print('update success')
            return video
        except cls.DoesNotExist:
            return None
    @classmethod
    def get_video_by_id(cls,id):
        try:
            return cls.get_or_none(cls.id == id)
        except DoesNotExist:
            return None
    @classmethod

    # Read
    def get_video_by_hash(cls,hash):
        try:
            return cls.get(cls.unique_hash == hash).id
        except DoesNotExist:
            return None
    @classmethod
        
    def get_all_videos():
        return YoutubeVideoModel.select()
    @classmethod

    def delete_video(id):
        try:
            video = YoutubeVideoModel.objects.get(id=id)
            video.is_deleted = True
            video.inserted_at = int(time.time())  # Update insert_date
            video.save(force_insert=True) 
            return video
        except YoutubeVideoModel.DoesNotExist:
            return None
