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


function moveMapToCity(map){
    map.setCenter({lat: lat, lng: lon});
    map.setZoom(14);
}

window.onload = function () {
    moveMapToCity(map);
    addMarkers();
}

function addMarkers(){
    map.removeObjects(map.getObjects());
    const currentPlace = placeItems[currentPlaceIndex];
    const attraction_lat = parseFloat(currentPlace.dataset.lat);
    const attraction_lon = parseFloat(currentPlace.dataset.lon);
    var marker = new H.map.Marker({lat: attraction_lat, lng: attraction_lon});
    map.addObject(marker);
}