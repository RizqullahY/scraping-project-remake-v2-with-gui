import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.komikindo_chapter import scrape_judulseries as scrape_judulseries_komikindo
from modules.komiku_chapter import scrape_judulseries as scrape_judulseries_komiku
from modules.softkomik_chapter import scrape_judulseries as scrape_judulseries_softkomik 
from modules.shinigami_chapter import shinigami_scrape_series as scrape_judulseries_shinigami
 
komikindo_chapter_scrape_url = 'https://komikindo.ch/komik/698479-the-regressed-son-of-a-duke-is-an-assassin/'
scrape_judulseries_komikindo(komikindo_chapter_scrape_url)

komiku_chapter_scrape_url    = 'https://komiku.org/manga/the-regressed-son-of-a-duke-is-an-assassin/'
scrape_judulseries_komiku(komiku_chapter_scrape_url)

softkomik_chapter_scrape_url = 'https://softkomik.com/i-became-the-first-prince-bahasa-indonesia'
scrape_judulseries_softkomik(softkomik_chapter_scrape_url)

shinigami_chapter_scrape_url = 'https://09.shinigami.asia/series/b5f07831-f952-4919-af7c-aae4cadeb607'
scrape_judulseries_shinigami(shinigami_chapter_scrape_url)