import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil
from utils.get_exe_path import get_base_path

BASE = get_base_path()
TXT_DIR = os.path.join(BASE,"komiku_chapter_list")
OUT_DIR = os.path.join(BASE,"komiku_result")

os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def download_image(url, path, log=lambda x: None):
    try:
        with requests.get(url, stream=True, timeout=10) as r:
            if r.status_code == 200:
                with open(path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
                log(f"[OK] {os.path.basename(path)}")
            else:
                log(f"[FAIL] HTTP {r.status_code}")
    except Exception as e:
        log(f"[ERROR] {e}")

def scrape_chapter(url, folder, log=lambda x: None):
    log(f"[CHAPTER] {url}")
    try:
        r = requests.get(url, timeout=10)
    except:
        log("[ERROR] tidak bisa fetch halaman")
        return

    soup = BeautifulSoup(r.text, "lxml")
    images = [img["src"] for img in soup.find_all("img", itemprop="image")]

    pad = len(str(len(images)))
    os.makedirs(folder, exist_ok=True)

    with ThreadPoolExecutor(max_workers=10) as exe:
        futures = []
        for i, img_url in enumerate(images, 1):
            filename = f"{str(i).zfill(pad)}.jpg"
            img_path = os.path.join(folder, filename)
            futures.append(exe.submit(download_image, img_url, img_path, log))
        for _ in as_completed(futures):
            pass

    log(f"[DONE] {folder}")

def scrape_images_batch(txt_file, log=lambda x: None):
    path = os.path.join(TXT_DIR, txt_file)
    out = os.path.join(OUT_DIR, txt_file.replace(".txt", ""))

    os.makedirs(out, exist_ok=True)

    with open(path, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f]

    log(f"[INFO] Total chapter {len(urls)}")

    for idx, url in enumerate(urls, 1):
        folder = os.path.join(out, f"chapter_{idx}")
        scrape_chapter(url, folder, log)
