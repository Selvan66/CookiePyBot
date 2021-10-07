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

    def active(self):
        self.find_window()

    def find_window(self):
        self.get_winlist()
        self.cookiewin =  [(hwnd, title) for hwnd, title in self.winlist if 'cookie clicker' in title.lower()]
        while not self.cookiewin:
            print('Cannot find cookie cliker window')
            self.get_winlist()
            self.cookiewin =  [(hwnd, title) for hwnd, title in self.winlist if 'cookie clicker' in title.lower()]
            time.sleep(1)

        self.cookiewin = self.cookiewin[0]
        self.hwnd = self.cookiewin[0]
        win32gui.ShowWindow(self.hwnd,win32con.SW_MAXIMIZE)
        self.win_rec = win32gui.GetWindowRect(self.hwnd)
        self.w = self.win_rec[2] - self.win_rec[0]
        self.h = self.win_rec[3] - self.win_rec[1]

    def get_screen(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

        return img

    def get_winlist(self):
        def enum_cb(hwnd, results):
            self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, None)

    def get_pos(self, pos):
        return (pos[0] + self.win_rec[0], pos[1] + self.win_rec[1])