import geopandas as gpd
from shapely.geometry import Point
from math import cos, pi
import os
import requests
from math import log2
import configparser
from math import radians, sin, cos, sqrt, atan2

# Create a ConfigParser instance
config = configparser.ConfigParser()
# Read the '.env' file
config.read('.env')

# Get the access token from the file
mapbox_access_token = config.get('DEFAULT', 'MAPBOX_TOKEN')
print(f"access token: {mapbox_access_token}")

# Choose a Mapbox style (e.g., streets, satellite, etc.)
mapbox_style = 'mapbox/satellite-v9'


# Image size and resolution approximate the types of images the model was trained on
# Desired image size in meters
image_size_meters = 1000
# Image dimensions in pixels (e.g., 300x300, 500x500, etc.)
image_width = 1000
image_height = 1000

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def meters_to_degrees(min_distance_meters, latitude):
    lat1 = latitude
    lon1 = 0
    lat2 = latitude
    lon2 = 1

    distance_degrees = haversine(lat1, lon1, lat2, lon2)
    return min_distance_meters / distance_degrees

# Function to calculate the zoom level for a given image size in meters
def calculate_zoom_level(latitude, image_size_meters, image_width):
    meters_per_pixel = image_size_meters / image_width
    zoom_level = log2(156543.03392 * cos(latitude * pi/180) / meters_per_pixel)
    return round(zoom_level, 2)

# Function to request images from Mapbox Static Images API
def get_mapbox_image(latitude, longitude, width, height, zoom_level, style, access_token):
    url = f"https://api.mapbox.com/styles/v1/{style}/static/{longitude},{latitude},{zoom_level}/{width}x{height}?access_token={access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error fetching image: {response.text}")


output_directory_name = "images"
polyname = "oregon"
sampled_points = gpd.read_file('sampled_points_mindist11000_734points.geojson')

# Will take a total of cluster_dimension_x by cluster_dimension_y images around a given long/lat point
# INCLUDES THE CENTER IMAGE
cluster_dimension_x = 3
cluster_dimension_y = 3
# (need to have a center point)
assert(cluster_dimension_x % 2 == 1 and cluster_dimension_y % 2 == 1)
assert(cluster_dimension_x > 0 and cluster_dimension_y > 0)

avg_zoom_level = 0
std_dev_zoom_level = 0

# Make sure the subdirectory exists; if not, create it
os.makedirs(output_directory_name, exist_ok=True)

for index, row in sampled_points.iterrows():    
    latitude = row.geometry.y
    longitude = row.geometry.x

    zoom_level = calculate_zoom_level(latitude, image_size_meters, image_width)
    print(f"Cluster {index:4d} of {len(sampled_points):4d} || zoom: {zoom_level:2f} || lat: {latitude:18.14f}  lon: {longitude:18.14f}")


    if index == 2:
        exit()

    cluster_name = f"{polyname}_{index}_{longitude}_{latitude}"
    cluster_output_directory = os.path.join(output_directory_name, cluster_name)
    os.makedirs(cluster_output_directory, exist_ok=True)

    offset_in_meters = image_size_meters # Clustered images will be directly next to each other (lined up edge-wise)

    METERS_PER_DEGREE = 111_320
    delta_latitude = offset_in_meters / 111_320
    delta_longitude = offset_in_meters / (111_320 * cos(radians(latitude)))

    cluster_features_geojson = []

    for i in range(-(cluster_dimension_x//2), (cluster_dimension_x//2) + 1):
        for j in range(-(cluster_dimension_y//2), (cluster_dimension_y//2) + 1):
            # print("i: ", i, "j: ", j)
            latitude_offset = row.geometry.y + i * delta_latitude
            longitude_offset = row.geometry.x + j * delta_longitude
            zoom_level = calculate_zoom_level(latitude_offset, image_size_meters, image_width)

            image_data = get_mapbox_image(latitude_offset, longitude_offset, image_width, image_height, zoom_level, mapbox_style, mapbox_access_token)

            with open(os.path.join(cluster_output_directory, f'{polyname}_{index}_[{i},{j}]_{longitude_offset}_{latitude_offset}.png'), 'wb') as f:
                f.write(image_data)

            # Store the data for this image as geojson for debugging purposes
            point = Point(longitude_offset, latitude_offset)
            cluster_features_geojson.append({
                "geometry": point,
                "filename": f'{polyname}_{index}_[{i},{j}]_{longitude_offset}_{latitude_offset}.png'
            })

    # Create a GeoDataFrame for this cluster and write it to a GeoJSON file
    gdf = gpd.GeoDataFrame(cluster_features_geojson, crs="EPSG:4326")
    gdf.to_file(os.path.join(cluster_output_directory, f'features_{polyname}_{index}.geojson'), driver='GeoJSON')


