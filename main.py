import os
import glob
import base64
import traceback
from typing import List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from yt_video_fetcher import download_latest_tiktok_videos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also restrict to ["https://your-lovable-subdomain.lovable.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the downloads folder as /static
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Serve video files from /downloads as /static
app.mount("/static", StaticFiles(directory="downloads"), name="static")

class DownloadRequest(BaseModel):
    username: str

@app.post("/download")
def download_videos(request: DownloadRequest):
    try:
        download_latest_tiktok_videos(request.username)
        
        video_files = sorted(
            glob.glob(f"downloads/{request.username}_video_*.mp4"),
            key=os.path.getmtime,
            reverse=True
        )[:5]

        video_urls = [f"/static/{os.path.basename(f)}" for f in video_files]
        return {"status": "success", "video_urls": video_urls}
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()  # 🔍 This will print full traceback
        raise HTTPException(status_code=500, detail=str(e))
