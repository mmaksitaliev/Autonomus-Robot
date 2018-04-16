# Libraries
import RPi.GPIO as GPIO
import time


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

# set GPIO Pins
GPIO_Ain1 = 11
GPIO_Ain2 = 13
GPIO_Apwm = 15
GPIO_Bin1 = 29
GPIO_Bin2 = 31
GPIO_Bpwm = 33

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)

# Both motors are stopped 
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Set PWM parameters
pwm_frequency = 50

# Create the PWM instances
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)

# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(100)
pwmB.start(100)


def normalize(speed):
    return speed, speed - 10

def forward(speed):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)

    lSpeed, rSpeed = normalize(speed)
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print ("FORWARD {} speed".format(speed))
    time.sleep(1)
    stop()


def backwards(speed):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)

    lSpeed, rSpeed = normalize(speed)    
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print ("BACKWARDS {} speed".format(speed))
    time.sleep(1)
    stop()


def right(speed):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)

    lSpeed, rSpeed = normalize(speed)    
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print ("RIGHT {} speed".format(speed))
    time.sleep(0.5)
    stop()


def left(speed):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)

    lSpeed, rSpeed = normalize(speed)    
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print ("LEFT {} speed".format(speed))
    time.sleep(0.5)
    stop()


def stop():
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, False)
    time.sleep(0.2)


def cleanup():
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
