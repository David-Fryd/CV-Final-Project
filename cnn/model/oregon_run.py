import geopandas as gp
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from shapely.geometry import Point
import json
import random
import cv2
from cnn import YourModel

weights_path = "/Users/aldai/Documents/Brown/cs1430/CV-Final-Project/cnn/model/checkpoints/your.weights.e004-acc0.9568.h5"
dims = (224, 224, 3)

model = YourModel()
model(tf.keras.Input(shape=dims))
model.summary()
model.load_weights(weights_path, by_name=False)
# Compile model graph
model.compile(
    optimizer=model.optimizer,
    loss=model.loss_fn,
    metrics=["binary_accuracy"])

geoJSON = []

# cluster_path: name_index_long_lat
def filename_to_coordinates(cluster_path):
    items = cluster_path.split('_')
    lon, lat = items[3], items[4]
    return lon, lat

def model_confidence_vote(cluster_path):
    lon, lat = filename_to_coordinates(cluster_path)
    # iterate through cluster path and get predictions
    votes = 0
    images = np.zeros(
            (9, 224, 224, 3))
    i = 0
    for filename in os.listdir(cluster_path):
        f = os.path.join(cluster_path, filename)
        if os.path.isfile(f) and f.endswith('.png'):
            data = cv2.imread(f)
            data = np.array(data, dtype=np.float32)
            data /= 255.
            data = cv2.resize(src=data, dsize=(224, 224), interpolation=cv2.INTER_LINEAR)
            images[i] = data
            i += 1
    mean = np.mean(images, axis=0)
    std = np.std(images, axis=0)
    images = (images - mean) / std
    predictions = np.reshape(model.predict(images), (9,))
    print(predictions)
    votes = np.count_nonzero(predictions > 0.5)
    print(votes)
    geoJSON.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "wildfire": votes >= 5,
                "votes": votes,
            }
        }
    )

def predict_wildfire_risk(dir_path):
    for path, directories, files in os.walk(dir_path):
        for cluster_dir in directories:
            print(os.path.join(path, cluster_dir))
            model_confidence_vote(os.path.join(path, cluster_dir))

predict_wildfire_risk("/Users/aldai/Documents/Brown/cs1430/CV-Final-Project/cnn/oregon_sample")
with open("sample.json", "w") as outfile:
    json.dump(geoJSON, outfile)


