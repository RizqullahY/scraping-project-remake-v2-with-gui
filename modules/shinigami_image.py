# modules/shinigami_image.py

import os
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.get_exe_path import get_base_path

BASE = get_base_path()
TXT_DIR = os.path.join(BASE, "shinigami_chapter_list")
OUT_DIR = os.path.join(BASE, "shinigami_result")

os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def download_image(url, path):
    try:
        with requests.get(url, stream=True, timeout=10) as r:
            if r.status_code == 200:
                with open(path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
                print(f"[OK] {os.path.basename(path)}")
            else:
                print(f"[FAIL] HTTP {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")


def scrape_chapter(uuid, out_folder):
    api_url = f"https://api.shngm.io/v1/chapter/detail/{uuid}"

    try:
        r = requests.get(api_url, timeout=10)
        data = r.json()["data"]
    except:
        print("[ERROR] API gagal")
        return

    base = data["base_url"]
    path = data["chapter"]["path"]
    images = data["chapter"]["data"]

    pad = len(str(len(images)))
    os.makedirs(out_folder, exist_ok=True)

    print(f"[CHAPTER] {uuid} | {len(images)} gambar")

    with ThreadPoolExecutor(max_workers=12) as exe:
        futures = []
        for i, img in enumerate(images, 1):
            img_url = base + path + img
            filename = f"{str(i).zfill(pad)}.jpg"
            img_path = os.path.join(out_folder, filename)

            futures.append(exe.submit(download_image, img_url, img_path))

        for _ in as_completed(futures):
            pass

    print(f"[DONE] Chapter {uuid}")


def shinigami_download_batch(txt_file):
    txt_path = os.path.join(TXT_DIR, txt_file)
    out_root = os.path.join(OUT_DIR, txt_file.replace(".txt", ""))

    os.makedirs(out_root, exist_ok=True)

    with open(txt_path, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f]

    print(f"[INFO] Total chapter: {len(urls)}")

    for idx, url in enumerate(urls, 1):
        uuid = url.rstrip("/").split("/")[-1]
        chapter_folder = os.path.join(out_root, f"chapter_{idx}")

        scrape_chapter(uuid, chapter_folder)
