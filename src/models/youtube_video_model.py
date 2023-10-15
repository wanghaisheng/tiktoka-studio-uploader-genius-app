import time
import peewee
from peewee import *
from models import generate_unique_hash
from src.models import BaseModel,db

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

    # Mapping of options to human-readable text
    WAIT_POLICY_TEXT = {
        GO_NEXT_UPLOAD_SUCCESS: "Go next after uploading success",
        GO_NEXT_PROCESSING_SUCCESS: "Go next after processing success",
        GO_NEXT_COPYRIGHT_CHECK_SUCCESS: "Go next after copyright check success"
    }

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
        # Video Categories Options
    VIDEO_CATEGORIES_OPTIONS = {
        "None":0,
        "Autos & Vehicles": 15,
        "Comedy": 1,
        "Education": 2,
        "Entertainment": 3,
        "Film & Animation": 4,
        "Gaming": 5,
        "Howto & Style": 6,
        "Music": 7,
        "News & Politics": 8,
        "Nonprofits & Activism": 9,
        "People & Blogs": 10,
        "Pets & Animals": 11,
        "Science & Technology": 12,
        "Sports": 13,
        "Travel & Events": 14
    }

    VIDEO_LANGUAGE_TEXT = {v: k for k, v in VIDEO_LANGUAGE_OPTIONS.items()}
    VIDEO_CATEGORIES_TEXT = {v: k for k, v in VIDEO_CATEGORIES_OPTIONS.items()}
    

    # Publish Policy Options
    PUBLISH_POLICY_OPTIONS = {
        "Private": 0,
        "Publish": 1,
        "Schedule": 2,
        "Unlisted": 3,
        "Public & Premiere": 4
    }

    PUBLISH_POLICY_TEXT = {v: k for k, v in PUBLISH_POLICY_OPTIONS.items()}
class YoutubeVideoModel(BaseModel):
    id = BlobField(primary_key=True)    
    
    video_local_path = TextField(default=None)
    video_title = TextField(default=None)
    video_description = TextField(default=None)
    thumbnail_local_path = TextField(default=None)
    publish_policy = IntegerField(default=0)
    is_age_restriction = BooleanField(default=True)
    is_paid_promotion = BooleanField(default=True)
    is_automatic_chapters = BooleanField(default=True)
    is_featured_place = BooleanField(default=True)
    video_language = TextField(default=None)
    captions_certification = IntegerField(default=0)
    video_film_date = TextField(default=None)
    video_film_location = TextField(default=None)
    license_type = IntegerField(default=0)
    is_allow_embedding = BooleanField(default=True)
    is_publish_to_subscriptions_feed_notify = BooleanField(default=True)
    shorts_remixing_type = IntegerField(default=0)
    is_show_howmany_likes = BooleanField(default=True)
    is_monetization_allowed = BooleanField(default=True)
    first_comment = TextField(default=None)
    subtitles = TextField(default=None)
    is_not_for_kid = BooleanField(default=True)
    categories = IntegerField(default=10)
    comments_ratings_policy = IntegerField(default=1)
    tags = TextField(default=None)
    release_date = TextField(default=None)
    release_date_hour = TextField(default=None)
    
    insert_date = IntegerField(null=True)  # Updated field definition
    
    unique_hash = TextField(index=True, unique=True, null=True, default=None)  # Add this line
    is_deleted = BooleanField(default=False)  # Add a field to flag if video is deleted

    class Meta:
        db_table = db


# Assuming you have defined VideoModel as shown earlier
def create_video(video_data):
    try:
        unique_hash = generate_unique_hash(video_data)
        video_data['unique_hash'] = unique_hash
        
        video = VideoModel(**video_data)
        video.insert_date = int(time.time())  # Update insert_date
        
        video.save()
        return video
    except Exception as e:
        return str(e)
# Assuming you have defined VideoModel as shown earlier
def bulk_add_videos(video_data_list):
    inserted_videos = []
    for video_data in video_data_list:    
        try:
            unique_hash = generate_unique_hash(video_data)
            video_data['unique_hash'] = unique_hash
            
            video = VideoModel(**video_data)
            video.insert_date = int(time.time())  # Update insert_date
            
            video.save()
            inserted_videos.append(video)
            
            return video
        except Exception as e:
            return str(e)

    return inserted_videos        
def update_video(video_id, video_data):
    try:
        video = VideoModel.objects.get(id=video_id)
        unique_hash = generate_unique_hash(video_data)
        video_data['unique_hash'] = unique_hash
        video.insert_date = int(time.time())  # Update insert_date
        for key, value in video_data.items():
            setattr(video, key, value)
        video.save()
        return video
    except VideoModel.DoesNotExist:
        return None

# Read
def get_video_by_id(video_id):
    try:
        return VideoModel.get(VideoModel.id == video_id)
    except DoesNotExist:
        return None
# Read
def get_video_by_hash(hash):
    try:
        return VideoModel.get(VideoModel.unique_hash == hash).id
    except DoesNotExist:
        return None
def get_all_videos():
    return VideoModel.select()

def delete_video(video_id):
    try:
        video = VideoModel.objects.get(id=video_id)
        video.is_deleted = True
        video.insert_date = int(time.time())  # Update insert_date
        video.save()
        return video
    except VideoModel.DoesNotExist:
        return None
