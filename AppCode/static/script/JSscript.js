// The script below runs the image slideshow on the index.html
// It is designed to ensure the images rotate the slideshow as an infinite loop, rather than resetting

document.addEventListener("DOMContentLoaded", function () {
    const slideImages = document.querySelector(".image-slide-images");
    const images = Array.from(slideImages.children);
    const prevButton = document.querySelector(".image-slide-button.back");
    const nextButton = document.querySelector(".image-slide-button.next");
    const activeNavigationItem = document.querySelector(".section-two .section-two-item-active");

    let currentIndex = 0;

    const firstClone = images[0].cloneNode(true);
    const lastClone = images[images.length - 1].cloneNode(true);
    slideImages.appendChild(firstClone);
    slideImages.insertBefore(lastClone, images[0]);

    const allImages = Array.from(slideImages.children);
    const totalImages = allImages.length;
    slideImages.style.transition = "none";
    slideImages.style.transform = `translateX(-100%)`;

    const imageTitles = ["Platypus", "Kangaroo", "Tassie Devil"];

    function updateNavigationText(index) {
        const title = imageTitles[index] || "Preview";
        activeNavigationItem.textContent = title;
    }

    function showImage(index) {
        slideImages.style.transition = "transform 0.5s ease";
        slideImages.style.transform = `translateX(${-100 * (index + 1)}%)`;
        currentIndex = index;
        updateNavigationText(currentIndex);
    }

    function handleTransitionEnd() {
        if (currentIndex === -1) {
            slideImages.style.transition = "none";
            currentIndex = images.length - 1;
            slideImages.style.transform = `translateX(${-100 * (currentIndex + 1)}%)`;
        }
        if (currentIndex === images.length) {
            slideImages.style.transition = "none";
            currentIndex = 0;
            slideImages.style.transform = `translateX(${-100 * (currentIndex + 1)}%)`;
        }
        updateNavigationText(currentIndex);
    }

    slideImages.addEventListener("transitionend", handleTransitionEnd);

    prevButton.addEventListener("click", function () {
        showImage(currentIndex - 1);
    });

    nextButton.addEventListener("click", function () {
        showImage(currentIndex + 1);
    });

    // Swiping Function for smartphones

    let startX = 0;
    let endX = 0;

    slideImages.addEventListener("touchstart", (e) => {
        startX = e.touches[0].clientX;
    });

    slideImages.addEventListener("touchmove", (e) => {
        endX = e.touches[0].clientX;
    });

    slideImages.addEventListener("touchend", () => {
        const swipeDistance = startX - endX;

        if (swipeDistance > 50) {
            showImage(currentIndex + 1);
        } else if (swipeDistance < -50) {
            showImage(currentIndex - 1);
        }

        startX = 0;
        endX = 0;
    });

});