import cv2
import picamera
import picamera.array  # This needs to be imported explicitly
import time
import frameProcessor


def cleanup():
    print("Cleaninup")
    cv2.destroyAllWindows()
    camera.close()


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

# allow the camera to warm up
time.sleep(0.1)

if __name__ == "__main__":
    try:
        for frame in camera.capture_continuous(rawframe, format="bgr", use_video_port=True):
            # Clear the stream in preparation for the next frame
            rawframe.truncate(0)

            # Create a numpy array representing the image
            image = frame.array
            color = frameProcessor.process(image)
            print(color)
            # The waitKey command is needed to force openCV to show the image
            cv2.waitKey(1)

    except KeyboardInterrupt:
        cleanup()
