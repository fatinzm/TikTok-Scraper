import os
import glob
import base64
from typing import List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from yt_video_fetcher import download_latest_tiktok_videos

app = FastAPI()

# Serve video files from /downloads as /static
app.mount("/static", StaticFiles(directory="downloads"), name="static")

class DownloadRequest(BaseModel):
    username: str

@app.post("/download")
def download_videos(request: DownloadRequest):
    try:
        download_latest_tiktok_videos(request.username)
        # Get last 2 downloaded .mp4 files by modification time
        video_files = sorted(
            glob.glob("downloads/*.mp4"),
            key=os.path.getmtime,
            reverse=True
        )[:2]

        # Return public URLs to frontend
        video_urls = [f"/static/{os.path.basename(f)}" for f in video_files]
        return {"status": "success", "video_urls": video_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))