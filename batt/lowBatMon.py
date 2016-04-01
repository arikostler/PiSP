import RPi.GPIO as GPIO
import time
import os
import urllib2

battPin = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(battPin, GPIO.IN)
GPIO.setup(battPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def alert():
	urllib2.urlopen("http://arikostler.com/on.php?pin=10").read()
	os.system('echo ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ' >> lowBatt.txt')
	while GPIO.input(battPin)==0:
		os.system('echo BATTERY LOW! | wall')
		time.sleep(5)

try:
	while True:
		print("Monitoring")
		if GPIO.input(battPin) == 0:
			alert()
		GPIO.wait_for_edge(battPin, GPIO.FALLING)
		alert()
except:
	pass

GPIO.cleanup()
