# modules/shinigami_image.py

import os
import sys
import time
import requests
import shutil
from utils.get_exe_path import get_base_path
from INITIAL_VAR import SHINIGAMI

# ===== stdout fix for PyInstaller =====
sys.stdout = sys.__stdout__

BASE = get_base_path()
TXT_DIR = os.path.join(BASE, SHINIGAMI["CHAPTER_LIST_FOLDER"])
OUT_DIR = os.path.join(BASE, SHINIGAMI["IMAGE_FOLDER"])

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


def scrape_chapter(uuid, out_folder, log=print):
    api_url = f"https://api.shngm.io/v1/chapter/detail/{uuid}"

    try:
        r = requests.get(api_url, timeout=15)
        r.raise_for_status()
        data = r.json()["data"]
    except Exception as e:
        log(f"[ERROR] API gagal: {e}")
        return

    base = data["base_url"]
    path = data["chapter"]["path"]
    images = data["chapter"]["data"]

    if not images:
        log("[WARN] Tidak ada gambar")
        return

    pad = len(str(len(images)))
    os.makedirs(out_folder, exist_ok=True)

    log(f"\n[CHAPTER] {uuid} | {len(images)} gambar")

    for i, img in enumerate(images, 1):
        img_url = base + path + img
        filename = f"{str(i).zfill(pad)}.jpg"
        img_path = os.path.join(out_folder, filename)

        if os.path.exists(img_path):
            log(f"[SKIP] {filename}")
            continue

        download_image(img_url, img_path, log)
        time.sleep(0.3)  # delay antar gambar

    log(f"[DONE] Chapter {uuid}")


def shinigami_download_batch(txt_file, log=print):
    txt_path = os.path.join(TXT_DIR, txt_file)
    out_root = os.path.join(OUT_DIR, txt_file.replace(".txt", ""))

    os.makedirs(out_root, exist_ok=True)

    with open(txt_path, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]

    log(f"[INFO] Total chapter: {len(urls)}")

    for idx, url in enumerate(urls, 1):
        uuid = url.rstrip("/").split("/")[-1]
        chapter_folder = os.path.join(out_root, f"chapter_{idx}")
        scrape_chapter(uuid, chapter_folder, log)
