import keras,os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

class VGGModel(keras.Model):

    def __init__(self):
        super(VGGModel, self).__init__()

        self.optimizer = keras.optimizers.Adam(learning_rate = hp.learning_rate)

        self.vgg16 = [
            Conv2D(input_shape=(224,224,3),filters=64,kernel_size=(3,3),padding="same", activation="relu"),
            Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"),
            MaxPool2D(pool_size=(2,2),strides=(2,2)),

            Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"),
            MaxPool2D(pool_size=(2,2),strides=(2,2)),

            Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"),
            MaxPool2D(pool_size=(2,2),strides=(2,2)),

            Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
            MaxPool2D(pool_size=(2,2),strides=(2,2)),

            Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
            Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"),
            MaxPool2D(pool_size=(2,2),strides=(2,2))
        ]

        for layer in self.vgg16:
            layer.trainable = False

        self.head = [
            Flatten(),

            Dense(units=4096, ativation="relu"),
            Dense(units=4096, activation="relu"),

            Dense(units=2, activation="softmax")
        ]

        self.vgg16 = keras.Sequential(self.vgg16, name="vgg_base")
        self.head = keras.Sequential(self.head, name="vgg_head")

    def call(self, x):
        """ Passes the image through the network. """

        x = self.vgg16(x)
        x = self.head(x)

        return x

    @staticmethod
    def loss_fn(labels, predictions):
        """ Loss function for model. """

        return keras.losses.sparse_categorical_crossentropy(labels, predictions)