import cv2

# putting predicted text(non zero) on blank image
def displayNumbers(img, numbers, color = (0, 255, 0)):
    secW = int(img.shape[0]/9)  # width of one image
    secH = int(img.shape[1]/9)  # height of one image
    # putting text in column wise manner
    for x in range(0, 9):  # row
        for y in range(0, 9):  # col
            if numbers[(y*9)+x] != 0:
                cv2.putText(img, str(numbers[(y * 9) + x]),
                            (x * secW + int(secW / 2) - 10, int((y + 0.8) * secH)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            2, color, 2, cv2.LINE_AA)
    return img
