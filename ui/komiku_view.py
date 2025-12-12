import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import os

from modules.komiku_chapter import scrape_judulseries
from modules.komiku_image import scrape_images_batch, TXT_DIR


class KomikuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Komiku Scraper", font=("Segoe UI", 18, "bold")).pack(pady=15)

        # URL Input
        self.url_entry = ttk.Entry(self, width=60)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "Masukkan URL Komiku…")

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

        # Logger area
        ttk.Label(self, text="Logger:", font=("Segoe UI", 12, "bold")).pack(pady=(15, 0))
        log_frame = ttk.Frame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = ttk.Text(log_frame, height=10, wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Hapus Log", bootstyle=DANGER, command=self.clear_log).pack(pady=8)

    # Logger function (thread-safe)
    def log(self, msg):
        self.log_text.after(0, lambda: self._append_log(msg))

    def _append_log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    # Reload txt files
    def reload_txt_files(self):
        files = [f for f in os.listdir(TXT_DIR) if f.endswith(".txt")]
        self.txt_box["values"] = files if files else ["<Tidak ada txt>"]
        if files:
            self.txt_box.current(0)

    # Threads
    def thread_scrape_chapter(self):
        threading.Thread(target=self.scrape_chapter, daemon=True).start()

    def thread_scrape_images(self):
        threading.Thread(target=self.scrape_images, daemon=True).start()

    # Scraping functions
    def scrape_chapter(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("[ERROR] URL kosong!")
            return

        self.log(f"[START] Scraping URL: {url}")
        scrape_judulseries(url, log=self.log)
        self.reload_txt_files()
        self.log("[DONE] Scrape chapter selesai.\n")

    def scrape_images(self):
        selected = self.txt_var.get().strip()
        if "<Tidak ada txt>" in selected:
            self.log("[ERROR] Tidak ada file .txt ditemukan.")
            return

        self.log(f"[START] Download images dari: {selected}")
        scrape_images_batch(selected, log=self.log)
        self.log("[DONE] Download images selesai.\n")
