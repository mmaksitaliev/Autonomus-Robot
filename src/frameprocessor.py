import cv2
import numpy as np
import colors

def get_pixels(hsv_image, color_range):
    image_mask = cv2.inRange(hsv_image, color_range[0], color_range[1])
    return cv2.countNonZero(image_mask), image_mask


def process(frame, remote=True):
    # Convert for BGR to HSV color space, using openCV
    # The reason is that it is easier to extract colors in the HSV space
    # Note: the fact that we are using openCV is why the format for the camera.capture was chosen to be BGR
    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    px_pink, mask_pink = get_pixels(image_hsv, colors.pink)
    px_green, mask_green = get_pixels(image_hsv, colors.green)
    px_orange, mask_orange = get_pixels(image_hsv, colors.blue)

    if px_pink > max(px_green, px_orange):
        mask = mask_pink
        detected_color = colors.PINK
    elif px_green > max(px_orange, px_pink):
        mask = mask_green
        detected_color = colors.GREEN
    elif px_orange > max(px_green, px_pink):
        mask = mask_orange
        detected_color = colors.BLUE
    else:
        mask = mask_pink
        detected_color = colors.NOCOLOR

    # No need to show images if running from remote machine
    if not remote:
        # Bitwise AND of the mask and the original image
        image_masked = cv2.bitwise_and(frame, frame, mask=mask)

        # Show the frames
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Res", image_masked)
    
    return detected_color
