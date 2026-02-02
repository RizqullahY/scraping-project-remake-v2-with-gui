import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

# from modules.komiku_image import download_image as download_image_komiku
from modules.komiku_image import scrape_chapter as scrape_chapter_komiku

example_image_komiku_url    = 'https://komiku.org/the-regressed-son-of-a-duke-is-an-assassin-chapter-01/'
scrape_chapter_komiku(example_image_komiku_url, '0_TEST')


from modules.komikindo_image import download_image as download_image_komikindo
from modules.softkomik_image import download_image as download_image_softkomik_image
from modules.shinigami_image import download_image as download_image_shinigami
# example_image_komikindo_url = 'https://komikindo.ch/the-regressed-son-of-a-duke-is-an-assassin-chapter-1/'
# download_image_komikindo(example_image_komikindo_url)
# example_image_shinigami_url = 'https://08.shinigami.asia/chapter/3e53ba8f-8890-4cc5-b308-e2f894b3dd82'
# download_image_shinigami(example_image_shinigami_url)
# example_image_softkomik_url = 'https://softkomik.com/i-became-the-first-prince-bahasa-indonesia/chapter/000'
# download_image_softkomik_image(example_image_softkomik_url)