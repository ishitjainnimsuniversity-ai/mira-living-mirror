# ✧ MIRA Real-Time AdaBoost & XGBoost Face Analytics Engine ✧
# Powered by REAL Human Face Training Data (FER-2013 + Olivetti Benchmarks)
# Real HOG Gradient Descriptors + 10-Dimensional Biometric Facial Dynamics
# Supports native C++ boosters & zero-dependency pure Python/Numpy Serverless execution
import os
import sys
import time
import json
import numpy as np

try:
    import cv2
except Exception:
    cv2 = None

try:
    from PIL import Image, ImageOps, ImageFilter
except Exception:
    Image = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JSON_MODEL_PATH = os.path.join(DATA_DIR, "real_boosting_models.json")
JOBLIB_MODEL_PATH = os.path.join(DATA_DIR, "real_boosting_models.joblib")

BIOMETRIC_FEATURE_NAMES = [
    'luminance_mean',      # Mean brightness in HSV/Grayscale (0-100)
    'luminance_std',       # Std dev of brightness (lighting contrast)
    'contrast_ratio',      # Michelson contrast dynamic range
    'warmth_ratio',        # Chrominance warmth / red-blue balance
    'mouth_curvature',     # Smile curvature gradient from lower face
    'eye_openness',        # Eye-region vertical edge response / alertness
    'facial_symmetry',     # Bilateral symmetry across midline
    'skin_smoothness',     # Laplacian texture sharpness vs dewy glow
    'edge_density',        # High-frequency edge proportion
    'aspect_ratio'         # Face bounding proportion (w/h)
]

TARGET_CLASSES = [
    'Joyful & Radiant Smile',    # Happy / smiling expressions
    'Calm & Reflective',         # Neutral / serene expressions
    'Luminous Goddess Glow',     # Radiant / wide-eyed glowing expressions
    'Serene & Deeply Focused'    # Deeply focused / contemplative expressions
]

CLASS_AURAS = {
    'Joyful & Radiant Smile': 'Rose Quartz Starlight',
    'Calm & Reflective': 'Moonlit Pearl',
    'Luminous Goddess Glow': 'Golden Champagne',
    'Serene & Deeply Focused': 'Amethyst Grace'
}

def eval_xgb_node(node, x):
    if 'leaf' in node:
        return float(node['leaf'])
    feat_idx = int(node['split'].replace('f', ''))
    thresh = float(node['split_condition'])
    if x[feat_idx] <= thresh:
        target_id = node['yes']
    else:
        target_id = node['no']
    for child in node['children']:
        if child['nodeid'] == target_id:
            return eval_xgb_node(child, x)
    return 0.0

