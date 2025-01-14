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
            base=base,
            icon=icon,
            shortcut_name="UploaderGenius",
            target_name="UploaderGenius",
        )
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
            target_name="UploaderGenius.exe",
        )
    ]

# directory_table = [
#     ("ProgramMenuFolder", "TARGETDIR", "."),
#     ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
# ]

# msi_data = {
#     "Directory": directory_table,
#     "ProgId": [
#         ("UploaderGenius", None, None, "A simple, lightweight, & beautiful timer app built in Python and tkinter.ttk using rdbende's Sun Valley TTk Theme", "IconId", None),
#     ],
#     "Icon": [
#         ("IconId", "assets/logo.ico"),
#     ],
# }
import uuid

upgradeid = (
    "{" + str(uuid.uuid3(uuid.NAMESPACE_DNS, "UploaderGenius-App.UploaderGenius.org")).upper() + "}"
)

build_exe_options = {
    "include_msvcr": True,
    "packages":["src"],
    "include_files": [
         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )

         ],
    'includes': ['uvicorn',"PIL",'moviepy','upgenius',"requests",'i18n_json','jsons','lastversion','jsonschema','pystray','bcrypt','peewee','fastapi','pycountry','pyperclip','async_tkinter_loop'], # list of extra modules to include (from your virtualenv of system path),


}

bdist_rpm_options = {"icon": icon}

bdist_msi_options = {
    "add_to_path": False,
    "install_icon": "assets/icon.ico",
    "upgrade_code": upgradeid,
    "target_name": "UploaderGenius",
}
bdist_mac_options = {"bundle_name": "UploaderGenius", "iconfile": "./assets/icon.ico",
        "custom_info_plist": None,  # Set this to use a custom info.plist file
        "codesign_entitlements": os.path.join(
            os.path.dirname(__file__), "codesign-entitlements.plist"
        ),
        "codesign_identity":None,  # Set this to enable signing with custom identity (replaces adhoc signature)
        "codesign_options": "runtime",  # Ensure codesign uses 'hardened runtime'
        "codesign_verify": False,  # Enable to get more verbose logging regarding codesign
        "spctl_assess": False,  # Enable to get more verbose logging regarding codesigns
"include_resources":[

         ( './assets/', 'assets' ),
         ( './locales/', 'locales' ),
         ( './static/', 'static' )
]

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