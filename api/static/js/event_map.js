// event map script
var map;

var currentEventMarker = null;

function initMap() {
    var platform = new H.service.Platform({
        'apikey': 'J_jCI8FU0l9fJkPkv6FLn9PusIeY1jxSECepGED2WP4'
    });
    var defaultLayers = platform.createDefaultLayers();

    map = new H.Map(
        document.getElementById('map'),
        defaultLayers.vector.normal.map,
        {
            zoom: 12,
            center: {lat: lat, lng: lon},
            pixelRatio: window.devicePixelRatio || 1
        }
    );
    window.addEventListener('resize', () => map.getViewPort().resize());
    var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
    var ui = H.ui.UI.createDefault(map, defaultLayers);
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
    initMap();;
    addEventMarker();
}