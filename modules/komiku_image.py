import os
import sys
import time
import requests
from bs4 import BeautifulSoup
import shutil
from utils.get_exe_path import get_base_path
from INITIAL_VAR import KOMIKU

# ===== FIX stdout PyInstaller =====
sys.stdout = sys.__stdout__

BASE = get_base_path()
TXT_DIR = os.path.join(BASE, KOMIKU["CHAPTER_LIST_FOLDER"])
OUT_DIR = os.path.join(BASE, KOMIKU["IMAGE_FOLDER"])

os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def download_image(url, path, log=print, retries=3, delay=0.5):
    for attempt in range(1, retries + 1):
        try:
            with requests.get(url, stream=True, timeout=15) as r:
                if r.status_code == 200:
                    with open(path, "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                    log(f"[OK] {os.path.basename(path)}")
                    return True
                else:
                    log(f"[FAIL] HTTP {r.status_code} (try {attempt})")
        except Exception as e:
            log(f"[ERROR] {e} (try {attempt})")

        time.sleep(delay)

    log(f"[GIVE UP] {os.path.basename(path)}")
    return False


def scrape_chapter(url, folder, log=print):
    log(f"\n[CHAPTER] {url}")

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except Exception as e:
        log(f"[ERROR] fetch halaman: {e}")
        return

    soup = BeautifulSoup(r.text, "lxml")
    images = [img["src"] for img in soup.find_all("img", itemprop="image")]

    if not images:
        log("[WARN] tidak ada gambar ditemukan")
        return

    pad = len(str(len(images)))
    os.makedirs(folder, exist_ok=True)

    for i, img_url in enumerate(images, 1):
        filename = f"{str(i).zfill(pad)}.jpg"
        img_path = os.path.join(folder, filename)

        if os.path.exists(img_path):
            log(f"[SKIP] {filename}")
            continue

        download_image(img_url, img_path, log)
        time.sleep(0.3)  # delay antar gambar

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
