import sys
import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from tkinter import *

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import asyncio
import tkinter as tk
from asyncio import CancelledError
from contextlib import suppress
import random
from async_tkinter_loop import async_handler, async_mainloop

from asyncio.subprocess import Process
from typing import Optional
import platform

from src.api.account import router

app = FastAPI()
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)