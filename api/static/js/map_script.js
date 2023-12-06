var platform = new H.service.Platform({
    'apikey': 'J_jCI8FU0l9fJkPkv6FLn9PusIeY1jxSECepGED2WP4'
});
var defaultLayers = platform.createDefaultLayers();

var mapContainer = document.getElementById('map');

var map = new H.Map(document.getElementById('map'),
    defaultLayers.vector.normal.map,{
    center: {lat:50, lng:5},
    zoom: 14,
    pixelRatio: window.devicePixelRatio || 1
});

window.addEventListener('resize', () => map.getViewPort().resize());

var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

var ui = H.ui.UI.createDefault(map, defaultLayers);

var currentPlaceMarker = null;

var currentEventMarker = null;

function moveMapToCity(map){
    map.setCenter({lat: lat, lng: lon});
    map.setZoom(14);
}

function addPlaceMarker() {
    if (currentPlaceMarker) {
        map.removeObject(currentPlaceMarker);
    }
    const currentPlace = placeItems[currentPlaceIndex];
    const lat = parseFloat(currentPlace.dataset.lat);
    const lng = parseFloat(currentPlace.dataset.lon);
    currentPlaceMarker = new H.map.Marker({lat: lat, lng: lng});
    map.addObject(currentPlaceMarker);
}

function addEventMarker() {
    if (currentEventMarker) {
        map.removeObject(currentEventMarker);
    }
    const currentEvent = eventItems[currentEventIndex];
    const lat = parseFloat(currentEvent.dataset.lat);
    const lng = parseFloat(currentEvent.dataset.lon);
    currentEventMarker = new H.map.Marker({lat: lat, lng: lng});
    map.addObject(currentEventMarker);
}

window.onload = function () {
    moveMapToCity(map);
    addPlaceMarker();
    addEventMarker();
}