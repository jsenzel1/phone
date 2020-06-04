import time
import digitalio
import board
import adafruit_matrixkeypad

import os
import subprocess
import time
import signal
import sys
import random

from datetime import datetime


##KEYPAD CODE

# 3x4 matrix keypad on Raspberry Pi -
# rows and columns are mixed up for https://www.adafruit.com/product/3845
cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D5, board.D26)]
rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D21, board.D20, board.D19)]

keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

curKey = "none"

recording = False

hashDown = False

depthCount = 1

starDown = False

while True:
    keys = keypad.pressed_keys

    if len(keys) >0:
        # os.system("omxplayer ~/padPhone/clips/beep.mp3")

        # os.system("omxplayer ~/padPhone/questions/q" + str(keys[0]) + ".mp3")

        # subprocess version below
        # recordProcess = subprocess.Popen("omxplayer ~/padPhone/questions/q" + str(keys[0]) + ".mp3",shell=True)
        
        #TODO kill keys on hold down like with star and hash
        if isinstance(keys[0], int):

            # os.system('killall -s 9 omxplayer')
            os.system('pkill omxplayer')

            playString = 'omxplayer ~/padPhone/questions/q' + str(keys[0])+".mp3"

            # os.system(playString)

            recordProcess = subprocess.Popen(playString,shell=True)
            print(keys[0])
            curKey = keys[0]

########################################################################

        #playback
        #TODO loop or give message when all responses have been listened to 
    
        
        if keys[0] == "*":

            os.system('pkill omxplayer')


            print("pressed *")
            

            if not starDown:
                
                starDown = True

                prevPlayString = "cd ~/padPhone/answers/" + str(curKey) +"&& aplay $(ls -tr | tail -" + str(depthCount)+"| head -n 1)"

                recordProcess = subprocess.Popen(prevPlayString,shell=True)

                depthCount = depthCount+1



#######################################################################

        #RECORDING
        #TODO set conditions if there is no selected quesiton ie play message "please select a question"

        if keys[0] == "#":
            os.system('pkill omxplayer')


            if not hashDown:
                hashDown = True

                recording = not recording

                if recording:
                    depthCount = depthCount+1
                    curTime = (datetime.now().strftime("%d_%m_%Y_%H:%M:%S:%f"))

                    if curKey is not "none":
                        systemString= 'arecord -V mono --device=hw:1,0 --format s16_LE --rate 44100 -c1 ~/padPhone/answers/'+ str(curKey) +'/' + curTime + '.mp3'

                        recordProcess = subprocess.Popen(systemString,shell=True)

                    #os.system(systemString)

                if not recording:
                    os.system('killall arecord')


                print(recording)

                print("pressed #")

#####################################################################


    if "#" not in keys and hashDown == True:
        hashDown = False

    if "*" not in keys and starDown == True:
        starDown = False


        


    

    time.sleep(0.1)

