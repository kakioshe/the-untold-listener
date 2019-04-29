import requests
import time
from functions import *
import board
import neopixel
import RPi.GPIO as GPIO
import time
from datetime import datetime
import json
import os

pixel_pin = board.D18
num_pixels = 49

ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,pixel_order=ORDER)

# LISTENER SIDE
# Status List:
# 1. idle = Initial status, when no one is inside the booth
# 2. speaker = When the speaker is currently speaking
# 3. listener = When the speaker has finished speaking, the emotion will
#               be sent to the listener. Listener side will read the emotion
#               and ask for feedback. Speaker side will play a pre-recorded msg
# 4. feedback = When the listener has finished saying feedback, and its uploaded
#               speaker side will play that feedback and some pre-recorded msg.

def updateStatus():
    r = requests.get('http://the-untold.herokuapp.com/status')
    return r.json()[0]['status']

def change_color(emotions):
    if 'Fear' in emotions:
        pixels.fill((0,255,0))
        pixels.show()
        print("Green")
    elif 'Sadness' in emotions:
        pixels.fill((0,0,255))
        pixels.show()
        print("Blue")
    elif 'Joy' in emotions:
        pixels.fill((255,255,0))
        pixels.show()
        print("Yellow")
    elif 'Anger' in emotions:
        pixels.fill((255,0,0))
        pixels.show()
        print("Red")

def main():
    STATUS_LIST = ["idle", "speaker", "listener", "feedback"]
    HEROKU_URL = "http://the-untold.herokuapp.com/status/5cc1ab8dfb6fc0265f2903a3"
    bucket = 'the-untold'
    status = updateStatus()
    while True:
        #Do infinite loop, catch current status each loop
        
        if status == STATUS_LIST[1]:
            status = updateStatus()
            print("LISTENER Speaker currently speaking")
            time.sleep(2)
            # DO nothing?
            
        elif status == STATUS_LIST[2]:
            print("LISTENER Listener currently making a feedback")
            r = requests.get('http://the-untold.herokuapp.com/status')
            emotion = r.json()[0]['emotion']
            print("Speaker is currently feeling {}".format(emotion))
            change_color(emotion)
            filename = str(datetime.now()) + '.wav'
            record(filename)
            uploadFile(bucket, emotion, filename)
            os.remove(filename)
            #DO record feedback and upload it
            requests.put(HEROKU_URL, json={
                "status": STATUS_LIST[3],
                "emotion": emotion,
                "filename" : filename
                })
            time.sleep(10)
            status = updateStatus()
            

        elif status == STATUS_LIST[3]:
            print("LISTENER feedback is being played by the speaker")
            status = updateStatus()
            time.sleep(2)
            #DO nothing?

        else:
            print("idling")
            
            pixels.fill((0,0,0))
            pixels.show()
            status = updateStatus()
            time.sleep(2)

main()
