import sys
import cv2
import picamera
import picamera.array  # This needs to be imported explicitly
import time
import frameprocessor
import colors
import chases


def cleanup():
    print("Cleaningup")
    cv2.destroyAllWindows()
    camera.close()
    chases.cleanup()


remote = True
if len(sys.argv) > 1:
    remote = True if sys.argv[1] == 0 else False

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

cXStart = 220
cXEnd = 420
LASTCOLOR = ""

forwardSpeed = 50
turnSpeed = 60
forwardTime = 0.5
turnTime = 0.5

# camera.vflip = True

# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

# allow the camera to warm up
time.sleep(0.1)

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
            if color != colors.NOCOLOR:
                if color == colors.GREEN:
                    chases.forward(forwardSpeed, forwardTime)
                elif color == colors.BLUE:
                    chases.forward(forwardSpeed, 1.5)
                    chases.right(turnSpeed + 20, turnTime)
                    chases.forward(forwardSpeed, 0.7)                    
                elif color == colors.PINK:
                    if cXEnd > cX > cXStart:
                        pass
                    chases.forward(forwardSpeed, 1)
                    chases.left(turnSpeed, turnTime)
                    chases.forward(forwardSpeed, 0.7)                    
                LASTCOLOR = color

            elif color == colors.NOCOLOR:
                if LASTCOLOR == colors.GREEN:
                    chases.forward(forwardSpeed, forwardTime)
                elif LASTCOLOR == colors.BLUE:
                    chases.forward(forwardSpeed, forwardTime)
                    chases.right(turnSpeed, turnTime)
                elif LASTCOLOR == colors.PINK:
                    chases.forward(forwardSpeed, forwardTime)
                    chases.left(turnSpeed, turnTime)

            cv2.waitKey(1)

    except KeyboardInterrupt:
        cleanup()
