# 🐨 BearShare: Fauna & Flora Recognition App

BearShare is an interactive web application that identifies Australian wildlife species using your webcam. It features a collectible card-flip animation for each recognized animal. This project combines machine learning, a custom-trained classifier, and a Flask backend, integrated with an HTML/CSS/JS frontend.

---

## 🚀 How to Set Up the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/BearShare-app.git
cd BearShare-app
```

### 2. Create a Virtual Environment (Python 3.11)

```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧠 How It Works

- A webcam image is captured in the browser.
- The image is sent to a Flask backend via the `/predict` route.
- The backend processes the image and classifies it using a trained Random Forest model (`fauna_flora_model.pkl`).
- Based on the prediction, the user is redirected to a specific HTML page showing a collectible wildlife card, with flip animation.
- For "rare" animals like the Platypus, special effects are shown.

---

## 🧪 Run the App (Locally)

To run the app locally (to access the camera and model integration):

```bash
python app.py --web
```

Then open your browser and visit:

```
http://127.0.0.1:5050
```

---

## 📂 Project Structure

```
BearShare-app/
│
├── app.py                      # Main Flask backend
├── training.py                 # Model training script
├── download_images.py          # Helper script to fetch training images
├── fauna_flora_model.pkl       # Trained model
├── labels.pkl                  # Class label mappings
├── scaler.pkl                  # Feature scaler
├── requirements.txt            # All Python dependencies
├── cards/                      # Card images (front/back)
├── training_data/              # Dataset for training
│
├── AppCode/                    # Frontend HTML/JS/CSS files
│   ├── index.html
│   ├── camera.html
│   ├── script/
│   ├── style.css
│   └── ...
│
├── .venv/                      # Virtual environment (excluded via .gitignore)
```

---

## 🛠️ Notes

- This app requires webcam access. Run locally for full camera integration.
- Ensure your `.venv/` is excluded from GitHub commits.
- Tested with Python 3.11.