# https://github.com/Futura-Py/TimerX/tree/master
import sys,os

from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
    base = "Win32GUI"

    icon = "./assets/icon.ico"
    executables = [
        Executable(
            "uploadergenius.py",
            base=base,
            icon=icon,
            shortcut_name="UploaderGenius",
            target_name="UploaderGenius.exe",
            shortcut_dir="ProgramMenuFolder",
        )
    ]
elif sys.platform == "darwin":

    # icon = "./assets/logo_new.icns"
    icon = "./assets/icon.ico"

    executables = [
        Executable(
            "uploadergenius.py",
            base=base)
    ]
else:
    # icon = "./assets/logo_new.png"
    icon = "./assets/icon.ico"

    executables = [
        Executable(
            "uploadergenius.py",
            base=base,
            icon=icon,
            shortcut_name="UploaderGenius",
            target_name="UploaderGenius",
        )
    ]

import uuid

upgradeid = (
    "{" + str(uuid.uuid3(uuid.NAMESPACE_DNS, "UploaderGenius-App.UploaderGenius.org")).upper() + "}"
)


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
    "include_files": [
         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )
         ],
    'includes':modules_include+others
}


build_exe_options = {
    "include_msvcr": True,
    "include_files": [
         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )

         ],
    'includes': ["PIL",'loguru','psutil','pandas','better_exceptions','undetected_playwright','webdriver_manager','selenium','atomics','w3lib','moviepy','upgenius',"requests",'i18n_json','jsons','lastversion','jsonschema','pystray','bcrypt','peewee','fastapi','pycountry','pyperclip','async_tkinter_loop'], # list of extra modules to include (from your virtualenv of system path),


}

bdist_rpm_options = {"icon": icon}

bdist_msi_options = {
    "add_to_path": False,
    "install_icon": "assets/icon.ico",
    "upgrade_code": upgradeid,
    "dist_dir":"dist",
    "target_name": "UploaderGenius",
}
bdist_mac_options = {"bundle_name": "UploaderGenius", "iconfile": "./assets/icon.ico"
                     }

bdist_dmg_options = {
    "volume_label": "UploaderGenius",
    "applications_shortcut": True,
}

version = "0.9.0"

setup(
    name="UploaderGenius",
    version=version,
    description="The only social media videos publish management tool you'll ever need",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_dmg": bdist_dmg_options,
        "bdist_msi": bdist_msi_options,
        "bdist_rpm": bdist_rpm_options,
    },
)