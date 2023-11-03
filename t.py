import json
path=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\assets\country-db\json\country-state-db.json'

s=open(path,encoding='utf-8').read()
f=json.loads(s)
print(f)