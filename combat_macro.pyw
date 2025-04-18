import time
import win32gui
import win32api
import win32con

# === CONFIGURATION ===
TARGET_WINDOW_NAME = "FINAL FANTASY XIV"

# === LOG ===
sys.stdout = open("macro.log", "w")
sys.stderr = sys.stdout

# === WINDOW ===
def find_window_handle(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        return None
    return hwnd

# === KEYS ===
def send_key(hwnd, key_code):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    time.sleep(0.05)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_code, 0)

# === MACRO ===
def run_macro():
    hwnd = find_window_handle(TARGET_WINDOW_NAME)
    if not hwnd:
        return

    send_key(hwnd, 0x31)  # 1
    time.sleep(2.5)
    send_key(hwnd, 0x32)  # 2
    time.sleep(2.5)
    send_key(hwnd, 0x33)  # 3
    time.sleep(2.5)

if __name__ == "__main__":
    while True:
        run_macro()
