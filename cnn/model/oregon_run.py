import geopandas as gp
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from shapely.geometry import Point
import json
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
    lon, lat = items[2], items[3]
    return lon, lat

def model_predict(image_path):
    im = Image.open(image_path)
    data = np.array(im,dtype=np.float32)
    data = np.reshape(data, dims)
    return model.predict_classes(data)

def model_confidence_vote(cluster_path):
    lon, lat = filename_to_coordinates(cluster_path)
    # iterate through cluster path and get predictions
    votes = 0
    for filename in os.listdir(cluster_path):
        f = os.path.join(cluster_path, filename)
        if os.path.isfile(f) and not f.endswith('.geojson'):
            if model_predict(f):
                votes += 1
    prediction = votes > 4
    geoJSON.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "wildfire": prediction,
                "votes": votes,
            }
        }
    )

def predict_wildfire_risk(dir_path):
    for path, directories, files in os.walk(dir_path):
        for cluster_dir in directories:
            f = os.path.join(path, cluster_dir)
            print(f)
            model_confidence_vote(f)

predict_wildfire_risk("/Users/aldai/Documents/Brown/cs1430/CV-Final-Project/cnn/oregon_sample")
with open("sample.json", "w") as outfile:
    json.dump(geoJSON, outfile)
