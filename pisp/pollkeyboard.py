import RPi.GPIO as GPIO
import time
import uinput
import spidev

device = uinput.Device([
	uinput.KEY_A,
	uinput.KEY_B,
	uinput.KEY_X,
	uinput.KEY_Y,
	uinput.KEY_L,
	uinput.KEY_R,
	uinput.KEY_BACKSPACE,
	uinput.KEY_ENTER,	
	uinput.KEY_J,
	uinput.KEY_UP,
	uinput.KEY_DOWN,
	uinput.KEY_LEFT,
	uinput.KEY_RIGHT
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
	'joySel':uinput.KEY_J,
	'up':uinput.KEY_UP,
	'down':uinput.KEY_DOWN,
	'left':uinput.KEY_LEFT,
	'right':uinput.KEY_RIGHT
	}

keyMap = {
	km['a']:0,
	km['b']:0,
	km['x']:0,
	km['y']:0,
	km['l']:0,
	km['r']:0,
	km['select']:0,
	km['start']:0,
	km['joySel']:0,
	km['up']:0,
	km['down']:0,
	km['left']:0,
	km['right']:0
	}

pinMap = {
	'a':19,
	'b':13,
	'x':26,
	'y':6,
	'l':12,
	'r':5,
	'select':20,
	'start':16,
	'joySel':18
	}

GPIO.setmode(GPIO.BCM)
button_list = [5, 6, 13, 19, 26, 12, 16, 20, 18]
GPIO.setup(button_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Joystick calibration offsets
offset_x = 15
offset_y = 0

# Open SPI bus
spi=spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def buttonPressed(bp):
	resetKeys()
	if GPIO.input(pinMap['a']) == 0:
		keyMap[km['a']] = 1
	if GPIO.input(pinMap['b']) == 0:
		keyMap[km['b']] = 1
	if GPIO.input(pinMap['x']) == 0:
		keyMap[km['x']] = 1
	if GPIO.input(pinMap['y']) == 0:
		keyMap[km['y']] = 1
	if GPIO.input(pinMap['l']) == 0:
		keyMap[km['l']] = 1
	if GPIO.input(pinMap['r']) == 0:
		keyMap[km['r']] = 1
	if GPIO.input(pinMap['select']) == 0:
		keyMap[km['select']] = 1
	if GPIO.input(pinMap['start']) == 0:
		keyMap[km['start']] = 1
	if GPIO.input(pinMap['joySel']) == 0:
		keyMap[km['joySel']] = 1
	updateKeys()

def updateKeys():
	for key in keyMap:
		device.emit(key, keyMap[key])

def resetKeys():
	for key in keyMap:
		keyMap[key] = 0

def arduinoMap(x, inmin, inmax, outmin, outmax):
	return (x-inmin)*(outmax-outmin)/(inmax-inmin)+outmin

def calibrateJoystick(x, y):
	jx = ReadChannel(x)
	jy = ReadChannel(y)
	offset_x = (512) - jx
	offset_y = (512) - jy

def applyCalibration(x, y):
	return (x+offset_x), (y+offset_y)
	

# MAIN CODE STARTS HERE
for pin in button_list:
	GPIO.add_event_detect(pin, GPIO.FALLING, callback=buttonPressed, bouncetime=150)

try:
	joy_x = 0
	joy_y = 1
	calibrateJoystick(joy_x, joy_y)
	while True:
		joy_x_value, joy_y_value = applyCalibration(ReadChannel(joy_x), ReadChannel(joy_y))
		x = arduinoMap(joy_x_value, 0, 1023, -10, 10)
		y = arduinoMap(joy_y_value, 0, 1023, -10, 10)
		y = y*-1
		#print("X: "+str(x)+" Y: "+str(y))
		if x <= -5:
			device.emit(km['left'], 1)
		else:
			device.emit(km['left'], 0)
		
		if x >= 5:
			device.emit(km['right'], 1)
		else:
			device.emit(km['right'], 0)

		if y <= -5:
			device.emit(km['up'], 1)
		else:
			device.emit(km['up'], 0)

		if y >= 5:
			device.emit(km['down'], 1)
		else:
			device.emit(km['down'], 0)

		time.sleep(.02)
finally:
	GPIO.cleanup()