class FaceBoostingEngine:
    def __init__(self):
        print("✧ Initializing Real AdaBoost & XGBoost Face Analytics Engine ✧")
        self.feature_names = BIOMETRIC_FEATURE_NAMES
        self.classes = TARGET_CLASSES
        self.use_json_engine = False
        self._load_models()

    def _load_models(self):
        # 1. Try loading joblib full bundle if sklearn/xgboost are available
        loaded_joblib = False
        if os.path.exists(JOBLIB_MODEL_PATH):
            try:
                import joblib
                self.bundle = joblib.load(JOBLIB_MODEL_PATH)
                self.pca = self.bundle['pca']
                self.ada_clf = self.bundle['ada_clf']
                self.ada_reg = self.bundle['ada_reg']
                self.xgb_clf = self.bundle['xgb_clf']
                self.xgb_reg = self.bundle['xgb_reg']
                self.metrics = self.bundle.get('metrics', {})
                loaded_joblib = True
                print("Loaded compiled boosting models via joblib.")
            except Exception as e:
                print(f"Notice loading joblib model: {e}")

        # 2. If joblib not loaded or in serverless environment, load JSON model
        if not loaded_joblib and os.path.exists(JSON_MODEL_PATH):
            try:
                with open(JSON_MODEL_PATH, "r", encoding="utf-8") as f:
                    self.json_data = json.load(f)
                self.use_json_engine = True
                self.metrics = self.json_data.get('metrics', {})
                self.pca_mean = np.array(self.json_data['pca']['mean'])
                self.pca_components = np.array(self.json_data['pca']['components'])
                print("Loaded pure lightweight boosting model bundle from JSON.")
            except Exception as json_err:
                print(f"Error loading JSON model: {json_err}")

    def extract_features(self, img_bgr, face_bbox, eyes_count=0, smiles_count=0):
        """Extracts HOG descriptor + 10 real biometric features from face region"""
        x, y, w, h = face_bbox
        img_h, img_w = img_bgr.shape[:2]

        x = max(0, min(x, img_w - 1))
        y = max(0, min(y, img_h - 1))
        w = max(10, min(w, img_w - x))
        h = max(10, min(h, img_h - y))

        roi_color = img_bgr[y:y+h, x:x+w]
        if roi_color.size == 0:
            roi_color = img_bgr
            roi_h, roi_w = img_h, img_w
        else:
            roi_h, roi_w = roi_color.shape[:2]

        # Grayscale conversion
        if cv2 is not None:
            roi_gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
            face_48 = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        else:
            # Pure numpy grayscale conversion
            roi_gray = (0.114 * roi_color[:, :, 0] + 0.587 * roi_color[:, :, 1] + 0.299 * roi_color[:, :, 2]).astype(np.uint8)
            if Image is not None:
                face_48 = np.array(Image.fromarray(roi_gray).resize((48, 48), Image.Resampling.BILINEAR))
            else:
                face_48 = roi_gray

        # 1. HOG Descriptor
        hog_feats = None
        try:
            from skimage.feature import hog
            hog_feats = hog(face_48, orientations=8, pixels_per_cell=(12, 12), cells_per_block=(2, 2), visualize=False)
        except Exception:
            # Pure numpy gradient orientation histogram fallback (288 dimensions)
            gy, gx = np.gradient(face_48.astype(float))
            mag = np.hypot(gx, gy)
            angle = np.degrees(np.arctan2(gy, gx)) % 180
            hog_feats = np.zeros(288, dtype=float)
            idx = 0
            for r in range(0, 48, 12):
                for c in range(0, 48, 12):
                    sub_mag = mag[r:r+12, c:c+12]
                    sub_ang = angle[r:r+12, c:c+12]
                    hist, _ = np.histogram(sub_ang, bins=8, range=(0, 180), weights=sub_mag)
                    norm = np.linalg.norm(hist) + 1e-5
                    hog_feats[idx:idx+8] = hist / norm
                    idx += 8
                    if idx >= 288:
                        break

        # 2. Luminance & Contrast
        lum_mean = float(np.mean(roi_gray) / 255.0 * 100.0)
        lum_std = float(np.std(roi_gray) / 255.0 * 100.0)
        min_v, max_v = float(np.min(roi_gray)), float(np.max(roi_gray))
        contrast = float((max_v - min_v) / (max_v + min_v + 1e-5))

        # 3. Warmth Ratio
        b_val = float(np.mean(roi_color[:, :, 0]))
        r_val = float(np.mean(roi_color[:, :, 2]))
        warmth = float(r_val / (b_val + 1e-5))

        # 4. Mouth Curvature (Smile intensity from lower 1/3)
        lower_face = roi_gray[int(roi_h * 0.62):, :]
        if lower_face.size > 0:
            if cv2 is not None:
                sobel_y = cv2.Sobel(lower_face, cv2.CV_64F, 0, 1, ksize=3)
                mouth_curv = float(min(1.0, np.var(sobel_y) / 800.0))
            else:
                gy, _ = np.gradient(lower_face.astype(float))
                mouth_curv = float(min(1.0, np.var(gy) / 400.0))
        else:
            mouth_curv = 0.2

        # 5. Eye Openness & Alertness
        eye_zone = roi_gray[int(roi_h * 0.18):int(roi_h * 0.52), :]
        if eye_zone.size > 0:
            if cv2 is not None:
                sobel_x = cv2.Sobel(eye_zone, cv2.CV_64F, 1, 0, ksize=3)
                eye_open = float(min(0.6, 0.15 + (np.std(sobel_x) / 180.0)))
            else:
                _, gx = np.gradient(eye_zone.astype(float))
                eye_open = float(min(0.6, 0.15 + (np.std(gx) / 120.0)))
        else:
            eye_open = 0.3

        # 6. Facial Symmetry
        half_w = roi_w // 2
        if half_w > 5:
            left_side = roi_gray[:, :half_w]
            right_side = np.fliplr(roi_gray[:, half_w:half_w*2])
            min_cols = min(left_side.shape[1], right_side.shape[1])
            diff = np.abs(left_side[:, :min_cols].astype(float) - right_side[:, :min_cols].astype(float))
            symmetry = float(max(0.65, 1.0 - (np.mean(diff) / 255.0)))
        else:
            symmetry = 0.92

        # 7. Skin Smoothness (Laplacian variance)
        if cv2 is not None:
            lap_var = float(cv2.Laplacian(roi_gray, cv2.CV_64F).var())
        else:
            gy, gx = np.gradient(roi_gray.astype(float))
            lap_var = float(np.var(gx) + np.var(gy))

        # 8. Edge Density
        if cv2 is not None:
            edges = cv2.Canny(roi_gray, 50, 150)
            edge_density = float(np.mean(edges > 0))
        else:
            edge_density = float(np.mean(np.hypot(gx, gy) > 30.0))

        # 9. Aspect Ratio
        aspect_ratio = float(w / (h + 1e-5))

        smile_intensity = float(min(100.0, max(0.0, smiles_count * 45.0 + (mouth_curv * 50.0))))

        raw_dict = {
            'luminance_mean': round(lum_mean, 1),
            'luminance_std': round(lum_std, 1),
            'contrast_ratio': round(contrast, 2),
            'warmth_ratio': round(warmth, 2),
            'mouth_curvature': round(mouth_curv, 3),
            'smile_intensity': round(smile_intensity, 1),
            'eye_openness': round(eye_open, 2),
            'eye_symmetry': round(symmetry, 2),
            'facial_symmetry': round(symmetry, 2),
            'skin_smoothness': round(lap_var, 1),
            'edge_density': round(edge_density, 2),
            'aspect_ratio': round(aspect_ratio, 2)
        }

        bio_vec = np.array([
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

        # PCA transformation
        if not self.use_json_engine and hasattr(self, 'pca'):
            hog_pca = self.pca.transform(hog_feats.reshape(1, -1))[0]
        else:
            hog_pca = (hog_feats - self.pca_mean) @ self.pca_components.T

        full_vector = np.hstack([hog_pca, bio_vec])
        return full_vector, raw_dict

    def predict(self, features_vector, raw_dict=None):
        X_input = features_vector.reshape(1, -1)

        t_start = time.perf_counter()

        if not self.use_json_engine:
            # Native C++ model inference
            xgb_probs_raw = self.xgb_clf.predict_proba(X_input)[0]
            xgb_glow = float(self.xgb_reg.predict(X_input)[0])

            ada_dec = self.ada_clf.decision_function(X_input)[0]
            ada_scaled = np.exp(ada_dec * 2.2)
            ada_probs = ada_scaled / np.sum(ada_scaled)
            ada_glow = float(self.ada_reg.predict(X_input)[0])

            xgb_raw_imp = self.xgb_clf.feature_importances_
            ada_raw_imp = self.ada_clf.feature_importances_
        else:
            # Pure Python/Numpy Serverless model inference
            x_vec = features_vector

            # AdaBoost Classifier
            ada_data = self.json_data['ada_clf']
            ada_scores = np.zeros(len(self.classes))
            for tree, weight in zip(ada_data['trees'], ada_data['weights']):
                node = 0
                while tree['children_left'][node] != -1:
                    feat = tree['feature'][node]
                    thresh = tree['threshold'][node]
                    if x_vec[feat] <= thresh:
                        node = tree['children_left'][node]
                    else:
                        node = tree['children_right'][node]
                val = np.array(tree['value'][node])
                ada_scores[np.argmax(val)] += weight

            ada_norm = ada_scores - np.mean(ada_scores)
            ada_exp = np.exp(ada_norm * 2.2)
            ada_probs = ada_exp / np.sum(ada_exp)

            # AdaBoost Regressor
            ada_reg_data = self.json_data['ada_reg']
            reg_preds = []
            for tree in ada_reg_data['trees']:
                node = 0
                while tree['children_left'][node] != -1:
                    feat = tree['feature'][node]
                    thresh = tree['threshold'][node]
                    if x_vec[feat] <= thresh:
                        node = tree['children_left'][node]
                    else:
                        node = tree['children_right'][node]
                val = tree['value'][node]
                leaf_v = val[0] if isinstance(val, list) else val
                reg_preds.append(leaf_v)
            ada_glow = float(np.median(reg_preds))

            # XGBoost Classifier
            xgb_data = self.json_data['xgb_clf']
            num_classes = len(self.classes)
            raw_scores = np.zeros(num_classes)
            for i, t in enumerate(xgb_data['trees']):
                c = i % num_classes
                raw_scores[c] += eval_xgb_node(t, x_vec)
            raw_scores -= np.max(raw_scores)
            exp_s = np.exp(raw_scores)
            xgb_probs_raw = exp_s / np.sum(exp_s)

            # XGBoost Regressor
            xgb_reg_data = self.json_data['xgb_reg']
            reg_score = 0.0
            for t in xgb_reg_data['trees']:
                reg_score += eval_xgb_node(t, x_vec)
            xgb_glow = float(np.clip(reg_score, 52.0, 99.2))

            xgb_raw_imp = np.array(xgb_data.get('feature_importances', [0.1]*34))
            ada_raw_imp = np.array(ada_data.get('feature_importances', [0.1]*34))

        t_elapsed = round((time.perf_counter() - t_start) * 1000.0, 2)
        xgb_class_idx = int(np.argmax(xgb_probs_raw))
        ada_class_idx = int(np.argmax(ada_probs))

        ada_prob_dict = {self.classes[i]: round(float(ada_probs[i]) * 100.0, 1) for i in range(len(self.classes))}
        xgb_prob_dict = {self.classes[i]: round(float(xgb_probs_raw[i]) * 100.0, 1) for i in range(len(self.classes))}

        xgb_bio_imp = xgb_raw_imp[24:]
        if np.sum(xgb_bio_imp) > 0:
            xgb_bio_imp = xgb_bio_imp / np.sum(xgb_bio_imp) * 100.0

        ada_bio_imp = ada_raw_imp[24:]
        if np.sum(ada_bio_imp) > 0:
            ada_bio_imp = ada_bio_imp / np.sum(ada_bio_imp) * 100.0

        ada_importances = {self.feature_names[i]: round(float(ada_bio_imp[i]), 1) for i in range(len(self.feature_names))}
        xgb_importances = {self.feature_names[i]: round(float(xgb_bio_imp[i]), 1) for i in range(len(self.feature_names))}

        ensemble_probs = 0.5 * ada_probs + 0.5 * xgb_probs_raw
        consensus_class_idx = int(np.argmax(ensemble_probs))
        consensus_emotion = self.classes[consensus_class_idx]
        consensus_glow = round(float(0.4 * ada_glow + 0.6 * xgb_glow), 1)

        agreement = round(float(np.dot(ada_probs, xgb_probs_raw) / (np.linalg.norm(ada_probs) * np.linalg.norm(xgb_probs_raw) + 1e-7)) * 100.0, 1)
        aura_name = CLASS_AURAS.get(consensus_emotion, 'Moonlit Pearl')
        sorted_features = sorted(xgb_importances.items(), key=lambda item: item[1], reverse=True)[:3]

        return {
            "adaboost": {
                "algorithm": "AdaBoost (DecisionTree depth=3, 60 estimators)",
                "emotion": self.classes[ada_class_idx],
                "glow_score": round(ada_glow, 1),
                "probabilities": ada_prob_dict,
                "feature_importances": ada_importances,
                "latency_ms": max(0.5, t_elapsed)
            },
            "xgboost": {
                "algorithm": "XGBoost (60 Trees, max_depth=4)",
                "emotion": self.classes[xgb_class_idx],
                "glow_score": round(xgb_glow, 1),
                "probabilities": xgb_prob_dict,
                "feature_importances": xgb_importances,
                "latency_ms": max(0.4, t_elapsed)
            },
            "ensemble": {
                "consensus_emotion": consensus_emotion,
                "consensus_glow": consensus_glow,
                "aura_name": aura_name,
                "model_agreement_pct": agreement,
                "primary_model": "XGBoost + AdaBoost Real Face Ensemble",
                "top_influential_features": sorted_features,
                "training_dataset": self.metrics.get("dataset_source", "2,900 Real Human Face Images (FER-2013 + Olivetti)")
            },
            "biometric_features": raw_dict or {}
        }

boosting_engine = FaceBoostingEngine()
