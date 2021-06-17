print("SETTING UP")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# ****************************************************
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from Utils.preprocessing import preProcess
from Utils.biggestContours import biggestContours
from Utils.reorderCordinates import reorder
from Utils.boxSplit import splitBoxes
from Utils.getPrediction import getPrediction
from Utils.displayNumbers import displayNumbers
from Utils.sudokuSolver import solve, print_board
from Utils.checkValidSudoku import isValid, noZero
#######################################
imagePath = "Resources/1.jpeg"
widthImg = 450
heightImg = 450
pathModel = 'Model/trainedModel/myModel.h5'
model = load_model(pathModel)
opWidthImg, opHeightImg = 315, 315
outputPath = "Output_Images/"
#######################################

# Reading Sudoku image
sudokuImg = cv2.imread(imagePath)
sudokuImg = cv2.resize(sudokuImg, (widthImg, heightImg))
preProcessedSudokuImg = preProcess(sudokuImg)

# Finding contours
sudokuImgContour = sudokuImg.copy()
contours, hierarchy = cv2.findContours(preProcessedSudokuImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(sudokuImgContour, contours, -1, (0, 255, 0), 3)

# Finding the maximum contour in image (expecting sudoku to cover major part of image)
biggestContourImg = sudokuImg.copy()
biggestContour, maxArea = biggestContours(contours)

if biggestContour.size != 0:
    # we need to reorder the contour points in proper manner
    biggestContour = reorder(biggestContour)  # biggestContours shape -> (4,1,2)
    # drawing biggest contour on sudokuImg copy
    cv2.drawContours(biggestContourImg, biggestContour, -1, (0, 0, 255), 10)

    # performing warp perspective using biggestContours on sudokuImg
    pts1 = np.float32(biggestContour)  # prepare points for warp
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # prepare points for warp
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(sudokuImg, matrix, (widthImg, heightImg))  # getting perspective
    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)  # converting the warped image into gray scale

    # split the sudoku image into 81 different square image and predicting image using CNN Model trained on MNIST
    boxes = splitBoxes(imgWarpGray)
    predictions, prob = getPrediction(boxes, model)  # predicted number along with its probability

    # display the predicted numbers on blank image
    blankImg = np.zeros((heightImg, widthImg, 3), np.uint8)
    displayNumberImg = displayNumbers(blankImg, predictions, color=(255, 0, 255))
    predictions = np.asarray(predictions)
    # finding the position where 0 is present
    posArray = np.where(predictions > 0, 0, 1)

    # solve the sudoku problem
    sudokuBoard = np.array_split(predictions, 9)

    if isValid(sudokuBoard):  # if board in valid
        print("BOARD IS VALID")
        print("******************************************")
        print("Before solving")
        print_board(sudokuBoard)
        solve(sudokuBoard)  # calling solve function which will solve sudoku problem
        if noZero(sudokuBoard):  # if solution has 0, then puzzle was invalid
            print("******************************************")
            print("after solving")
            print_board(sudokuBoard)
            flatList = []
            for sublist in sudokuBoard:
                for item in sublist:
                    flatList.append(item)
            solvedNumbers = flatList*posArray
            imgSolvedDigits = np.zeros((widthImg, heightImg, 3), np.uint8)  # blank image
            imgSolvedDigits = displayNumbers(imgSolvedDigits, solvedNumbers)  # print only sol values on blank image

            #  Blending the solution on input image
            pts2 = np.float32(biggestContour) # PREPARE POINTS FOR WARP
            pts1 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (widthImg, heightImg))
            # invPerspective = cv2.add(imgInvWarpColored, sudokuImg)
            invPerspective = cv2.addWeighted(imgInvWarpColored, 1, sudokuImg, 0.5, 1)  # Blending part

            # removing the all the old files from the directory
            fileName = os.listdir(outputPath)
            for file in fileName:
                os.remove(os.path.join(outputPath, file))
            cv2.imwrite(os.path.join(outputPath, "1.sudokuImg.jpg"), cv2.resize(sudokuImg, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "2.preProcessedImg.jpg"), cv2.resize(preProcessedSudokuImg, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "3.sudokuImgContour.jpg"), cv2.resize(sudokuImgContour, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "4.biggestContourImg.jpg"), cv2.resize(biggestContourImg, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "5.imgWarpGray.jpg"), cv2.resize(imgWarpGray, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "6.displayNumberImg.jpg"), cv2.resize(displayNumberImg, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "7.imgSolvedDigits.jpg"), cv2.resize(imgSolvedDigits, (opWidthImg, opHeightImg)))
            cv2.imwrite(os.path.join(outputPath, "8.invPerspective.jpg"),  cv2.resize(invPerspective, (opWidthImg, opHeightImg)))

            # displaying the input and final output image
            cv2.imshow("Question Image", sudokuImg)
            cv2.imshow("Answer Image", invPerspective)
            cv2.waitKey(0)
        else:
            #  If for the given sudoku solution doesn't exists
            print("Algorithm was not able to solve the Sudoku puzzle.")
    else:
        #  When sudoku puzzle had any duplicate value in same row/col/sub-box
        print("Sudoku is Invalid. Please upload correct sudoku.")
else:
    #  When contours of 4 vertices was not found
    print("Algorithm was not able to detect the Sudoku in image. Please upload proper image.")
