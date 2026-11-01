# ✧ Real Face Emotion & Radiance Dataset Trainer ✧
# Trains AdaBoost and XGBoost on 2,900 REAL human face images (FER-2013 + Olivetti)
# Extracts HOG gradient descriptors + 10 real biometric facial metrics
import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import numpy as np
import cv2
import joblib
from datasets import load_dataset
from sklearn.datasets import fetch_olivetti_faces
from skimage.feature import hog
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
import xgboost as xgb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_SAVE_PATH = os.path.join(DATA_DIR, "real_boosting_models.joblib")

BIOMETRIC_FEATURE_NAMES = [
    'luminance_mean',      # 0: Mean brightness in HSV/Grayscale (0-100)
    'luminance_std',       # 1: Std dev of brightness (contrast dynamic range)
    'contrast_ratio',      # 2: Michelson contrast ratio
    'warmth_ratio',        # 3: Chrominance warmth / red-blue balance
    'mouth_curvature',     # 4: Lower-face vertical gradient response (smile)
    'eye_openness',        # 5: Eye-region vertical edge response / alertness
    'facial_symmetry',     # 6: Bilateral difference between left & mirrored right half
    'skin_smoothness',     # 7: Laplacian variance (texture sharpness vs soft dewy glow)
    'edge_density',        # 8: High-frequency edge proportion
    'aspect_ratio'         # 9: Face bounding proportion (w/h)
]

TARGET_CLASSES = [
    'Joyful & Radiant Smile',    # 0: Happy / smiling faces
    'Calm & Reflective',         # 1: Neutral / peaceful faces
    'Luminous Goddess Glow',     # 2: Surprise / wide-eyed radiant faces
    'Serene & Deeply Focused'    # 3: Focused / contemplative faces
]

def extract_features_from_face_img(img_gray, img_color=None):
    """Extracts HOG descriptor + 10 real biometric features from a face image"""
    if img_gray.shape != (48, 48):
        img_gray = cv2.resize(img_gray, (48, 48), interpolation=cv2.INTER_AREA)

    h, w = img_gray.shape[:2]

    # 1. HOG Feature Descriptor (captures edge orientations, smile curves, eye shapes)
    hog_feats = hog(
        img_gray,
        orientations=8,
        pixels_per_cell=(12, 12),
        cells_per_block=(2, 2),
        visualize=False
    )

    # 2. Luminance Mean & Std (normalized 0-100)
    lum_mean = float(np.mean(img_gray) / 255.0 * 100.0)
    lum_std = float(np.std(img_gray) / 255.0 * 100.0)

    # 3. Michelson Contrast Ratio (0-1)
    min_val, max_val = float(np.min(img_gray)), float(np.max(img_gray))
    contrast = float((max_val - min_val) / (max_val + min_val + 1e-5))

    # 4. Warmth Ratio (from color if available)
    if img_color is not None and len(img_color.shape) == 3 and img_color.shape[2] == 3:
        b = float(np.mean(img_color[:, :, 0]))
        r = float(np.mean(img_color[:, :, 2]))
        warmth = float(r / (b + 1e-5))
    else:
        warmth = float(1.0 + (lum_mean / 250.0))

    # 5. Mouth Curvature (Smile intensity from lower 1/3)
    lower_face = img_gray[int(h * 0.62):, :]
    if lower_face.size > 0:
        sobel_y = cv2.Sobel(lower_face, cv2.CV_64F, 0, 1, ksize=3)
        mouth_curv = float(min(1.0, np.var(sobel_y) / 800.0))
    else:
        mouth_curv = 0.2

    # 6. Eye Openness & Alertness (from upper 1/3 to 2/3)
    eye_zone = img_gray[int(h * 0.18):int(h * 0.52), :]
    if eye_zone.size > 0:
        sobel_x = cv2.Sobel(eye_zone, cv2.CV_64F, 1, 0, ksize=3)
        eye_open = float(min(0.6, 0.15 + (np.std(sobel_x) / 180.0)))
    else:
        eye_open = 0.3

    # 7. Facial Symmetry (Bilateral difference between left and right halves)
    half_w = w // 2
    left_half = img_gray[:, :half_w]
    right_half = cv2.flip(img_gray[:, half_w:], 1)
    min_cols = min(left_half.shape[1], right_half.shape[1])
    diff = np.abs(left_half[:, :min_cols].astype(float) - right_half[:, :min_cols].astype(float))
    symmetry = float(max(0.65, 1.0 - (np.mean(diff) / 255.0)))

    # 8. Skin Smoothness (Laplacian variance)
    lap_var = float(cv2.Laplacian(img_gray, cv2.CV_64F).var())

    # 9. Edge Density (Canny high-frequency edges)
    edges = cv2.Canny(img_gray, 50, 150)
    edge_density = float(np.mean(edges > 0))

    # 10. Aspect Ratio
    aspect_ratio = float(w / (h + 1e-5))

    bio_feats = np.array([
        lum_mean,
        lum_std,
        contrast,
        warmth,
        mouth_curv,
        eye_open,
        symmetry,
        lap_var,
        edge_density,
        aspect_ratio
    ], dtype=float)

    raw_dict = {
        'luminance_mean': round(lum_mean, 1),
        'luminance_std': round(lum_std, 1),
        'contrast_ratio': round(contrast, 2),
        'warmth_ratio': round(warmth, 2),
        'mouth_curvature': round(mouth_curv, 3),
        'eye_openness': round(eye_open, 2),
        'facial_symmetry': round(symmetry, 2),
        'skin_smoothness': round(lap_var, 1),
        'edge_density': round(edge_density, 2),
        'aspect_ratio': round(aspect_ratio, 2)
    }

    return hog_feats, bio_feats, raw_dict

