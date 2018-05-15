import sys, time
import cv2
import picamera
import picamera.array  # This needs to be imported explicitly

# our modules
import frameprocessor, chassis, ultrasound, colors


def cleanup():
    print("Cleaning up")
    camera.close()
    frameprocessor.cleanup()
    ultrasound.cleanup()
    chassis.cleanup()


remote = True
if len(sys.argv) > 1:
    remote = True if sys.argv[1] == 0 else False

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

cXStart = 220
cXEnd = 420

cYStart = 460
cYEnd = 480

forwardSpeed = 50
forwardTime = 0.5

turnSpeed = 60
turnTime = 0.5

balanceSpeed = 50
balanceTurnTime = 0.3

obstacleDistance = 10

# set GREEN as initial color, so initially car goes forward
LASTCOLOR = colors.GREEN
TURNING = False
X = "X"
Y = "Y"

# camera.vflip = True

# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

# allow the camera to warm up
time.sleep(0.1)

def execute(axis, cX, cY):
    if axis == X:
        if cXStart <= cX <= cXEnd:
            chassis.forward(forwardSpeed, forwardTime)
        elif cXEnd < cX:
            print("BALANCING", axis)
            chassis.right(balanceSpeed, balanceTurnTime)
        elif cXStart > cX:
            print("BALANCING", axis)
            chassis.left(balanceSpeed, balanceTurnTime)
    elif axis == Y:
        print("BALANCING", axis)                
        if cY < cYStart:
            chassis.forward(balanceSpeed, balanceTurnTime)


if __name__ == "__main__":
    try:
        for frame in camera.capture_continuous(rawframe, format="bgr", use_video_port=True):
            frontD = ultrasound.distance(ultrasound.FRONT)

            # Clear the stream in preparation for the next frame
            rawframe.truncate(0)

            # Create a numpy array representing the image
            image = frame.array
            color, cX, cY = frameprocessor.process(image, remote)
            print("-------- {} -------- x={} | y={}".format(color.upper(), cX, cY))
            if color == colors.NOCOLOR:
                color = LASTCOLOR

            # go straight forward
            if color == colors.GREEN:
                if TURNING:
                    TURNING = False

                if cX == -1:
                    cX = 320

                # obstacle is far away or signal was not recieved, just go straight by keeping balance 
                if frontD > obstacleDistance or frontD == -1:
                    execute(X, cX, cY)

                # obstacle is close enough, avoid it
                elif frontD <= obstacleDistance:
                    chassis.right(60, 0.8)
                    leftD = rotations = 0
                    while leftD < 40:
                        rotations += 1
                        chassis.forward(forwardSpeed, 0.4)
                        leftD = ultrasound.distance(ultrasound.LEFT)

                    chassis.left(60, 0.8)
                    chassis.forward(forwardSpeed, 1.3)
                    leftD = 0
                    while leftD < 40:
                        chassis.forward(forwardSpeed, 0.4)
                        leftD = ultrasound.distance(ultrasound.LEFT)

                    chassis.left(60, 0.8)
                    chassis.forward(forwardSpeed, 1)
                    while rotations - 1 > 0:
                        chassis.forward(forwardSpeed, 0.4)
                        rotations -= 1                        

                    chassis.right(60, 0.8)

                    # obstacle avoided, keep going straight forward 
                    color = colors.GREEN

            # turn right
            elif color == colors.PINK:
                # last color was PINK, but now the color is not visible so keep turning                
                if TURNING or cY == -1:
                    chassis.right(turnSpeed, turnTime)

                # get closer to sticker and turn
                elif cYStart <= cY <= cYEnd:
                    TURNING = True
                    chassis.forward(forwardSpeed, 1)
                    chassis.right(turnSpeed, turnTime)

                # get closer to sticker, do not turn yet 
                elif not TURNING:
                    execute(Y, cX, cY)

            # turn left 
            elif color == colors.BLUE:
                # last color was BLUE, but now the color is not visible so keep turning
                if TURNING or cY == -1:
                    chassis.left(turnSpeed, turnTime)

                # get closer to sticker and turn
                elif cYStart <= cY <= cYEnd:
                    TURNING = True
                    chassis.forward(forwardSpeed, 1)
                    chassis.left(turnSpeed, turnTime)

                # get closer to sticker, do not turn yet 
                elif not TURNING:
                    execute(Y, cX, cY)
            LASTCOLOR = color

    except KeyboardInterrupt:
        cleanup()
