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

weights_path = "/Users/davidfryd/Documents/your.weights.e016-acc0.9663.h5"
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
        if i == 8:
            break
    mean = np.mean(images, axis=0)
    std = np.std(images, axis=0)
    images = (images - mean) / std
    predictions = np.reshape(model.predict(images), (9,))
    votes = np.count_nonzero(predictions > 0.5)
    geoJSON.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "wildfire": votes == 9,
                "votes": votes,
            }
        }
    )
    return votes == 9

def predict_wildfire_risk(dir_path):
    clusters = 0
    wildfires = 0
    for path, directories, files in os.walk(dir_path):
        for cluster_dir in directories:
            clusters += 1
            if clusters % 10:
                print(clusters)
            wildfire = model_confidence_vote(os.path.join(path, cluster_dir))
            if wildfire:
                wildfires += 1
    print(f"num wildfires: {wildfires} out of {clusters}")

predict_wildfire_risk("/Users/davidfryd/BrownCS/cs1430/CV-Final-Project/geo/getimagesmapbox/images")
with open("wildfire-predictions.json", "w") as outfile:
    json.dump(geoJSON, outfile)


