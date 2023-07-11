import numpy as np
import cv2 as cv
import glob

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points
objp = np.zeros((6*7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1,2)

# arrays to store object points and image points from image
objpoints = [] # 3D points
imgpoints = [] # 2D points

# cam = cv.VideoCapture(0)

images = glob.glob('./images/*.JPG')
print(f"Images are: {images}")

for image in images:
    print(image)
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    cv.namedWindow(str(image), cv.WINDOW_KEEPRATIO)
    cv.resizeWindow(str(image), 600, 600)
    cv.imshow(str(image), gray)
    
    cv.waitKey(1000)
    
    cv.destroyWindow(str(image))

    ret, corners = cv.findChessboardCorners(gray, (7,5), None)

    if ret == True:
        print("Found points")
        objpoints.append(objp) # just add raw object point
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1, -1), criteria)
        imgpoints.append(corners2)

            # draw and display the corners
        cv.drawChessboardCorners(img, (7,5), corners2, ret)
        cv.namedWindow(str(image), cv.WINDOW_KEEPRATIO)
        cv.resizeWindow(str(image), 600, 600)
        cv.imshow('img', img)

        parts = image.split("/")
        parts[1] = "results"
        parts[2] = parts[2][:-4] + "_detect" + parts[2][-4:]
        
        new_path = "".join(parts)
        print(f"New path is: {new_path}")
        cv.imwrite(new_path, img)

    print("Done")

    # if corners is None:
    #     print("Found nothing...")
    
    # if ret == True:
        # print("Found points")
# # while True:
# for image in images:
#     img = cv.imread(image)
#     if img is not None:
#         print("IMAGE IS NOT NONE")
#         gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#         cv.imshow(str(image), img)

#         # find chess board corners
#         ret, corners = cv.findChessboardCorners(gray, (8,6), None)
#         if corners is None:
#             print("Found nothing...") 
        
#         # if found, add the object and image points
#         if ret == True:
#             print("FOUND POINTS")
#             objpoints.append(objp) # just add raw object point
#             corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1, -1), criteria)
#             imgpoints.append(corners2)

#             # draw and display the corners
#             cv.drawChessboardCorners(img, (7,6), corners2, ret)
#             cv.imshow('img', img)

#     else:
#         break
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
    

# cv.destroyAllWindows()