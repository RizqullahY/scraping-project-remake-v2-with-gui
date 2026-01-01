import os
import sys


def get_base_path():
    if getattr(sys, 'frozen', False):
        # Saat sudah menjadi EXE → pakai folder tempat EXE berada
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Saat masih script → pakai utils/get_exe_path.py ini berada
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
def get_asset_path(*paths):
    """
    Aman untuk:
    - mode python biasa
    - PyInstaller --onefile
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *paths)