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
		device.emit_click(km['a'])
	elif bp == 13:
		device.emit_click(km['b'])
	elif bp == 26:
		device.emit_click(km['x'])
	elif bp == 6:
		device.emit_click(km['y'])
	elif bp == 12:
		device.emit_click(km['l'])
	elif bp == 5:
		device.emit_click(km['r'])
	elif bp == 20:
		device.emit_click(km['select'])
	elif bp == 16:
		device.emit_click(km['start'])
	elif bp == 18:
		device.emit_click(km['joySel'])


for pin in button_list:
	GPIO.add_event_detect(pin, GPIO.FALLING, callback=buttonPressed, bouncetime=150)

try:
	while True:
		time.sleep(1)
finally:
	GPIO.cleanup()
