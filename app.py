import multiprocessing
import cv2
import os
import numpy as np
import joblib
import tkinter as tk
from PIL import Image, ImageTk


def show_flipping_card(species_name):
    root = tk.Tk()
    root.withdraw()  # hide the root window

    window = tk.Toplevel()
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)
    window.title(f"{species_name} Card")

    species_key = species_name.lower().replace(' ', '_')
    front_path = f"cards/{species_key}_front.png"
    back_path = "cards/back.png"

    if not os.path.exists(back_path):
        print("❌ Missing default back card image.")
        label = tk.Label(window, text="Card back not found.")
        label.pack()
        window.mainloop()
        return

    back_image = Image.open(back_path).resize((360, 504))

    label = tk.Label(window)
    label.pack()

    flip_steps = 10
    flip_delay = 30  # milliseconds

    def animate_flip(images, step=0):
        if step < len(images):
            label.imgtk = ImageTk.PhotoImage(images[step])
            label.config(image=label.imgtk)
            window.after(flip_delay, lambda: animate_flip(images, step + 1))
        else:
            label.config(image=label.imgtk)

    def flip():
        if front_path and os.path.exists(front_path):
            front_image = Image.open(front_path).resize((360, 504))

            flip_sequence = []
            # Create shrinking back image frames
            for i in range(flip_steps):
                scale = 1 - (i / flip_steps)
                w = max(1, int(360 * scale))
                resized = back_image.resize((w, 504), Image.LANCZOS)
                flip_sequence.append(resized)

            # Create expanding front image frames
            for i in range(flip_steps):
                scale = (i + 1) / flip_steps
                w = max(1, int(360 * scale))
                resized = front_image.resize((w, 504), Image.LANCZOS)
                flip_sequence.append(resized)

            animate_flip(flip_sequence)
        else:
            label.config(text=f"No front image for {species_name}")

    label.imgtk = ImageTk.PhotoImage(back_image)
    label.config(image=label.imgtk)
    window.after(500, flip)
    window.mainloop()


def capture_photo():
    print("🔧 Attempting to access the webcam...")
    camera_indices = [0, 1]
    backends = [cv2.CAP_AVFOUNDATION, cv2.CAP_QT, cv2.CAP_ANY]

    cap = None
    for cam_index in camera_indices:
        for backend in backends:
            print(
                f"🎥 Trying camera index: {cam_index} with backend: {backend}")
            cap = cv2.VideoCapture(cam_index, backend)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    print("✅ Camera opened and frame captured successfully.")
                    break
                else:
                    print("⚠️ Opened but failed to read frame.")
                    cap.release()
                    cap = None
            else:
                print("❌ Camera could not be opened.")
        if cap:
            break
    else:
        print("❌ No usable camera found.")
        return None

    print("📷 Press SPACE to capture an image. Press ESC to cancel.")
    start_time = cv2.getTickCount()
    timeout = 60  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame from camera.")
            break

        # Add instruction overlay
        cv2.putText(frame, "Press SPACE to capture, ESC to cancel",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Auto-capture in 10s...",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow("Press SPACE to capture", frame)
        key = cv2.waitKey(1)

        elapsed_time = (cv2.getTickCount() - start_time) / \
            cv2.getTickFrequency()
        if key % 256 == 27:  # ESC
            print("❌ Capture cancelled.")
            cap.release()
            return None
        elif key % 256 == 32:  # SPACE
            photo_path = "snapshot.jpg"
            cv2.imwrite(photo_path, frame)
            print(f"✅ Photo saved to {photo_path}")
            cap.release()
            return photo_path


# Load model, labels, and scaler
model = joblib.load("fauna_flora_model.pkl")
labels = joblib.load("labels.pkl")
if not os.path.exists("scaler.pkl"):
    raise FileNotFoundError("❌ scaler.pkl not found. Cannot scale features for prediction.")
scaler = joblib.load("scaler.pkl")


def extract_features(img_path):
    img_color = cv2.imread(img_path)
    if img_color is None:
        print(f"❌ Failed to read image: {img_path}")
        return None

    img_color = cv2.resize(img_color, (128, 128))
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.resize(img_gray, (64, 64))

    winSize = (64, 64)
    blockSize = (16, 16)
    blockStride = (8, 8)
    cellSize = (8, 8)
    nbins = 9
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

    h = hog.compute(img_gray).flatten()

    chans = cv2.split(img_color)
    hist_features = []
    for chan in chans:
        hist = cv2.calcHist([chan], [0], None, [16], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        hist_features.extend(hist)

    features = np.concatenate([h, hist_features])
    return features


def recognize_species(img_path):
    features = extract_features(img_path)
    if features is None or features.shape[0] != scaler.mean_.shape[0]:
        print("❌ Invalid feature shape. Skipping prediction.")
        return "Unknown"
    print("🔍 Feature shape:", features.shape)
    print("🔍 Feature sample:", features[:10])
    if scaler:
        features = scaler.transform([features])
    probs = model.predict_proba(features)[0]
    for i, p in enumerate(probs):
        print(f"{labels[i]}: {p:.2f}")
    prediction = np.argmax(probs)
    return labels[prediction]


def run_cli():
    print("📸 Starting photo capture...")
    img_path = capture_photo()
    if img_path is None:
        print("No image captured.")
        return
    print(f"🔍 Image captured at {img_path}")
    species = recognize_species(img_path)
    print(f"Detected: {species}")
    cv2.destroyAllWindows()
    p = multiprocessing.Process(target=show_flipping_card, args=(species,))
    p.start()
    p.join()


from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from multiprocessing import Process

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1>Fauna & Flora Identifier</h1><p>Use POST /predict with an image.</p>"

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    file.save("snapshot.jpg")

    species = recognize_species("snapshot.jpg")

    # ✅ Launch Tkinter flipping card in a separate process
    p = Process(target=show_flipping_card, args=(species,))
    p.start()

    return jsonify({'prediction': species})

if __name__ == "__main__":
    import sys
    if "--web" in sys.argv:
        app.run(debug=True)
    else:
        run_cli()