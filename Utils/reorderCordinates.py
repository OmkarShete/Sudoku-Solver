import numpy as np

# Reordering the image into proper manner
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))  # 4 points which are represented using 2 coordinates
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)  # 2nd col - 1st col
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew
