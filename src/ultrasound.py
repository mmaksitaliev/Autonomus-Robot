# Libraries
import RPi.GPIO as GPIO
import time

FRONT = "front"
LEFT = "left"

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
GPIO_TRIGGER_FRONT    = 18
GPIO_ECHO_FRONT       = 22

GPIO_TRIGGER_LEFT    = 24
GPIO_ECHO_LEFT       = 26

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_FRONT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_FRONT, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)

# Wait for sensor to settle
GPIO.output(GPIO_TRIGGER_FRONT, False)
GPIO.output(GPIO_TRIGGER_LEFT, False)
print("Waiting for sensor to settle")
time.sleep(2)
print("Start sensing")


# Get the distance from the ultrasound sensor 
def distance(sensor):
    if sensor == LEFT:
        trigger = GPIO_TRIGGER_LEFT
        echo = GPIO_ECHO_LEFT
    else:
        trigger = GPIO_TRIGGER_FRONT
        echo = GPIO_ECHO_FRONT
    # set Trigger to HIGH
    GPIO.output(trigger, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    valid = True
    RefTime = time.time()
    StartTime = RefTime
    # save StartTime
    while (GPIO.input(echo) == 0) and (StartTime-RefTime < 0.1):
        StartTime = time.time()
    if (StartTime-RefTime >= 0.1):
        valid = False
        
    RefTime = time.time()
    StopTime = time.time()
    # save time of arrival
    while (GPIO.input(echo) == 1) and (StopTime-RefTime < 0.2):
        StopTime = time.time()
    if (StopTime-RefTime >= 0.1):
        valid = False
        
    
    if (valid):
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    else:
        distance = -1
        
    return distance


def cleanup():
    GPIO.cleanup()
    