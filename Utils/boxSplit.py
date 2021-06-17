import numpy as np

# > This function splits the sudoku image into 81(9X9) different images
# > To split sudoku into 81 different images make sure sudoku image is square
# > Also the small boxes formed using grid should be square, it should not be rectangle because
# this images are used for predicting purpose using CNN Model which is trained on square image

def splitBoxes(img):
    rows = np.vsplit(img, 9)  # splits the image into 9 different rows
    boxes = []  # will store the all split images
    for row in rows:
        cols = np.hsplit(row, 9)  # split the row image into 9 different images
        for box in cols:  # append images
            boxes.append(box)
    return boxes
