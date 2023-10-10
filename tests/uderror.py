from UltraDict import UltraDict
ultra = UltraDict(shared_lock=True,recurse=True)
ultra['empty']={}
new={'1': {'video_local_path': 'D:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.mp4', 'video_filename': '1.mp4', 'video_title': 1, 'heading': None, 'subheading': None, 'extraheading': None, 'video_description': None, 'thumbnail_bg_image_path': None, 'thumbnail_local_path': '[]', 'release_date': None, 'release_date_hour': '10:15', 'is_not_for_kid': True, 'categories': None, 'comments_ratings_policy': 1, 'is_age_restriction': False, 'is_paid_promotion': False, 'is_automatic_chapters': True, 'is_featured_place': True, 'video_language': None, 'captions_certification': 0, 'video_film_date': None, 'video_film_location': None, 'license_type': 0, 'is_allow_embedding': True, 'is_publish_to_subscriptions_feed_notify': True, 'shorts_remixing_type': 0, 'is_show_howmany_likes': True, 'is_monetization_allowed': True, 'first_comment': None, 'subtitles': None, 'tags': None}}

new2={'2': {'video_local_path': 'D:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.mp4', 'video_filename': '1.mp4', 'video_title': 222, 'heading': None, 'subheading': None, 'extraheading': None, 'video_description': None, 'thumbnail_bg_image_path': None, 'thumbnail_local_path': '[]', 'release_date': None, 'release_date_hour': '10:15', 'is_not_for_kid': True, 'categories': None, 'comments_ratings_policy': 1, 'is_age_restriction': False, 'is_paid_promotion': False, 'is_automatic_chapters': True, 'is_featured_place': True, 'video_language': None, 'captions_certification': 0, 'video_film_date': None, 'video_film_location': None, 'license_type': 0, 'is_allow_embedding': True, 'is_publish_to_subscriptions_feed_notify': True, 'shorts_remixing_type': 0, 'is_show_howmany_likes': True, 'is_monetization_allowed': True, 'first_comment': None, 'subtitles': None, 'tags': 'xxxxxx'}}
new3={'3': {'video_local_path': 'D:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.mp4', 'video_filename': '1.mp4', 'video_title': 222, 'heading': None, 'subheading': None, 'extraheading': None, 'video_description': None, 'thumbnail_bg_image_path': None, 'thumbnail_local_path': '[]', 'release_date': None, 'release_date_hour': '10:15', 'is_not_for_kid': True, 'categories': None, 'comments_ratings_policy': 1, 'is_age_restriction': False, 'is_paid_promotion': False, 'is_automatic_chapters': True, 'is_featured_place': True, 'video_language': None, 'captions_certification': 0, 'video_film_date': None, 'video_film_location': None, 'license_type': 0, 'is_allow_embedding': True, 'is_publish_to_subscriptions_feed_notify': True, 'shorts_remixing_type': 0, 'is_show_howmany_likes': True, 'is_monetization_allowed': True, 'first_comment': None, 'subtitles': None, 'tags': 'xxxxxx'}}


ultra['new']=new
def t0(key):
#overwrite with same dict
    ultra[key]=new


def t1(key):
        #overwrite with same key diff field
        ultra[key]={'1': {'video_local_path': 'C:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.mp4', 'video_filename': '1.mp4', 'video_title': 1, 'heading': None, 'subheading': None, 'extraheading': None, 'video_description': None, 'thumbnail_bg_image_path': None, 'thumbnail_local_path': '[]', 'release_date': None, 'release_date_hour': '10:15', 'is_not_for_kid': True, 'categories': None, 'comments_ratings_policy': 1, 'is_age_restriction': False, 'is_paid_promotion': False, 'is_automatic_chapters': True, 'is_featured_place': True, 'video_language': None, 'captions_certification': 0, 'video_film_date': None, 'video_film_location': None, 'license_type': 0, 'is_allow_embedding': True, 'is_publish_to_subscriptions_feed_notify': True, 'shorts_remixing_type': 0, 'is_show_howmany_likes': True, 'is_monetization_allowed': True, 'first_comment': None, 'subtitles': None, 'tags': None}}
        print('same key diff field',ultra[key])
def t11(key):
        #overwrite with same key diff field
        ultra[key]={'1': {'video_local_path': 'C:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.mp4', 'video_filename': '1.mp4', 'video_title': 1, 'heading': None, 'subheading': None, 'extraheading': None, 'video_description': None, 'thumbnail_bg_image_path': None, 'thumbnail_local_path': '[]', 'release_date': None, 'release_date_hour': '10:15', 'is_not_for_kid': True, 'categories': None, 'comments_ratings_policy': 1, 'is_age_restriction': False, 'is_paid_promotion': False, 'is_automatic_chapters': True, 'is_featured_place': True, 'video_language': None, 'captions_certification': 0, 'video_film_date': None, 'video_film_location': None, 'license_type': 0, 'is_allow_embedding': True, 'is_publish_to_subscriptions_feed_notify': True, 'shorts_remixing_type': 0, 'is_show_howmany_likes': True, 'is_monetization_allowed': True, 'first_comment': None, 'subtitles': None, 'tags': None}}
        print('same key diff field',ultra[key])
def t12(key):
        # make it a  empty one at first
        ultra[key]=dict({})
        #overwrite with same key diff field

        ultra[key]={'1': {'video_local_path': 'C:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.mp4', 'video_filename': '1.mp4', 'video_title': 1, 'heading': None, 'subheading': None, 'extraheading': None, 'video_description': None, 'thumbnail_bg_image_path': None, 'thumbnail_local_path': '[]', 'release_date': None, 'release_date_hour': '10:15', 'is_not_for_kid': True, 'categories': None, 'comments_ratings_policy': 1, 'is_age_restriction': False, 'is_paid_promotion': False, 'is_automatic_chapters': True, 'is_featured_place': True, 'video_language': None, 'captions_certification': 0, 'video_film_date': None, 'video_film_location': None, 'license_type': 0, 'is_allow_embedding': True, 'is_publish_to_subscriptions_feed_notify': True, 'shorts_remixing_type': 0, 'is_show_howmany_likes': True, 'is_monetization_allowed': True, 'first_comment': None, 'subtitles': None, 'tags': None}}
        print('same key diff field',ultra[key])
def t2(key):
#overwrite with diff key 

        ultra[key]=new2
        print(ultra[key])

def method1(key):
    ultra[key]=new3
    print(ultra[key])    

def method2(key):
    for filename,video in new3.items(key):
        #     print('debug',filename,video)
        ultra[key][filename]= video
        print(ultra[key])
    print('m2 pass')
for key in ['empty','new']:
    print(f'start to deal {key}')
    for func in [t0,t1,t11,t12,t2,method1,method2]:
        try:
            func(key)
            print(f'{func} ok')

        except :
            print(f'{func} failed')



