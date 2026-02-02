import requests
import os
from utils.get_exe_path import get_base_path
from INITIAL_VAR import SOFTKOMIK

BASE_DIR = get_base_path()
OUTPUT_DIR = os.path.join(BASE_DIR, SOFTKOMIK["CHAPTER_LIST_FOLDER"])
os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_filename(slug: str) -> str:
    words = slug.replace("-", " ").split()

    blacklist = {"bahasa", "indonesia"}
    words = [w for w in words if w not in blacklist]

    formatted = "_".join(w.capitalize() for w in words)

    return formatted + ".txt"



def get_slug(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def scrape_judulseries(url, log=lambda x: None):
    slug = get_slug(url)

    api_url = (
        f"https://v2.softkomik.com/komik/"
        f"{slug}/chapter?limit=9999999"
    )

    try:
        res = requests.get(api_url, timeout=15)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        log(f"[ERROR] API fetch gagal: {e}")
        return

    # ✅ STRUKTUR JSON YANG BENAR
    chapters = data.get("chapter")

    if not isinstance(chapters, list) or not chapters:
        log("[ERROR] Chapter kosong / struktur API berubah")
        return

    chapters = list(reversed(chapters))

    chapter_urls = []

    for ch in chapters:
        chap_str = ch.get("chapter")
        if not chap_str:
            continue

        # ❗ PAKAI APA ADANYA (0010 TETAP 0010)
        chapter_urls.append(f"{url}/chapter/{chap_str}")

    # optional: urutkan STRING apa adanya

    out_file = os.path.join(
        OUTPUT_DIR,
        format_filename(slug)
    )

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(chapter_urls))

    log(f"[DONE] {len(chapter_urls)} chapter disimpan ke {out_file}")
