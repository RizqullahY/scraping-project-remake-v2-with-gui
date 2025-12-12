import os
import sys


def get_base_path():
    if getattr(sys, 'frozen', False):
        # Saat sudah menjadi EXE → pakai folder tempat EXE berada
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Saat masih script → pakai folder file .py ini berada
        return os.path.dirname(os.path.abspath(__file__))
