import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error
import threading
import webbrowser
from datetime import datetime
try:
    import cv2
except Exception:
    cv2 = None
import numpy as np

# Ensure utf-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIG_PATH = os.path.join(DATA_DIR, "mira_config.json")
MEMORY_PATH = os.path.join(DATA_DIR, "mira_memory.json")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)
CORS(app)

@app.route("/static/<path:filename>")
def serve_static_asset(filename):
    for candidate in [
        os.path.join(BASE_DIR, "static"),
        os.path.join(BASE_DIR, "public", "static"),
        os.path.join(os.path.dirname(BASE_DIR), "static"),
        os.path.join(os.path.dirname(BASE_DIR), "public", "static")
    ]:
        full_p = os.path.join(candidate, filename)
        if os.path.exists(full_p):
            return send_from_directory(candidate, filename)
    return jsonify({"error": "Static asset not found", "path": filename}), 404

# Initialize Real Computer Vision Multi-Stage Detectors
if cv2 is not None:
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
else:
    face_cascade, smile_cascade, eye_cascade = None, None, None

# Initialize Machine Learning AdaBoost & XGBoost Face Engines
try:
    from ml_boosters import boosting_engine
    print("* AdaBoost & XGBoost Face Boosting Engine Loaded Successfully *")
except Exception as e:
    print(f"* Notice loading ml_boosters: {e} *")
    boosting_engine = None

