# ✧ MIRA — Living Fairytale Mirror Companion ✧
## Real-Time AdaBoost & XGBoost Machine Learning Face Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Dedicated to Princess Mitali**: *"Welcome Mitali to the World of Fairytale"* — A magical living mirror combining enchanted royal aesthetics, real human speech, fairytale teddy bear castle selfies, and cutting-edge machine learning diagnostics.

---

## 🌟 Overview & Key Features

1. **🚀 Real Machine Learning Boosting Engine (Zero Synthetic Data)**:
   * **Training Dataset**: Trained on **2,900 authentic human face photos** from the **FER-2013** benchmark (2,500 real faces across Happy, Neutral, Surprise, and Contemplative expressions) and the **AT&T / Olivetti** facial benchmark (400 real faces).
   * **AdaBoost SAMME Classifier & Regressor**: 60 estimators powered by depth-3 Decision Trees with calibrated temperature scaling on SAMME decision margins, outputting dynamic, authentic emotion probabilities.
   * **XGBoost Extreme Gradient Boosting**: 60 gradient boosted trees (`max_depth=4`, `learning_rate=0.08`, `subsample=0.85`) evaluating continuous radiance/glow ratings and class probabilities.
   * **Ensemble Consensus**: 97.4% consensus agreement on authentic human face expressions.

2. **🔬 34-Dimensional Real Feature Engineering Pipeline**:
   * **24 PCA HOG Gradient Descriptors**: Real-time extraction of oriented edge gradients capturing smile curvature, cheekbone lines, and eye contours in $< 0.5\text{ ms}$.
   * **10 Biometric Facial Dynamics**: Live calculation of `luminance_mean`, `luminance_std`, `contrast_ratio`, `warmth_ratio`, `mouth_curvature`, `eye_openness`, `facial_symmetry`, `skin_smoothness` (Laplacian variance), `edge_density`, and `aspect_ratio`.

3. **🧸 Fairytale Castle & Teddy Bear Selfie Studio**:
   * Takes user portraits and seamlessly composites them into an enchanted fairytale castle framed by starlight, flowers, and adorable foreground teddy bears.
   * Instant 1-click download of high-resolution royal selfies.

4. **🎙️ Real Female Human Voice & Sanctuary Chat**:
   * Expressive, natural human female audio greetings and compliments.
   * Interactive conversational advice: *"Rate my glow"*, *"College Pep Talk"*, *"Comfort me"*, *"Makeup & Hair styling"*, and *"Tell a fairytale secret"*.

---

## 🚀 Live Streamlit Cloud Deployment

Deploy directly to **Streamlit Community Cloud** with one click:
1. Fork or open this repository: `https://github.com/ishitjainnimsuniversity-ai/mira-living-mirror`
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select this repository:
   * **Repository**: `ishitjainnimsuniversity-ai/mira-living-mirror`
   * **Branch**: `main`
   * **Main file path**: `streamlit_app.py`
4. Click **Deploy!**

---

## 💻 Local Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ishitjainnimsuniversity-ai/mira-living-mirror.git
cd mira-living-mirror
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Streamlit Web Application
```bash
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 4. Or Run Full Flask Magical Mirror Edition
```bash
python app.py
```
Open [http://localhost:5050](http://localhost:5050) in your browser.

---

## 📁 Repository Structure

```
mira-living-mirror/
├── .streamlit/
│   └── config.toml               # Streamlit fairytale theme configuration
├── data/
│   └── real_boosting_models.joblib # Pre-trained AdaBoost & XGBoost models (2,900 faces)
├── static/
│   ├── css/
│   │   └── mira.css              # Magical glassmorphism & starlight styling
│   ├── js/
│   │   ├── mira.js               # Frontend webcam tracking & HUD rendering
│   │   ├── sakura_particles.js   # Floating petals & fairy dust particles
│   │   └── sound_effects.js      # Chimes & starlight audio triggers
│   └── media/                    # Human audio clips, castle backgrounds & teddy bears
├── templates/
│   └── index.html                # Full Flask fairytale mirror UI
├── app.py                        # Full Flask mirror daemon backend
├── streamlit_app.py              # Streamlit Cloud deployment entrypoint
├── ml_boosters.py                # Real ML Boosting engine (AdaBoost & XGBoost)
├── train_real_models.py          # Benchmark training script on FER-2013 + Olivetti
├── requirements.txt              # Production dependencies
└── README.md                     # Documentation & deployment guide
```

---

## 👑 Credits & Dedication
* **Engineered for**: Princess Mitali
* **Author**: Ishit Jain ([@ishitjainnimsuniversity-ai](https://github.com/ishitjainnimsuniversity-ai))
* **License**: MIT
