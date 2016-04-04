import curses
import time

screen = curses.initscr()
screen.nodelay(1)
dims = screen.getmaxyx()
string = 'Hello World!'
q = -1
x, y = 0, 0
vertical = 1
horizontal = 1

while q < 0:
	screen.clear()
	screen.addstr(y, x, string)
	screen.refresh()
	x += horizontal
	y += vertical
	
	if y >= dims[0]-1:
		vertical *= -1
	elif y <= 0:
		vertical *= -1

	if x >= dims[1]-len(string)-1:
		horizontal *= -1
	elif x <= 0:
		horizontal *= -1

	q = screen.getch()
	time.sleep(.05)

screen.getch()
curses.endwin()
