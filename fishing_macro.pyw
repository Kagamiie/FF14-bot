import cv2
import numpy as np
import threading
import time
import win32gui
import win32ui
import win32con
import win32process
import win32api
import os
import sys

# === LOG ===
sys.stdout = open("macro.log", "w")
sys.stderr = sys.stdout

# === CONFIGURATION ===
IMAGE_PATHS = ["target1.png", "target2.png", "target3.png"]
PID_FILE = "ffxiv_macro.pid"
TARGET_WINDOW_NAME = "FINAL FANTASY XIV"

# === WINDOW ===
def find_window_handle(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print(f"Window '{title}' not found.")
        return None
    return hwnd

def capture_window(hwnd):
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width, height = right - left, bottom - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr  = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

# === MATCHING ===
def image_found_on_window(hwnd, image_paths):
    screen = capture_window(hwnd)
    for path in image_paths:
        template = cv2.imread(path)
        if template is None:
            print(f"Image not found on disk: {path}")
            continue
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > 0.85:
            print(f"Match found: {path} (conf: {max_val:.2f})")
            return True
    return False

# === KEYS ===
def send_key(hwnd, key_code):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    time.sleep(0.05)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_code, 0)

# === MACRO ===
def macro_loop():
    hwnd = find_window_handle(TARGET_WINDOW_NAME)
    if not hwnd:
        return

    print("Window found. Fishing macro started.")

    while True:
        print("Start fishing: send 1")
        send_key(hwnd, 0x31)  # Key '1'

        # Wait up to 5s for fish target
        target = False
        for _ in range(10):
            if image_found_on_window(hwnd, IMAGE_PATHS):
                print("Fish target detected! Send 2.")
                send_key(hwnd, 0x32)  # Key '2'
                target = True
                break
            time.sleep(0.5)

        if not target:
            print("No target, retrying... Send 1 then wait then 1 again")
            send_key(hwnd, 0x31)
            time.sleep(1.5)
            send_key(hwnd, 0x31)

# === THREAD LAUNCHER ===
def start_macro():
    t = threading.Thread(target=macro_loop, daemon=True)
    t.start()
    pid = os.getpid()
    with open(PID_FILE, "w") as f:
        f.write(str(pid))
    print(f"Macro started. PID: {pid} saved to {PID_FILE}.")
    t.join()

if __name__ == "__main__":
    start_macro()