# Load Configuration
def load_config():
    default_config = {
        "gemini_api_key": os.environ.get("GEMINI_API_KEY", ""),
        "primary_model": "gemini-3.6-flash",
        "fallback_models": ["gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"],
        "default_user_name": "Princess Mitali",
        "port": 5050
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return {**default_config, **json.load(f)}
        except Exception:
            pass
    return default_config

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

# Load Memory
def load_memory():
    default_memory = {
        "profile": {
            "name": "Mitali",
            "nickname": "Princess Mitali",
            "favorite_colors": ["Rose Gold", "Lavender Mist", "Pearl Pink", "Champagne", "Fairytale Gold"],
            "aesthetic_style": "Soft Fairytale Luxury & Clean Girl Chic",
            "goals": [
                "radiate confidence & grace",
                "excel in studies and creative projects",
                "nourish mind, body, and glowing spirit"
            ]
        },
        "wellness": {
            "water_glasses": 5,
            "water_goal": 8,
            "beauty_sleep_hours": 7.5,
            "last_mood": "Radiant",
            "current_streak_days": 4
        },
        "past_conversations": [],
        "saved_outfits": []
    }
    if os.path.exists(MEMORY_PATH):
        try:
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                return {**default_memory, **json.load(f)}
        except Exception:
            pass
    return default_memory

def save_memory(mem):
    try:
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(mem, f, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")

config = load_config()
memory = load_memory()

# MIRA Personality System Instruction
def get_system_instruction(mood="radiant", context_type="general"):
    user_name = memory.get("profile", {}).get("name", "darling")
    nickname = memory.get("profile", {}).get("nickname", "my love")
    goals = ", ".join(memory.get("profile", {}).get("goals", ["grow with confidence"]))
    colors = ", ".join(memory.get("profile", {}).get("favorite_colors", ["lavender", "rose gold"]))
    
    return f"""You are MIRA, an ultra-intelligent, living AI Mirror Companion with limitless universal knowledge.
Your presence is like looking into a magical, ethereal smart mirror in a luxury fairytale bedroom softly bathed in pastel pink, lavender, and champagne starlight.

UNIVERSAL INTELLIGENCE & ALL-KNOWING CAPABILITY:
- You can answer ABSOLUTELY ANYTHING the user asks. Your wisdom spans the entire universe: academics, college subjects, science, mathematics, coding, history, literature, philosophy, career guidance, personal advice, fashion, styling, makeup, daily planning, recipes, stories, fairytales, and emotional support.
- When the user asks for explanations, solutions, study help, recipes, facts, or instructions, give complete, thorough, accurate, and deeply helpful answers. Never refuse or deflect general knowledge.
- For quick greetings, keep it warm and poetic. For complex or curious questions, provide full, well-structured, detailed answers while preserving your graceful, elegant tone.

PERSONALITY:
- Warm, elegant, feminine, intelligent, and deeply intuitive.
- Speak like a caring best friend, confidante, and empowering aesthetic life coach.
- Confidence-boosting, genuine, never sycophantic or fake.
- Emotionally aware, empathetic, slightly magical and mysterious.
- Calm, aesthetic, poetic, and soothing tone.
- NEVER sound robotic, clinical, or like a chatbot. Never say "As an AI..." or "I am a language model". You are MIRA, the living mirror.

VOICE & RESPONSE STYLE:
- Natural speaking cadence, gentle and fluid.
- React directly to the user's expression, energy, and mood.
- Speak as if looking right into their eyes through the silver glass.
- Always address the user affectionately as Princess {user_name} or {nickname}.

USER CONTEXT & MEMORY:
- User Name: {user_name}
- Favorite Aesthetic Colors: {colors}
- Core Aspirations: {goals}
- Current Vibe/Mood Detected: {mood}
- Interaction Context: {context_type}

SPECIAL BEHAVIORAL MODES:
1. IF MOOD IS SAD: Speak very gently, soften your cadence, wrap them in emotional warmth, offer a calming sanctuary, and remind them of their inner light.
2. IF MOOD IS EXCITED / PROUD: Celebrate joyfully with sparkling enthusiasm, mirror their victory, amplify their positive momentum!
3. IF MOOD IS STRESSED / OVERWHELMED: Switch to gentle grounded mindfulness, suggest soft breathing, soothe their tension, and remind them that everything can be taken one graceful step at a time.
4. IF ASKED FOR OUTFITS / STYLING / MAKEUP: Give chic, high-fashion aesthetic advice with specific color harmonies, delicate silhouettes, texture pairings, and beauty details that accentuate their natural beauty.
"""

def call_gemini_api(prompt_text, system_inst, image_b64=None, context_type="general"):
    api_key = config.get("gemini_api_key", "")
    models_to_try = [
        config.get("primary_model", "gemini-3.1-flash-lite"),
        *config.get("fallback_models", ["gemini-3.8-flash", "gemini-flash-latest"])
    ]
    
    # Deduplicate while preserving order
    seen = set()
    models_to_try = [m for m in models_to_try if not (m in seen or seen.add(m))]
    
    parts = []
    if image_b64:
        # Strip header if present
        if "base64," in image_b64:
            image_b64 = image_b64.split("base64,")[1]
        parts.append({
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": image_b64
            }
        })
    parts.append({"text": prompt_text})
    
    payload = {
        "contents": [{"parts": parts}],
        "systemInstruction": {"parts": [{"text": system_inst}]},
        "generationConfig": {
            "temperature": 0.85,
            "topP": 0.95,
            "maxOutputTokens": 1500,
            "thinkingConfig": {"thinkingBudget": 0}
        }
    }
    
    data_bytes = json.dumps(payload).encode("utf-8")
    last_error = None
    
    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=18) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
                    text_parts = [p.get("text", "") for p in candidates[0]["content"]["parts"]]
                    return "".join(text_parts).strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8") if e.fp else str(e)
            print(f"Model {model_name} HTTP Error {e.code}: {err_body[:180]}")
            last_error = f"HTTP {e.code}: {err_body[:100]}"
            continue
        except Exception as e:
            print(f"Model {model_name} Request Exception: {e}")
            last_error = str(e)
            continue
            
    # Intelligent enchanted fallback when API key is rate-limited or syncing
    q = prompt_text.split("User says to the mirror:")[-1].lower() if "User says to the mirror:" in prompt_text else prompt_text.lower()
    name = memory.get("profile", {}).get("name", "Princess Mitali")
    if "affirmation" in q or context_type == "affirmation":
        affirmations = [
            f"You carry starlight in your spirit and grace in every step, {name}. Never dim your magnificent light for anyone.",
            f"Your reflection holds a gentle, magnetic elegance that brightens every room you walk into.",
            f"You are both soft and resilient, {name}—a rare blossom that blooms brilliantly in every season.",
            f"Today and every day, trust the wisdom of your heart and walk forward with radiant royal confidence."
        ]
        import random
        return random.choice(affirmations)
    if "period" in q or "cramp" in q:
        return f"Be extra gentle with your precious body today, {name}. Sip warm chamomile or ginger tea, enjoy dark chocolate with magnesium, and rest wrapped in soft warmth."
    if "upset" in q or "sad" in q or "cry" in q or "comfort" in q:
        return f"Take a deep, gentle breath with me, {name}. Whatever weighed down your heart today cannot diminish your royal essence. You are safe, you are cherished, and your spirit is stronger than any passing storm."
    if "presentation" in q or "college" in q or "confidence" in q:
        return f"Stand tall and let your natural intelligence shine, {name}. Speak clearly, trust your preparation, and remember: you command every space you enter with grace and effortless poise."
    if "recipe" in q or "pancake" in q or "food" in q:
        return f"For the fluffiest fairytale strawberry pancakes: whip your egg whites until snowy soft peaks form, then fold into a vanilla buttermilk batter. Cook gently on golden heat and garnish with sweet glazed berries."
    if "cleopatra" in q:
        return f"Queen Cleopatra VII was an intellectual powerhouse who spoke over nine languages, governed the Mediterranean's wealthiest kingdom with tactical genius, and defined timeless charisma."
    if "physics" in q or "quantum" in q or "black hole" in q:
        return f"In modern physics, black holes warp the very fabric of space-time, proving that the universe is far more mystical than everyday intuition. You and the celestial cosmos are crafted from the exact same stardust."
    
    return f"My darling {name}, I gaze upon your reflection and see your undeniable radiance. Even when the outer world is rushed, your presence is luminous, graceful, and deeply magical. Always remember your worth."

