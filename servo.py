import RPi.GPIO as GPIO
import time

class SortServo:
    # To calibrate this motor, adjust ONLY the "center" variable so that the servo arm sticks straight up in the middle position
    # This value can be between 2-12, but somewhere in the 5-7 range is recommended
    servoPIN = 4
    center = 6.75 

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.p = GPIO.PWM(self.servoPIN, 50) # GPIO 17 for PWM with 50Hz
        self.p.start(0) # Initialization

    def right(self):
        self.p.ChangeDutyCycle(self.center + 1.5)
        time.sleep(0.3)
        self.end()

    def left(self):
        self.p.ChangeDutyCycle(self.center - 1.5)
        time.sleep(0.3)
        self.end()

    def middle(self):
        self.p.ChangeDutyCycle(self.center)
        time.sleep(0.3)
        self.end()

    def end(self):
        self.p.ChangeDutyCycle(0)
        time.sleep(0.2)

class DoorServo:
    # To calibrate this motor, adjust ONLY the "center" variable so that the servo arm points straight down in the closed position
    # This value can be between 2-12, but somewhere in the 7-9 range is recommended
    servoPIN = 17
    center = 8

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.p = GPIO.PWM(self.servoPIN, 50) # GPIO 17 for PWM with 50Hz
        self.p.start(0) # Initialization

    def open(self):
        self.p.ChangeDutyCycle(self.center - 4)
        time.sleep(0.2)
        self.end()

    def close(self):
        self.p.ChangeDutyCycle(self.center)
        time.sleep(0.2)
        self.end()

    def end(self):
        self.p.ChangeDutyCycle(0)
        time.sleep(0.2)
