# IMPORTANT: It is recommended to use a white background and position the camera approximately 15 cm from the top
import cv2 as cv
import numpy as np

def calculateValue(area):
    if area < 9000:
        return 0.1
    elif area < 11000:
        return 2
    elif area < 12000:
        return 0.2
    elif area < 13000:
        return 5
    elif area < 16000:
        return 1
    else:
        return 0

# open external webcam, use 0 for built-in webcam
cap = cv.VideoCapture(1)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # binarization using OTSU
    ret, th = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # defining a 5x5 kernel
    kernel5 = np.ones((5, 5), np.uint8)

    # erosion and dilation
    erosion =  cv.erode(th, kernel5, iterations=3)
    dilation = cv.dilate(erosion, kernel5, iterations=3)

    # detecting contours
    contours, _ = cv.findContours(dilation, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(frame, contours, -1, (0,255,0), 2, cv.LINE_AA)

    # calculate value of the coins
    total = 0

    for c in contours:
        area = cv.contourArea(c)
        if area > 5000 and area < 18000:
            cv.drawContours(frame, [c], -1, (0,255,0), 2, cv.LINE_AA)
            cv.putText(frame, str(calculateValue(area)), (c[0][0][0], c[0][0][1] + 70), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
            # displays area for each coin
            #cv.putText(frame, str(area), (c[0][0][0], c[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            total += calculateValue(area)

    # display total
    cv.putText(frame, "Total: S/." + str(round(total, 2)), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    # display webcam 
    cv.imshow('Webcam', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()