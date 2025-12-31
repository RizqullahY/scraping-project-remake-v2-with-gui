import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import os

from modules.kunmanga_image import scrape_by_id_range


class KunmangaView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Kunmanga Scraper", font=("Segoe UI", 18, "bold")).pack(pady=15)

        # ID Manga
        self.id_entry = ttk.Entry(self, width=60)
        self.id_entry.pack(pady=5)
        self.id_entry.insert(0, "manga_xxxxxxxxxxxxxxxxx")

        # Chapter range
        range_frame = ttk.Frame(self)
        range_frame.pack(pady=5)

        ttk.Label(range_frame, text="Chapter Awal").grid(row=0, column=0, padx=5)
        self.start_entry = ttk.Entry(range_frame, width=10)
        self.start_entry.grid(row=0, column=1, padx=5)

        ttk.Label(range_frame, text="Chapter Akhir").grid(row=0, column=2, padx=5)
        self.end_entry = ttk.Entry(range_frame, width=10)
        self.end_entry.grid(row=0, column=3, padx=5)

        ttk.Button(
            self,
            text="Download Images",
            bootstyle=SUCCESS,
            command=self.thread_scrape
        ).pack(pady=10)

        # Logger
        ttk.Label(self, text="Logger:", font=("Segoe UI", 12, "bold")).pack(pady=(15, 0))
        log_frame = ttk.Frame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = ttk.Text(log_frame, height=12, wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Hapus Log", bootstyle=DANGER, command=self.clear_log).pack(pady=8)

    # ================= LOGGER =================

    def log(self, msg):
        self.log_text.after(0, lambda: self._append_log(msg))

    def _append_log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    # ================= THREAD =================

    def thread_scrape(self):
        threading.Thread(target=self.start_scrape, daemon=True).start()

    # ================= LOGIC =================

    def start_scrape(self):
        manga_id = self.id_entry.get().strip()

        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
        except:
            self.log("[ERROR] Chapter harus angka")
            return

        if not manga_id:
            self.log("[ERROR] ID Manga kosong")
            return

        self.log("[START] Scraping dimulai")

        scrape_by_id_range(
            manga_id=manga_id,
            start_chapter=start,
            end_chapter=end,
            log=self.log
        )

        self.log("[DONE] Semua chapter selesai\n")