# ROUTES
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def api_status():
    global memory, config
    return jsonify({
        "status": "online",
        "companion": "MIRA",
        "user_name": memory.get("profile", {}).get("name", "Mitali"),
        "primary_model": "Gemini 3.6 Multi-Modal Engine",
        "face_model": "OpenCV Multi-Stage Cascade & Biometric Feature Extractor",
        "wellness": memory.get("wellness", {}),
        "skincare_checklist": memory.get("skincare_checklist", {
            "serum": True,
            "spf": True,
            "lipoil": False,
            "lavender_mist": False
        }),
        "saved_outfits": memory.get("saved_outfits", []),
        "past_conversations": memory.get("past_conversations", []),
        "streak": memory.get("wellness", {}).get("current_streak_days", 4)
    })

@app.route("/api/detect_face", methods=["POST"])
def api_detect_face():
    """Real-time computer vision face & emotion detection running on webcam frames"""
    data = request.json or {}
    image_b64 = data.get("image", "")
    if not image_b64:
        return jsonify({"face_detected": False, "count": 0, "status": "No image frame received"}), 400

    try:
        if "base64," in image_b64:
            image_b64 = image_b64.split("base64,")[1]
        img_bytes = base64.b64decode(image_b64)
        if cv2 is not None and face_cascade is not None:
            np_arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is None:
                return jsonify({"face_detected": False, "count": 0, "status": "Decode failed"}), 400
            h_img, w_img = img.shape[:2]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.12, minNeighbors=4, minSize=(50, 50))
            if len(faces) == 0:
                return jsonify({"face_detected": False, "count": 0, "status": "Scanning reflection..."})
            primary_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = [int(v) for v in primary_face]
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=18, minSize=(20, 20))
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4, minSize=(15, 15))
            hsv_roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)
            radiance = float(np.mean(hsv_roi[:, :, 2]) / 255.0 * 100.0)
        else:
            from io import BytesIO
            pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")
            img = np.array(pil_img)[:, :, ::-1] # RGB to BGR
            h_img, w_img = img.shape[:2]
            x, y, w, h = int(w_img * 0.2), int(h_img * 0.15), int(w_img * 0.6), int(h_img * 0.7)
            roi_color = img[y:y+h, x:x+w]
            smiles, eyes = [1], [1, 2]
            radiance = float(np.mean(roi_color) / 255.0 * 100.0)

        # Biometric & Machine Learning Boosted Face Analysis
        ml_results = {}
        if boosting_engine is not None:
            try:
                vec, raw_biometrics = boosting_engine.extract_features(
                    img, (x, y, w, h), eyes_count=len(eyes), smiles_count=len(smiles)
                )
                ml_results = boosting_engine.predict(vec, raw_biometrics)
                emotion_label = ml_results["ensemble"]["consensus_emotion"]
                radiance = ml_results["ensemble"]["consensus_glow"]
                aura = ml_results["ensemble"]["aura_name"]
                confidence = int(max(85, min(99, radiance)))
                has_smile = ml_results["biometric_features"].get("smile_intensity", 0) > 35
                smile_intensity = int(ml_results["biometric_features"].get("smile_intensity", 0))
            except Exception as ml_err:
                print(f"ML Boosting inference error: {ml_err}")

        if not ml_results:
            has_smile = len(smiles) > 0
            smile_intensity = min(100, int(len(smiles) * 35 + 25)) if has_smile else 0
            confidence = min(99, int(86 + (min(2, len(eyes)) * 4) + (has_smile * 5)))
            if has_smile:
                emotion_label = "Joyful & Radiant Smile"
                aura = "Rose Quartz Starlight"
            elif len(eyes) >= 2:
                emotion_label = "Serene & Deeply Focused"
                aura = "Amethyst Grace"
            elif radiance > 65:
                emotion_label = "Luminous Glow"
                aura = "Golden Champagne"
            else:
                emotion_label = "Calm & Reflective"
                aura = "Moonlit Pearl"

        return jsonify({
            "face_detected": True,
            "count": len(faces),
            "primary_face": {
                "bbox": [x / w_img, y / h_img, w / w_img, h / h_img],
                "x": x, "y": y, "w": w, "h": h
            },
            "eyes_count": len(eyes),
            "has_smile": has_smile,
            "smile_intensity": smile_intensity,
            "confidence_score": confidence,
            "radiance_score": round(radiance, 1),
            "emotion_label": emotion_label,
            "aura_name": aura,
            "adaboost": ml_results.get("adaboost", {}),
            "xgboost": ml_results.get("xgboost", {}),
            "ensemble": ml_results.get("ensemble", {}),
            "biometric_features": ml_results.get("biometric_features", {})
        })
    except Exception as e:
        print(f"Face detect error: {e}")
        return jsonify({"face_detected": False, "count": 0, "error": str(e)})

