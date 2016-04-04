import curses
import time

screen = curses.initscr()
curses.noecho()
dims = screen.getmaxyx()
string = 'Hello World!'
q = -1
x, y = 0, 0
vertical = 1
horizontal = 1

while q != ord('q'):
	screen.clear()
	screen.addstr(y, x, string)
	screen.refresh()
	screen.move(dims[0]-1, dims[1]-1)
	q = screen.getch()

	if q == ord('w') and y > 0:
		y-=1
	elif q == ord('s') and y < dims[0]-1:
		y+=1
	elif q == ord('a') and x > 0:
		x -= 1
	elif q == ord('d') and x< dims[1]-len(string):
		x+= 1
	
	if y == dims[0]-1 and x == dims[1] - len(string):
		if q == ord('s'):
			y-=1
		elif q == ord('d'):
			x-=1
	time.sleep(.05)

screen.getch()
curses.endwin()
