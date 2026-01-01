import os
import webbrowser
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

from utils.get_exe_path import get_base_path


BASE_DIR = get_base_path()
LOGO_PATH = os.path.join(BASE_DIR, "assets" ,"logo.png")


class HomeView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.pack(fill=BOTH, expand=True)

        ttk.Label(
            self,
            text="SCRAPING MANHWA & MANGA PROJECT",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(40, 20))

        self.load_logo()

        self.github_url = "https://github.com/RizqullahY/scraping-project-remake-v2-with-gui"

        link = ttk.Label(
            self,
            text=self.github_url,
            font=("Segoe UI", 11, "bold"),
            foreground="#f5f5f5",   
            cursor="hand2"
        )
        link.pack(pady=(15, 5))
        link.bind("<Button-1>", self.open_github)

        ttk.Button(
            self,
            text="Open GitHub Repository",
            bootstyle=PRIMARY,
            command=self.open_github
        ).pack(pady=15)

    def open_github(self, event=None):
        webbrowser.open(self.github_url)

    def load_logo(self):
        if not os.path.exists(LOGO_PATH):
            ttk.Label(self, text="(logo.png not found)").pack()
            return

        img = Image.open(LOGO_PATH)
        img = img.resize((320, 320), Image.LANCZOS)

        self.logo_img = ImageTk.PhotoImage(img)

        ttk.Label(
            self,
            image=self.logo_img
        ).pack()
