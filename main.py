import os
from bot import CookiePyBot
from pynput.keyboard import Listener, Key

os.chdir(os.path.dirname(os.path.abspath(__file__)))

############################OPTIONS###########################

delay = 0.001
start_stop_key = Key.caps_lock
exit_key = Key.esc

##############################################################

bot = CookiePyBot(delay)
bot.start()

def on_press(key):
	if key == start_stop_key:
		if bot.running:
			bot.stop_clicking()
		else:
			bot.start_clicking()
	elif key == exit_key:
		bot.exit()
		listener.stop()
		
with Listener(on_press=on_press) as listener:
	listener.join()
