# Libraries
import RPi.GPIO as GPIO
import time


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

# set GPIO Pins
GPIO_Ain1 = 11  # left
GPIO_Ain2 = 13
GPIO_Apwm = 15
GPIO_Bin1 = 29  # right
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
pwm_frequency = 100

# Create the PWM instances
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)

# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(50)
pwmB.start(50)


def normalize(speed):
    return speed + 15, speed


def forward(speed, t):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)

    lSpeed, rSpeed = normalize(speed)
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print("FORWARD {} speed".format(speed))
    if t != 0:
        time.sleep(t)
        stop()


def backwards(speed, t):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)

    lSpeed, rSpeed = normalize(speed)
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print("BACKWARDS {} speed".format(speed))
    if t != 0:
        time.sleep(t)
        stop()


def right(speed, t):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)

    lSpeed, rSpeed = normalize(speed)
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print("RIGHT {} speed".format(speed))
    time.sleep(t)
    if t != 0:
        time.sleep(t)
        stop()


def left(speed, t):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)

    lSpeed, rSpeed = normalize(speed)
    pwmA.ChangeDutyCycle(rSpeed)
    pwmB.ChangeDutyCycle(lSpeed)
    print("LEFT {} speed".format(speed))
    time.sleep(t)
    if t != 0:
        time.sleep(t)
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
