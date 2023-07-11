import numpy as np
import cv2 as cv
import signal
from multiprocessing import Process, Manager
import time

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def chessboardWorker(img, size, corners, return_dict):
    return_dict["results"] = cv.findChessboardCorners(img, size, corners)
    return

signal.signal(signal.SIGALRM, timeout_handler)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points
objp = np.zeros((6*7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1,2)

# arrays to store object points and image points from image
objpoints = [] # 3D points
imgpoints = [] # 2D points

cam = cv.VideoCapture(0)

while cam.isOpened: 
    ret, img = cam.read()

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    manager = Manager()
    return_dict = manager.dict()
    
    start_time = time.time()
    process = Process(target=chessboardWorker, args=(gray, (7,5), None, return_dict))
    process.start()
    while process.is_alive():
        length = time.time() - start_time
        if length > .04:
            process.kill()
            return_dict["results"] = (False, None)

    ret, corners = return_dict["results"]
    

    if ret == True:
        print("Found points")
        objpoints.append(objp) # just add raw object point
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # draw and display the corners
        cv.drawChessboardCorners(img, (7,5), corners2, ret)
    else:
        print("No detection")
    cv.namedWindow("Camera", cv.WINDOW_KEEPRATIO)
    cv.resizeWindow("Camera", 1000, 1000)
    cv.imshow("Camera", img)
    cv.waitKey(1)

cam.release()
