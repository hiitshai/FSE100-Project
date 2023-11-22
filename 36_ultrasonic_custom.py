#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import board
import adafruit_tcs34725
import subprocess
import speech_recognition as sr
import math
# variables and constants
TRIG = 17
ECHO = 13
SIG = 27
BSIG = 18
a = 1
turnoff = 1
i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)
redWeight = 1.20 #0.30
greenWeight = 0.35 #0.59
blueWeight = 0.05 #0.11
# setting up board mode and sensors
def setup():
    global buzzer
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SIG, GPIO.OUT)
    GPIO.setup(BSIG, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(BSIG, GPIO.BOTH, callback= detect, bouncetime=1)
    buzzer = GPIO.PWM(SIG, 440)
# uses ultrasonic sensor to get distance by using time variables
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.00002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()
    during = time2 - time1
    return during * 340 / 2 * 100
# detects when there is input from button
def detect(chn):
    buttonpress(GPIO.input(BSIG))
# speaks color using tts
def speak(text):
    text = text.replace(" ", "_")
    subprocess.run(("espeak \"" + text + " 2>/dev/null").split(" "))
# action that happens on button press
def buttonpress(x):
    global turnoff
    if x == 1 and turnoff == 0:
        turnoff = 1
    elif x == 1 and turnoff == 1:
        turnoff = 0
# main loop for sensor input and output
def colorLoop():
    global redWeight, blueWeight, greenWeight
    while True:
        if turnoff == 1:
            color = sensor.color_rgb_bytes
            colorList = [(255,0,0),(255,128,0),(255,255,0),(0,255,0),(0,0,255),(127,0,255),(255,0,255),(255,255,255)]
            distList = []
            for col in colorList:
              distList.append(math.sqrt(((col[0] - color[0])*redWeight)**2 + ((col[1] - color[1])*greenWeight)**2 + ((col[2] - color[2])*blueWeight)**2))
            minimum = float('inf')
            index = 0
            for i in range(8): 
                dist = distList[i]
                if dist < minimum:
                    minimum = dist
                    index = i
            colorName = ""
            if index == 0:
              colorName = "red"
            elif index == 1:
                colorName = "orange"
            elif index == 2:
                colorName = "yellow"
            elif index == 3:
                colorName = "green"
            elif index == 4:
                colorName = "blue"
            elif index == 5:
                colorName = "indigo"
            elif index == 6:
                colorName = "violet"
            elif index == 7:
                colorName = "white"
            time.sleep(2)
            speak(colorName)
        elif turnoff == 0:
            time.sleep(0.1)
def ultraLoop():
    while True:
        if turnoff == 1:
            dis = distance()
            if dis >= 150:
                time.sleep(1.25)
                buzzer.start(10)
                time.sleep(.1)
                buzzer.stop()
            elif dis >= 120 and dis < 150:
                time.sleep(1)
                buzzer.start(10)
                time.sleep(.1)
                buzzer.stop()
            elif dis >= 90 and dis < 120:
                time.sleep(.75)
                buzzer.start(10)
                time.sleep(.1)
                buzzer.stop()
            elif dis >= 60 and dis < 90:
                time.sleep(.5)
                buzzer.start(10)
                time.sleep(.1)
                buzzer.stop()
            elif dis >= 30 and dis < 60:
                time.sleep(.25)
                buzzer.start(10)
                time.sleep(.1)
                buzzer.stop()
            elif dis >= 0 and dis < 30:
                time.sleep(.07)
                buzzer.start(10)
                time.sleep(.1)
                buzzer.stop()
            else:
                print("too far")
        elif turnoff == 0:
            time.sleep(0.1)
# clears board of any inputs 
def destroy():
    GPIO.cleanup()
# main loop
if __name__ == "__main__":
    setup()
    try:
        colorLoop()
        ultraLoop()
    except KeyboardInterrupt:
        destroy()
