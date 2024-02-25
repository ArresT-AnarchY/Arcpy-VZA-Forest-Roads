/* eslint-disable no-undef */
/**
 * leaflet-geoman
 */

const options = {
  position: "topleft", // toolbar position, options are 'topleft', 'topright', 'bottomleft', 'bottomright'
  drawMarker: true, // adds button to draw markers
  drawPolygon: true, // adds button to draw a polygon
  drawPolyline: true, // adds button to draw a polyline
  drawCircle: true, // adds button to draw a cricle
  editPolygon: true, // adds button to toggle global edit mode
  deleteLayer: true, // adds a button to delete layers
  oneBlock: true,
};

// add leaflet.pm controls to the map
map.pm.addControls(options);
map.pm.setLang('tr');

// get array of all available shapes
map.pm.Draw.getShapes();

// disable drawing mode
map.pm.disableDraw("Polygon");

// listen to when drawing mode gets enabled
map.on("pm:drawstart", function (e) {
  console.log(e);
});

// listen to when drawing mode gets disabled
map.on("pm:drawend", function (e) {
  console.log(e);
});

// listen to when a new layer is created
map.on("pm:create", function (e) {
  console.log(e);

  // listen to changes on the new layer
  e.layer.on("pm:edit", function (x) {
    console.log("edit", x);
  });
});