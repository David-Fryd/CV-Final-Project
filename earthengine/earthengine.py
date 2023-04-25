import ee
import folium # Helps visualize data locally to help with debugging


firecount = 0
fires = []
MIN_INCIDENT_SIZE = 0
# read from csv file
with open('2023_Wildland_Fire_Incident_Locations_to_Date.csv', 'r') as f:
    # Headers: X,Y,OBJECTID,SourceOID,ABCDMisc,ADSPermissionState,ContainmentDateTime,ControlDateTime,CreatedBySystem,IncidentSize,DiscoveryAcres,DispatchCenterID,EstimatedCostToDate,FinalAcres,FinalFireReportApprovedByTitle,FinalFireReportApprovedByUnit,FinalFireReportApprovedDate,FireBehaviorGeneral,FireBehaviorGeneral1,FireBehaviorGeneral2,FireBehaviorGeneral3,FireCause,FireCauseGeneral,FireCauseSpecific,FireCode,FireDepartmentID,FireDiscoveryDateTime,FireMgmtComplexity,FireOutDateTime,FireStrategyConfinePercent,FireStrategyFullSuppPercent,FireStrategyMonitorPercent,FireStrategyPointZonePercent,FSJobCode,FSOverrideCode,GACC,ICS209ReportDateTime,ICS209ReportForTimePeriodFrom,ICS209ReportForTimePeriodTo,ICS209ReportStatus,IncidentManagementOrganization,IncidentName,IncidentShortDescription,IncidentTypeCategory,IncidentTypeKind,InitialLatitude,InitialLongitude,InitialResponseAcres,InitialResponseDateTime,IrwinID,IsFireCauseInvestigated,IsFireCodeRequested,IsFSAssisted,IsMultiJurisdictional,IsReimbursable,IsTrespass,IsUnifiedCommand,LocalIncidentIdentifier,ModifiedBySystem,PercentContained,PercentPerimeterToBeContained,POOCity,POOCounty,POODispatchCenterID,POOFips,POOJurisdictionalAgency,POOJurisdictionalUnit,POOJurisdictionalUnitParentUnit,POOLandownerCategory,POOLandownerKind,POOLegalDescPrincipalMeridian,POOLegalDescQtr,POOLegalDescQtrQtr,POOLegalDescRange,POOLegalDescSection,POOLegalDescTownship,POOPredictiveServiceAreaID,POOProtectingAgency,POOProtectingUnit,POOState,PredominantFuelGroup,PredominantFuelModel,PrimaryFuelModel,SecondaryFuelModel,TotalIncidentPersonnel,UniqueFireIdentifier,WFDSSDecisionStatus,EstimatedFinalCost,OrganizationalAssessment,StrategicDecisionPublishDate,CreatedOnDateTime_dt,ModifiedOnDateTime_dt,IsCpxChild,CpxName,CpxID,SourceGlobalID,GlobalID
    # Get the X,Y coordinates from the csv file where the header ADSPermissionState is FIREREPORT and the header IncidentSize is greater than 1000
    for line in f:
        # print(line.split(',')[5])
        # print(line.split(',')[9])
        ADSPermissionState = line.split(',')[5]
        IncidentSize = line.split(',')[9]
        try:
            IncidentSize = float(IncidentSize)
        except:
            # print(f"Incident Size {IncidentSize} could not be converted to a float")
            continue
        if ADSPermissionState == 'FIREREPORTING' and IncidentSize > MIN_INCIDENT_SIZE:
            firecount+=1
            # print(line.split(',')[0], line.split(',')[1])
            fires.append({'size': IncidentSize, 'x': line.split(',')[0], 'y': line.split(',')[1]})

print(f'firecount: {firecount}')
fires.sort(key=lambda x: x['size'], reverse=True)
# print(fires)
print(len(fires))

# If debugging, consider disabling this to avoid auth/actual export tasks queuing
EXPORT_ENABLED = True

# Use geemap to display the data locally
DISPLAY_LOCAL = False 

IMAGE_RESOLUTION = 1 # 1 is NAIP's resolution, but some older images have a GSD of 2 meters

# Authenticate and initialize the Earth Engine API
if EXPORT_ENABLED:
    ee.Authenticate()
ee.Initialize()

# Define the date range for the imagery
startDate = '2015-01-01'
endDate = '2023-12-31'

# Set the desired width and height around the points (in meters)
width = 1000
height = 1000



