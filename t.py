import pandas as pd
import os,json

old_df_metas=None
selectedMetafileformat='json'
folder=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\tests\videos\vertical'
print(os.path.join(folder,'videos-meta.'+selectedMetafileformat))
if os.path.exists(os.path.join(folder,'videos-meta.'+selectedMetafileformat)):
    if selectedMetafileformat=='xlsx':
        old_df_metas=pd.read_excel(os.path.join(folder,'videos-meta.xlsx'), index_col=[0])
        old_df_metas.replace('nan', '')
        
        old_df_metas=old_df_metas.iterrows()
    elif selectedMetafileformat=='json':
        old_df_metas=pd.read_json(os.path.join(folder,'videos-meta.json'))  
        old_df_metas.replace('nan', '')
        
        # old_df_metas=old_df_metas.items()      
    elif selectedMetafileformat=='csv':
        old_df_metas=pd.read_csv(os.path.join(folder,'videos-meta.csv'), index_col=[0])
        old_df_metas.replace('nan', '')
        
        # old_df_metas=old_df_metas.iterrows()

old_df_metas=json.loads(old_df_metas.to_json())   
print(old_df_metas['1'])

for key, entry in old_df_metas:
    print(entry['1'])