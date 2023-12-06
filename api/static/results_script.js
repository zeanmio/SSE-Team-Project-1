// carousel script
const placeItems = document.querySelectorAll('.place-carousel-item');
const eventItems = document.querySelectorAll('.event-carousel-item');


// Assume airquality_forecast is already set to the JSON data in the correct format

function renderAqiChart(airqualityData) {
    const labels = airqualityData.map(forecast => new Date(forecast.time * 1000).toLocaleString());
    const values = airqualityData.map(forecast => forecast.avg_aqi);
    const ctx = document.getElementById('airQualityChart').getContext('2d');

    // Calculate gradient stops based on data
    function calculateGradientStops(minAqi, maxAqi) {
        const aqiLimits = {good: 1, fair: 2, moderate: 3, poor: 4, veryPoor: 5};
        const aqiColors = {
            good: 'rgba(110, 235, 152, 0.5)',
            fair: 'rgba(228, 232, 21, 0.5)',
            moderate: 'rgba(247, 185, 52, 0.5)',
            poor: 'rgba(235, 50, 40, 0.5)',
            veryPoor: 'rgba(97, 30, 26, 0.5)'
        };

        const stops = [];
        Object.keys(aqiLimits).forEach((key, index, array) => {
            if (minAqi <= aqiLimits[key] && maxAqi >= aqiLimits[key]) {
                let nextLimit = aqiLimits[array[index + 1]] || maxAqi;
                let stopPosition = (aqiLimits[key] - minAqi) / (maxAqi - minAqi);
                let nextStopPosition = (nextLimit - minAqi) / (maxAqi - minAqi);
                stops.push({stop: stopPosition, color: aqiColors[key]});
                if (index === array.length - 1 || nextStopPosition > 1) {
                    stops.push({stop: nextStopPosition, color: aqiColors[key]});
                }
            }
        });
        return stops;
    }

    // Get the min and max AQI values
    const minAqiValue = Math.min(...values);
    const maxAqiValue = Math.max(...values);

    // Create gradient
    let gradientStops = calculateGradientStops(minAqiValue, maxAqiValue);
    let gradient = ctx.createLinearGradient(0, ctx.canvas.clientHeight, 0, 0);
    gradientStops.forEach(stop => {
        // gradient.addColorStop(stop.stop, stop.color);
        console.log(`Adding color stop: ${stop.stop}, ${stop.color}`); // Log the stop position and color
        if (stop.stop < 0 || stop.stop > 1) {
            console.error(`Invalid stop position: ${stop.stop}, color: ${stop.color}`);
        } else {
            gradient.addColorStop(stop.stop, stop.color);
        }
    });

    const aqiChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                label: 'Air quality',
                borderColor: 'black',
                borderWidth: 2,
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        min: 1,
                        max: 5,
                        stepSize: 1,
                        callback: function(value) {
                            switch (value) {
                                case 1: return 'Good';
                                case 2: return 'Fair';
                                case 3: return 'Moderate';
                                case 4: return 'Poor';
                                case 5: return 'Very Poor';
                                default: return '';
                            }
                        }
                    }
                },
                x: {
                    display: false
                }
            },
            plugins:{
                legend: {
                    display: true
                }
            },
            elements: {
                point: {
                    radius: 0
                },
                line: {
                    tension: 0.5
                }
            },
            responsive: true,
            maintainAspectRatio: true
        },
        plugins: [{
            beforeDraw: (chart) => {
                const ctx = chart.ctx;
                const chartArea = chart.chartArea;
                ctx.save();
                ctx.globalCompositeOperation = 'destination-over';
                ctx.fillStyle = gradient;
                ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                ctx.restore();
            }
        }]
    });
}
renderAqiChart(airquality_forecast);

//End of air quality line chart 

let currentPlaceIndex = 0;
let currentEventIndex = 0;

function updateCarousel(items, currentIndex, direction) {
    items[currentIndex].classList.remove('active');
    const totalItems = items.length;
    currentIndex = (currentIndex + direction + totalItems) % totalItems;
    items[currentIndex].classList.add('active');
    return currentIndex;
}

document.getElementById('place-prev').addEventListener('click', function() {
    currentPlaceIndex = updateCarousel(placeItems, currentPlaceIndex, -1);
    addMarkers();
});

document.getElementById('place-next').addEventListener('click', function() {
    currentPlaceIndex = updateCarousel(placeItems, currentPlaceIndex, 1);
    addMarkers();
});

document.getElementById('event-prev').addEventListener('click', function() {
    currentEventIndex = updateCarousel(eventItems, currentEventIndex, -1);
});

document.getElementById('event-next').addEventListener('click', function() {
    currentEventIndex = updateCarousel(eventItems, currentEventIndex, 1);
});

if (placeItems.length > 0) {
    placeItems[0].classList.add('active');
}
if (eventItems.length > 0) {
    eventItems[0].classList.add('active');
}

// map script 
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