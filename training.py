import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import StandardScaler
import os
import cv2
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from PIL import Image, ImageOps
from PIL import ImageEnhance


def augment_image(img):
    """Returns a list of augmented images (original, flipped, rotated, contrast, blur, brightness)."""
    augmented = []
    img_pil = Image.fromarray(img)

    # Original
    augmented.append(img_pil)

    # Horizontal Flip
    augmented.append(ImageOps.mirror(img_pil))

    # Rotate 90, 180, 270
    for angle in [90, 180, 270]:
        augmented.append(img_pil.rotate(angle))

    # Contrast variations
    contrast_factors = [0.8, 1.2]
    for factor in contrast_factors:
        contrasted = ImageEnhance.Contrast(img_pil).enhance(factor)
        augmented.append(contrasted)

    # Brightness variations
    brightness_factors = [0.7, 1.3]
    for factor in brightness_factors:
        brightened = ImageEnhance.Brightness(img_pil).enhance(factor)
        augmented.append(brightened)

    # Blur (using OpenCV and rewrap in PIL)
    img_cv2 = np.array(img_pil)
    blurred = cv2.GaussianBlur(img_cv2, (5, 5), 0)
    augmented.append(Image.fromarray(blurred))

    return augmented


# Prepare dataset
X = []
y = []
labels = []

base_path = 'training_data'

# Ensure consistent label ordering
label_names = sorted([
    name for name in os.listdir(base_path)
    if os.path.isdir(os.path.join(base_path, name))
])
for i, label in enumerate(label_names):
    labels.append(label)
    folder = os.path.join(base_path, label)
    for img_file in os.listdir(folder):
        if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(folder, img_file)
            img_color = cv2.imread(path)
            if img_color is None:
                print(f"Warning: Could not read {path}")
                os.remove(path)
                continue
            img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (128, 128))
            for aug_img_pil in augment_image(img):
                # Skip if this class already reached cap
                if y.count(i) >= 600:
                    break
                aug_array_gray = cv2.resize(np.array(aug_img_pil), (64, 64))

                # Resize color image separately for histogram
                aug_array_color = cv2.resize(np.array(aug_img_pil.convert('RGB')), (64, 64))

                # HOG descriptor
                hog = cv2.HOGDescriptor((64, 64), (16, 16), (8, 8), (8, 8), 9)
                h = hog.compute(aug_array_gray).flatten()

                # Color histogram (16 bins per channel)
                chans = cv2.split(aug_array_color)
                hist_features = []
                for chan in chans:
                    hist = cv2.calcHist([chan], [0], None, [16], [0, 256])
                    hist = cv2.normalize(hist, hist).flatten()
                    hist_features.extend(hist)

                # Combine HOG + color hist
                features = np.concatenate([h, hist_features])
                X.append(features)
                y.append(i)


X = np.array(X)
y = np.array(y)
scaler = StandardScaler()
X = scaler.fit_transform(X)
joblib.dump(scaler, 'scaler.pkl')

# Count and display the number of augmented images per label

label_counts = Counter(y)
print("\n📊 Augmented image count per class:")
for idx, count in label_counts.items():
    print(f"{labels[idx]}: {count}")

#
# Train classifier
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
clf = ExtraTreesClassifier(n_estimators=100, class_weight='balanced')
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Show prediction probabilities for debugging
proba_samples = clf.predict_proba(X_test[:5])
for i, probs in enumerate(proba_samples):
    print(
        f"Sample {i} - True: {labels[y_test[i]]}, Probabilities: {probs}, Predicted: {labels[np.argmax(probs)]}")

# Save model and labels
joblib.dump(clf, 'fauna_flora_model.pkl')
joblib.dump(labels, 'labels.pkl')

# Visualize misclassified samples
print("\n🔍 Misclassified Samples:")
for i in range(len(y_test)):
    if y_pred[i] != y_test[i]:
        sample = X_test[i]
        # Reverse standardization for visualization (only HOG, not color hist)
        sample_unscaled = scaler.inverse_transform(sample.reshape(1, -1))[0]
        hog_len = 1764  # 64x64 HOG with 9 bins
        hog_feat = sample_unscaled[:hog_len].reshape(-1, 1)

        # Convert HOG back to image (rough visual approximation)
        # We'll just show a blank image with labels instead of trying to recreate original
        plt.figure()
        plt.title(f"True: {labels[y_test[i]]} | Pred: {labels[y_pred[i]]}")
        plt.text(0.5, 0.5, 'Image not available\n(Feature-based model)', fontsize=12,
                 ha='center', va='center', bbox=dict(boxstyle="round", facecolor="wheat"))
        plt.axis('off')
        plt.show()

        # Only show a few for sanity
        if i >= 4:
            break

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(cmap='Blues', xticks_rotation=45)
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

# Optional cleanup: delete misclassified training images (if available)
print("\n🧹 Removing misclassified image files from training_data...")
for i in range(len(y_test)):
    if y_pred[i] != y_test[i]:
        true_label = labels[y_test[i]]
        folder = os.path.join(base_path, true_label)
        # Find original filenames from folder
        for img_file in os.listdir(folder):
            if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                path = os.path.join(folder, img_file)
                img_color = cv2.imread(path)
                if img_color is None:
                    continue
                img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (128, 128))
                # Match feature to sample
                for aug_img_pil in augment_image(img):
                    aug_array_gray = cv2.resize(np.array(aug_img_pil), (64, 64))
                    hog = cv2.HOGDescriptor((64, 64), (16, 16), (8, 8), (8, 8), 9)
                    h = hog.compute(aug_array_gray).flatten()
                    chans = cv2.split(cv2.resize(np.array(aug_img_pil.convert('RGB')), (64, 64)))
                    hist_features = []
                    for chan in chans:
                        hist = cv2.calcHist([chan], [0], None, [16], [0, 256])
                        hist = cv2.normalize(hist, hist).flatten()
                        hist_features.extend(hist)
                    combined = np.concatenate([h, hist_features])
                    scaled = scaler.transform([combined])[0]
                    if np.allclose(scaled, X_test[i], atol=1e-3):
                        print(f"🗑️  Removing {path}")
                        os.remove(path)
                        break
                break

import joblib

# Save final model, scaler, and labels
joblib.dump(clf, "fauna_flora_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(labels, "labels.pkl")
print("✅ Model, scaler, and labels saved successfully.")
 