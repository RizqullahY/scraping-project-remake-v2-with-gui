# utils/window_utils.py


def center_window(win):
    """
    Memposisikan window/Toplevel di tengah layar.
    win = instance ttk.Window atau ttk.Toplevel
    """
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)

    win.geometry(f"{width}x{height}+{x}+{y}")
