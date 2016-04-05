
#The idea is that you have a dictionary with 
#all the keys and their values. Then you iterate
#through them and set their values. 

#You can do this using either the interrupt method 
#or the polling method.

#if its the polling method, just poll each gpio pin
#and update the map accordingly.

#The interrupt method is the same except this action
#is triggered by interrupt. It doesnt matter which button
#you hit. It will trigger a refresh on every keypress and 
#it will refresh all keys.


buttons = {
	"uniput.KEY_A": 0,
	"uinput.KEY_B": 1
}

def handleKeys(keymap):
	for key in keymap:
		device.emit(key, keymap[key])
