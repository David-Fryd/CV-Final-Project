import keras,os
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import hyperparameters as hp

class YourModel(keras.Model):
    """ Your own neural network model. """

    def __init__(self):
        super(YourModel, self).__init__()

        # TASK 1.1
        #     Select an optimizer for your network (see the documentation
        #     for tf.keras.optimizers)
       
        self.optimizer = keras.optimizers.SGD(
            learning_rate = 0.001,
        )
    
        # TASK 1
        # 1.4 and after 1.7: Build your own convolutional neural network with a 
        #       15 million parameter budget. The input image will be 
        #       passed through each layer in self.architecture sequentially. 
        #       The imported layers at the top of this file are sufficient
        #       to pass the homework, but feel free to import other layers.
        #
        #       Note 1: 
        #       You will see a model summary when you run the program that
        #       displays the total number of parameters of your network.
        #
        #       Note 2: 
        #       Because this is a 15-scene classification task,
        #       the output dimension of the network must be 15. That is,
        #       passing a tensor of shape [batch_size, img_size, img_size, 1]
        #       into the network will produce an output of shape
        #       [batch_size, 15].
        #
        #       Note 3: 
        #       Keras layers such as Conv2D and Dense give you the
        #       option of defining an activation function for the layer.
        #       For example, if you wanted ReLU activation on a Conv2D
        #       layer, you'd simply pass the string 'relu' to the
        #       activation parameter when instantiating the layer.
        #       While the choice of what activation functions you use
        #       is up to you, the final layer must use the softmax
        #       activation function so that the output of your network
        #       is a probability distribution.
        #
        #       Note 4: 
        #       Flatten is a useful layer to vectorize activations. 
        #       This saves having to reshape tensors in your network.

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

        # TASK 1.1
        #     Select a loss function for your network 
        #     (see the documentation for tf.keras.losses)

        return keras.metrics.binary_crossentropy(labels, predictions, from_logits=False)