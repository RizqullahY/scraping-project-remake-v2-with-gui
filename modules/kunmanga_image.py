import os
import time
import requests
from PIL import Image
from io import BytesIO
from utils.get_exe_path import get_base_path
from INITIAL_VAR import KUNMANGA

BASE_DIR = get_base_path()
OUTPUT_DIR = os.path.join(BASE_DIR, KUNMANGA["IMAGE_FOLDER"])
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "https://sv5.kunsv1.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://kunmanga.com/"
}


def download_and_convert(url, save_path):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return False

        img = Image.open(BytesIO(r.content)).convert("RGB")
        img.save(save_path, "JPEG", quality=95)
        return True
    except:
        return False


def scrape_by_id_range(manga_id, start_chapter, end_chapter, log=print):
    for chapter in range(start_chapter, end_chapter + 1):
        log(f"\n[CHAPTER] {chapter}")

        chapter_index = chapter - 1
        page = 1
        found_any = False

        # ✅ FIX 1: folder chapter
        chapter_dir = os.path.join(OUTPUT_DIR, manga_id, f"Chapter_{chapter}")
        os.makedirs(chapter_dir, exist_ok=True)

        while True:
            filename = f"{str(page).zfill(3)}.jpg"

            # ✅ FIX 2: simpan ke folder chapter
            save_path = os.path.join(chapter_dir, filename)

            jpg_url = (
                f"{BASE_URL}/{manga_id}"
                f"/chapter_{chapter_index}/ch_{chapter}_{page}.jpg"
            )
            webp_url = jpg_url.replace(".jpg", ".webp")

            success = (
                download_and_convert(jpg_url, save_path)
                or
                download_and_convert(webp_url, save_path)
            )

            if not success:
                if page == 1 and not found_any:
                    log("[SKIP] Tidak ada gambar, lanjut chapter berikutnya")
                break

            log(f"[OK] {filename}")
            found_any = True
            page += 1
            time.sleep(0.25)

        if found_any:
            log(f"[DONE] Chapter {chapter}")
