class PLATFORM_TYPE:
    YOUTUBE = 1
    TIKTOK = 2
    INSTAGRAM=3
    TWITTER=4
    FACEBOOK=5
    DOUYIN=6
    SHIPINHAO=7
    XIAOHONGSHU=8
    UNKNOWN=100
    PLATFORM_TYPE_TEXT = [
        (YOUTUBE, "youtube"),
        (TIKTOK, "tiktok"),
        (INSTAGRAM, "instagram"),
        (TWITTER, "twitter"),
        (FACEBOOK, "facebook"),
        (DOUYIN, "douyin"),        
        (SHIPINHAO, "视频号"),
        (XIAOHONGSHU, "小红书"),
        (UNKNOWN, "unknown")

    ]




def find_key(input_dict, value):
    if type(input_dict)==list:
        input_dict=dict(input_dict)
    result = "None"
    for key,val in input_dict.items():
        if val == value:
            result = key
    return result

d=dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)
print(d.get('douyin'))
i=next((k for k in d if d[k] == 'douyin'), None)
print(i)
print(find_key(d,'unknown'))
print(d[100])
print(list(d.values()))
print(list(d.keys()))


