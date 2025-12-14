import re
import zipfile
from pathlib import Path
import sys
import questionary


# -----------------------------------------------------------
# BASE DIR (AMAN UNTUK EXE)
# -----------------------------------------------------------
if getattr(sys, "frozen", False):
    base_dir = Path(sys.executable).parent
else:
    base_dir = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------
# UTIL: Parse input "1,2,5,10-15"
# -----------------------------------------------------------
def parse_selection(selection):
    numbers = set()
    for part in selection.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
            numbers.update(range(start, end + 1))
        else:
            numbers.add(int(part))
    return sorted(numbers)


# -----------------------------------------------------------
# UTIL: Collect chapterXXX folders
# -----------------------------------------------------------
def collect_chapters(series_dir):
    chapters = {}
    for folder in series_dir.iterdir():
        if folder.is_dir() and folder.name.lower().startswith("chapter"):
            match = re.search(r"(\d+)", folder.name)
            if match:
                chapters[int(match.group(1))] = folder
    return dict(sorted(chapters.items()))


# -----------------------------------------------------------
# UTIL: Create ZIP for a batch of chapters
# -----------------------------------------------------------
def zip_batch(series_dir, chapters, start_num, end_num):
    prefix = series_dir.name
    zip_name = f"{prefix}_{start_num}-{end_num}.zip"
    zip_path = series_dir / zip_name
    wrapper_folder = f"{prefix}_{start_num}-{end_num}"

    print(f"\n📦 Membuat ZIP: {zip_name}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for num in range(start_num, end_num + 1):
            if num not in chapters:
                continue

            for file_path in chapters[num].rglob("*"):
                if file_path.is_file():
                    arcname = Path(wrapper_folder) / file_path.relative_to(series_dir)
                    zf.write(file_path, arcname)

    print(f"✅ ZIP selesai → {zip_path}")


# -----------------------------------------------------------
# MODE: Manual
# -----------------------------------------------------------
def mode_manual(series_dir, chapters):
    selection = questionary.text(
        "Masukkan daftar chapter (contoh: 1,2,5,10-15):"
    ).ask()

    selected = parse_selection(selection)
    print(f"→ Chapter terpilih: {selected}")

    zip_batch(series_dir, chapters, selected[0], selected[-1])


# -----------------------------------------------------------
# MODE: Otomatis
# -----------------------------------------------------------
def mode_otomatis(series_dir, chapters):
    chapter_nums = list(chapters.keys())

    start_from = int(questionary.text(
        f"Mulai dari chapter berapa? ({chapter_nums[0]}–{chapter_nums[-1]}):"
    ).ask())

    batch_size = int(questionary.text(
        "Batch size berapa? (contoh: 5):"
    ).ask())

    filtered = [c for c in chapter_nums if c >= start_from]

    for i in range(0, len(filtered), batch_size):
        batch = filtered[i:i + batch_size]
        zip_batch(series_dir, chapters, batch[0], batch[-1])


# -----------------------------------------------------------
# MODE: Range
# -----------------------------------------------------------
def mode_range(series_dir, chapters):
    start_range = int(questionary.text("Mulai dari chapter berapa?").ask())
    end_range = int(questionary.text("Sampai chapter berapa?").ask())
    batch_size = int(questionary.text("Batch size berapa?").ask())

    filtered = [c for c in chapters if start_range <= c <= end_range]

    for i in range(0, len(filtered), batch_size):
        batch = filtered[i:i + batch_size]
        zip_batch(series_dir, chapters, batch[0], batch[-1])


# -----------------------------------------------------------
# SELECT SERIES FOLDER
# -----------------------------------------------------------
def choose_series_folder(base_dir):
    candidates = [p for p in base_dir.rglob("0_IMAGE*/*") if p.is_dir()]

    if not candidates:
        print("❌ Folder series tidak ditemukan.")
        return None

    selected = questionary.select(
        "Pilih folder series:",
        choices=[str(p) for p in candidates]
    ).ask()

    return Path(selected)


# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------
if __name__ == "__main__":
    series_dir = choose_series_folder(base_dir)
    if not series_dir:
        sys.exit()

    chapters = collect_chapters(series_dir)
    if not chapters:
        print("❌ Tidak ada folder chapter.")
        sys.exit()

    mode = questionary.select(
        "Pilih mode:",
        choices=[
            "Manual",
            "Otomatis",
            "Range",
        ]
    ).ask()

    if mode == "Manual":
        mode_manual(series_dir, chapters)
    elif mode == "Otomatis":
        mode_otomatis(series_dir, chapters)
    else:
        mode_range(series_dir, chapters)

    input("\n🎉 Selesai. Tekan ENTER untuk keluar...")
