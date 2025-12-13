import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from utils.get_exe_path import get_base_path
from INITIAL_VAR import KOMIKU

BASE_DIR = get_base_path()
OUTPUT_DIR = os.path.join(BASE_DIR, KOMIKU["CHAPTER_LIST_FOLDER"])
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scrape_judulseries(url, log=lambda x: None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except:
        log("[ERROR] Request gagal.")
        return

    soup = BeautifulSoup(r.text, "lxml")
    title_tag = soup.find("title")

    safe_title = "output"
    if title_tag:
        valid = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        safe_title = "".join(c for c in title_tag.text if c in valid).replace(" ", "_")

    output_file = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")

    urls = []
    for td in soup.find_all("td", class_="judulseries"):
        link = td.find("a")
        if link and "href" in link.attrs:
            urls.append(urljoin(url, link["href"]))

    urls.reverse()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(urls))

    log(f"[DONE] {len(urls)} chapter disimpan ke {output_file}")
