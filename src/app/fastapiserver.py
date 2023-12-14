import sys
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.api.account import router
from pathlib import Path
from uploadergenius import tmp
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))



if sys.platform=='darwin':
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

root=Path(__file__).parent.parent

print('fastserver  static files location======',ROOT_DIR,parent_dir,root)
print('env ',tmp["ROOT_DIR"])
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
app.mount("/static", StaticFiles(directory=os.path.join(tmp["ROOT_DIR"],"static")), name="static")
# https://www.starlette.io/staticfiles/
# app.mount("/static", StaticFiles(directory="static",packages=[('src.app','static')]), name="static")

app.include_router(router)