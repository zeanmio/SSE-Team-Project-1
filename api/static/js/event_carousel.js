// event carousel script
const eventItems = document.querySelectorAll('.event-carousel-item');

let currentEventIndex = 0;

function updateCarousel(items, currentIndex, direction) {
    items[currentIndex].classList.remove('active');
    const totalItems = items.length;
    currentIndex = (currentIndex + direction + totalItems) % totalItems;
    items[currentIndex].classList.add('active');
    return currentIndex;
}

if (eventItems.length > 0) {
    eventItems[0].classList.add('active');
}

document.getElementById('event-prev').addEventListener('click', function() {
    currentEventIndex = updateCarousel(eventItems, currentEventIndex, -1);
    addEventMarker();
});

document.getElementById('event-next').addEventListener('click', function() {
    currentEventIndex = updateCarousel(eventItems, currentEventIndex, 1);
    addEventMarker();
});
