import curses
import os
import subprocess
import commands
import urllib2

screen = curses.initscr()
curses.noecho()
dims = screen.getmaxyx()

options = 	[
			"Circuit One",
			"Circuit Two",
			"Get Status",
			"Blackout",
			"All ON",
			"Exit"
			]

circuitOneStatus = "UNKNOWN"
circuitTwoStatus = "UNKNOWN"

def centerHorizontal(string):
	return (dims[1]/2) - (len(string)/2)

def drawMenu(currentOption):
	topOfList = (dims[0]/2) - (len(options)/2)
	screen.clear()
	for x in range(len(options)):
		if x == currentOption:
			screen.addstr(topOfList+x, centerHorizontal(options[x]), options[x], curses.A_STANDOUT)
		else:
			screen.addstr(topOfList+x, centerHorizontal(options[x]), options[x])

def drawSystemStatus():
	screen.addstr(0,0,"Circuit ONE: "+str(circuitOneStatus))
	screen.addstr(1,0,"Circuit TWO: "+str(circuitTwoStatus))

def updateSystemStatus():
	global circuitOneStatus
	global circuitTwoStatus
	screen.clear()
	screen.addstr(0,0,'UPDATING SYSTEM STATUS. PLEASE WAIT...')
	screen.refresh()
	circuitOneStatus = str(getCircuitStatus(10))
	circuitTwoStatus = str(getCircuitStatus(11))

def getCircuitStatus(pin):
	response = urllib2.urlopen("http://arikostler.com/getState.php?pin="+str(pin))
	return response.read()

def quickMessage(msg):
	screen.clear()
	screen.addstr(0,0, msg)
	screen.getch()

def toggleCircuit(pin):
	global circuitOneStatus
	global circuitTwoStatus
	if pin == 10:
		if circuitOneStatus == 1:
			turnOn(pin)
			circuitOneStatus = 0
		else:
			turnOff(pin)
			circuitOneStatus = 1

	elif pin == 11:
		if circuitTwoStatus == 1:
			turnOn(pin)
			circuitTwoStatus = 0
		else:
			turnOff(pin)
			circuitTwoStatus = 1

def turnOn(pin):
	response = urllib2.urlopen("http://arikostler.com/on.php?pin="+str(pin))

def turnOff(pin):
	response = urllib2.urlopen("http://arikostler.com/off.php?pin="+str(pin))

def blackout():
	turnOff(10)
	turnOff(11)
	pinStates(1, 1)

def allOn():
	turnOn(10)
	turnOn(11)
	pinStates(0,0)

def pinStates(one, two):
	global circuitOneStatus
	global circuitTwoStatus
	circuitOneStatus = one
	circuitTwoStatus = two

def selectOption(op):
	if op == 0:
		#quickMessage("not yet implemented")
		toggleCircuit(10)
	elif op == 1:
		#quickMessage("not yet implemented")
		toggleCircuit(11)
	elif op == 2:
		updateSystemStatus()
	elif op == 3:
		#quickMessage("not yet implemented")
		blackout()
	elif op == 4:
		#quickMessage("not yet implemented")
		allOn()
	elif op == 5:
		cleanExit()
		

def cleanExit():
	curses.endwin()
	os.system("clear")
	exit()

q = -1
active = 0
while q != ord('q') and q != ord('l'):
	drawMenu(active)
	drawSystemStatus()
	screen.move(dims[0]-1, dims[1]-1)
	screen.refresh()

	q = screen.getch()
	
	if q == ord('s') or q == 66:#curses.KEY_DOWN:
		active += 1
	elif q == ord('w') or q == 65:#curses.KEY_UP:
		active -= 1
	elif q == ord('a') or q == 10:#curses.KEY_ENTER
		selectOption(active)

	if active < 0:
		active += len(options)
	elif active >= len(options):
		active -= len(options)
	
cleanExit()