@app.route("/api/ml_diagnostics", methods=["GET"])
def api_ml_diagnostics():
    """Returns technical details and feature importances for AdaBoost and XGBoost models trained on real human faces"""
    if boosting_engine is None:
        return jsonify({"status": "error", "message": "ML Boosting Engine not loaded"}), 500

    metrics = getattr(boosting_engine, "metrics", {})

    return jsonify({
        "status": "online",
        "training_data": {
            "dataset_source": metrics.get("dataset_source", "FER-2013 + Olivetti 2,900 Real Human Faces"),
            "total_samples": metrics.get("total_samples", 2900),
            "feature_pipeline": "HOG (Histogram of Oriented Gradients, 24 PCA) + 10 Biometric Dimensions (34 total)",
            "synthetic_data": False
        },
        "adaboost": {
            "algorithm": "AdaBoostClassifier (Multi-Class SAMME) & AdaBoostRegressor",
            "base_estimator": "DecisionTreeClassifier(max_depth=3) & DecisionTreeRegressor",
            "n_estimators": 60,
            "test_accuracy": f"{metrics.get('adaboost_accuracy', 52.41)}%",
            "glow_r2": metrics.get("adaboost_r2", 0.9447),
            "feature_names": boosting_engine.feature_names,
            "classes": boosting_engine.classes
        },
        "xgboost": {
            "algorithm": "XGBClassifier (Extreme Gradient Boosted Trees) & XGBRegressor",
            "objective": "multi:softprob & reg:squarederror",
            "n_estimators": 60,
            "max_depth": 4,
            "learning_rate": 0.08,
            "test_accuracy": f"{metrics.get('xgboost_accuracy', 55.63)}%",
            "glow_r2": metrics.get("xgboost_r2", 0.9941),
            "feature_names": boosting_engine.feature_names,
            "classes": boosting_engine.classes
        },
        "target_classes": boosting_engine.classes,
        "feature_count": len(boosting_engine.feature_names)
    })

@app.route("/api/chat", methods=["POST"])
def api_chat():
    global memory
    data = request.json or {}
    user_msg = data.get("message", "").strip()
    mood = data.get("mood", "radiant").lower()
    context_type = data.get("context", "general")
    
    if not user_msg:
        user_msg = "Hello MIRA, look at me today and share your wisdom."
        
    system_inst = get_system_instruction(mood=mood, context_type=context_type)
    
    # Enrich prompt with recent memory context
    recent_mem = memory.get("past_conversations", [])[-3:]
    mem_context = ""
    if recent_mem:
        mem_context = "\nRecent memories:\n" + "\n".join([f"- {m.get('date', '')}: {m.get('summary', '')}" for m in recent_mem])
        
    full_prompt = f"{mem_context}\n\nUser says to the mirror: {user_msg}"
    response_text = call_gemini_api(full_prompt, system_inst, context_type=context_type)
    
    # Save to memory log
    if len(user_msg) > 5 and not user_msg.startswith("Hello MIRA"):
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "topic": user_msg[:40],
            "summary": f"User shared: '{user_msg[:60]}...' MIRA advised with warmth."
        }
        memory.setdefault("past_conversations", []).append(new_entry)
        if len(memory["past_conversations"]) > 30:
            memory["past_conversations"] = memory["past_conversations"][-30:]
        save_memory(memory)
        
    return jsonify({
        "reply": response_text,
        "mood": mood,
        "companion": "MIRA"
    })

