import RPi.GPIO as GPIO
import time

ledPin = 11

GPIO.setmode(GPIO.BOARD)

GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

if __name__ == "__main__":
    try:
        print("LED ON")
        GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(1)

        print("LED OFF")
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(1)
        
    except KeyboardInterrupt:
        GPIO.output(ledPin, GPIO.LOW)
        GPIO.cleanup()
