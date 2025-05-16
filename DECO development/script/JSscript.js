document.addEventListener("DOMContentLoaded", function () {
    const carouselImages = document.querySelector(".image-slide-images");
    const images = Array.from(carouselImages.children);
    const prevButton = document.querySelector(".image-slide-button.back");
    const nextButton = document.querySelector(".image-slide-button.next");
    const activeNavigationItem = document.querySelector(".section-two .section-two-item-active");

    let currentIndex = 0;

    // Clone first and last images to create a seamless loop
    const firstClone = images[0].cloneNode(true);
    const lastClone = images[images.length - 1].cloneNode(true);
    carouselImages.appendChild(firstClone);
    carouselImages.insertBefore(lastClone, images[0]);

    // Update the images array after cloning
    const allImages = Array.from(carouselImages.children);
    const totalImages = allImages.length;
    carouselImages.style.transition = "none";
    carouselImages.style.transform = `translateX(-100%)`;

    // Image titles to display in navigation
    const imageTitles = ["Platypus", "Kangaroo", "Tassie Devil"];

    function updateNavigationText(index) {
        const title = imageTitles[index] || "Overview";
        activeNavigationItem.textContent = title;
    }

    function showImage(index) {
        carouselImages.style.transition = "transform 0.5s ease";
        carouselImages.style.transform = `translateX(${-100 * (index + 1)}%)`;
        currentIndex = index;
        updateNavigationText(currentIndex);
    }

    function handleTransitionEnd() {
        if (currentIndex === -1) {
            carouselImages.style.transition = "none";
            currentIndex = images.length - 1;
            carouselImages.style.transform = `translateX(${-100 * (currentIndex + 1)}%)`;
        }
        if (currentIndex === images.length) {
            carouselImages.style.transition = "none";
            currentIndex = 0;
            carouselImages.style.transform = `translateX(${-100 * (currentIndex + 1)}%)`;
        }
        updateNavigationText(currentIndex);
    }
    

    carouselImages.addEventListener("transitionend", handleTransitionEnd);

    prevButton.addEventListener("click", function () {
        showImage(currentIndex - 1);
    });

    nextButton.addEventListener("click", function () {
        showImage(currentIndex + 1);
    });

    // Initialize navigation text
    updateNavigationText(currentIndex);
});

// JSscript.js: Handles image enlargement on click

function toggleImageSize(image) {
    image.classList.toggle("enlarge");
}