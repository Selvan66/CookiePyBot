from PIL import ImageGrab
import numpy as np
import time
import win32gui, win32con
import cv2

class CookieWindowCapture:
    winlist = []
    cookiewin = None
    hwnd = None
    win_rec = None
    w, h = 0, 0 
    window_name = ' cookie '

    def get_winlist(self):
        def enum_cb(hwnd, _):
            self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, None)

    def find_window(self):
        self.get_winlist()
        self.cookiewin =  [(hwnd, title) for hwnd, title in self.winlist if self.window_name in title.lower()]
        if not self.cookiewin:
            raise NameError('Window %s not found' % self.window_name)
        self.cookiewin = self.cookiewin[0]
        self.hwnd = self.cookiewin[0]
        # There is no better way to focus window
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWMINIMIZED)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWMAXIMIZED)

        
        self.win_rec = win32gui.GetWindowRect(self.hwnd)
        time.sleep(0.5) # time to open window while is minimized

    def get_screen(self):
        self.find_window()
        img = ImageGrab.grab(self.win_rec, all_screens=True)
        return np.array(img)

    def get_pos(self, pos):
        return (pos[0] + self.win_rec[0], pos[1] + self.win_rec[1])