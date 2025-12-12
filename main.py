import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ui.home_view import HomeView
from ui.komiku_view import KomikuView
from ui.shinigami_view import ShinigamiView
from utils.window_utils import center_window


class App(ttk.Window):
    def __init__(self):
        super().__init__(
            title="Manga Scraper GUI",
            themename="superhero",
            size=(700, 400),
            resizable=(False, False)
        )
        center_window(self)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # BUAT FRAME
        self.home_tab = HomeView(self.notebook, self)
        self.komiku_tab = KomikuView(self.notebook, self)
        self.shini_tab = ShinigamiView(self.notebook, self)

        # TAMBAH TAB
        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.komiku_tab, text="Komiku")
        self.notebook.add(self.shini_tab, text="Shinigami")


if __name__ == "__main__":
    app = App()
    app.mainloop()
