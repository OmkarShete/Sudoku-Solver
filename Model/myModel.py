from tensorflow import keras
from tensorflow.keras import regularizers

# Creating Model using Functional Keras API
def myModel():
    inputs = keras.Input(shape=(28, 28, 1))
    # First Layer
    X1 = keras.layers.Conv2D(32, (3, 3), padding='same', kernel_initializer='he_normal', kernel_regularizer=regularizers.l2(0.001))(inputs)
    X1 = keras.activations.relu(X1)
    X1 = keras.layers.MaxPooling2D((2, 2))(X1)
    # Second Layer
    X2 = keras.layers.Conv2D(64, (3, 3), padding='same', kernel_initializer='he_normal', kernel_regularizer=regularizers.l2(0.001))(X1)
    X2 = keras.activations.relu(X2)
    X2 = keras.layers.MaxPooling2D((2, 2))(X2)
    # Third Layer
    X3 = keras.layers.Conv2D(128, (5, 5), padding='same', kernel_initializer='he_normal', kernel_regularizer=regularizers.l2(0.001))(X2)
    X3 = keras.activations.relu(X3)
    X3 = keras.layers.MaxPooling2D((2, 2))(X3)
    # Flatten
    X4 = keras.layers.Flatten()(X3)
    # Dense Layers (Third Layer)
    X5 = keras.layers.Dense(100, activation='relu')(X4)
    X5 = keras.layers.Dropout(0.4)(X5)
    # Fourth Layer
    outputs = keras.layers.Dense(10, activation='softmax')(X5)

    my_model = keras.Model(inputs=inputs, outputs=outputs)

    return my_model
