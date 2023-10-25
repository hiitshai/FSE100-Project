import board
import adafruit_tcs34725
import subprocess
import time
import speech_recognition as sr

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

def main():
    while True:
        speak(sensor.color)
        time.sleep(1.0)

def speak(text):
    text = text.replace(" ", "_")
    subprocess.run(("espeak \"" + text + " 2>/dev/null").split(" "))

if __name__ == "__main__":
    main()
