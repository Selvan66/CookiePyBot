
import time
import threading
import cv2
from pynput.mouse import Button, Controller
from windowcapture import CookieWindowCapture

mouse = Controller()
button = Button.left

class CookiePyBot(threading.Thread):
    def __init__(self, delay):
        super(CookiePyBot, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
        self.mouse_pos = mouse.position
        self.window = CookieWindowCapture()
        self.image = None

    def start_clicking(self):
        self.window.find_window()
        self.find_on_screen('Photo/main_cookie.jpg')
        self.running = True
        
    def stop_clicking(self):
        self.running = False
        
    def find_on_screen(self, photo):
        self.image = self.window.get_screen()
        find_photo = cv2.imread(photo, cv2.IMREAD_UNCHANGED)
        result = cv2.matchTemplate(self.image, find_photo, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        threshold = 0.7
        if max_val >= threshold:
            cookie_width = find_photo.shape[1]
            cookie_height= find_photo.shape[0]
            top_left = max_loc
            middle = (top_left[0] + (cookie_width / 2), top_left[1] + (cookie_height / 2))
            self.mouse_pos = self.window.get_pos(middle)

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.position = self.mouse_pos
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)