import time
import subprocess
import speech_recognition as sr
import board
import adafruit_tcs34725

from scipy.spatial import KDTree
from webcolors import (
    css3_hex_to_names,
    hex_to_rgb,
)

i2c = board.I2C()
sensor = adafruit_tcs34725.TCS34725(i2c)

def convert_rgb_to_names(rgb_tuple):
    css3_db = css3_hex_to_names
    names = []
    rgb_values = []

    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)

    distance, index = kdt_db.query(rgb_tuple)
    return f'closest match: {names[index]}'

def speak(text):
    text = text.replace(" ", "_")
    subprocess.run(("espeak \"" + text + " 2>/dev/null").split(" "))

while True:
    color_name = convert_rgb_to_names((sensor.color_rgb_bytes))
    #color_name = convert_rgb_to_names((17, 245, 129))
    print(color_name)
    #speak(color_name)
    time.sleep(1.0)