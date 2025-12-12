# modules/shinigami_chapter.py

import os
import requests
from utils.get_exe_path import get_base_path

BASE = get_base_path()
OUT = os.path.join(BASE, "..", "shinigami_chapter_list")
os.makedirs(OUT, exist_ok=True)


def extract_uuid(url):
    return url.rstrip("/").split("/")[-1]


def fetch_all(uuid):
    page = 1
    all_items = []

    while True:
        api = f"https://api.shngm.io/v1/chapter/{uuid}/list?page={page}&page_size=24"
        r = requests.get(api, timeout=10)
        if r.status_code != 200:
            break

        items = r.json().get("data", [])
        if not items:
            break

        all_items.extend(items)

        if len(items) < 24:
            break

        page += 1

    return all_items


def fetch_title(uuid):
    r = requests.get(f"https://api.shngm.io/v1/manga/detail/{uuid}", timeout=10)
    if r.status_code != 200:
        return uuid
    return r.json().get("data", {}).get("title", uuid)


def shinigami_scrape_series(url):

    uuid = extract_uuid(url)
    items = fetch_all(uuid)
    title = fetch_title(uuid)

    chapter_urls = []
    for c in items:
        cid = c.get("chapter_id")
        if cid:
            chapter_urls.append("https://08.shinigami.asia/chapter/" + cid)

    chapter_urls.reverse()

    safe = title.replace(" ", "_")
    out_file = os.path.join(OUT, safe + ".txt")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(chapter_urls))

    print(f"[DONE] Disimpan: {out_file}")
