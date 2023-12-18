import sys
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.api.account import router
from pathlib import Path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))



if getattr(sys, 'frozen', False):
    # The application is frozen
    datadir = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    datadir = os.path.dirname(__file__)

print('fastserver  static files location======',os.path.join(datadir,"static"))
# venv
# fastserver  static files location====== /Users/wenke/github/tiktoka-studio-uploader-genius/.venv/bin /Users/wenke/github/tiktoka-studio-uploader-genius /Users/wenke/github/tiktoka-studio-uploader-genius/src

# bundle exe
#fastserver  static files location====== /Users/wenke/github/tiktoka-studio-uploader-genius/build/exe.macosx-10.9-x86_64-3.9 /Users/wenke/github/tiktoka-studio-uploader-genius/build/exe.macosx-10.9-x86_64-3.9/lib /Users/wenke/github/tiktoka-studio-uploader-genius/build/exe.macosx-10.9-x86_64-3.9/lib/src
app = FastAPI()
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/static", StaticFiles(directory=os.path.join(datadir,"static")), name="static")
# https://www.starlette.io/staticfiles/


# you should have static under src/app/static
# app.mount("/static", StaticFiles(packages=[('src.app','static')]), name="static")

# you should have static at the same level of         Executable( "uploadergenius.py",
app.mount("/static", StaticFiles(directory=os.path.join(datadir,"static")), name="static")

# for macos  'static' dont work


# app.mount("/static", StaticFiles(directory="static",packages=[('src.app','static')]), name="static")

app.include_router(router)

@app.get("/")
def howdy():
    return {"Howdy": "World"}
