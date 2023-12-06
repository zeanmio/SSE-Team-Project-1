// carousel script
const placeItems = document.querySelectorAll('.place-carousel-item');
const eventItems = document.querySelectorAll('.event-carousel-item');

let currentPlaceIndex = 0;
let currentEventIndex = 0;

function updateCarousel(items, currentIndex, direction) {
    items[currentIndex].classList.remove('active');
    const totalItems = items.length;
    currentIndex = (currentIndex + direction + totalItems) % totalItems;
    items[currentIndex].classList.add('active');
    return currentIndex;
}

if (placeItems.length > 0) {
    placeItems[0].classList.add('active');
}
if (eventItems.length > 0) {
    eventItems[0].classList.add('active');
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