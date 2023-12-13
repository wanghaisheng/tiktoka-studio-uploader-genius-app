
from i18n_json import i18n_json
root = i18n_json(recurse=True)
root['folder']={}
ultra=root['folder']
ultra['videos'] = dict({'1': {'captions_certification': 0, 'categories': '', 'comments_ratings_policy': 1, 'extraheading': '', 'first_comment': '', 'heading': '3333', 'is_age_restriction': False, 'is_allow_embedding': True, 'is_automatic_chapters': True, 'is_featured_place': True, 'is_monetization_allowed': True, 'is_not_for_kid': True, 'is_paid_promotion': False, 'is_publish_to_subscriptions_feed_notify': True, 'is_show_howmany_likes': True, 'license_type': 0, 'release_date': '', 'release_date_hour': '10:15', 'shorts_remixing_type': 0, 'subheading': '2222', 'subtitles': '', 'tags': '', 'thumbnail_bg_image_path': '', 'thumbnail_local_path': [], 'video_description': '', 'video_filename': '1.mp4', 'video_film_date': '', 'video_film_location': '', 'video_language': '', 'video_local_path': '/Users/wenke/github/tiktoka-studio-uploader-app/tests/videos/1.mp4', 'video_title': '1'}})
d=dict({})
root['folder']['videos'] = d
print(root)
# {'d': {'1': {'captions_certification': 0, 'categories': '', 'comments_ratings_policy': 1, 'extraheading': '', 'first_comment': '', 'heading': '3333', 'is_age_restriction': False, 'is_allow_embedding': True, 'is_automatic_chapters': True, 'is_featured_place': True, 'is_monetization_allowed': True, 'is_not_for_kid': True, 'is_paid_promotion': False, 'is_publish_to_subscriptions_feed_notify': True, 'is_show_howmany_likes': True, 'license_type': 0, 'release_date': '', 'release_date_hour': '10:15', 'shorts_remixing_type': 0, 'subheading': '2222', 'subtitles': '', 'tags': '', 'thumbnail_bg_image_path': '', 'thumbnail_local_path': [], 'video_description': '', 'video_filename': '1.mp4', 'video_film_date': '', 'video_film_location': '', 'video_language': '', 'video_local_path': '/Users/wenke/github/tiktoka-studio-uploader-app/tests/videos/1.mp4', 'video_title': '1'}}}
