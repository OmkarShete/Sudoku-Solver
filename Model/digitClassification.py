import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# ****************************************************
# Importing Libraries
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

from myModel import myModel

# ###############################################
num_classes = 10
epoch = 25
dataPath = "Model/trainedModel/model.h5"
# ###############################################

# Importing MNIST dataset
mnistData = np.load(dataPath)
X_test = mnistData["x_test"]
X_train = mnistData["x_train"]
y_test = mnistData["y_test"]
y_train = mnistData["y_train"]

X_train = X_train.reshape(-1, 28, 28, 1).astype('float32')/255.0 # resizing the data and normalizing it to ease the compuation
X_test = X_test.reshape(-1, 28, 28, 1).astype('float32') /255.0 # resizing the data and normalizing it to ease the compuation

# Printing the shapes
print("Shape of X_train : {}".format(X_train.shape))
print("Shape of y_train : {}".format(y_train.shape))
print("Shape of X_test  : {}".format(X_test.shape))
print("Shape of y_test  : {}".format(y_test.shape))


# Creating a model
model = myModel()
model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy'],
    optimizer=keras.optimizers.Adam(learning_rate=3e-4)
        )
model.summary()

# Training model
history = model.fit(X_train, y_train, epochs=epoch, batch_size=64, verbose=1)

# Evaluating the trained model
model.evaluate(X_test, y_test, batch_size=64, verbose=1)

# Saving model and weights
model.save("trainedModel/myModel.h5")


# Plotting the learning curve
loss = history.history['loss']
epochs = history.epoch
plt.plot(epochs, loss)
plt.xlabel('number of Epochs')
plt.ylabel('Loss')
plt.title('Learning Curve')
plt.savefig('graphs/LearningCurve.png', dpi=300, bbox_inches='tight')
plt.show()

# Plotting the Accuracy curve
acc = history.history['accuracy']
epochs = history.epoch
plt.plot(epochs, acc)
plt.xlabel('number of Epochs')
plt.ylabel('Accuracy')
plt.title('Accuracy vs Epochs')
plt.savefig('graphs/AccuracyCurve.png', dpi=300, bbox_inches='tight')
plt.show()
