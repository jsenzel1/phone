import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import os
import time
import subprocess

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

os.system('echo hellooooooo')

started = False
startTime = time.time()

while True: # Run forever

    ##PICKUP HANGUP ##

    if GPIO.input(2) == GPIO.HIGH:

        # if(True):
        if(started):
            os.system('pkill -f master')

            os.system('echo off')
            
            time.sleep(.2)


            started = False
    
    if GPIO.input(2) == GPIO.LOW and not started:

        os.system('pkill -f master')

        subprocess.Popen(["python3", "master.py"])
       
        started = True
        os.system('echo on')

        startTime = time.time()



    time.sleep(.2)
    ##OFF THE HOOK##

    if started and GPIO.input(2) == GPIO.LOW: 
        print(time.time()-startTime)
        #ADD: code that checks to make sure no buttons are pressed
        # if any button pressed, startTime = time.time()

        if(time.time()-startTime > 30):
  
            time.sleep(.2)

            os.system('pkill -f talkToMe.py')





      


        

