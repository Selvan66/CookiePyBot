from PIL import ImageGrab
import numpy as np
import win32gui
import cv2

class CookieWindowCapture:
    winlist = []
    cookiewin = None
    hwnd = None
    win_rec = None
    w, h = 0, 0

    def __init__(self):
        self.find_window()
        self.win_rec = win32gui.GetWindowRect(self.hwnd)
        self.w = self.win_rec[2] - self.win_rec[0]
        self.h = self.win_rec[3] - self.win_rec[1]

    def find_window(self):
        self.get_winlist()
        self.cookiewin =  [(hwnd, title) for hwnd, title in self.winlist if 'cookie clicker' in title.lower()]
        self.cookiewin = self.cookiewin[0]
        self.hwnd = self.cookiewin[0]

    def get_screen(self):
        self.find_window()
        win32gui.SetForegroundWindow(self.hwnd)
        img = ImageGrab.grab(self.win_rec)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        return img

    def get_winlist(self):
        def enum_cb(hwnd, results):
            self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, None)

    def get_pos(self, pos):
        return (pos[0] + self.win_rec[0], pos[1] + self.win_rec[1])