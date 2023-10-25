import RPi.GPIO as GPIO
import time
import board
import adafruit_tcs34725

TRIG = 17
ECHO = 13
SIG = 27

a = 1

def setup():
    global buzzer
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SIG, GPIO.OUT)
    buzzer = GPIO.PWM(SIG, 440)
    

def distance():
    # global time, distance, time1, time2
    GPIO.output(TRIG, 0)
    time.sleep(0.00002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        a = 0
        #print("testbefore")
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
        
    time2 = time.time()
    during = time2 - time1
    return during * 340 / 2 * 100

def loop():
    global a
    a = 1
    
    while True:
        
        dis = distance()
        
        time.sleep(1)
        
        if dis >= 100:
            buzzer.start(50)
            time.sleep(.3)
            buzzer.stop()
        elif dis >= 75 and dis < 100:
            for num in range(2):
                buzzer.start(50)
                time.sleep(.3)
                buzzer.stop()
        elif dis >= 50 and dis < 75:
            for num in range(3):
                buzzer.start(50)
                time.sleep(.3)
                buzzer.stop()
        elif dis >= 25 and dis < 50:
            for num in range(4):
                buzzer.start(50)
                time.sleep(.3)
                buzzer.stop()
        elif dis >= 1 and dis < 25:
            for num in range(5):
                buzzer.start(50)
                time.sleep(.3)
                buzzer.stop()
        else:
            print("too far")
 
def destroy():
    GPIO.cleanup()
    
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
