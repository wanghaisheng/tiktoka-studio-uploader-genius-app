import sys
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.api.account import router

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



if sys.platform=='darwin':
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


parent_dir = os.path.dirname(ROOT_DIR)

print('fastserver  static files location======',ROOT_DIR,parent_dir)
app = FastAPI()
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR,"static")), name="static")
app.include_router(router)