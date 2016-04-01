import RPi.GPIO as GPIO
import time
import uinput

device = uinput.Device([
	uinput.KEY_A,
	uinput.KEY_B,
	uinput.KEY_X,
	uinput.KEY_Y,
	uinput.KEY_L,
	uinput.KEY_R,
	uinput.KEY_BACKSPACE,
	uinput.KEY_ENTER,	
	uinput.KEY_J
	])

km = {
	'a':uinput.KEY_A,
	'b':uinput.KEY_B,
	'x':uinput.KEY_X,
	'y':uinput.KEY_Y,
	'l':uinput.KEY_L,
	'r':uinput.KEY_R,
	'select':uinput.KEY_BACKSPACE,
	'start':uinput.KEY_ENTER,
	'joySel':uinput.KEY_J
	}

GPIO.setmode(GPIO.BCM)
button_list = [5, 6, 13, 19, 26, 12, 16, 20, 18]
GPIO.setup(button_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonPressed(bp):
	if bp == 19:
		 holdButton(bp, km['a'])
	elif bp == 13:
		 holdButton(bp, km['b'])
	elif bp == 26:
		 holdButton(bp, km['x'])
	elif bp == 6:
		 holdButton(bp, km['y'])
	elif bp == 12:
		 holdButton(bp, km['l'])
	elif bp == 5:
		 holdButton(bp, km['r'])
	elif bp == 20:
		 holdButton(bp, km['select'])
	elif bp == 16:
		 holdButton(bp, km['start'])
	elif bp == 18:
		 holdButton(bp, km['joySel'])

def holdButton(button, key):
	while GPIO.input(button)==0:
		device.emit(key, 1)
		time.sleep(.02)
	device.emit(key, 0)

for pin in button_list:
	GPIO.add_event_detect(pin, GPIO.FALLING, callback=buttonPressed, bouncetime=150)

try:
	while True:
		time.sleep(1)
finally:
	GPIO.cleanup()
