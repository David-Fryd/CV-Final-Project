import ee
import geemap # Helps visualize data locally to help with debugging

# If debugging, consider disabling this to avoid auth/actual export tasks queuing
EXPORT_ENABLED = False

# Authenticate and initialize the Earth Engine API
if EXPORT_ENABLED:
    ee.Authenticate()
ee.Initialize()

# Define the date range for the imagery
startDate = '2020-01-01'
endDate = '2023-12-31'

# Set the desired width and height around the points (in meters)
width = 1000
height = 1000

# Define a list of points
points = [
#   ee.Geometry.Point([-80.128110, 25.790654]),  # Miami Beach
  ee.Geometry.Point([-118.243683, 34.052235])  # Los Angeles
]

def export_image_at_point_async(point, index):
    # Calculate the coordinates for the rectangle
    rect_coords = point.transform('EPSG:32617', 1e-3).buffer(width / 2, height / 2).bounds().transform('EPSG:4326', 1e-3).coordinates()

    # Create a rectangular geometry around the point
    rectangular_geometry = ee.Geometry.Polygon(rect_coords)

    # Load the NAIP dataset
    naip = ee.ImageCollection("USDA/NAIP/DOQQ") \
        .filterDate(startDate, endDate) \
        .filterBounds(point)

    # Select the best image (least cloud cover)
    best_image = naip.sort('CLOUD_COVER').first()

    if best_image:
        # Clip the image to the rectangular geometry
        clipped_image = best_image.clip(rectangular_geometry)

        # Compute the min and max values for each band
        stats = clipped_image.reduceRegion(
            reducer=ee.Reducer.minMax(),
            geometry=rectangular_geometry,
            scale=1,  # NAIP's resolution
            maxPixels=1e10
        ).getInfo()

        # Extract the min and max values
        min_values = [stats['R_min'], stats['G_min'], stats['B_min']]
        max_values = [stats['R_max'], stats['G_max'], stats['B_max']]

        print(f'stats for point {index}: {stats}')
        # print(f'min_values for point {index}: {min_values}')
        # print(f'max_values for point {index}: {max_values}')

        # Check if any of the values are None and set default values if needed
        if any(value is None for value in min_values + max_values):
            
            min_values = [0, 0, 0]
            max_values = [255, 255, 255]
            print(f'Could not find min/max values for point {index}, using default values. (min_values = [0, 0, 0], max_values = [255, 255, 255])')

        if EXPORT_ENABLED:
            # Create an export task
            export_task = ee.batch.Export.image.toDrive(
                image=clipped_image.visualize(
                    bands=['R', 'G', 'B'],
                    min=min_values,
                    max=max_values
                ),
                description=f'Fixed-Image_{index}_NAIP_Rectangle',
                driveFolder='CV-Final',
                scale=1,  # NAIP's resolution
                region=rectangular_geometry,
                fileFormat='GeoTIFF',
                maxPixels=1e10
            )

            # Start the export task
            export_task.start()

    else:
        print(f'No suitable image found for point {index} in the specified date range and location.')

# Iterate through the list of points and export images asynchronously
for i, point in enumerate(points):
    export_image_at_point_async(point, i)
    # Raw editor available here: https://code.earthengine.google.com/
    # See tasks here: https://code.earthengine.google.com/tasks