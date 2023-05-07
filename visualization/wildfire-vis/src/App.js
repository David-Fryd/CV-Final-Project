import logo from "./logo.svg";
import "./App.css";
import ReactMapGL from "react-map-gl";
import { useState } from "react";
import { heatmapLayer } from "./map-style.js";
import MapGL, { Source, Layer } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css"; // required import

const mapboxToken =
  "pk.eyJ1IjoiZGF2aWQtZnJ5ZCIsImEiOiJjbGhjbmIzMWYxMnR5M2VvMWp4dGQ4NjlyIn0.-6wciYJoESyTo6nSJhX4TQ";

// Make a new geoJSON object
const geojson = {
  type: "FeatureCollection",
  features: [],
};

// Injest "wildfires.json" and set the features array to the geojson.features array
fetch("/wildfires.json")
  .then((response) => response.json())
  .then((data) => {
    geojson.features = data;
    console.log(geojson); // Move this line inside the .then() block
  });

console.log(geojson);

function App() {
  const [viewport, setViewport] = useState({
    // width: "100vw",
    // height: "100vh",
    latitude: 37.7577,
    longitude: -122.4376,
    zoom: 8,
  });

  return (
    <div className="App">
      <ReactMapGL
        {...viewport}
        width="100vw"
        height="100vh"
        mapboxAccessToken={mapboxToken}
        onMove={(event) => setViewport(event.viewState)}
        mapStyle="mapbox://styles/mapbox/dark-v10"
        // Streets: mapbox://styles/mapbox/streets-v11
        // Outdoors: mapbox://styles/mapbox/outdoors-v11
        // Light: mapbox://styles/mapbox/light-v10
        // Dark: mapbox://styles/mapbox/dark-v10
        // Satellite: mapbox://styles/mapbox/satellite-v9
        // Satellite Streets: mapbox://styles/mapbox/satellite-streets-v11
      >
        <Source type="geojson" data={geojson}>
          <Layer {...heatmapLayer} />
        </Source>
      </ReactMapGL>
    </div>
  );
}

export default App;
