import sys
import cv2
import picamera
import picamera.array  # This needs to be imported explicitly
import time
import frameprocessor
import colors
import chassis


def cleanup():
    print("Cleaningup")
    cv2.destroyAllWindows()
    camera.close()
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

LASTCOLOR = ""

forwardSpeed = 50
forwardTime = 0.5

turnSpeed = 60
turnTime = 0.5

balanceSpeed = 40
balanceTurn = 0.2

# camera.vflip = True

# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

# allow the camera to warm up
time.sleep(0.1)

def execute(cX, cY):
    if cXEnd >= cX >= cXStart:
        chassis.forward(forwardSpeed, forwardTime)
    elif cXEnd < cX:
        chassis.right(balanceSpeed, balanceTurn)
    elif cXStart > cX:
        chassis.left(balanceSpeed, balanceTurn)

if __name__ == "__main__":
    try:
        # car.init()
        for frame in camera.capture_continuous(rawframe, format="bgr", use_video_port=True):
            # Clear the stream in preparation for the next frame
            rawframe.truncate(0)

            # Create a numpy array representing the image
            image = frame.array
            color, cX, cY = frameprocessor.process(image, remote)
            print(color.upper())
            if color == colors.NOCOLOR:
                color = LASTCOLOR

            if color == colors.GREEN:
                execute(cX, cY)

            elif color == colors.BLUE:
                if cYEnd >= cY >= cYStart:
                    chassis.forward(forwardSpeed, forwardTime)
                    chassis.right(turnSpeed, turnTime)
                else:
                    execute(cX, cY)

            elif color == colors.PINK:
                if cYEnd >= cY >= cYStart:
                    chassis.forward(forwardSpeed, forwardTime)
                    chassis.left(turnSpeed, turnTime)
                else:
                    execute(cX, cY)
            LASTCOLOR = color

    except KeyboardInterrupt:
        cleanup()
