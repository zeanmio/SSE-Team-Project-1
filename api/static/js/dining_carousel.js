// dining carousel script
const diningItems = document.querySelectorAll('.dining-carousel-item');

let currentDiningIndex = 0;

function updateCarousel(items, currentIndex, direction) {
    items[currentIndex].classList.remove('active');
    const totalItems = items.length;
    currentIndex = (currentIndex + direction + totalItems) % totalItems;
    items[currentIndex].classList.add('active');
    return currentIndex;
}

if (diningItems.length > 0) {
    diningItems[0].classList.add('active');
}

document.getElementById('dining-prev').addEventListener('click', function() {
    currentDiningIndex = updateCarousel(diningItems, currentDiningIndex, -1);
    addDiningMarker();
});

document.getElementById('dining-next').addEventListener('click', function() {
    currentDiningIndex = updateCarousel(diningItems, currentDiningIndex, 1);
    addDiningMarker();
});
