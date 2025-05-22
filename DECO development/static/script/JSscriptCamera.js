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

        capture.addEventListener('click', () => {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
        });

        uploadForm.addEventListener('submit', (e) => {
            e.preventDefault();

            canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'snapshot.jpg');

            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                window.location.href = response.url;
            }
            })
            .catch(err => console.error('Upload failed', err));
            }, 'image/jpeg');
        });