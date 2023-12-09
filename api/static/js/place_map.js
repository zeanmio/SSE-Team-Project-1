// place map script
var map;

var currentPlaceMarker = null;

function initMap() {
    var platform = new H.service.Platform({
        'apikey': 'J_jCI8FU0l9fJkPkv6FLn9PusIeY1jxSECepGED2WP4'
    });
    var defaultLayers = platform.createDefaultLayers();

    map = new H.Map(
        document.getElementById('map'),
        defaultLayers.vector.normal.map,
        {
            zoom: 14,
            center: {lat: lat, lng: lon},
            pixelRatio: window.devicePixelRatio || 1
        }
    );
    window.addEventListener('resize', () => map.getViewPort().resize());
    var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
    var ui = H.ui.UI.createDefault(map, defaultLayers);
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

window.onload = function () {
    initMap();
    addPlaceMarker();
}