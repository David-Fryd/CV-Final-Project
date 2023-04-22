// Set the area of interest: Miami Beach
var miamiBeach = ee.Geometry.Point([-80.12811, 25.790654]);

// Define the date range for the imagery
var startDate = "2020-01-01";
var endDate = "2023-12-31";

// Set the desired width and height around Miami Beach (in meters)
var width = 1000; // Adjust this value to define the width of the area of interest
var height = 1000; // Adjust this value to define the height of the area of interest

// Calculate the coordinates for the rectangle
var rectCoords = miamiBeach
  .transform("EPSG:32617", 1e-3)
  .buffer(width / 2, height / 2)
  .bounds()
  .transform("EPSG:4326", 1e-3)
  .coordinates();

// Create a rectangular geometry around Miami Beach
var rectangularGeometry = ee.Geometry.Polygon(rectCoords);

// Load the NAIP dataset
var naip = ee
  .ImageCollection("USDA/NAIP/DOQQ")
  .filterDate(startDate, endDate)
  .filterBounds(miamiBeach);

// Select the best image (least cloud cover)
var bestImage = naip.sort("CLOUD_COVER").first();

if (bestImage) {
  // Clip the image to the rectangular geometry
  var clippedImage = bestImage.clip(rectangularGeometry);

  // Compute the min and max values for each band
  var stats = clippedImage
    .reduceRegion({
      reducer: ee.Reducer.minMax(),
      geometry: rectangularGeometry,
      scale: 1, // NAIP's resolution
      maxPixels: 1e10,
    })
    .getInfo();

  // Extract the min and max values
  var minValues = [stats["R_min"], stats["G_min"], stats["B_min"]];
  var maxValues = [stats["R_max"], stats["G_max"], stats["B_max"]];

  // Display the result
  Map.setCenter(
    miamiBeach.coordinates().get(0).getInfo(),
    miamiBeach.coordinates().get(1).getInfo(),
    15
  );
  Map.addLayer(
    clippedImage,
    {
      bands: ["R", "G", "B"],
      min: minValues,
      max: maxValues,
    },
    "Miami Beach"
  );

  // Export the image as a GeoTIFF
  Export.image.toDrive({
    image: clippedImage.visualize({
      bands: ["R", "G", "B"],
      min: minValues,
      max: maxValues,
    }),
    description: "MiamiBeach_NAIP_Rectangle_Colorcorrect",
    scale: 1, // NAIP's resolution
    region: rectangularGeometry,
    fileFormat: "GeoTIFF",
    maxPixels: 1e10,
  });
} else {
  print("No suitable image found for the specified date range and location.");
}
