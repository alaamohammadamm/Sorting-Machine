import cv2
import time
import numpy as np
from model import Model
from picamera2 import Picamera2
import servo
import RPi.GPIO as GPIO

# Camera Settings (DEFAULT VALUES: exposure: 1000000, gain: 2.0)
# These settings must match settings in model_train.py
exposure = 1000000
gain = 2.0

LED_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.HIGH)

cv2.waitKey(500)

model = Model()

sort = servo.SortServo()
door = servo.DoorServo()

sort.middle()
door.close()

def main():
    try:
        cam = Picamera2()
        cam.framerate = 100
        cam.configure(cam.create_preview_configuration(main={"format": "BGR888"}))
        cam.start()
        cam.set_controls({"ExposureTime": exposure, "AnalogueGain": gain})
        time.sleep(2)
        class0_count = 0
        class1_count = 0

        x = False

        while True:
            frame = cam.capture_array()
            frame = cv2.flip(frame, 1)
            # To enable preview, uncomment 2 lines below:
            cv2.imshow("Camera Feed", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            cv2.waitKey(50)
            result = model.assess(frame)

            if (result == "red") and x == True:
                sort.right()
                door.open()
                print("sorting red (right)")
                x = False
                class1_count += 1
            if (result == "yellow") and x == True:
                sort.left()
                door.open()
                print("sorting yellow (left)")
                x = False
                class0_count += 1
            if result == "none" and x == False:
                door.close()
                x = True
                #sort.middle()

    except KeyboardInterrupt:
        print("\n\nSorting terminated")
        print("Yellow:", class0_count)
        print("Red:", class1_count)


main()

GPIO.output(LED_PIN, GPIO.LOW)
GPIO.cleanup()
