import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from utils.get_exe_path import get_base_path
from INITIAL_VAR import KOMIKINDO

# ===== FIX stdout PyInstaller =====
sys.stdout = sys.__stdout__

BASE = get_base_path()
TXT_DIR = os.path.join(BASE, KOMIKINDO["CHAPTER_LIST_FOLDER"])
OUT_DIR = os.path.join(BASE, KOMIKINDO["IMAGE_FOLDER"])

os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer": "https://komikindo.tv/"
}


def download_image(url, path, log=print, retries=5, delay=0.5):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200 and r.content:
                with open(path, "wb") as f:
                    f.write(r.content)

                log(f"[OK] {os.path.basename(path)}")
                return True
            else:
                log(f"[FAIL] HTTP {r.status_code} (try {attempt})")

        except Exception as e:
            log(f"[ERROR] {e} (try {attempt})")

        time.sleep(delay)

    log(f"[GIVE UP] {os.path.basename(path)} {url}")
    return False


def scrape_chapter(url, folder, log=print):
    log(f"\n[CHAPTER] {url}")

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        log(f"[ERROR] fetch halaman: {e}")
        return

    soup = BeautifulSoup(r.text, "lxml")

    images = [
        img.get("src")
        for img in soup.select("#chimg-auh img")
        if img.get("src")
    ]

    if not images:
        log("[WARN] tidak ada gambar ditemukan")
        return

    os.makedirs(folder, exist_ok=True)
    pad = len(str(len(images)))

    for i, img_url in enumerate(images, 1):
        filename = f"{str(i).zfill(pad)}.jpg"
        img_path = os.path.join(folder, filename)

        if os.path.exists(img_path):
            log(f"[SKIP] {filename}")
            continue

        download_image(img_url, img_path, log)
        time.sleep(0.3)

    log(f"[DONE] {folder}")


def scrape_images_batch(txt_file, log=print):
    path = os.path.join(TXT_DIR, txt_file)
    out = os.path.join(OUT_DIR, txt_file.replace(".txt", ""))

    os.makedirs(out, exist_ok=True)

    with open(path, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]

    log(f"[INFO] Total chapter {len(urls)}")

    for idx, url in enumerate(urls, 1):
        folder = os.path.join(out, f"chapter_{idx}")
        scrape_chapter(url, folder, log)
