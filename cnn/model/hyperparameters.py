"""
Number of epochs. 
"""
num_epochs = 15

"""
Learning rate for the optimizer.
"""
learning_rate = 0.001

"""
Momentum on the gradient
"""
momentum = 0.01

"""
Resize image size for preprocessing.
"""
img_size = 224

"""
Sample size for calculating the mean and standard deviation of the
training data.
"""
preprocess_sample_size = 400

"""
Maximum number of weight files to save to checkpoint directory. If
set to a number <= 0, then all weight files of every epoch will be
saved. Otherwise, only the weights with highest accuracy will be saved.
"""
max_num_weights = 5

"""
Number of training examples per batch.
"""
batch_size = 10

"""
Number of classes in the dataset.
"""
num_classes = 2