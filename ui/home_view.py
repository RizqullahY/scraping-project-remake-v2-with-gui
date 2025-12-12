import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from ui.komiku_view import KomikuView
# from ui.shinigami_view import ShinigamiView


class HomeView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Manga Scraper", font=("Segoe UI", 24, "bold")).pack(pady=40)
