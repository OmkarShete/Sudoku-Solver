import cv2
# Preprocessing the image
def preProcess(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # converting image into gray scale
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # adding gaussian blur to smooth the image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2) # thresholding on image to get edges of objects
    return imgThreshold
