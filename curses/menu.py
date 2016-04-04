import curses
import os
import subprocess
import commands

screen = curses.initscr()
curses.noecho()
dims = screen.getmaxyx()

options = 	[
			"Start Desktop Env",
			"Show IP Address",
			"Exit to Console",
			"Shutdown"
			]

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
			
def selectOption(op):
	if op == 0:
		os.system("startx")
	elif op == 1:
		os.system("clear")
		ipaddr = commands.getoutput("hostname -I")
		screen.addstr(0,0, "IP ADDRESS")
		if " " not in ipaddr:
			screen.addstr(1,0, str(ipaddr))
		else:
			screen.addstr(1,0, str(ipaddr).split(" ")[0])
			screen.addstr(2,0, str(ipaddr).split(" ")[1])
		screen.getch()
	elif op == 2:
		cleanExit()
	elif op == 3:
		os.system("clear")
		screen.addstr(1,1,"SHUTDOWN")
		screen.addstr(2,1,"Are you sure? (y/N)")
		ch = screen.getch()
		if ch == ord('y'):
			os.system("sudo shutdown -h now")
		

def cleanExit():
	curses.endwin()
	os.system("clear")
	exit()

q = -1
active = 0
while q != ord('q') and q != ord('l'):
	drawMenu(active)
	#screen.addstr(0,0,str(active))
	#screen.addstr(1,0,str(q))
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
