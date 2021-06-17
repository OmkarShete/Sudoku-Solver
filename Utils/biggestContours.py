import cv2
import numpy as np

# finding the biggest contour (which will have our sudoku in image)
def biggestContours(contours):
    biggestContour = np.array([])  # to store the biggest contour (finally will be converted into 3D numpy matrix)
    maxArea = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # removing noise i.e small unnecessary contours
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)  # approximates the object vertices
            # 2nd parameter refers to amount of maximum approximation to be done to satisfy the respective polygon
            if area > maxArea and len(approx) == 4:
                biggestContour = approx  # appending 2D matrix into 1D matrix and converting into 3D matrix
                maxArea = area  # storing the maximum area
    return biggestContour, maxArea
