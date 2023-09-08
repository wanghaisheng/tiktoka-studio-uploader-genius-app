import pandas as pd
from sqlalchemy import create_engine
import json

import logging

logger = logging.getLogger()     
header2015=['country', 'region', 'happiness_rank', 'happiness_score',
           'standard_error', 'economy', 'family',
           'life_expectancy', 'freedom', 'government_corruption',
           'generosity', 'dystopia_residual']

header2016=['country', 'region', 'happiness_rank', 'happiness_score',
           'lowerconfidenceinterval', 'upperconfidenceinterval',
           'economy', 'family', 'life_expectancy', 'freedom', 'government_corruption',
           'generosity', 'dystopia_residual']

header2017=['country', 'happiness_rank', 'happiness_score', 'lowerconfidenceinterval','upperconfidenceinterval', 
            'economy', 'family','life_expectancy', 'freedom', 'generosity',
            'government_corruption', 'dystopia_residual']

header2018=['overall_rank', 'country', 'happiness_score', 'economy','social_support', 'life_expectancy',
            'freedom', 'generosity','government_corruption']

header2019=['overall_rank', 'country', 'happiness_score', 'economy',
             'social_support', 'life_expectancy',
            'freedom', 'generosity','government_corruption']
# Load the CSV file into a Pandas DataFrame
# df = pd.read_csv('2015.csv',header=0, names=header2015)

# # Establish a connection to the PostgreSQL database using SQLAlchemy
# engine = create_engine('sqlite:///t.sqlite3')

# # Save the DataFrame to the PostgreSQL database
# df.to_sql('socialind2015', engine, if_exists='replace', index=False)

# query = 'SELECT * FROM socialind2015'
# df = pd.read_sql_query(query, engine)

# # Display the results
# print(df.head(3))


metafile=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-app\tests\youtube-videos-meta.json'
data = json.load(open(metafile))
setting=pd.json_normalize(data["uploadSetting"])

for key in ['proxy_option','channel_cookie_path']:
    if data["uploadSetting"].get(key)==None:
        logger.error(f"No target{key} in given setting json data")
        raise ValueError(f"No target{key} in given data")
        
for key in ['timeout','timeout','debug','wait_policy','is_record_video','username','password']:
    if data["uploadSetting"].get(key)==None:
        logger.info(f"No target{key} in given setting json data")

if data["uploadSetting"].get('browser_type')==None:
    setting['browser_type']='firefox'        
    logger.info('we use browser_type =firefox')
else:
    if type(data["uploadSetting"].get('browser_type'))!=str:
        logger.error('browser_type should be one of "chromium", "firefox", "webkit"')
    else:
        if not data["uploadSetting"].get('browser_type') in ["chromium", "firefox", "webkit"]:
            logger.error('browser_type should be one of"chromium", "firefox", "webkit"')

if data["uploadSetting"].get('platform')==None:
    setting['platform']='youtube'        
    logger.info('we use platform =youtube')
else:
    if type(data["uploadSetting"].get('platform'))!=str:
        logger.error('platform should be one of "youtube", "tiktok", "douyin"')
    else:
        if not data["uploadSetting"].get('platform') in ["youtube", "tiktok", "douyin"]:
            logger.error('platform should be one of "youtube", "tiktok", "douyin"')


if data["uploadSetting"].get('timeout')==None:
    setting['timeout']=200000
else:
    if type(data["uploadSetting"].get('timeout'))!=int:
        logger.error('timeout should be integer,such as 20*1000=20000, 20 seconds')
if data["uploadSetting"].get('is_open_browser')==None:
    setting['is_open_browser']=True
else:
    if type(data["uploadSetting"].get('is_open_browser'))!=bool:
        print('==,',setting['is_open_browser'].values,type(setting.get('is_open_browser')))
        logger.error('is_open_browser should be bool, true or false{}')

if data["uploadSetting"].get('debug')==None:
    setting['debug']=True
else:
    if type(data["uploadSetting"].get('debug'))!=bool:
        logger.error('debug should be bool, true or false')                        
if data["uploadSetting"].get('wait_policy')==None:
    setting['wait_policy']=2        
    logger.info('we use wait_policy =2')
else:
    if type(data["uploadSetting"].get('wait_policy'))!=int:
        logger.error('wait_policy should be one of 0,1,2')
    else:
        if not data["uploadSetting"].get('wait_policy') in [0,1,2]:
            logger.error('wait_policy should be one of 0,1,2')

if data["uploadSetting"].get('is_record_video')==None:
    setting['is_record_video']=True        
else:
    if type(data["uploadSetting"].get('is_record_video'))!=bool:
        logger.error('is_record_video should be bool, true or false') 

engine = create_engine('sqlite:///t1.sqlite3')
table_name = "uploadSetting"

try:
    with engine.begin() as conn:
        setting.to_sql(table_name, conn, if_exists="replace", index=False)
        print(">>> All good.")
except Exception as e:
    print(">>> Something went wrong!")
query = 'SELECT * FROM uploadSetting'
df = pd.read_sql_query(query, engine)

# Display the results
print(df.head(3))