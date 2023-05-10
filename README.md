# CV-Final-Project

Quick overview of the directory structure, and the code we wrote and their purpose:

### cnn/

Contains the `.py` files associated w/ our Binary Image Classifier. We also have the trained weights for the model.

### earthengine/

Contains the logic we used to analyze the 2023 Wildfire data and query Google Earth Engine for the satellite images we needed to agument the dataset. Contains the original `earthengine.js` used in Google's in-browser editor, and the `earthengine.py` file that was actually run locally to to query and automatically save the data to drive from the command line.

### geo/first-pass

Contains the manually defined GeoJSON border data for the state of Oregon

### geo/getpoints

Contains the logic for generating points within the borders of Oregon using Poisson-disc sampling. `getpoints.py` file contains the logic, all other `.csv`/`.geojson` files are some of the outputted results from the function.

### geo/getimagesmapbox

Contains the logic for ingesting points generated by `getpoints.py`, querying Mapbox for a cluster of satellite images surrounding each point, and storing the results locally.

### visualization/

Contains code for the web-app used to generate the heatmap visualization, taking as input the `.geojson` results from `run_oregon.py` from the `cnn` directory.
