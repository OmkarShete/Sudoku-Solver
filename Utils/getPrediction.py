import cv2
import numpy as np

# All the 81 images are normalized and resized into 28-by-28 pixel
# Then the images are sent for the prediction using the CNN Model trained on MNIST dataset
def getPrediction(boxes, model):
    result = []
    prob = []
    for image in boxes:
        img = np.asarray(image)
        img = img[4:img.shape[0]-4, 4:img.shape[1]-4]
        img = cv2.resize(img, (28, 28))
        img = img / 255
        img = img.reshape(1, 28, 28, 1)
        prediction = model.predict(img)
        classIndex = np.argmax(prediction, axis=-1)  # returns index of maximum value
        predictionProb = np.amax(prediction)  # returns maximum value along columns
        if predictionProb > 0.8:
            result.append(classIndex[0])
            prob.append(predictionProb)
        else:
            result.append(0)
            prob.append(predictionProb)
    return result, prob  # list of prediction in single list
