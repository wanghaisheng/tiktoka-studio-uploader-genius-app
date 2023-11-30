import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["unittest"],
    'includes': ["PIL",'moviepy','tsup',"requests",'UltraDict','jsons','lastversion','jsonschema','pystray','bcrypt','peewee','fastapi','pycountry','pyperclip'], # list of extra modules to include (from your virtualenv of system path),
    'packages': [], # list of packages to include in the froze executable (from your application)
    "zip_include_packages": ["encodings"],
    "include_files": [
         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )

         ]
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="uploadergenius",
    version="0.9",
    description="Uploader Genius-your last social media publish management tool!",
    options={"build_exe": build_exe_options},

    executables = 
        [
            Executable(
                "uploadergenius.py",
                copyright="Copyright (C) 2023 TiktokaStudio",
                base=base,
                icon="assets\\icon.ico",
                shortcut_name="uploadergenius",
                # shortcut_dir="MyProgramMenu",
            ),
        ],



)