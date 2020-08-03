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

##SINGLETON CODEnano

# from tendo import singleton
# me = singleton.SingleInstance()



#-------- KEYPAD SETUP vvvvvvvv --------------------------------------------------------

langString = sys.argv[1]
print("---------********------MASTER STARTING------*********-------MASTER STARTING--------------MASTER STARTING ----**")
print("selected language: ", langString)
# os.system("omxplayer /home/pi/master/lang/"+langString+"/questions/q1.mp3")


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

firstPressed = False

answeredQuestions = [False,False,False,False,False,False,False,False,False,False]
questionTimes = ["","","","","","","","","",""]

depthCount = 1

# playString = 'mpg321 /home/pi/master/clips/introChord.mp3 && mpg321 -g 60 /home/pi/master/clips/music1.mp3 && mpg321 -g 60 /home/pi/master/clips/music2.mp3'
playString = 'mpg321 /home/pi/master/lang/'+langString+'/prompts/introduction.mp3'
recordProcess = subprocess.Popen(playString,shell=True)

# playString = 'mpg321 --loop -1 /home/pi/master/clips/menuMusic.mp3'
# recordProcess = subprocess.Popen(playString,shell=True)

# os.system('mpg321 /home/pi/master/clips/introChord.mp3')
# os.system('mpg321 /home/pi/master/clips/introduction.mp3')


def playChord():
    num = str(random.randint(1,10))
    # playString = 'mpg321 /home/pi/master/clips/piano/' + num + '.mp3'
    playString = 'mpg321 /home/pi/master/clips/buttonSounds/' + num + '.mp3'
    # recordProcess = subprocess.Popen(playString,shell=True)
    os.system(playString)

def playBeep():
    num = str(random.randint(1,12))
    playString = 'mpg321 /home/pi/master/clips/beeps/' + num + '.mp3'
    recordProcess = subprocess.Popen(playString,shell=True)


def onKey(key):
    print(key)

    global firstPressed
    global currentKey
    global depthCount
    global recording

    if not firstPressed:
        firstPressed = True
        # playString = 'mpg123 --loop -1 /home/pi/master/clips/menuMusic.mp3'
        # recordProcess = subprocess.Popen(playString,shell=True)


    #TODO kill keys on hold down like with star and hash
    if isinstance(key, int):



        currentKey = key
        depthCount = 1 

        # os.system('killall -s 9 mpg321')
        os.system('pkill mpg321')
        os.system('pkill omxplayer')

        playChord()


        playString = 'mpg321 /home/pi/master/lang/' + langString+'/questions/q' + str(key)+'.mp3 && mpg321 /home/pi/master/lang/' + langString+'/prompts/recordingInstructions.mp3'



        # os.system(playString)

        recordProcess = subprocess.Popen(playString,shell=True)
        print(key)
        

    ########################################################################

        #playback
        #TODO loop or give message when all responses have been listened to 
    
        
    if key == "*":

        print(currentKey)    

        os.system('pkill mpg321')
        os.system('pkill omxplayer')


        playBeep()

        print("pressed *")
            
        # if not starDown:
                
        #     starDown = True

        prevPlayString = "cd /home/pi/master/lang/" + langString+"/answers/" + str(currentKey) +"&& omxplayer $(ls -tr | tail -" + str(depthCount)+"| head -n 1)"

        

        recordProcess = subprocess.Popen(prevPlayString,shell=True)

        depthCount = depthCount+1

        #looping playpack attempts


        # onlyfiles = next(os.walk(os.walk("/home/pi/master/lang/" + langString+"/answers/" + str(currentKey)))[2] #dir is your directory path as string

        # print(onlyfiles)

        # dirString = "/home/pi/master/lang/" + langString+ "/answers/" + str(currentKey)

        # print("DIRESTRING" + dirString)

        # print("NUM OF FILES: " + str(os.system("cd "+dirString+" && ls -1 | wc -l")))

        # path, dirs, files = next(os.walk("/home/pi/master/lang/" + langString+"/answers/" + str(currentKey))
        # file_count = len(files)

        # if depthCount > 5:
        #     depthCount = 1
        

    ######################### RECORDING

    if key == "#":


     

        os.system('pkill mpg321')
        os.system('pkill omxplayer')


        # playBeep()


        recording = not recording

        if recording:
            os.system('mpg321 /home/pi/master/clips/rOn.mp3')

            depthCount = depthCount+1
            curTime = (datetime.now().strftime("%d_%m_%Y_%H-%M-%S-%f"))

            if currentKey is not "none":

                if not answeredQuestions[currentKey]:
                    systemString= 'arecord -d 160 -V mono --device=hw:1,0 --format s16_LE --rate 44100 -c1 /home/pi/master/lang/'+langString+'/answers/'+ str(currentKey) +'/' + curTime + '.mp3 && mpg321 /home/pi/master/clips/rOff.mp3 &&mpg321 /home/pi/master/lang/'+langString+'/prompts/afterRecording.mp3'
                    answeredQuestions[currentKey] = True
                    questionTimes[currentKey] = curTime
                else:
                    systemString= 'arecord -d 160 -V mono --device=hw:1,0 --format s16_LE --rate 44100 -c1 /home/pi/master/lang/'+langString+'/answers/'+ str(currentKey) +'/' + questionTimes[currentKey] + '.mp3 && mpg321 /home/pi/master/clips/rOff.mp3 &&mpg321 /home/pi/master/lang/'+langString+'/prompts/afterRecording.mp3'
                    


                


                recordProcess = subprocess.Popen(systemString,shell=True)

            #os.system(systemString)

        if not recording:

            os.system('killall arecord')
            os.system('mpg321 /home/pi/master/clips/rOff.mp3')

            playString = 'mpg321 /home/pi/master/lang/'+langString+'/prompts/afterRecording.mp3'

            recordProcess = subprocess.Popen(playString,shell=True)

        # os.system('pkill mpg321')
        # os.system('pkill omxplayer')



keypad.registerKeyPressHandler(onKey)	

#-------- KEYPAD SETUP ^^^^^ --------------------------------------------------------

while True:
    pass



## TODO
## watch dog setup
## make sure there's only ever 1 running at the same time (this could make large problems!)


# TODO for reapeted spamming
# use the bool array to set questions as already answered
# have a second string array that takes the date/time of the answered question
# if already answered, when recording that question use the appropriate previous name and overwrite the other question rather than recording a new one
# obviously this should reset on re-use
