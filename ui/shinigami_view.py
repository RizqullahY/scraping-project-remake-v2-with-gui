import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import os

from modules.shinigami_chapter import shinigami_scrape_series
from modules.shinigami_image import shinigami_download_batch, TXT_DIR


class ShinigamiView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        ttk.Label(self, text="Shinigami Scraper", font=("Segoe UI", 18, "bold")).pack(pady=15)

        self.url_entry = ttk.Entry(self, width=60)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "Masukkan URL Shinigami…")

        ttk.Button(self, text="Scrape Chapter List",
                   bootstyle=PRIMARY,
                   command=self.thread_scrape_chapter).pack(pady=5)

        ttk.Label(self, text="Pilih file chapter list:", font=("Segoe UI", 12)).pack(pady=10)

        self.txt_var = ttk.StringVar()
        self.txt_box = ttk.Combobox(self, textvariable=self.txt_var, width=50, bootstyle=INFO)
        self.txt_box.pack()

        self.reload_txt_files()

        ttk.Button(self, text="Download Images",
                   bootstyle=SUCCESS,
                   command=self.thread_scrape_images).pack(pady=10)


    def reload_txt_files(self):
        files = [f for f in os.listdir(TXT_DIR) if f.endswith(".txt")]
        self.txt_box["values"] = files if files else ["<Tidak ada txt>"]
        if files:
            self.txt_box.current(0)

    def thread_scrape_chapter(self):
        threading.Thread(target=self.scrape_chapter, daemon=True).start()

    def thread_scrape_images(self):
        threading.Thread(target=self.scrape_images, daemon=True).start()

    def scrape_chapter(self):
        url = self.url_entry.get().strip()
        if not url:
            print("[ERROR] URL kosong!")
            return

        print(f"[START] Scraping Shinigami: {url}")

        shinigami_scrape_series(url)

        self.reload_txt_files()
        print("[DONE] Scrape chapter list selesai.")

    def scrape_images(self):
        selected = self.txt_var.get().strip()

        if "<Tidak ada txt>" in selected:
            print("[ERROR] Tidak ada file .txt")
            return

        print(f"[START] Download images dari: {selected}")
        shinigami_download_batch(selected)
        print("[DONE] Download images selesai.")