# Define a list of points
points = [
    # -84.42249405	30.2562356600001
    # ee.Geometry.Point([-84.42249405, 30.2562356600001]),  # size 8409, FIREREPORT
#     # -80.65444723	26.3305604170001
#     ee.Geometry.Point([-80.65444723, 26.3305604170001]),  # size 135000
#     # -80.8615328659999	25.416114581
#     ee.Geometry.Point([-80.8615328659999, 25.416114581]),  # size 9000
#      # -104.381610663	44.7551771110001
#     ee.Geometry.Point([-104.381610663, 44.7551771110001]),  # size 1150
#     # -104.063310449	43.893227032
#     ee.Geometry.Point([-104.063310449, 43.893227032]),  # size 256
#    # -103.865010429	44.077117071
#     ee.Geometry.Point([-103.865010429, 44.077117071]),  # size 210
#     # -103.097210034	42.670166952
#     ee.Geometry.Point([-103.097210034, 42.670166952]),  # Wildfire rows 73/74 size 165/164
#     ee.Geometry.Point([-102.929309994, 42.673336965]),  # Wildfire rows 73/74 size 165/164
    

    # ee.Geometry.Point([-103.528510301, 43.7764470600001]),  # Wildfire row 60 (FIREREPORTING size 108)
    # ee.Geometry.Point([-116.803511886, 33.3478248550001]), # Wildfire row 9 (incident size 1)
    # ee.Geometry.Point([-114.706111533, 33.645165003]), # Wildfire row 72 (incident size .1)
    # ee.Geometry.Point([-71.40207331520767, 41.8262773805333]), # Brown university
    # ee.Geometry.Point([-87.66129247116406, 41.94811829191719,]),  # Stella Chicago House
    # ee.Geometry.Point([-118.734, 37.0477]),  # Los Angeles
    # ee.Geometry.Point([-121.9667, 44.3742]),  # Oregon
    # ee.Geometry.Point([-80.128110, 25.790654]),  # Miami Beach
    # ee.Geometry.Point([-87.629798, 41.878114]), # Chicago
]

def export_image_at_point(point, index, firesize):
    # Calculate the coordinates for the rectangle
    rect_coords = point.transform('EPSG:32617', 1e-3).buffer(width / 2, height / 2).bounds().transform('EPSG:4326', 1e-3).coordinates()

    lon = point.coordinates().get(0).getInfo()
    lat = point.coordinates().get(1).getInfo()
    

    # Create a rectangular geometry around the point
    rectangular_geometry = ee.Geometry.Polygon(rect_coords)

    # Load the NAIP dataset
    naip = ee.ImageCollection("USDA/NAIP/DOQQ") \
        .filterDate(startDate, endDate) \
        .filterBounds(point)
    
    # print(naip.size().getInfo())

    # Select the best image (least cloud cover)
    best_image = naip.sort('CLOUD_COVER').first()

    if best_image:
        # Clip the image to the rectangular geometry
        clipped_image = best_image.clip(rectangular_geometry)

        # Compute the min and max values for each band
        stats = clipped_image.reduceRegion(
            reducer=ee.Reducer.minMax(),
            geometry=rectangular_geometry,
            scale=IMAGE_RESOLUTION,  # NAIP's resolution
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
            print(f"WARNING, some values are None for point {index}. This will cause an error and make the task fail. This might be because the image is empty (try expanding date/time range to find a best image for this point.)")
            stats = clipped_image.reduceRegion(
                reducer=ee.Reducer.percentile([0, 100]),
                geometry=rectangular_geometry,
                scale=IMAGE_RESOLUTION,  # NAIP's resolution
                maxPixels=1e10
            ).getInfo()
            print(f'\tstats for point {index}: {stats}')
            min_values = [0, 0, 0]
            max_values = [1,1,1]

        if EXPORT_ENABLED:
            # Create an export task
            export_task = ee.batch.Export.image.toDrive(
                image=clipped_image.visualize(
                    bands=['R', 'G', 'B'],
                    min=min_values,
                    max=max_values
                ),
                description=f'Wildfire_{index}_FIREREPORTING_YEAR2023_Size_{firesize}_at_{lat}_{lon}_NAIP_Rectangle',
                driveFolder='CV-Final/Wildfire',
                scale=IMAGE_RESOLUTION,
                region=rectangular_geometry,
                fileFormat='GeoTIFF',
                maxPixels=1e10
            )

            # Start the export task
            export_task.start()
        
        if DISPLAY_LOCAL:
            # Create a Folium map object
            m = folium.Map(location=[point.coordinates().getInfo()[1], point.coordinates().getInfo()[0]], zoom_start=100)

            # Get the bounds of the clipped image
            bounds = rectangular_geometry.bounds().getInfo()['coordinates'][0]

            # Add the clipped image as a layer on the map
            folium.raster_layers.ImageOverlay(
                clipped_image.getThumbUrl({
                    'min': [min_values[0], min_values[1], min_values[2]],
                    'max': [max_values[0], max_values[1], max_values[2]],
                    'bands': 'R,G,B'
                }),
                bounds=[[bounds[0][1], bounds[0][0]], [bounds[2][1], bounds[2][0]]]
            ).add_to(m)

            # Display the map
            m.save(f'localdisplay/index_{index}_map.html')

    else:
        print(f'No suitable image found for point {index} in the specified date range and location.')

# Iterate through the list of points and export images asynchronously
# for i, point in enumerate(points):
#     export_image_at_point(point, i)
    # Raw editor available here: https://code.earthengine.google.com/
    # See tasks here: https://code.earthengine.google.com/tasks


SKIP_TO = 311
for idx, fire in enumerate(fires):
    print(f"idx: {idx}")
    print(f"attempting to export {fire['x']}, {fire['y']}: size {fire['size']}")
    point = ee.Geometry.Point([float(fire['x']), float(fire['y'])])
    export_image_at_point(point, idx, fire['size'])