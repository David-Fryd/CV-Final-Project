const MAX_ZOOM_LEVEL = 12;

const MIN_VOTES = 6;
const MAX_VOTES = 9;

export const heatmapLayer = {
  id: "heatmap",
  maxzoom: MAX_ZOOM_LEVEL,
  type: "heatmap",
  paint: {
    "heatmap-weight": [
      "interpolate",
      ["linear"],
      ["get", "votes"],
      MIN_VOTES,
      0.1,
      MAX_VOTES,
      3,
    ],
    "heatmap-intensity": 0.8,
    "heatmap-radius": [
      "interpolate",
      ["linear"],
      ["get", "votes"],
      MIN_VOTES,
      5,
      MAX_VOTES,
      35,
    ],
    // Transition from heatmap to circle layer by zoom level
    "heatmap-opacity": ["interpolate", ["linear"], ["zoom"], 7, 1, 9, 0],
  },
};
