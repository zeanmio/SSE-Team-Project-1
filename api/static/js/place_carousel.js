// place carousel script
const placeItems = document.querySelectorAll('.place-carousel-item');

let currentPlaceIndex = 0;

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

document.getElementById('place-prev').addEventListener('click', function() {
    currentPlaceIndex = updateCarousel(placeItems, currentPlaceIndex, -1);
    addPlaceMarker();
});

document.getElementById('place-next').addEventListener('click', function() {
    currentPlaceIndex = updateCarousel(placeItems, currentPlaceIndex, 1);
    addPlaceMarker();
});
