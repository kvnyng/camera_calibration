import cv2 as cv

cam = cv.VideoCapture(0)

while cam.isOpened:
    ret, frame = cam.read()

    if ret:
        cv.imshow("Frame", frame)
    else:
        break

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()

cv.destroyAllWindows()
    