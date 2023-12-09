var map;

var currentDiningMarker = null;

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

function addDiningMarker() {
    if (currentDiningMarker) {
        map.removeObject(currentDiningMarker);
    }
    const currentDining = diningItems[currentDiningIndex];
    const lat = parseFloat(currentDining.dataset.lat);
    const lng = parseFloat(currentDining.dataset.lon);
    currentDiningMarker = new H.map.Marker({lat: lat, lng: lng});
    map.addObject(currentDiningMarker);
}

window.onload = function () {
    initMap();
    addDiningMarker();
}