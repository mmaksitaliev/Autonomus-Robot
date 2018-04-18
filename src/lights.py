import RPi.GPIO as GPIO
import time

LedPin = 40                                     # pin 40

def setup():
        ''' One time set up configurations'''
        GPIO.setmode(GPIO.BOARD)                # Numbers GPIOs by physical location
                                                # An alternative is GPIO.BCM
        GPIO.setup(LedPin, GPIO.OUT)            # Set LedPin's mode is output
        GPIO.output(LedPin, GPIO.LOW)          	# Set LedPin low to turn the led off


def blink(times):
    for i in range(times):
        GPIO.output(LedPin, GPIO.HIGH)  # led on
        time.sleep(0.5)
        GPIO.output(LedPin, GPIO.LOW)  	# led off
        time.sleep(0.7)


# keep led on
def on():
    GPIO.output(LedPin, GPIO.HIGH)  # led on    


def cleanup():
        GPIO.output(LedPin, GPIO.LOW)          	# led off
        GPIO.cleanup()  