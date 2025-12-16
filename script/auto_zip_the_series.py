import re
import zipfile
from pathlib import Path
import sys
import questionary
from itertools import islice
from tqdm import tqdm


# ===========================================================
# BASE DIR
# ===========================================================
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent


# ===========================================================
# BANNER
# ===========================================================
def banner():
    print("\n" + "=" * 60)
    print("📦  CHAPTER ZIPPER TOOL  |  FAST • CLEAN • PROGRESS")
    print("=" * 60)


# ===========================================================
# COLLECT CHAPTERS
# ===========================================================
def collect_chapters(series_dir):
    chapters = {}
    for folder in series_dir.iterdir():
        if folder.is_dir() and folder.name.lower().startswith("chapter"):
            m = re.search(r"(\d+)", folder.name)
            if m:
                chapters[int(m.group(1))] = folder
    return dict(sorted(chapters.items()))


# ===========================================================
# ZIP BATCH + PROGRESS
# ===========================================================
def zip_batch(series_dir, chapters, batch):
    start_num, end_num = batch[0], batch[-1]
    prefix = series_dir.name
    zip_name = f"{prefix}_{start_num}-{end_num}.zip"
    zip_path = series_dir / zip_name
    wrapper = f"{prefix}_{start_num}-{end_num}"

    # kumpulin file dulu (biar tqdm akurat)
    files = []
    for num in batch:
        for f in chapters[num].rglob("*"):
            if f.is_file():
                files.append(f)

    print(f"\n📦 Membuat ZIP: {zip_name}")
    print(f"📂 Total file: {len(files)}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in tqdm(files, desc="🗜️ Zipping", unit="file"):
            arcname = Path(wrapper) / file.relative_to(series_dir)
            zf.write(file, arcname)

    print(f"✅ ZIP selesai → {zip_path.name}")


# ===========================================================
# MODE RANGE
# ===========================================================
def mode_range(series_dir, chapters):
    chapter_nums = list(chapters.keys())

    print(f"\n📊 Chapter ditemukan: {len(chapter_nums)}")
    print(f"📘 Range tersedia: {chapter_nums[0]} - {chapter_nums[-1]}")

    start_range = int(questionary.text("▶ Mulai dari chapter?").ask())
    end_range = int(questionary.text("▶ Sampai chapter?").ask())
    batch_size = int(questionary.text("▶ Per ZIP berapa chapter?").ask())

    filtered = [c for c in chapter_nums if start_range <= c <= end_range]
    if not filtered:
        print("❌ Range kosong.")
        return

    it = iter(filtered)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        zip_batch(series_dir, chapters, batch)


# ===========================================================
# PILIH FOLDER SERIES
# ===========================================================
def choose_series_folder(base_dir):
    candidates = [p for p in base_dir.rglob("0_IMAGE*/*") if p.is_dir()]

    if not candidates:
        print("❌ Folder series tidak ditemukan.")
        return None

    selected = questionary.select(
        "📂 Pilih folder series:",
        choices=[str(p) for p in candidates]
    ).ask()

    return Path(selected)


# ===========================================================
# MAIN LOOP
# ===========================================================
def main():
    banner()
    series_dir = None
    chapters = None

    while True:
        if not series_dir:
            series_dir = choose_series_folder(BASE_DIR)
            if not series_dir:
                return

            chapters = collect_chapters(series_dir)
            if not chapters:
                print("❌ Tidak ada folder chapter.")
                series_dir = None
                continue

        mode_range(series_dir, chapters)

        action = questionary.select(
            "\n🔁 Pilih aksi selanjutnya:",
            choices=[
                "📦 Zip lagi (range baru)",
                "📂 Pilih folder series lain",
                "🚪 Keluar"
            ]
        ).ask()

        if "folder" in action:
            series_dir = None
            chapters = None
        elif "Keluar" in action:
            print("\n👋 Selesai! Semua ZIP beres.")
            break


if __name__ == "__main__":
    main()
