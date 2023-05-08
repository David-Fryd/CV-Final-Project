const MAX_ZOOM_LEVEL = 12;

const MIN_VOTES = 1;
const MAX_VOTES = 9;

export const heatmapLayer = {
  id: "heatmap",
  maxzoom: MAX_ZOOM_LEVEL,
  type: "heatmap",
  paint: {
    "heatmap-weight": [
      "interpolate",
      // ["linear"],
      ["exponential", 2],
      ["get", "votes"],
      MIN_VOTES,
      0.1,
      MAX_VOTES,
      3,
    ],
    "heatmap-intensity": 0.7,
    "heatmap-radius": [
      "interpolate",
      ["exponential", 1],
      // ["linear"],
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

export const heatmapLayerDENSE = {
  id: "heatmap",
  maxzoom: MAX_ZOOM_LEVEL,
  type: "heatmap",
  paint: {
    "heatmap-weight": [
      "interpolate",
      // ["linear"],
      ["exponential", 2],
      ["get", "votes"],
      MIN_VOTES,
      0.2,
      MAX_VOTES,
      1.2,
    ],
    "heatmap-intensity": 0.7,
    "heatmap-radius": [
      "interpolate",
      ["exponential", 1],
      // ["linear"],
      ["get", "votes"],
      MIN_VOTES,
      10,
      MAX_VOTES,
      22,
    ],
    // Transition from heatmap to circle layer by zoom level
    "heatmap-opacity": ["interpolate", ["linear"], ["zoom"], 7, 1, 9, 0],
  },
};

export const circleLayerForHeatmap = {
  id: "circle-heatmap",
  type: "circle",
  paint: {
    "circle-radius": 3,
    "circle-color": "#FF00FF",
    "circle-opacity": 1,
  },
};

export const circleLayerOutlineForHeatmap = {
  id: "circle-outline-heatmap",
  type: "circle",
  paint: {
    "circle-radius": 4,
    "circle-color": "#FFFFFF",
    "circle-opacity": 1,
  },
};
export const circleLayerForHeatmapDENSE = {
  id: "circle-heatmap",
  type: "circle",
  paint: {
    "circle-radius": 1.5,
    "circle-color": "#FF00FF",
    "circle-opacity": 1,
  },
};
export const circleLayerOutlineForHeatmapDENSE = {
  id: "circle-outline-heatmap",
  type: "circle",
  paint: {
    "circle-radius": 2,
    "circle-color": "#FFFFFF",
    "circle-opacity": 1,
  },
};

export const circleLayerOutline = {
  id: "circle-outline",
  type: "circle",
  paint: {
    "circle-radius": 8,
    "circle-color": "#FFFFFF",
    "circle-opacity": 1,
  },
};
export const circleLayerDot = {
  id: "circle-dot",
  type: "circle",
  paint: {
    "circle-radius": 4,
    "circle-color": "#ff00ff",
    "circle-opacity": 1,
  },
};

export const circleLayerOutline2 = {
  id: "circle-outline2",
  type: "circle",
  paint: {
    "circle-radius": 4,
    "circle-color": "#FFFFFF",
    "circle-opacity": 1,
  },
};
export const circleLayerDot2 = {
  id: "circle-dot2",
  type: "circle",
  paint: {
    "circle-radius": 2,
    "circle-color": "#cc00cc",
    "circle-opacity": 1,
  },
};
