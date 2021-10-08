from PIL import ImageGrab
import numpy as np
import time
import win32gui, win32ui, win32con
import cv2

class CookieWindowCapture:
    winlist = []
    cookiewin = None
    hwnd = None
    win_rec = None
    w, h = 0, 0 
    window_name = 'studio code'

    def get_winlist(self):
        def enum_cb(hwnd, results):
            self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, None)

    def find_window(self):
        self.get_winlist()
        self.cookiewin =  [(hwnd, title) for hwnd, title in self.winlist if self.window_name in title.lower()]
        while not self.cookiewin:
            print(f'Cannot find {self.window_name} window')
            self.get_winlist()
            self.cookiewin =  [(hwnd, title) for hwnd, title in self.winlist if self.window_name in title.lower()]
            time.sleep(1)

        self.cookiewin = self.cookiewin[0]
        self.hwnd = self.cookiewin[0]
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        self.win_rec = win32gui.GetWindowRect(self.hwnd)

    def get_screen(self):
        img = ImageGrab.grab(self.win_rec, all_screens=True)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGR)

    def get_pos(self, pos):
        return (pos[0] + self.win_rec[0], pos[1] + self.win_rec[1])