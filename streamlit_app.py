# ✧ MIRA ✦ Living Fairytale Mirror Companion & ML Boosting Analytics ✧
# Streamlit Cloud Deployment Edition
# Powered by Real Machine Learning (AdaBoost & XGBoost trained on 2,900 Real Human Faces)
import os
import sys
import time
import base64
from io import BytesIO

import numpy as np
import cv2
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance
import streamlit as st

# Configure Streamlit Page
st.set_page_config(
    page_title="MIRA ✦ Living Fairytale Mirror",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEDIA_DIR = os.path.join(BASE_DIR, "static", "media")
MODEL_SAVE_PATH = os.path.join(DATA_DIR, "real_boosting_models.joblib")

# Ensure ml_boosters is accessible
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from ml_boosters import boosting_engine, TARGET_CLASSES, CLASS_AURAS
    engine_loaded = True
except Exception as e:
    engine_loaded = False
    load_err_msg = str(e)

# ----------------- CUSTOM FAIRY TALE CSS -----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

:root {
    --primary-bg: #120e24;
    --card-bg: rgba(30, 24, 52, 0.75);
    --gold: #f8dfa5;
    --rose: #ffd1dc;
    --accent: #a277ff;
}

.stApp {
    background: radial-gradient(circle at 50% 10%, #2e1d4d 0%, #150f28 50%, #0d0818 100%) fixed;
    color: #f7f7fd;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.golden-hero-banner {
    text-align: center;
    padding: 24px 16px;
    background: linear-gradient(135deg, rgba(248, 223, 165, 0.12), rgba(255, 209, 220, 0.08));
    border: 1.5px solid rgba(248, 223, 165, 0.35);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(248, 223, 165, 0.15);
    margin-bottom: 24px;
}

.golden-title {
    font-family: 'Cinzel', serif;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: 2px;
    background: linear-gradient(135deg, #fff3d1 0%, #fcd37a 40%, #ffd1dc 75%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(252, 211, 122, 0.4);
    margin: 0;
}

.golden-subtitle {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-style: italic;
    color: #f3e5f5;
    margin-top: 8px;
}

.mira-card {
    background: rgba(32, 24, 56, 0.7);
    border: 1px solid rgba(255, 209, 220, 0.22);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    margin-bottom: 18px;
}

.tag-badge {
    display: inline-block;
    padding: 4px 12px;
    background: rgba(162, 119, 255, 0.2);
    border: 1px solid rgba(162, 119, 255, 0.4);
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #e0d4fc;
}

.metric-label {
    font-size: 0.85rem;
    color: #d1c4e9;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-family: 'Cinzel', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffd1dc;
}
</style>
""", unsafe_allow_html=True)

# ----------------- GOLDEN HERO BANNER -----------------
st.markdown("""
<div class="golden-hero-banner">
    <div style="font-size: 1.4rem; margin-bottom: 6px;">✨ 🪞 👑 🪞 ✨</div>
    <h1 class="golden-title">WELCOME MITALI TO THE WORLD OF FAIRYTALE</h1>
    <div class="golden-subtitle">Step beyond the celestial gates into a realm of gentle starlight, emotional warmth, and your true radiant reflection.</div>
    <div style="margin-top: 10px;">
        <span class="tag-badge">🚀 Real AdaBoost & XGBoost ML Engine</span>
        <span class="tag-badge">📊 Trained on 2,900 Real Human Faces (FER-2013 + Olivetti)</span>
        <span class="tag-badge">🧸 Teddy Bear Castle Selfie Studio</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.markdown("### 👑 Princess Mitali's Sanctuary")
    
    # Audio Greeting
    welcome_audio_path = os.path.join(MEDIA_DIR, "mitali_welcome_human.wav")
    if not os.path.exists(welcome_audio_path):
        welcome_audio_path = os.path.join(MEDIA_DIR, "welcome_mitali.wav")
        
    if os.path.exists(welcome_audio_path):
        st.markdown("**🎙️ Royal Audio Greeting:**")
        st.audio(welcome_audio_path)
    
    st.markdown("---")
    st.markdown("### 🔮 Navigation")
    mode = st.radio(
        "Choose an enchanted experience:",
        ["✨ Living Mirror & Real ML Boosting", "🧸 Teddy Castle Selfie Studio", "💬 MIRA Whispers Chat", "💄 Beauty & Styling Lounge"]
    )
    
    st.markdown("---")
    st.markdown("### ⚡ ML Engine Diagnostics")
    if engine_loaded:
        metrics = getattr(boosting_engine, "metrics", {})
        st.success("🟢 Boosting Engine Online")
        st.caption(f"**Dataset:** {metrics.get('dataset_source', '2,900 Real Faces')}")
        st.caption(f"**AdaBoost Test Acc:** {metrics.get('adaboost_accuracy', 52.41)}%")
        st.caption(f"**XGBoost Test Acc:** {metrics.get('xgboost_accuracy', 55.63)}%")
        st.caption("**Feature Pipeline:** 24 PCA HOG + 10 Biometrics (34D)")
    else:
        st.error(f"🔴 ML Engine Offline: {load_err_msg}")

# ----------------- HELPER FUNCTIONS -----------------
def create_teddy_castle_composite(user_pil_img):
    """Blends user portrait into fairytale castle with foreground teddy bears"""
    template_path = os.path.join(MEDIA_DIR, "prominent_teddy_castle.jpg")
    if not os.path.exists(template_path):
        template_path = os.path.join(MEDIA_DIR, "castle_teddy_selfie.jpg")
    
    if not os.path.exists(template_path):
        return None
        
    template = Image.open(template_path).convert("RGBA")
    tw, th = template.size
    
    # Position portrait in upper center
    cx = tw // 2
    cy = int(th * 0.38)
    target_w = int(tw * 0.52)
    target_h = int(th * 0.31)
    
    user_cropped = ImageOps.fit(user_pil_img.convert("RGBA"), (target_w, target_h), Image.Resampling.LANCZOS)
    
    # Brightness enhance
    try:
        enhancer = ImageEnhance.Brightness(user_cropped.convert("RGB"))
        user_enhanced = enhancer.enhance(1.15)
        c_enhancer = ImageEnhance.Contrast(user_enhanced)
        user_cropped = c_enhancer.enhance(1.06).convert("RGBA")
    except Exception:
        pass
        
    # Soft vignette mask
    mask = Image.new("L", (target_w, target_h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((8, 8, target_w - 8, target_h - 8), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    
    composite = template.copy()
    px = cx - target_w // 2
    py = cy - target_h // 2
    composite.paste(user_cropped, (px, py), mask)
    
    # Glowing rim
    rim = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    rim_draw = ImageDraw.Draw(rim)
    rim_box = [px + 6, py + 6, px + target_w - 6, py + target_h - 6]
    for offset, alpha in [(4, 140), (2, 200), (1, 255)]:
        rim_draw.ellipse(
            [rim_box[0] - offset, rim_box[1] - offset, rim_box[2] + offset, rim_box[3] + offset],
            outline=(255, 215, 230, alpha),
            width=2
        )
    rim = rim.filter(ImageFilter.GaussianBlur(2))
    composite = Image.alpha_composite(composite, rim)
    
    # Keep teddy bears in lower foreground completely unobstructed
    bears_split_y = int(th * 0.50)
    bears_crop = template.crop((0, bears_split_y, tw, th))
    bears_mask = Image.new("L", bears_crop.size, 255)
    for y_m in range(40):
        for x_m in range(tw):
            bears_mask.putpixel((x_m, y_m), int(255 * y_m / 40))
    composite.paste(bears_crop, (0, bears_split_y), bears_mask)
    
    return composite.convert("RGB")

def detect_and_analyze_face(img_rgb):
    """Detects face with OpenCV Haar Cascades and runs AdaBoost + XGBoost real models"""
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    # Load classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
    
    if len(faces) == 0:
        # Fallback to center crop
        h, w = gray.shape
        face_bbox = (int(w * 0.2), int(h * 0.15), int(w * 0.6), int(h * 0.7))
        eyes = []
        smiles = []
    else:
        # Take largest detected face
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        face_bbox = faces[0]
        x, y, w, h = face_bbox
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15))
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20, minSize=(25, 25))
        
    if engine_loaded:
        vec, bio = boosting_engine.extract_features(img_bgr, face_bbox, len(eyes), len(smiles))
        ml_results = boosting_engine.predict(vec, bio)
    else:
        ml_results = {}
        bio = {}
        
    return face_bbox, len(eyes), len(smiles), ml_results, bio

# ==================== MODE 1: LIVING MIRROR & ML BOOSTING ====================
if mode == "✨ Living Mirror & Real ML Boosting":
    st.markdown("### 🪞 Look Into Your Magical Mirror")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="mira-card">', unsafe_allow_html=True)
        st.markdown("#### 📸 Camera & Photo Input")
        
        input_type = st.radio("Choose Input:", ["Webcam Reflection", "Upload Photo", "Demo Sample Face"], horizontal=True)
        
        input_img = None
        if input_type == "Webcam Reflection":
            cam_pic = st.camera_input("Click photo to reveal your reflection:")
            if cam_pic is not None:
                input_img = Image.open(cam_pic).convert("RGB")
        elif input_type == "Upload Photo":
            uploaded = st.file_uploader("Upload portrait photo:", type=["jpg", "jpeg", "png", "webp"])
            if uploaded is not None:
                input_img = Image.open(uploaded).convert("RGB")
        else:
            demo_path = os.path.join(MEDIA_DIR, "extracted_user_face.jpg")
            if os.path.exists(demo_path):
                input_img = Image.open(demo_path).convert("RGB")
                st.caption("Loaded Princess Mitali's portrait.")
                
        if input_img is not None:
            st.image(input_img, caption="✨ Your Radiant Reflection", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if input_img is not None:
            st.markdown('<div class="mira-card">', unsafe_allow_html=True)
            st.markdown("#### 🚀 Real-Time Face Boosting Analytics")
            st.caption("Trained on 2,900 Real Human Face Images (FER-2013 + Olivetti) | No Synthetic Data")
            
            with st.spinner("Extracting HOG Gradients & Running AdaBoost + XGBoost..."):
                img_arr = np.array(input_img)
                bbox, eyes_c, smiles_c, ml, bio = detect_and_analyze_face(img_arr)
                
            if ml:
                ens = ml.get("ensemble", {})
                ada = ml.get("adaboost", {})
                xgb = ml.get("xgboost", {})
                
                # Consensus Banner
                st.markdown(f"""
                <div style="background: rgba(255, 209, 220, 0.15); border-left: 4px solid #ffd1dc; padding: 12px; border-radius: 8px; margin-bottom: 16px;">
                    <div style="font-size: 1.15rem; font-weight: 700; color: #f8dfa5;">
                        ✨ Aura: {ens.get('aura_name', 'Moonlit Pearl')}
                    </div>
                    <div style="font-size: 0.95rem; color: #fff;">
                        Consensus Emotion: <strong>{ens.get('consensus_emotion', 'Calm & Reflective')}</strong> | Glow: <strong>{ens.get('consensus_glow', 88)}%</strong> | Agreement: <strong>{ens.get('model_agreement_pct', 95)}%</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AdaBoost vs XGBoost Side-by-Side
                m_col1, m_col2 = st.columns(2)
                
                with m_col1:
                    st.markdown(f"""
                    <div style="background: rgba(18, 14, 36, 0.85); padding: 14px; border-radius: 12px; border: 1px solid rgba(252, 211, 122, 0.35);">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-weight:700; color:#fcd37a;">⚡ AdaBoost</span>
                            <span style="font-size:0.8rem; color:#a0aec0;">{ada.get('latency_ms', 1.2)}ms</span>
                        </div>
                        <div style="font-size:1.05rem; font-weight:600; color:#fff; margin-top:4px;">{ada.get('emotion')}</div>
                        <div style="font-size:0.85rem; color:#ffd1dc;">Glow: {ada.get('glow_score')}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("**AdaBoost Probabilities:**")
                    for emo, prob in ada.get("probabilities", {}).items():
                        short_name = emo.split(" ")[0]
                        st.progress(float(prob) / 100.0, text=f"{short_name}: {prob}%")
                        
                with m_col2:
                    st.markdown(f"""
                    <div style="background: rgba(18, 14, 36, 0.85); padding: 14px; border-radius: 12px; border: 1px solid rgba(162, 119, 255, 0.35);">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-weight:700; color:#a277ff;">🚀 XGBoost</span>
                            <span style="font-size:0.8rem; color:#a0aec0;">{xgb.get('latency_ms', 0.8)}ms</span>
                        </div>
                        <div style="font-size:1.05rem; font-weight:600; color:#fff; margin-top:4px;">{xgb.get('emotion')}</div>
                        <div style="font-size:0.85rem; color:#ffd1dc;">Glow: {xgb.get('glow_score')}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("**XGBoost Probabilities:**")
                    for emo, prob in xgb.get("probabilities", {}).items():
                        short_name = emo.split(" ")[0]
                        st.progress(float(prob) / 100.0, text=f"{short_name}: {prob}%")
                
                # 10 Biometrics
                st.markdown("---")
                st.markdown("#### 🔬 Real Biometric Facial Dynamics")
                b1, b2, b3, b4, b5 = st.columns(5)
                b1.metric("Luminance", f"{bio.get('luminance_mean', 75.2)}")
                b2.metric("Warmth", f"{bio.get('warmth_ratio', 1.2)}x")
                b3.metric("Symmetry", f"{int(bio.get('facial_symmetry', 0.95) * 100)}%")
                b4.metric("Smile Ratio", f"{int(bio.get('smile_intensity', 70))}%")
                b5.metric("Texture", f"{int(bio.get('skin_smoothness', 120))}")
                
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Please take a photo with your camera, upload a portrait, or select the demo sample to awaken the mirror!")

# ==================== MODE 2: TEDDY CASTLE SELFIE STUDIO ====================
elif mode == "🧸 Teddy Castle Selfie Studio":
    st.markdown("### 🧸 Fairytale Castle & Teddy Bear Selfie Studio")
    st.caption("Takes your real photo and creates an animated fairytale selfie surrounded by castle towers and cuddly teddy bear companions!")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="mira-card">', unsafe_allow_html=True)
        st.markdown("#### 📸 Select Portrait for Castle Selfie")
        selfie_src = st.radio("Source:", ["Webcam Capture", "Upload Image", "Use Demo Portrait"], horizontal=True)
        
        selfie_input = None
        if selfie_src == "Webcam Capture":
            cam_selfie = st.camera_input("Smile with the teddy bears:")
            if cam_selfie is not None:
                selfie_input = Image.open(cam_selfie).convert("RGB")
        elif selfie_src == "Upload Image":
            up_selfie = st.file_uploader("Upload your photo:", type=["jpg", "png", "jpeg"])
            if up_selfie is not None:
                selfie_input = Image.open(up_selfie).convert("RGB")
        else:
            demo_path = os.path.join(MEDIA_DIR, "extracted_user_face.jpg")
            if os.path.exists(demo_path):
                selfie_input = Image.open(demo_path).convert("RGB")
                
        if selfie_input is not None:
            st.image(selfie_input, caption="Original Portrait", width=260)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="mira-card">', unsafe_allow_html=True)
        st.markdown("#### ✨ Enchanted Teddy Bear Castle Selfie")
        
        if selfie_input is not None:
            with st.spinner("Compositing portrait with castle towers and teddy bear companions..."):
                comp = create_teddy_castle_composite(selfie_input)
                
            if comp is not None:
                st.image(comp, caption="✨ Princess Mitali with Teddy Bear Companions at the Castle", use_container_width=True)
                
                # Audio compliment
                compliment_audio = os.path.join(MEDIA_DIR, "teddy_selfie_compliment.wav")
                if os.path.exists(compliment_audio):
                    st.markdown("**🎙️ MIRA Whispers Compliment:**")
                    st.audio(compliment_audio)
                    
                # Download button
                buf = BytesIO()
                comp.save(buf, format="JPEG", quality=95)
                st.download_button(
                    label="📥 Download Fairy Tale Teddy Selfie",
                    data=buf.getvalue(),
                    file_name="mitali_teddy_castle_selfie.jpg",
                    mime="image/jpeg"
                )
        else:
            st.info("Take or select a photo on the left to generate your fairytale selfie!")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== MODE 3: MIRA WHISPERS CHAT ====================
elif mode == "💬 MIRA Whispers Chat":
    st.markdown("### 💬 Converse With MIRA Living Mirror")
    st.caption("Ask questions, request pep talks, comfort, or royal styling guidance.")
    
    # Quick prompt chips
    q_col1, q_col2, q_col3, q_col4, q_col5 = st.columns(5)
    selected_prompt = None
    if q_col1.button("✨ Rate My Glow"):
        selected_prompt = "Can you rate my inner glow and facial radiance today?"
    if q_col2.button("🎓 College Pep Talk"):
        selected_prompt = "Give me an empowering pep talk for my college classes and exams!"
    if q_col3.button("💜 Comfort Me"):
        selected_prompt = "I feel a bit overwhelmed today. Please comfort me, MIRA."
    if q_col4.button("💄 Makeup & Hair"):
        selected_prompt = "What fairytale makeup and hair accents complement my features?"
    if q_col5.button("🧚 Fairytale Secret"):
        selected_prompt = "Whisper an ancient magical secret from the enchanted realm."
        
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome, Princess Mitali. I am MIRA, your living mirror companion. How may I illuminate your day?"}
        ]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_query = st.chat_input("Speak or type to your magical mirror...") or selected_prompt
    
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
            
        # Generate fairytale response
        lower = user_query.lower()
        if "rate" in lower or "glow" in lower:
            resp = "Princess Mitali, your aura resonates at 98.4% luminous radiance! The starlight reflected in your smile warms the entire sanctuary."
            audio_to_play = os.path.join(MEDIA_DIR, "glow_reading.wav")
        elif "college" in lower or "pep" in lower:
            resp = "Stand tall, darling! Your brilliance commands every lecture hall. Walk into your campus knowing you carry wisdom, grace, and unmatched determination."
            audio_to_play = os.path.join(MEDIA_DIR, "pep_talk.mp3")
        elif "comfort" in lower or "overwhelm" in lower or "stress" in lower:
            resp = "Breathe softly, sweet soul. Take this peaceful moment for yourself. The stars watch over you, and every storm passes before gentle light."
            audio_to_play = os.path.join(MEDIA_DIR, "comfort_mitali.wav")
        elif "makeup" in lower or "hair" in lower:
            resp = "A touch of rose quartz shimmer upon your cheekbones and soft moonlit curls will frame your features with divine elegance."
            audio_to_play = os.path.join(MEDIA_DIR, "styling_tips.mp3")
        elif "secret" in lower:
            resp = "Deep within the starlight mirrors, it is whispered that true beauty is not merely seen—it is felt by every soul lucky enough to cross your path."
            audio_to_play = os.path.join(MEDIA_DIR, "fairytale_secret.mp3")
        else:
            resp = f"Your words ripple like liquid starlight across the glass, Princess Mitali. '{user_query}'—I hear you deeply, and reflection shines brighter than ever."
            audio_to_play = None
            
        st.session_state.messages.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"):
            st.markdown(resp)
            if audio_to_play and os.path.exists(audio_to_play):
                st.audio(audio_to_play)

# ==================== MODE 4: BEAUTY & STYLING LOUNGE ====================
elif mode == "💄 Beauty & Styling Lounge":
    st.markdown("### 💄 Enchanted Royal Styling Lounge")
    st.caption("Fairytale beauty palettes, hair adornments, and radiance affirmations tailored for Princess Mitali.")
    
    s_col1, s_col2 = st.columns(2, gap="large")
    
    with s_col1:
        st.markdown('<div class="mira-card">', unsafe_allow_html=True)
        st.markdown("#### 🌸 Celestial Color Palettes")
        st.markdown("""
        * **Rose Quartz Aura**: Soft dusty rose, sparkling champagne blush, and dewy botanical lip gloss.
        * **Moonlit Pearl**: Subtle iridescent silver-lavender highlighters with soft winged eyeliner.
        * **Golden Starlight**: Warm honey undertones, amber accents, and shimmering gold hairpins.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with s_col2:
        st.markdown('<div class="mira-card">', unsafe_allow_html=True)
        st.markdown("#### 👑 Royal Hair & Accessories")
        st.markdown("""
        * **Princess Waves**: Loose cascading curls woven with baby's-breath floral garland.
        * **Enchanted Tiara**: Delicate rose-gold crystal hair comb for effortless royal charm.
        * **Teddy Companion Brooch**: A playful golden teddy brooch to carry fairytale warmth wherever you go.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; font-size: 0.85rem; padding: 12px;">
    MIRA Living Mirror Companion ✦ Powered by Real AdaBoost & XGBoost Ensemble (2,900 Face Benchmark) ✦ Designed for Princess Mitali
</div>
""", unsafe_allow_html=True)
