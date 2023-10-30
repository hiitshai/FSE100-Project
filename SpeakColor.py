import board
import adafruit_tcs34725
import subprocess
import time
import speech_recognition as sr
import math

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

def main():
    while True:
        color = sensor.color_rgb_bytes
        colorList = [(255,0,0),(255,128,0),(255,255,0),(0,255,0),(0,0,255),(127,0,255),(255,0,255),(0,0,0),(255,255,255)]
        distList = []
        for col in colorList:
            distList.append(math.sqrt(((col[0] - color[0])*0.30)**2 + ((col[1] - color[1])*0.59)**2 + ((col[2] - color[2])*0.11)**2))
        minimum = float('inf')
        index = 0
        for i in range(9): 
            dist = distList[i]
            print(dist)
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
            colorName = "black"
        elif index == 8:
            colorName = "white"
        #try:
            #color2 = rgb_to_name(color, spec='css1')
            #speak(colorName)
        #except:
            #print("invalid")
            #print(color)
        speak(colorName)
        print(colorName)
        print(color)
        time.sleep(1.0)

def speak(text):
    text = text.replace(" ", "_")
    subprocess.run(("espeak \"" + text + " 2>/dev/null").split(" "))

if __name__ == "__main__":
    main()
