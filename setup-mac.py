import sys,os
from cx_Freeze import setup, Executable



modules_include: list = []

for folder in os.listdir(os.path.join(os.getcwd(), 'src')):
    if folder != '__pycache__' and os.path.isdir(os.path.join(os.path.join(os.getcwd(), 'src'), folder)):
        modules_include.append(f'src.{folder}')
        for module in os.listdir(os.path.join(os.path.join(os.getcwd(), 'src'), folder)):
            if module != '__pycache__' and '.py' in module:
                modules_include.append(f'src.{folder}.{module[:-3]}')


others=["PIL",'loguru','psutil','pandas','better_exceptions','undetected_playwright','webdriver_manager','selenium','atomics','w3lib','moviepy','upgenius',"requests",'i18n_json','jsons','lastversion','jsonschema','pystray','bcrypt','peewee','fastapi','pycountry','pyperclip','async_tkinter_loop']


executables = [
    Executable('uploadergenius.py', base=None)
]
build_exe_options = {
    "include_msvcr": True,
    # "packages":['src'],
    "include_files": [
         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )
         ],
    'includes':modules_include+others
}


bdist_mac_options = {
    "bundle_name": "UploaderGenius"
}

bdist_dmg_options = {
    "volume_label": "UploaderGenius",
}

setup(name='uploadergenius',
      version = '0.1',
      description = 'test',
      options = {
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_dmg": bdist_dmg_options,

          },
      executables = executables
      )