import os
import time
import threading
import pyautogui
import cv2
import numpy as np
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key

os.chdir(os.path.dirname(os.path.abspath(__file__)))

delay = 0.001
button = Button.left
start_stop_key = Key.caps_lock
exit_key = Key.esc
mouse = Controller()
pos_cookie_key = Key.f1
neg_cookie_key = Key.f2
pos_golden_key = Key.f3

class Bot(threading.Thread):
	def __init__(self):
		super(Bot, self).__init__()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True
		self.mouse_pos = mouse.position
		self.image = None

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False

	def make_screeshot(self):
		self.image = pyautogui.screenshot()
		self.image = cv2.cvtColor(np.array(self.image),cv2.COLOR_RGB2BGR)

	def find_on_screen(self, photo):
		find_photo = cv2.imread(photo, cv2.IMREAD_UNCHANGED)
		result = cv2.matchTemplate(self.image, find_photo, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
		threshold = 0.7
		if max_val >= threshold:
			cookie_width = find_photo.shape[1]
			cookie_height= find_photo.shape[0]

			top_left = max_loc
			middle = (top_left[0] + (cookie_width / 2), top_left[1] + (cookie_height / 2))
			self.mouse_pos = middle	
		cv2.imshow('test', result)
		cv2.waitKey(100)	

	def exit(self):
		self.stop_clicking()
		self.program_running = False

	def run(self):
		while self.program_running:
			self.make_screeshot()
			#self.find_on_screen('Photo/main_cookie.jpg')
			self.find_on_screen('Photo/wrath_cookie.jpg')
			self.find_on_screen('Photo/golden_cookie.jpg')
			while self.running:
				mouse.position = self.mouse_pos
				mouse.click(self.button)
				time.sleep(self.delay)
			time.sleep(0.1)


click_thread = Bot()
click_thread.start()

def on_press(key):
	if key == start_stop_key:
		if click_thread.running:
			click_thread.stop_clicking()
		else:
			click_thread.start_clicking()
	elif key == exit_key:
		click_thread.exit()
		listener.stop()
		

with Listener(on_press=on_press) as listener:
	listener.join()
