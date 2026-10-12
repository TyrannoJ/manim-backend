from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import base64
import mimetypes
from fastapi.responses import FileResponse
import subprocess
import sys
from pathlib import Path

#uvicorn main:app --reload
#uvicorn main:app --host 0.0.0.0 --port 8000
#cloudflared tunnel --url http://localhost:8000
app = FastAPI()
# Allow your Vercel frontend to call this API
#kein slash hinten an origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://manim-ochre.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]
@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running"}


@app.get("/picture/{filename}")
async def get_picture(filename: str):
    # Adjust path to your video folder
    #/home/julius/Desktop/manim-main/derivatives-app/backend/2x7
    path = f"/home/julius/Desktop/manim-backend/derivatives-app/backend/video/{filename}/images/derivatives_simple/Derivatives_ManimCE_v0.22.0.png"
    #derivatives-app/backend/video/2x2/images/derivatives_simple/Derivatives_ManimCE_v0.22.0.png
    
    mime_type, _ = mimetypes.guess_type(path)
    return FileResponse(
        path,
        media_type=mime_type or "video/mp4",
        headers={"Accept-Ranges": "bytes"},
    )



@app.post("/send-text")
async def receive_text(data: dict):
    
    user_text = data.get("text")
    print(user_text)
    finished=await render_picture(user_text)
    return {"received": user_text, "length": len(user_text)}


async def render_picture(text):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "manim",
           "--media_dir","./video/"+str(text) ,
            "-qh",
            str("derivatives_simple.py"),
            "Derivatives",
        ],
        input=f"{text}\n",
        text=True,
        check=True,
    )
    return "Dings"


@app.post("/send-text-video")
async def receive_text_video(data: dict):
    
    user_text = data.get("text")
    print(user_text)
    finished=await render_video(user_text)
    return {"received": user_text, "length": len(user_text)}

async def render_video(text):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "manim",
           "--media_dir","./video/"+str(text) ,
            "-qh",
            str("useful_derivatives.py"),
            "Derivatives",
        ],
        input=f"{text}\n",
        text=True,
        check=True,
    )
    return "Dings"

@app.get("/video/{filename}")
async def get_video(filename: str):
    # Adjust path to your video folder
    #/home/julius/Desktop/manim-main/derivatives-app/backend/2x7
    path = f"/home/julius/Desktop/manim-main/derivatives-app/backend/video/{filename}/videos/useful_derivatives/1080p60/Derivatives.mp4"
    #derivatives-app/backend/video/2x2/images/derivatives_simple/Derivatives_ManimCE_v0.22.0.png
    
    mime_type, _ = mimetypes.guess_type(path)
    return FileResponse(
        path,
        media_type=mime_type or "video/mp4",
        headers={"Accept-Ranges": "bytes"},
    )
