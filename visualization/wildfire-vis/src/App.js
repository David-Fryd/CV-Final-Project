import logo from "./logo.svg";
import "./App.css";
import ReactMapGL from "react-map-gl";
import { useState } from "react";
import {
  heatmapLayer,
  heatmapLayerDENSE,
  circleLayer,
  circleLayerOutline,
  circleLayerDot,
  circleLayerOutline2,
  circleLayerDot2,
  circleLayerForHeatmap,
  circleLayerOutlineForHeatmap,
  circleLayerOutlineForHeatmapDENSE,
  circleLayerForHeatmapDENSE,
} from "./map-style.js";
import MapGL, { Source, Layer } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css"; // required import

const USE_DENSE = true;

const mapboxToken =
  "pk.eyJ1IjoiZGF2aWQtZnJ5ZCIsImEiOiJjbGhjbmIzMWYxMnR5M2VvMWp4dGQ4NjlyIn0.-6wciYJoESyTo6nSJhX4TQ";

// Make a new geoJSON object
const geojson = {
  type: "FeatureCollection",
  features: [],
};

// Injest "wildfires.json" and set the features array to the geojson.features array

if (!USE_DENSE) {
  fetch("wildfires.json")
    .then((response) => response.json())
    .then((data) => {
      geojson.features = data;
      console.log(geojson);
    });
} else {
  fetch("wildfire-dense.json")
    .then((response) => response.json())
    .then((data) => {
      geojson.features = data;
      console.log(geojson);
    });
}

// fetch("/wildfires-dense.json")
//   .then((response) => response.json())
//   .then((data) => {
//     geojsonDense.features = data;
//     console.log(geojsonDense);
//   });

console.log(geojson);
// console.log(geojsonDense);

function App() {
  const [viewport, setViewport] = useState({
    // width: "100vw",
    // height: "100vh",
    latitude: 44.0041,
    longitude: -120.5542,
    zoom: 6.45,
  });

  return (
    <div className="App">
      <ReactMapGL
        {...viewport}
        attributionControl={false}
        width="100vw"
        height="100vh"
        mapboxAccessToken={mapboxToken}
        onMove={(event) => setViewport(event.viewState)}
        // CUSTOM DARK STYLE
        // mapStyle="mapbox://styles/david-fryd/clhctzym4009601pe266yh2ts"
        mapStyle="mapbox://styles/mapbox/satellite-v9"
        // mapStyle="mapbox://styles/mapbox/outdoors-v11"
        // mapStyle="mapbox://styles/mapbox/light-v10"
        // mapStyle="mapbox://styles/mapbox/dark-v10"
        // Streets: mapbox://styles/mapbox/streets-v11
        // Outdors: mapbox://styles/mapbox/outdoors-v11
        // Light: mapbox://styles/mapbox/light-v10
        // Dark: mapbox://styles/mapbox/dark-v10
        // Satellite: mapbox://styles/mapbox/satellite-v9
        // Satellite Streets: mapbox://styles/mapbox/satellite-streets-v11
      >
        {!USE_DENSE && (
          <Source type="geojson" data={geojson}>
            <Layer {...heatmapLayer} />
            <Layer {...circleLayerOutlineForHeatmap} />
            <Layer {...circleLayerForHeatmap} />
          </Source>
        )}
        {USE_DENSE && (
          <Source type="geojson" data={geojson}>
            <Layer {...heatmapLayerDENSE} />
            <Layer {...circleLayerOutlineForHeatmapDENSE} />
            <Layer {...circleLayerForHeatmapDENSE} />
          </Source>
        )}
        {/* Best results w/ mapStyle="mapbox://styles/mapbox/satellite-v9" */}
        {/* <Source type="geojson" data={geojson}>
          <Layer {...circleLayerOutline} />
          <Layer {...circleLayerDot} />
        </Source> */}
        {/* Best results w/ mapStyle="mapbox://styles/mapbox/satellite-v9" */}
        {/* <Source type="geojson" data={geojson}>
          <Layer {...heatmapLayer} />
          <Layer {...circleLayerOutline2} />
          <Layer {...circleLayerDot2} />
        </Source> */}
        {/* <Source type="geojson" data={geojson}>
          <Layer {...heatmapLayer} />
        </Source> */}
      </ReactMapGL>
    </div>
  );
}

export default App;
