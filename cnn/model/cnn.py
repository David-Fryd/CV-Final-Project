import keras,os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import hyperparameters as hp

class BinaryClassifier(keras.Model):
    """ Binary CNN Image Classifier. """

    def __init__(self):
        """ Initializes the model. """
        super(BinaryClassifier, self).__init__()

        self.optimizer = keras.optimizers.SGD(
            learning_rate = hp.learning_rate, momentum = hp.momentum
        )
    
        self.architecture = [
              Conv2D(16, (3,3), activation='leaky_relu', input_shape=(200, 200, 3)),
            MaxPool2D(2, 2),

            Conv2D(32, (3,3), activation='leaky_relu'),
            MaxPool2D(2, 2),

            Conv2D(64, (3,3), activation='leaky_relu'),
            MaxPool2D(2, 2),
            Dropout(0.2),

            Conv2D(64, (3,3), activation='leaky_relu'),
            MaxPool2D(2, 2),

            Conv2D(64, (3,3), activation='leaky_relu'),
            MaxPool2D(2, 2),
            Dropout(0.2),

            Flatten(),

            Dense(512, activation='leaky_relu'),
            Dense(1, activation='sigmoid')
        ]

    def call(self, x):
        """ Passes input image through the network. """

        for layer in self.architecture:
            x = layer(x)

        return x

    @staticmethod
    def loss_fn(labels, predictions):
        """ Loss function for the model. """
        
        return keras.metrics.binary_crossentropy(labels, predictions, from_logits=False)