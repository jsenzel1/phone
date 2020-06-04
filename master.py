import time
import digitalio
import board


import os
import subprocess
import time
import signal
import sys
import random

from datetime import datetime

from pad4pi import rpi_gpio

##SINGLETON CODE

# from tendo import singleton
# me = singleton.SingleInstance()



#-------- KEYPAD SETUP vvvvvvvv --------------------------------------------------------



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

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

myString = "good morning vietnam"

currentKey = "none"

recording = False

depthCount = 1

playString = 'mpg321 ~/master/clips/introChord.mp3 && mpg321 -g 60 ~/master/clips/music1.mp3'
recordProcess = subprocess.Popen(playString,shell=True)

# os.system('mpg321 ~/master/clips/introChord.mp3')
# os.system('mpg321 ~/master/clips/introduction.mp3')


def playBeep():
    num = str(random.randint(1,12))
    playString = 'mpg321 ~/master/clips/beeps/' + num + '.mp3'
    recordProcess = subprocess.Popen(playString,shell=True)


def onKey(key):
    print(key)

    

    #TODO kill keys on hold down like with star and hash
    if isinstance(key, int):

        global currentKey

        currentKey = key

        # os.system('killall -s 9 mpg321')
        os.system('pkill mpg321')
        os.system('pkill omxplayer')

        playString = 'mpg321 ~/master/questions/q' + str(key)+".mp3 && mpg321 ~/master/clips/recordingInstructions.mp3"



        # os.system(playString)

        recordProcess = subprocess.Popen(playString,shell=True)
        print(key)
        

    ########################################################################

        #playback
        #TODO loop or give message when all responses have been listened to 
    
        
    if key == "*":



        global currentKey
        global depthCount

        print(currentKey)    

        os.system('pkill mpg321')
        os.system('pkill omxplayer')


        playBeep()



        print("pressed *")
            

        # if not starDown:
                
        #     starDown = True

        prevPlayString = "cd ~/master/answers/" + str(currentKey) +"&& omxplayer $(ls -tr | tail -" + str(depthCount)+"| head -n 1)"

        recordProcess = subprocess.Popen(prevPlayString,shell=True)

        depthCount = depthCount+1

    ######################### RECORDING

    if key == "#":


        global currentKey
        global depthCount
        global recording

        os.system('pkill mpg321')
        os.system('pkill omxplayer')


        # playBeep()


        recording = not recording

        if recording:
            os.system('mpg321 ~/master/clips/rOn.mp3')

            depthCount = depthCount+1
            curTime = (datetime.now().strftime("%d_%m_%Y_%H:%M:%S:%f"))

            if currentKey is not "none":
                systemString= 'arecord -V mono --device=hw:1,0 --format s16_LE --rate 44100 -c1 ~/master/answers/'+ str(currentKey) +'/' + curTime + '.mp3'

                recordProcess = subprocess.Popen(systemString,shell=True)

            #os.system(systemString)

        if not recording:

            os.system('killall arecord')
            os.system('mpg321 ~/master/clips/rOff.mp3')

        # os.system('pkill mpg321')
        # os.system('pkill omxplayer')



keypad.registerKeyPressHandler(onKey)	

#-------- KEYPAD SETUP ^^^^^ --------------------------------------------------------

while True:
    pass



## TODO
## watch dog setup
## make sure there's only ever 1 running at the same time (this could make large problems!)