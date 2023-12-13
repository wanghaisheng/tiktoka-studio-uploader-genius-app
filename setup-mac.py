import sys
from cx_Freeze import setup, Executable

executables = [
    Executable('uploadergenius.py', base=None)
]
build_exe_options = {
    "include_msvcr": True,

    "include_files": [
         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )

         ],
    'includes': ["PIL",'loguru','psutil','pandas','better_exceptions','undetected_playwright','webdriver_manager','selenium','atomics','w3lib','moviepy','upgenius',"requests",'i18n_json','jsons','lastversion','jsonschema','pystray','bcrypt','peewee','fastapi','pycountry','pyperclip','async_tkinter_loop'], # list of extra modules to include (from your virtualenv of system path),


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