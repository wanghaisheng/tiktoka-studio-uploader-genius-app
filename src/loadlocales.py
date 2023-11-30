from constants import *
import os,platform
from src.log import logger
import json
from UltraDict import UltraDict

def load_setting():
    global settings
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
        )

    settingfile=os.path.join(ROOT_DIR,settingfilename)
    failed=False
    if os.path.exists(settingfile) :
        try:

            fp = open(settingfile, 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
            settings = json.loads(setting_json)

        except:
            failed=True

    else:
        failed=True
    if failed==True:
        logger.debug('start initialize settings with default')
        print('start initialize settings with default')

        try:
            settings
        except:

            if platform.system()!='Windows':
                settings = UltraDict(recurse=True)
            else:
                settings = UltraDict(shared_lock=True,recurse=True)
                
        settings['lastuselang']='en'
        settings['zh']=json.loads(open(os.path.join(ROOT_DIR+os.sep+'locales','zh.json'), 'r', encoding='utf-8').read())
        settings['en']=json.loads(open(os.path.join(ROOT_DIR+os.sep+'locales','en.json'), 'r', encoding='utf-8').read())
        logger.debug('end to initialize settings with default')