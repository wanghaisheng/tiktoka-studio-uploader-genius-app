import pandas as pd

import json
df=pd.read_excel('/Users/wenke/github/tiktoka-studio-uploader-app/tests/videos/vertical/videos-meta.xlsx',index_col=0)
allowedTextTypes=['heading','subheading']
# print(df)
# print(df.columns)
print(json.loads(df.to_json(orient = 'index'))    )


for key in json.loads(df.to_json()).keys():
    print(json.loads(df.to_json())[key]    )
                                            
                                            
for key, entry in df.iterrows():
    missing_fields = [field for field in allowedTextTypes if field not in entry.keys()]
    print('reading video meta\r',entry.keys())

    if missing_fields:
        print(f"The following allowed fields are missing in entry {key}: {', '.join(missing_fields)}")

        passed=False

    else:
        for field in allowedTextTypes:
            value = entry[field]
            if value == "":
                passed=False
            
            else:
                print(f'{field} value is {value} in entry {key}.')