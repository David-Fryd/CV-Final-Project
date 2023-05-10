# Given a GeoJSON polygon, generate a set of points that are at least a min. distance
# apart using Poissoin sampling (relatively even distribution)

import geopandas as gpd
import numpy as np
import json
from shapely.geometry import Point, Polygon
from bridson import poisson_disc_samples
from math import radians, sin, cos, sqrt, atan2

# import oregon.geojson and set to geojson
geojson = json.load(open('oregon.geojson'))

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

def generate_points_poisson(geojson, min_distance_meters):
    gdf = gpd.GeoDataFrame.from_features(geojson['features'])
    polygon = gdf['geometry'][0]
    
    min_x, min_y, max_x, max_y = polygon.bounds
    width = max_x - min_x
    height = max_y - min_y
    latitude = (min_y + max_y) / 2

    min_distance_degrees = meters_to_degrees(min_distance_meters, latitude)
    points = poisson_disc_samples(width=width, height=height, r=min_distance_degrees)
    points = [Point(x + min_x, y + min_y) for x, y in points]

    sampled_points = gpd.GeoDataFrame(geometry=points)
    sampled_points = sampled_points[sampled_points.within(polygon)]
    
    return sampled_points

def save_output(sampled_points, csv_filename, geojson_filename):
    sampled_points.to_csv(csv_filename, index=False)
    sampled_points.to_file(geojson_filename, driver='GeoJSON')


MIN_DIST_IN_METERS = 4000 # 10000 = 10 km minimum distance

# Generate points using Poisson Disk Sampling
sampled_points = generate_points_poisson(geojson, MIN_DIST_IN_METERS)
num_points = len(sampled_points)

# Save the output as CSV and GeoJSON files
save_output(sampled_points, f"sampled_points_mindist{MIN_DIST_IN_METERS}_{num_points}points.csv", f"sampled_points_mindist{MIN_DIST_IN_METERS}_{num_points}points.geojson")

print(sampled_points)
print(len(sampled_points))