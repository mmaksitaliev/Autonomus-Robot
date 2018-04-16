import sys
import cv2
import picamera
import picamera.array  # This needs to be imported explicitly
import time
import frameprocessor, colors, car


def cleanup():
    print("Cleaningup")
    cv2.destroyAllWindows()
    camera.close()

remote = True
if len(sys.argv) > 1:
    remote = sys.argv[1]

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

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
            color = frameprocessor.process(image, remote)
            if color == colors.PINK:
                car.forward(33)

            elif color == colors.BLUE:
                pass

            elif color == colors.PINK:
                pass
            car.stop()
            print(color)

            # The waitKey command is needed to force openCV to show the image
            cv2.waitKey(1)

    except KeyboardInterrupt:
        car.cleanup()
        cleanup()
