import pandas as pd

import json,platform,os
import jsons

from UltraDict import UltraDict
if platform.system()=='Windows':
    
    ultra = UltraDict(shared_lock=True,recurse=True)
else:
    ultra = UltraDict(recurse=True)

df=pd.read_json('/Users/wenke/github/tiktoka-studio-uploader/tests/videos-meta.json') 
print(f'user submited:\r{df.to_json(orient="records")}')
print(f'user submited:\r{df.to_json()}')
print('2',type(json.loads(df.to_json())))
ultra['videos']=json.loads(df.to_json())
print(ultra['videos']['1']['heading'])
totaljson='./1.json'

if os.path.exists(totaljson):
    with open(totaljson,'w') as f:
        f.write(jsons.dumps(ultra['videos']) )       
else:
    with open(totaljson,'a') as f:
        f.write(jsons.dumps(ultra['videos']))    