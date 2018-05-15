import cv2
import numpy as np
import colors
import imutils


def get_pixels(hsv_image, color_range):
    image_mask = cv2.inRange(hsv_image, color_range[0], color_range[1])
    return cv2.countNonZero(image_mask), image_mask


def process(frame, remote):
    # Convert for BGR to HSV color space, using openCV
    # The reason is that it is easier to extract colors in the HSV space
    # Note: the fact that we are using openCV is why the format for the camera.capture was chosen to be BGR
    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    px_pink, mask_pink = get_pixels(image_hsv, colors.pink)
    px_green, mask_green = get_pixels(image_hsv, colors.green)
    px_blue, mask_blue = get_pixels(image_hsv, colors.blue)

    if px_pink > max(px_green, px_blue):
        mask = mask_pink
        detected_color = colors.PINK
    elif px_green > max(px_blue, px_pink):
        mask = mask_green
        detected_color = colors.GREEN
    elif px_blue > max(px_green, px_pink):
        mask = mask_blue
        detected_color = colors.BLUE
    else:
        mask = mask_pink
        detected_color = colors.NOCOLOR

    c = None
    cX = cY = -1
    if detected_color != colors.NOCOLOR:
        image = cv2.bitwise_and(frame, frame, mask=mask)        
        # (1) Read
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        for c in cnts:
            if cv2.contourArea(c) > 30:
                # compute the center of the contour
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # draw the contour and center of the shape on the image
                    if not remote:
                        cv2.circle(image, (cX, cY), 7, (0, 0, 255), -1)
                break

        # show the image not remote
        if not remote:
            cv2.imshow("orig image", frame)
            cv2.imshow("image", image)
    return detected_color, cX, cY


def cleanup():
    cv2.destroyAllWindows()
    