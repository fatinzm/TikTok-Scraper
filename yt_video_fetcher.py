import os
import subprocess
import time
import sys
import tempfile
import base64
import re
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc


def fetch_latest_video_urls(username: str, max_videos: int = 2):
    url = f"https://www.tiktok.com/@{username}"
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/video/")]'))
        )
        links = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')
        hrefs = []
        for link in links:
            href = link.get_attribute("href")
            if href and "/video/" in href and href not in hrefs:
                hrefs.append(href)
            if len(hrefs) >= max_videos:
                break
        return hrefs
    finally:
        driver.quit()


def download_latest_tiktok_videos(username: str, output_dir: str = "downloads"):
    os.makedirs(output_dir, exist_ok=True)
    urls = fetch_latest_video_urls(username)
    for url in urls:
        subprocess.run([
            "yt-dlp",
            url,
            "-P", output_dir
        ])