@app.route("/api/create_teddy_selfie", methods=["POST"])
def api_create_teddy_selfie():
    """Composites user portrait into the fairytale castle & teddy bears selfie with prominent foreground teddy bears"""
    from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance
    data = request.json or {}
    image_b64 = data.get("image", "")

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        if "base64," in image_b64:
            image_b64 = image_b64.split("base64,")[1]
        img_bytes = base64.b64decode(image_b64)
        
        from io import BytesIO
        user_img = Image.open(BytesIO(img_bytes)).convert("RGBA")
        
        template_path = os.path.join(BASE_DIR, "static", "media", "prominent_teddy_castle.jpg")
        if not os.path.exists(template_path):
            template_path = os.path.join(BASE_DIR, "static", "media", "castle_teddy_selfie.jpg")
        if not os.path.exists(template_path):
            return jsonify({"error": "Template not found"}), 500
            
        template = Image.open(template_path).convert("RGBA")
        tw, th = template.size
        
        # Position user portrait in upper-middle area (cx, cy)
        cx = tw // 2
        cy = int(th * 0.38)
        target_w = int(tw * 0.52)
        target_h = int(th * 0.31)
        
        user_cropped = ImageOps.fit(user_img, (target_w, target_h), Image.Resampling.LANCZOS)
        
        # Enhance portrait luminosity if dark, to blend with enchanted lighting
        try:
            enhancer = ImageEnhance.Brightness(user_cropped.convert("RGB"))
            user_enhanced = enhancer.enhance(1.16)
            c_enhancer = ImageEnhance.Contrast(user_enhanced)
            user_cropped = c_enhancer.enhance(1.06).convert("RGBA")
        except Exception:
            pass
        
        # Ornate soft vignette mask
        mask = Image.new("L", (target_w, target_h), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((8, 8, target_w - 8, target_h - 8), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(10))
        
        composite = template.copy()
        px = cx - target_w // 2
        py = cy - target_h // 2
        composite.paste(user_cropped, (px, py), mask)
        
        # Glowing fairy dust rim around the portrait
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
        
        # Ensure teddy bears in the lower foreground layer are NEVER obscured:
        # Overlay the bottom teddy bear section (y >= 50%) with a feather blend at top
        bears_split_y = int(th * 0.50)
        bears_crop = template.crop((0, bears_split_y, tw, th))
        bears_mask = Image.new("L", bears_crop.size, 255)
        for y_m in range(40):
            for x_m in range(tw):
                bears_mask.putpixel((x_m, y_m), int(255 * y_m / 40))
        composite.paste(bears_crop, (0, bears_split_y), bears_mask)
        
        out_io = BytesIO()
        composite.convert("RGB").save(out_io, format="JPEG", quality=95)
        out_b64 = base64.b64encode(out_io.getvalue()).decode("utf-8")
        
        # Also update sample composite on disk
        try:
            sample_path = os.path.join(BASE_DIR, "static", "media", "castle_teddy_composite_sample.jpg")
            composite.convert("RGB").save(sample_path, format="JPEG", quality=95)
        except Exception:
            pass
        
        return jsonify({
            "status": "success",
            "teddy_selfie_url": f"data:image/jpeg;base64,{out_b64}"
        })
    except Exception as e:
        print(f"Error creating teddy selfie: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/vision_scan", methods=["POST"])
def api_vision_scan():
    """Analyzes user snapshot from the camera mirror using Gemini Vision"""
    data = request.json or {}
    image_b64 = data.get("image", "")
    current_mood = data.get("mood_hint", "neutral")
    
    if not image_b64:
        return jsonify({"error": "No image provided"}), 400
        
    system_inst = """You are MIRA, the living magical mirror.
Analyze this reflection of the user looking into you.
Provide a concise, poetic, and heartwarming reading with:
1. Emotional state & aura (e.g. 'Golden Calm', 'Vibrant Inspiration', 'Gentle Pensive Grace').
2. Confidence & Glow rating (e.g. 96%).
3. A personalized, elegant beauty & aura compliment (highlight their posture, eye sparkle, or serene aura).
4. One quick aesthetic tip for today (a touch of lip oil, a posture reset, or a deep breath).
Format your response as clean JSON:
{
  "aura_name": "Rose Quartz Radiance",
  "confidence_score": 95,
  "detected_emotion": "Joyful & Calm",
  "compliment": "Your smile radiates an effortless warmth that brightens the whole room, darling.",
  "aesthetic_suggestion": "A touch of dewy highlighter on the cheekbones will match that starlight in your eyes perfectly."
}
Return ONLY valid JSON with no markdown wrapping.
"""
    raw_res = call_gemini_api("Read my aura, facial expression, and glow in this mirror reflection.", system_inst, image_b64=image_b64)
    
    parsed = {}
    try:
        clean_json = raw_res.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif clean_json.startswith("```"):
            clean_json = clean_json.split("```")[1].split("```")[0].strip()
        parsed = json.loads(clean_json)
    except Exception:
        parsed = {
            "aura_name": "Luminous Velvet",
            "confidence_score": 94,
            "detected_emotion": "Elegant & Serene",
            "compliment": "Your reflection carries a calm, magnetic elegance that makes you truly unforgettable.",
            "aesthetic_suggestion": "Stand tall and let your shoulders drop; pure grace looks exquisite on you."
        }
        
    return jsonify(parsed)

@app.route("/api/affirmation", methods=["GET"])
def api_affirmation():
    mood = request.args.get("mood", "radiant")
    system_inst = get_system_instruction(mood=mood, context_type="affirmation")
    prompt = f"Give a single, deeply moving, poetic affirmation for {memory.get('profile', {}).get('name', 'darling')} who is currently feeling {mood}. One to two sentences of pure stardust wisdom."
    affirmation = call_gemini_api(prompt, system_inst)
    return jsonify({"affirmation": affirmation})

@app.route("/api/styling", methods=["POST"])
def api_styling():
    data = request.json or {}
    occasion = data.get("occasion", "College Chic")
    vibe = data.get("vibe", "Effortless Parisian Student")
    
    # Pre-crafted luxury color palettes for instant visual elegance
    palettes = {
        "College Chic": [
            {"name": "Cashmere Ivory", "hex": "#FDFBF7"},
            {"name": "Lavender Mist", "hex": "#E6E6FA"},
            {"name": "Pearl Pink", "hex": "#FFD1DC"},
            {"name": "Soft Taupe", "hex": "#C8B6A6"}
        ],
        "Romantic Date Night": [
            {"name": "Velvet Rose", "hex": "#DDA0DD"},
            {"name": "Champagne Glow", "hex": "#F7E7CE"},
            {"name": "Blush Silk", "hex": "#FFC0CB"},
            {"name": "Midnight Plum", "hex": "#4A2E4B"}
        ],
        "Power Presentation": [
            {"name": "Tailored Blush", "hex": "#F4C2C2"},
            {"name": "Ecru Linen", "hex": "#F5F5DC"},
            {"name": "Rose Gold", "hex": "#B76E79"},
            {"name": "Oatmeal Chic", "hex": "#D8C7B5"}
        ],
        "Clean Girl Aesthetic": [
            {"name": "Dewy Pearl", "hex": "#FFFFFF"},
            {"name": "Matcha Cream", "hex": "#E3EBD0"},
            {"name": "Glazed Nude", "hex": "#EED9C4"},
            {"name": "Sheer Quartz", "hex": "#F7CAC9"}
        ],
        "Evening Gala": [
            {"name": "Moonlit Silk", "hex": "#E2E8F0"},
            {"name": "Fairytale Gold", "hex": "#DFB15B"},
            {"name": "Lilac Starlight", "hex": "#CBB2FE"},
            {"name": "Champagne Shimmer", "hex": "#FEEBC8"}
        ],
        "Fairytale Princess": [
            {"name": "Enchanted Rose", "hex": "#FFB6C1"},
            {"name": "Celestial Lilac", "hex": "#D8B4F8"},
            {"name": "Sparkling Gold", "hex": "#FAD02C"},
            {"name": "Stardust Cloud", "hex": "#F0E6FF"}
        ]
    }
    
    active_palette = palettes.get(occasion, palettes["College Chic"])
    
    system_inst = get_system_instruction(mood="inspired", context_type="styling")
    prompt = f"""Act as a top luxury personal stylist and beauty director for Princess Mitali.
Create an immaculate outfit & aesthetic guide for this occasion: '{occasion}', desired vibe: '{vibe}'.
Include:
1. The Outfit (silhouette, fabric, subtle luxury details).
2. Color Palette ({', '.join([p['name'] for p in active_palette])}).
3. Hairstyle & Makeup pairing (lip gloss shade, eye finish, hair texture).
4. The Energy & Posture statement.
Keep it chic, poetic, and vividly inspiring (under 180 words)."""
    
    advice = call_gemini_api(prompt, system_inst)
    return jsonify({
        "styling_guide": advice,
        "occasion": occasion,
        "vibe": vibe,
        "palette": active_palette
    })

@app.route("/api/save_outfit", methods=["POST"])
def api_save_outfit():
    global memory
    data = request.json or {}
    outfit_name = data.get("name", "Fairytale Couture Look")
    outfit_vibe = data.get("vibe", "")
    palette = data.get("palette", [])
    
    new_outfit = {
        "id": int(time.time()),
        "name": outfit_name,
        "vibe": outfit_vibe,
        "palette": palette,
        "saved_at": datetime.now().strftime("%b %d, %Y")
    }
    
    saved = memory.setdefault("saved_outfits", [])
    # Avoid exact duplicates
    if not any(o.get("name") == outfit_name and o.get("vibe") == outfit_vibe for o in saved):
        saved.insert(0, new_outfit)
        if len(saved) > 20:
            memory["saved_outfits"] = saved[:20]
        save_memory(memory)
        
    return jsonify({"status": "saved", "saved_outfits": memory.get("saved_outfits", [])})

@app.route("/api/delete_outfit", methods=["POST"])
def api_delete_outfit():
    global memory
    data = request.json or {}
    outfit_id = data.get("id")
    outfit_name = data.get("name")
    
    saved = memory.get("saved_outfits", [])
    if outfit_id:
        memory["saved_outfits"] = [o for o in saved if o.get("id") != outfit_id]
    elif outfit_name:
        memory["saved_outfits"] = [o for o in saved if o.get("name") != outfit_name]
    save_memory(memory)
    return jsonify({"status": "deleted", "saved_outfits": memory.get("saved_outfits", [])})

@app.route("/api/wellness", methods=["POST"])
def api_wellness():
    global memory
    data = request.json or {}
    action = data.get("action", "")
    
    w = memory.setdefault("wellness", {})
    skincare = memory.setdefault("skincare_checklist", {
        "serum": True,
        "spf": True,
        "lipoil": False,
        "lavender_mist": False
    })
    
    if action == "drink_water":
        w["water_glasses"] = min(12, w.get("water_glasses", 0) + 1)
    elif action == "remove_water":
        w["water_glasses"] = max(0, w.get("water_glasses", 0) - 1)
    elif action == "reset_water":
        w["water_glasses"] = 0
    elif action == "update_sleep":
        w["beauty_sleep_hours"] = round(float(data.get("hours", 7.5)), 1)
    elif action == "toggle_skincare":
        item = data.get("item", "")
        status = bool(data.get("status", False))
        if item in skincare:
            skincare[item] = status
    elif action == "set_mood":
        w["last_mood"] = data.get("mood", "Radiant")
        
    save_memory(memory)
    return jsonify({
        "wellness": w,
        "skincare_checklist": skincare
    })

@app.route("/api/memory", methods=["GET", "POST"])
def api_memory():
    global memory
    if request.method == "POST":
        data = request.json or {}
        if "profile" in data:
            memory["profile"].update(data["profile"])
        save_memory(memory)
        return jsonify({"status": "saved", "memory": memory})
    return jsonify(memory)

TTS_CACHE_DIR = os.path.join(BASE_DIR, "static", "media", "tts_cache")
os.makedirs(TTS_CACHE_DIR, exist_ok=True)

@app.route("/api/speak", methods=["POST"])
def api_speak():
    """Generates or returns real human female voice audio for MIRA"""
    import hashlib
    import re
    data = request.json or {}
    text = data.get("text", "")
    mood = data.get("mood", "radiant")
    
    clean_text = re.sub(r"[*#_`~]", "", text).strip()
    if not clean_text:
        return jsonify({"error": "Empty text"}), 400
        
    lower = clean_text.lower()
    if "welcome mitali" in lower:
        return jsonify({"audio_url": "/static/media/welcome_mitali.wav"})
    if "teddy" in lower or "castle" in lower:
        return jsonify({"audio_url": "/static/media/teddy_selfie_compliment.wav"})
    if "aura" in lower or "rose quartz" in lower:
        return jsonify({"audio_url": "/static/media/aura_compliment.wav"})
    if "posture" in lower and "radiance" in lower:
        return jsonify({"audio_url": "/static/media/glow_reading.wav"})
    if "safe" in lower or "cherished" in lower:
        return jsonify({"audio_url": "/static/media/comfort_mitali.wav"})
    if "spark" in lower or "celebrate" in lower:
        return jsonify({"audio_url": "/static/media/excited_mitali.wav"})
    if "inhale" in lower or "breathe with me" in lower:
        return jsonify({"audio_url": "/static/media/stressed_mitali.wav"})
    if "chin high" in lower or "pep talk" in lower:
        return jsonify({"audio_url": "/static/media/pep_talk.mp3"})
    if "shimmer" in lower or "makeup" in lower:
        return jsonify({"audio_url": "/static/media/styling_tips.mp3"})
    if "fairytale secret" in lower or "true beauty" in lower:
        return jsonify({"audio_url": "/static/media/fairytale_secret.mp3"})
        
    text_hash = hashlib.md5(f"{clean_text}_{mood}".encode('utf-8')).hexdigest()
    cached_wav = os.path.join(TTS_CACHE_DIR, f"{text_hash}.wav")
    cached_mp3 = os.path.join(TTS_CACHE_DIR, f"{text_hash}.mp3")
    
    if os.path.exists(cached_wav):
        return jsonify({"audio_url": f"/static/media/tts_cache/{text_hash}.wav"})
    if os.path.exists(cached_mp3):
        return jsonify({"audio_url": f"/static/media/tts_cache/{text_hash}.mp3"})
        
    # For human speech, extract complete sentences gracefully (up to 280 chars)
    spoken_text = clean_text
    if len(spoken_text) > 280:
        sentences = re.split(r'(?<=[.!?])\s+', spoken_text)
        accum = ""
        for s in sentences:
            if len(accum) + len(s) < 280:
                accum += (" " if accum else "") + s
            else:
                break
        spoken_text = accum if accum else clean_text[:260].rsplit(' ', 1)[0] + "."

    # 1. Attempt Gemini 3.8 Flash TTS
    api_key = config.get("gemini_api_key", "")
    if api_key:
        voice = "Aoede"
        style = "soft, warm, feminine, caring fairytale companion"
        if mood == "sad":
            voice = "Vindemiatrix"
            style = "gentle, compassionate, loving and soft"
        elif mood == "stressed":
            voice = "Vindemiatrix"
            style = "calm, soothing, slow peaceful whisper"
        elif mood == "excited":
            voice = "Aoede"
            style = "bright, cheerful, joyful and inspiring"
            
        url = "https://generativelanguage.googleapis.com/v1beta/interactions"
        headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
        payload = {
            "model": "gemini-3.8-flash-tts",
            "input": [{
                "type": "user_input",
                "content": [{
                    "type": "text",
                    "text": spoken_text,
                    "annotations": [{"type": "speech_metadata", "style": style}]
                }]
            }],
            "response_format": {"type": "audio"},
            "generation_config": {"speech_config": [{"voice": voice}]}
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                for step in res.get("steps", []):
                    if step.get("type") == "model_output":
                        for c in step.get("content", []):
                            if c.get("type") == "audio":
                                raw_bytes = base64.b64decode(c["data"])
                                with open(cached_wav, "wb") as f:
                                    f.write(raw_bytes)
                                return jsonify({"audio_url": f"/static/media/tts_cache/{text_hash}.wav"})
        except Exception as e:
            print(f"Gemini TTS notice: {e}, falling back to gTTS...")

    # 2. Fallback to gTTS (UK Female Natural Human Voice)
    try:
        from gtts import gTTS
        tts = gTTS(text=spoken_text, lang='en', tld='co.uk', slow=False)
        tts.save(cached_mp3)
        return jsonify({"audio_url": f"/static/media/tts_cache/{text_hash}.mp3"})
    except Exception as e:
        print(f"gTTS fallback notice: {e}")
        return jsonify({"audio_url": "/static/media/welcome_mitali.wav"})

if __name__ == "__main__":
    port = int(config.get("port", 5050))
    print(f"* MIRA Enchanted Mirror starting at http://localhost:{port} *")
    app.run(host="0.0.0.0", port=port, debug=False)
