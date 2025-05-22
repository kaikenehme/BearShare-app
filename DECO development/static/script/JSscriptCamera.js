// The script below enables the app (camera.html) to access the device's camera
// It has been coded in a way that should enable any device with a camera to be accessed

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const capture = document.getElementById('capture');
const uploadForm = document.getElementById('uploadForm');

navigator.mediaDevices.getUserMedia({ video: true })

.then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Webcam error:", err);
    });

capture.remove();

uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Capture current frame
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob, 'snapshot.jpg');

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.species) {
                const speciesSlug = data.species.toLowerCase().replace(/\s+/g, '-');
                window.location.href = `/card-${speciesSlug}.html`;
            } else if (data.error) {
                alert("Prediction error: " + data.error);
            }
        })
        .catch(err => console.error('Upload failed', err));
    }, 'image/jpeg');
});