import os
import sys
import time
import json
import requests
from bs4 import BeautifulSoup
import shutil
from utils.get_exe_path import get_base_path
from INITIAL_VAR import SOFTKOMIK
from PIL import Image
from io import BytesIO

# ===== FIX stdout PyInstaller =====
sys.stdout = sys.__stdout__

BASE = get_base_path()
TXT_DIR = os.path.join(BASE, SOFTKOMIK["CHAPTER_LIST_FOLDER"])
OUT_DIR = os.path.join(BASE, SOFTKOMIK["IMAGE_FOLDER"])

os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


# ==============================
# IMAGE DOWNLOADER
# ==============================
def download_image(url, path, log=print, retries=3, delay=0.5):
    jpg_path = path.replace(".webp", ".jpg")

    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                img = Image.open(BytesIO(r.content)).convert("RGB")
                img.save(jpg_path, "JPEG", quality=95)

                log(f"[OK] {os.path.basename(jpg_path)}")
                return True
            else:
                log(f"[FAIL] HTTP {r.status_code} (try {attempt})")
        except Exception as e:
            log(f"[ERROR] {e} (try {attempt})")

        time.sleep(delay)

    log(f"[GIVE UP] {os.path.basename(jpg_path)}")
    return False



# ==============================
# SOFTKOMIK CHAPTER SCRAPER
# ==============================
def scrape_chapter_softkomik(url, folder, log=print):
    log(f"\n[SOFTKOMIK] {url}")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://softkomik.com/",
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        log(f"[ERROR] fetch halaman: {e}")
        return

    soup = BeautifulSoup(r.text, "lxml")
    script = soup.find("script", id="__NEXT_DATA__")

    if not script:
        log("[ERROR] __NEXT_DATA__ tidak ditemukan")
        return

    try:
        data = json.loads(script.string)
        images = data["props"]["pageProps"]["data"]["data"]["imageSrc"]
    except Exception as e:
        log(f"[ERROR] parse JSON: {e}")
        return

    if not images:
        log("[WARN] tidak ada gambar ditemukan")
        return

    os.makedirs(folder, exist_ok=True)
    pad = len(str(len(images)))

    for i, img in enumerate(images, 1):
        # 🛠 FIX: pakai base yang benar
        img_url = "https://image.softkomik.com/softkomik/" + img.lstrip("/")

        filename = f"{str(i).zfill(pad)}.webp"
        img_path = os.path.join(folder, filename)

        if os.path.exists(img_path):
            log(f"[SKIP] {filename}")
            continue

        download_image(img_url, img_path, log)
        time.sleep(0.3)

    log(f"[DONE] {folder}")

# ==============================
# BATCH SCRAPER (FROM TXT)
# ==============================
def scrape_images_batch(txt_file, log=print):
    path = os.path.join(TXT_DIR, txt_file)
    out = os.path.join(OUT_DIR, txt_file.replace(".txt", ""))

    os.makedirs(out, exist_ok=True)

    with open(path, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]

    log(f"[INFO] Total chapter {len(urls)}")

    for url in urls:
        chap = url.rstrip("/").split("/")[-1]  # ambil 085 / 0010 / dll
        folder = os.path.join(out, f"chapter_{chap}")
        scrape_chapter_softkomik(url, folder, log)

