import time
import threading
import pyautogui
import cv2
import numpy as np
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key

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

	def start_clicking(self):
		self.running = True
		self.mouse_pos = mouse.position

	def stop_clicking(self):
		self.running = False

	def save_screeshot(self, path):
		image = pyautogui.screenshot()
		image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
		cv2.imwrite('{}/{}.jpg'.format(path, time.time()), image)

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
	elif key == pos_cookie_key:
		click_thread.save_screeshot('MainCookie/Pos')
	elif key == neg_cookie_key:
		click_thread.save_screeshot('MainCookie/Neg')
	elif key == pos_golden_key:
		click_thread.save_screeshot('GoldenCookie/Pos')
		

with Listener(on_press=on_press) as listener:
	listener.join()
