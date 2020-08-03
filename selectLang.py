from pad4pi import rpi_gpio
import subprocess
import os
import sys

#os.system("sudo python3 ~/master/master.py en")


KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"],
    ["*","*","*"],
    ["#","#","#"]
]

ROW_PINS = [4, 14, 15, 17,5,6] # BCM numbering
COL_PINS = [18, 27, 22] # BCM numbering

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

os.system('sudo pkill -f master')
os.system('sudo pkill -f mpg123')
os.system('sudo pkill -f mpg321')
os.system('sudo pkill -f omxplayer')
os.system('sudo pkill -f aplay')



playString = 'mpg321 /home/pi/master/clips/introChord.mp3'
os.system(playString)

playString = 'omxplayer ~/master/clips/langSelection.mp3'
recordProcess = subprocess.Popen(playString,shell=True)

def fx():
    playString = 'mpg321 /home/pi/master/clips/buttonSounds/6.mp3'

    os.system(playString)

def printKey(key):
    
    print(key)

    if(key == 1):
        fx()
        os.system('pkill aplay')
        os.system('pkill omxplayer')
        print("english")
	
        myProcess = subprocess.Popen("sudo python3 /home/pi/master/master.py en && sudo pkill -f select", shell=True)

        os.system("sudo pkill -f select")
    
    if(key == 2):
        fx()

        os.system('pkill aplay')
        os.system('pkill omxplayer')
        print("greek")

        myProcess = subprocess.Popen("sudo python3 /home/pi/master/master.py el && sudo pkill -f select", shell=True)

        os.system("sudo pkill -f select")

    if(key == 3):
        fx()

        os.system('pkill aplay')
        print("french")

        myProcess = subprocess.Popen("sudo python3 /home/pi/master/master.py fr && sudo pkill -f select", shell=True)

        os.system("sudo pkill -f select")

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)	

while True:
	pass