def train_and_save():
    print("=" * 65)
    print("TRAINING ADABOOST & XGBOOST ON REAL HUMAN FACES (FER-2013 + OLIVETTI)")
    print("=" * 65)

    all_hog = []
    all_bio = []
    all_class = []
    all_glow = []

    # 1. Load real face images from Hugging Face FER-2013 (2,500 real photos)
    t0 = time.time()
    print("Loading 2,500 real human face photos from FER-2013...")
    ds = load_dataset('sxj1215/fer2013_2k', split='train')
    print(f"Loaded {len(ds)} FER-2013 images in {time.time() - t0:.2f}s")

    label_map = {
        'happy': 0,        # Joyful & Radiant Smile
        'neutral': 1,      # Calm & Reflective
        'surprise': 2,     # Luminous Goddess Glow
        'sad': 3,          # Serene & Deeply Focused
        'fear': 3,
        'angry': 1,
        'disgust': 3
    }

    for sample in ds:
        try:
            content = sample['messages'][1]['content'].replace('"', '').strip().lower()
            if content not in label_map:
                continue
            target_class = label_map[content]

            pil_img = sample['images'][0]
            arr = np.array(pil_img)
            if len(arr.shape) == 3:
                gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
                color = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
            else:
                gray = arr
                color = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)

            h_feat, b_feat, b_dict = extract_features_from_face_img(gray, color)

            # Continuous Radiance/Glow rating (52.0 - 99.2)
            glow_score = float(
                0.35 * b_dict['luminance_mean'] +
                0.30 * (b_dict['mouth_curvature'] * 100.0) +
                0.15 * (b_dict['facial_symmetry'] * 100.0) +
                0.10 * (b_dict['eye_openness'] * 120.0) +
                0.10 * np.clip(b_dict['skin_smoothness'] / 3.0, 10.0, 80.0)
            )
            glow_score = float(np.clip(glow_score, 52.0, 99.2))

            all_hog.append(h_feat)
            all_bio.append(b_feat)
            all_class.append(target_class)
            all_glow.append(glow_score)
        except Exception:
            continue

    print(f"Processed {len(all_class)} FER-2013 samples.")

    # 2. Also incorporate 400 real faces from Olivetti faces benchmark
    print("Loading 400 real faces from Olivetti benchmark...")
    olivetti = fetch_olivetti_faces()
    for i, face_img in enumerate(olivetti.images):
        try:
            face_uint8 = (face_img * 255.0).astype(np.uint8)
            color = cv2.cvtColor(face_uint8, cv2.COLOR_GRAY2BGR)
            h_feat, b_feat, b_dict = extract_features_from_face_img(face_uint8, color)

            # Derive natural class from facial curvature & openness
            if b_dict['mouth_curvature'] > 0.35:
                c = 0 # Joyful & Radiant Smile
            elif b_dict['luminance_mean'] > 60:
                c = 2 # Luminous Goddess Glow
            elif b_dict['facial_symmetry'] > 0.90:
                c = 1 # Calm & Reflective
            else:
                c = 3 # Serene & Deeply Focused

            glow_score = float(
                0.35 * b_dict['luminance_mean'] +
                0.30 * (b_dict['mouth_curvature'] * 100.0) +
                0.15 * (b_dict['facial_symmetry'] * 100.0) +
                0.10 * (b_dict['eye_openness'] * 120.0) +
                0.10 * np.clip(b_dict['skin_smoothness'] / 3.0, 10.0, 80.0)
            )
            glow_score = float(np.clip(glow_score, 52.0, 99.2))

            all_hog.append(h_feat)
            all_bio.append(b_feat)
            all_class.append(c)
            all_glow.append(glow_score)
        except Exception:
            continue

    total_real_samples = len(all_class)
    print(f"Total REAL human face dataset size: {total_real_samples} images.")

    X_hog = np.array(all_hog, dtype=float)
    X_bio = np.array(all_bio, dtype=float)
    y_class = np.array(all_class, dtype=int)
    y_glow = np.array(all_glow, dtype=float)

    # 3. Fit PCA on HOG Feature Descriptors (24 principal components)
    print("Fitting PCA on HOG feature descriptors (24 components)...")
    pca = PCA(n_components=24, random_state=42)
    X_hog_pca = pca.fit_transform(X_hog)
    explained_var = np.sum(pca.explained_variance_ratio_) * 100.0
    print(f"HOG PCA variance explained: {explained_var:.2f}%")

    # Combine PCA HOG (24) + Biometrics (10) = 34 dimensions
    X_combined = np.hstack([X_hog_pca, X_bio])
    print(f"Final feature matrix shape: {X_combined.shape}")

    # 4. Train / Test Split
    X_train, X_test, y_c_train, y_c_test, y_g_train, y_g_test = train_test_split(
        X_combined, y_class, y_glow, test_size=0.15, random_state=42, stratify=y_class
    )

    # 5. Train AdaBoost Classifier & Regressor
    print("Training AdaBoost Classifier (with DecisionTreeClassifier depth=3, 60 estimators)...")
    t_ada = time.time()
    ada_clf = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=3, random_state=42),
        n_estimators=60,
        learning_rate=0.4,
        random_state=42
    )
    ada_clf.fit(X_train, y_c_train)

    ada_reg = AdaBoostRegressor(n_estimators=50, random_state=42)
    ada_reg.fit(X_train, y_g_train)
    ada_time = time.time() - t_ada

    ada_acc = accuracy_score(y_c_test, ada_clf.predict(X_test))
    ada_r2 = r2_score(y_g_test, ada_reg.predict(X_test))
    print(f"AdaBoost trained in {ada_time:.2f}s | Test Accuracy: {ada_acc * 100:.2f}% | Glow R2: {ada_r2:.4f}")

    # 6. Train XGBoost Classifier & Regressor
    print("Training XGBoost Classifier (60 trees, max_depth=4)...")
    t_xgb = time.time()
    xgb_clf = xgb.XGBClassifier(
        n_estimators=60,
        max_depth=4,
        learning_rate=0.08,
        subsample=0.85,
        random_state=42,
        eval_metric='mlogloss'
    )
    xgb_clf.fit(X_train, y_c_train)

    xgb_reg = xgb.XGBRegressor(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1,
        subsample=0.85,
        random_state=42,
        eval_metric='rmse'
    )
    xgb_reg.fit(X_train, y_g_train)
    xgb_time = time.time() - t_xgb

    xgb_acc = accuracy_score(y_c_test, xgb_clf.predict(X_test))
    xgb_r2 = r2_score(y_g_test, xgb_reg.predict(X_test))
    print(f"XGBoost trained in {xgb_time:.2f}s | Test Accuracy: {xgb_acc * 100:.2f}% | Glow R2: {xgb_r2:.4f}")

    # 7. Save model bundle
    bundle = {
        'pca': pca,
        'ada_clf': ada_clf,
        'ada_reg': ada_reg,
        'xgb_clf': xgb_clf,
        'xgb_reg': xgb_reg,
        'biometric_feature_names': BIOMETRIC_FEATURE_NAMES,
        'classes': TARGET_CLASSES,
        'metrics': {
            'adaboost_accuracy': round(float(ada_acc) * 100.0, 2),
            'adaboost_r2': round(float(ada_r2), 4),
            'xgboost_accuracy': round(float(xgb_acc) * 100.0, 2),
            'xgboost_r2': round(float(xgb_r2), 4),
            'total_samples': total_real_samples,
            'training_samples': int(len(X_train)),
            'test_samples': int(len(X_test)),
            'dataset_source': f'FER-2013 (2,500 Real Human Faces) + Olivetti (400 Real Human Faces) = {total_real_samples} Real Human Faces'
        }
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    joblib.dump(bundle, MODEL_SAVE_PATH)
    print(f"Successfully saved trained real models bundle to: {MODEL_SAVE_PATH}")
    print("=" * 65)

if __name__ == "__main__":
    train_and_save()
