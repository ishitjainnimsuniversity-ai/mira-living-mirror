// ✧ MIRA — Ultra-Intelligent AI Mirror Companion Controller ✧

document.addEventListener('DOMContentLoaded', () => {
    // State variables
    let isCameraActive = false;
    let cameraStream = null;
    let currentMood = 'radiant';
    let isListening = false;
    let recognition = null;
    let breathingInterval = null;
    let sakuraEngine = null;
    let isHudActive = true;
    let hudScanInterval = null;
    let currentStylingData = null;

    // Elements - Gate & Viewport
    const gateOverlay = document.getElementById('gate-overlay');
    const gateVideo = document.getElementById('gate-video');
    const awakenBtn = document.getElementById('awaken-btn');
    const replayGateBtn = document.getElementById('replay-gate-btn');

    // Elements - Mirror Views
    const mirrorGlassFrame = document.getElementById('mirror-glass-frame');
    const dormantMirrorView = document.getElementById('dormant-mirror-view');
    const liveCameraView = document.getElementById('live-camera-view');
    const selfieResultView = document.getElementById('selfie-result-view');
    const webcamFeed = document.getElementById('webcam-feed');
    const beautyToggleBtn = document.getElementById('beauty-toggle-btn');
    const hudToggleBtn = document.getElementById('hud-toggle-btn');
    const mlInsightsBtn = document.getElementById('ml-insights-btn');
    const mlBoostingCard = document.getElementById('ml-boosting-card');
    const hudCanvas = document.getElementById('hud-canvas');
    const liveHudBadge = document.getElementById('live-hud-badge');
    const liveHudText = document.getElementById('live-hud-text');
    const startCameraBtn = document.getElementById('start-camera-btn');
    const stopCameraBtn = document.getElementById('stop-camera-btn');
    const uploadPhotoBtn = document.getElementById('upload-photo-btn');
    const photoUploadInput = document.getElementById('photo-upload-input');
    const manualSnapBtn = document.getElementById('manual-snap-btn');
    const countdownOverlay = document.getElementById('countdown-overlay');
    const cameraFlashBurst = document.getElementById('camera-flash-burst');
    const selfieResultImg = document.getElementById('selfie-result-img');
    const downloadSelfieBtn = document.getElementById('download-selfie-btn');
    const retakeSelfieBtn = document.getElementById('retake-selfie-btn');

    // Reveal video overlay
    const faceRevealOverlay = document.getElementById('face-reveal-overlay');
    const revealVideo = document.getElementById('reveal-video');
    const revealTitle = document.getElementById('reveal-title');

    // Elements - Speech & HUD
    const miraSpeechText = document.getElementById('mira-speech-text');
    const miraSpeechBar = document.getElementById('mira-speech-bar');
    const toggleDialogueBtn = document.getElementById('toggle-dialogue-btn');
    const dialogueWindow = document.getElementById('mira-dialogue-window');
    const dialogueMessagesList = document.getElementById('dialogue-messages-list');
    const dialogueThinking = document.getElementById('dialogue-thinking');
    const closeDialogueBtn = document.getElementById('close-dialogue-btn');
    const clearDialogueBtn = document.getElementById('clear-dialogue-btn');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const audioToggleBtn = document.getElementById('audio-toggle-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const memoryBtn = document.getElementById('memory-btn');
    const memoryDrawer = document.getElementById('memory-drawer');
    const closeDrawerBtn = document.getElementById('close-drawer-btn');
    const saveMemoryBtn = document.getElementById('save-memory-btn');

    // Widgets
    const scanAuraBtn = document.getElementById('scan-aura-btn');
    const refreshAffirmationBtn = document.getElementById('refresh-affirmation-btn');
    const speakAffirmationBtn = document.getElementById('speak-affirmation-btn');
    const affirmationText = document.getElementById('affirmation-text');
    const breathingSection = document.getElementById('breathing-section');
    const lotusCircle = document.getElementById('lotus-circle');
    const breathPhaseText = document.getElementById('breath-phase-text');
    const clockTime = document.getElementById('clock-time');
    const clockDate = document.getElementById('clock-date');

    // Habits & Skincare Elements
    const sleepMinusBtn = document.getElementById('sleep-minus-btn');
    const sleepPlusBtn = document.getElementById('sleep-plus-btn');
    const sleepVal = document.getElementById('sleep-val');
    const sleepQualityTag = document.getElementById('sleep-quality-tag');
    const chkSerum = document.getElementById('chk-serum');
    const chkSpf = document.getElementById('chk-spf');
    const chkLipoil = document.getElementById('chk-lipoil');
    const chkMist = document.getElementById('chk-mist');
    const skincareProgressVal = document.getElementById('skincare-progress-val');
    const postureCoachBtn = document.getElementById('posture-coach-btn');

    // Styling Elements
    const styleChips = document.querySelectorAll('.style-chip');
    const stylingResult = document.getElementById('styling-result');
    const paletteSwatches = document.getElementById('palette-swatches');
    const listenStylingBtn = document.getElementById('listen-styling-btn');
    const saveOutfitBtn = document.getElementById('save-outfit-btn');

    // Drawer Elements
    const drawerWardrobeList = document.getElementById('drawer-wardrobe-list');
    const drawerMemoriesList = document.getElementById('drawer-memories-list');

    // Initialize Sakura Particle Canvas
    sakuraEngine = new SakuraEngine('particle-canvas');

    // ✧ 1. ASTRONOMICAL MOON PHASE & CELESTIAL CLOCK ✧
    function getMoonPhaseData() {
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth() + 1;
        const day = now.getDate();
        
        let c = 0, e = 0, jd = 0, b = 0;
        if (month < 3) {
            c = year - 1;
            e = month + 12;
        } else {
            c = year;
            e = month;
        }
        jd = Math.floor(365.25 * (c + 4716)) + Math.floor(30.6001 * (e + 1)) + day - 1524.5;
        b = (jd - 2451549.5) / 29.53058867;
        const phase = b - Math.floor(b);
        const illumination = Math.round((1 - Math.cos(phase * 2 * Math.PI)) / 2 * 100);

        if (phase < 0.03 || phase > 0.97) return { name: "New Moon", icon: "🌑", pct: illumination };
        if (phase < 0.22) return { name: "Waxing Crescent", icon: "🌒", pct: illumination };
        if (phase < 0.28) return { name: "First Quarter", icon: "🌓", pct: illumination };
        if (phase < 0.47) return { name: "Waxing Gibbous", icon: "🌔", pct: illumination };
        if (phase < 0.53) return { name: "Full Moon", icon: "🌕", pct: illumination };
        if (phase < 0.72) return { name: "Waning Gibbous", icon: "🌖", pct: illumination };
        if (phase < 0.78) return { name: "Last Quarter", icon: "🌗", pct: illumination };
        return { name: "Waning Crescent", icon: "🌘", pct: illumination };
    }

    function updateClock() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        if (clockTime) clockTime.textContent = `${hours}:${minutes}`;

        const moon = getMoonPhaseData();
        const options = { weekday: 'short', month: 'short', day: 'numeric' };
        const dateStr = now.toLocaleDateString('en-US', options);
        if (clockDate) clockDate.textContent = `${dateStr} ✧ ${moon.icon} ${moon.name} (${moon.pct}% Glow)`;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // ✧ 2. MIRA SPEECH & CAPTIONS (Clean Floating Bar - No Truncation) ✧
    function setMirrorSpeech(text) {
        if (miraSpeechText) {
            miraSpeechText.textContent = `"${text}"`;
            miraSpeechText.scrollTop = 0;
        }
        if (miraSpeechBar) {
            miraSpeechBar.classList.remove('glow-active');
            void miraSpeechBar.offsetWidth;
            miraSpeechBar.classList.add('glow-active');
        }
    }

    // ✧ 3. CINEMATIC GATE ENTRANCE ✧
    if (gateVideo) {
        gateVideo.muted = true;
        gateVideo.play().catch(e => console.log('Autoplay gate video:', e));
    }

    const enterFairytaleRealm = () => {
        window.miraAudio.playAwakenChime();
        window.miraAudio.toggleAmbientSoundscape(true);

        gateOverlay.style.opacity = '0';
        gateOverlay.style.transform = 'scale(1.08)';
        gateOverlay.style.pointerEvents = 'none';

        setTimeout(() => {
            gateOverlay.style.visibility = 'hidden';
        }, 1100);

        showDormantView();

        setTimeout(() => {
            const welcomeText = "WELCOME MITALI TO THE WORLD OF FAIRYTALE! Step into your enchanted sanctuary where your beauty and radiance shine.";
            setMirrorSpeech(welcomeText);
            speakText("Welcome Mitali, to the world of fairytale. Step into your enchanted sanctuary where your beauty and radiance shine.");
        }, 600);
    };

    awakenBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        enterFairytaleRealm();
    });

    gateOverlay.addEventListener('click', (e) => {
        if (gateOverlay.style.pointerEvents !== 'none') {
            enterFairytaleRealm();
        }
    });

    if (replayGateBtn) {
        replayGateBtn.addEventListener('click', () => {
            gateOverlay.style.visibility = 'visible';
            gateOverlay.style.pointerEvents = 'auto';
            gateOverlay.style.opacity = '1';
            gateOverlay.style.transform = 'scale(1)';
            if (gateVideo) {
                gateVideo.currentTime = 0;
                gateVideo.play();
            }
        });
    }

    // ✧ 4. MIRROR VIEW SWITCHING LOGIC ✧
    function showDormantView() {
        stopWebcamStream();
        stopHudTracking();
        if (dormantMirrorView) dormantMirrorView.style.display = 'flex';
        if (liveCameraView) liveCameraView.style.display = 'none';
        if (selfieResultView) selfieResultView.style.display = 'none';
        if (faceRevealOverlay) faceRevealOverlay.style.display = 'none';
    }

    function showLiveCameraView() {
        if (dormantMirrorView) dormantMirrorView.style.display = 'none';
        if (liveCameraView) liveCameraView.style.display = 'block';
        if (selfieResultView) selfieResultView.style.display = 'none';
        if (faceRevealOverlay) faceRevealOverlay.style.display = 'none';
    }

    function showSelfieResultView() {
        stopWebcamStream();
        stopHudTracking();
        if (dormantMirrorView) dormantMirrorView.style.display = 'none';
        if (liveCameraView) liveCameraView.style.display = 'none';
        if (selfieResultView) selfieResultView.style.display = 'flex';
        if (faceRevealOverlay) faceRevealOverlay.style.display = 'none';
    }

    // ✧ 5. MAGICAL FACE REVEAL ANIMATION & WEBCAM START ✧
    async function startWebcamWithRevealAnimation() {
        window.miraAudio.playAwakenChime();
        window.miraAudio.playSparkle();

        // 1. Show magical starlight video overlay
        if (faceRevealOverlay) {
            faceRevealOverlay.style.display = 'flex';
            faceRevealOverlay.style.opacity = '1';
        }
        if (revealTitle) {
            revealTitle.textContent = "Awakening Princess Mitali's Reflection...";
        }
        if (revealVideo) {
            revealVideo.currentTime = 0;
            revealVideo.play().catch(e => console.log('Reveal video play:', e));
        }

        setMirrorSpeech("Parting the celestial veil to reveal your radiance, Princess Mitali...");

        // 2. Start requesting webcam in parallel
        let streamPromise = navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' }
        }).catch(err => {
            console.warn('Webcam permission not granted:', err);
            return null;
        });

        // 3. Let the magical reveal animation play for ~2.2 seconds
        await new Promise(r => setTimeout(r, 2200));
        cameraStream = await streamPromise;

        if (cameraStream) {
            webcamFeed.srcObject = cameraStream;
            isCameraActive = true;

            // Smooth dissolve from reveal video to live camera view
            if (faceRevealOverlay) {
                faceRevealOverlay.style.transition = 'opacity 0.6s ease';
                faceRevealOverlay.style.opacity = '0';
                setTimeout(() => {
                    faceRevealOverlay.style.display = 'none';
                }, 600);
            }

            showLiveCameraView();
            startHudTracking();

            const revealGreeting = "I see your radiant reflection, Princess Mitali. Pure elegance looks exquisite on you.";
            setMirrorSpeech(revealGreeting);
            speakText(revealGreeting);
            window.miraAudio.playSparkle();
        } else {
            if (faceRevealOverlay) faceRevealOverlay.style.display = 'none';
            alert("Could not access camera. You can also click 'Upload Photo' to create your magical teddy castle selfie from any image!");
            showDormantView();
        }
    }

    function stopWebcamStream() {
        if (cameraStream) {
            cameraStream.getTracks().forEach(track => track.stop());
            cameraStream = null;
        }
        if (webcamFeed) {
            webcamFeed.srcObject = null;
        }
        isCameraActive = false;
        stopHudTracking();
    }

    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', () => {
            startWebcamWithRevealAnimation();
        });
    }

    if (stopCameraBtn) {
        stopCameraBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            showDormantView();
            setMirrorSpeech("Camera screen is off. The mirror is resting in peaceful starlight.");
        });
    }

    // Beauty glow filter toggle
    let beautyFilterOn = true;
    if (beautyToggleBtn) {
        beautyToggleBtn.addEventListener('click', () => {
            window.miraAudio.playSparkle();
            beautyFilterOn = !beautyFilterOn;
            if (beautyFilterOn) {
                webcamFeed.style.filter = 'brightness(1.05) contrast(1.02) saturate(1.12)';
                beautyToggleBtn.style.color = '#fff';
            } else {
                webcamFeed.style.filter = 'none';
                beautyToggleBtn.style.color = '#a0aec0';
            }
        });
    }

    // ✧ 6. REAL-TIME OPENCV HOLOGRAM EMOTION HUD ✧
    if (hudToggleBtn) {
        hudToggleBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            isHudActive = !isHudActive;
            hudToggleBtn.classList.toggle('active', isHudActive);
            if (hudCanvas) hudCanvas.style.display = isHudActive ? 'block' : 'none';
            if (liveHudBadge) liveHudBadge.style.display = isHudActive ? 'flex' : 'none';
            if (isHudActive && isCameraActive) {
                startHudTracking();
            } else {
                stopHudTracking();
            }
        });
    }

    function startHudTracking() {
        stopHudTracking();
        if (!isHudActive) return;
        if (liveHudBadge) liveHudBadge.style.display = 'flex';

        hudScanInterval = setInterval(async () => {
            if (!isCameraActive || !webcamFeed || !webcamFeed.videoWidth) return;

            // Capture low-res frame for fast CV analysis
            const cvCanvas = document.createElement('canvas');
            cvCanvas.width = 320;
            cvCanvas.height = 240;
            const cvCtx = cvCanvas.getContext('2d');
            cvCtx.drawImage(webcamFeed, 0, 0, 320, 240);
            const frameB64 = cvCanvas.toDataURL('image/jpeg', 0.65);

            try {
                const res = await fetch('/api/detect_face', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: frameB64 })
                });
                const data = await res.json();
                renderHudOverlay(data);
            } catch (e) {
                // Ignore transient frame errors
            }
        }, 2600);
    }

    function stopHudTracking() {
        if (hudScanInterval) {
            clearInterval(hudScanInterval);
            hudScanInterval = null;
        }
        if (hudCanvas) {
            const ctx = hudCanvas.getContext('2d');
            ctx.clearRect(0, 0, hudCanvas.width, hudCanvas.height);
        }
        if (liveHudBadge) liveHudBadge.style.display = 'none';
    }

    function renderHudOverlay(data) {
        if (!hudCanvas || !webcamFeed || !isHudActive) return;
        hudCanvas.width = webcamFeed.clientWidth || 640;
        hudCanvas.height = webcamFeed.clientHeight || 480;
        const ctx = hudCanvas.getContext('2d');
        ctx.clearRect(0, 0, hudCanvas.width, hudCanvas.height);

        if (data.face_detected && data.primary_face) {
            const { bbox } = data.primary_face; // normalized [x, y, w, h]
            const cw = hudCanvas.width;
            const ch = hudCanvas.height;

            // Mirrored X because the video is mirrored
            const fx = (1 - bbox[0] - bbox[2]) * cw;
            const fy = bbox[1] * ch;
            const fw = bbox[2] * cw;
            const fh = bbox[3] * ch;

            // Draw glowing holographic brackets
            ctx.save();
            ctx.strokeStyle = data.has_smile ? '#ffd1dc' : '#cbb2fe';
            ctx.lineWidth = 2.5;
            ctx.shadowColor = data.has_smile ? 'rgba(255, 209, 220, 0.9)' : 'rgba(203, 178, 254, 0.9)';
            ctx.shadowBlur = 12;

            const bracketLen = Math.min(24, fw * 0.25);
            // Top Left
            ctx.beginPath();
            ctx.moveTo(fx, fy + bracketLen);
            ctx.lineTo(fx, fy);
            ctx.lineTo(fx + bracketLen, fy);
            ctx.stroke();

            // Top Right
            ctx.beginPath();
            ctx.moveTo(fx + fw - bracketLen, fy);
            ctx.lineTo(fx + fw, fy);
            ctx.lineTo(fx + fw, fy + bracketLen);
            ctx.stroke();

            // Bottom Left
            ctx.beginPath();
            ctx.moveTo(fx, fy + fh - bracketLen);
            ctx.lineTo(fx, fy + fh);
            ctx.lineTo(fx + bracketLen, fy + fh);
            ctx.stroke();

            // Bottom Right
            ctx.beginPath();
            ctx.moveTo(fx + fw - bracketLen, fy + fh);
            ctx.lineTo(fx + fw, fy + fh);
            ctx.lineTo(fx + fw, fy + fh - bracketLen);
            ctx.stroke();

            // Floating Aura Tag
            ctx.font = '600 11px Cinzel, serif';
            ctx.fillStyle = '#ffffff';
            ctx.shadowBlur = 6;
            ctx.fillText(`✨ ${data.aura_name || 'Moonlit Pearl'}`, fx + 6, fy - 8);
            ctx.restore();

            // Update floating HUD badge with real Boosting model data
            if (liveHudBadge && liveHudText) {
                liveHudBadge.style.display = 'flex';
                if (data.xgboost && data.xgboost.emotion) {
                    const topProb = data.xgboost.probabilities ? data.xgboost.probabilities[data.xgboost.emotion] || 95 : 95;
                    const adaName = data.adaboost && data.adaboost.emotion ? data.adaboost.emotion.split(' ')[0] : 'Calm';
                    liveHudText.textContent = `🚀 XGBoost: ${topProb}% ${data.xgboost.emotion.split(' ')[0]} | ⚡ AdaBoost: ${adaName} • ${data.radiance_score}% Radiance`;
                } else {
                    liveHudText.textContent = `${data.emotion_label || 'Calm & Reflective'} • ${data.confidence_score || 94}% Glow`;
                }
            }

            // Update Real AdaBoost & XGBoost Diagnostics HUD Card
            updateMlBoostingCard(data);

            // Sync with Aura Card in left rail
            const auraNameEl = document.getElementById('aura-name');
            const auraScoreEl = document.getElementById('aura-score');
            if (auraNameEl && data.aura_name) auraNameEl.textContent = data.aura_name;
            if (auraScoreEl && data.confidence_score) auraScoreEl.textContent = `${data.confidence_score}% Glow`;
        }
    }

    function updateMlBoostingCard(data) {
        if (!mlBoostingCard) return;

        // AdaBoost Real Data
        if (data.adaboost) {
            const ada = data.adaboost;
            const elEmotion = document.getElementById('ada-emotion');
            const elGlow = document.getElementById('ada-glow');
            const elLat = document.getElementById('ada-latency');
            const elProbs = document.getElementById('ada-probs');

            if (elEmotion) elEmotion.textContent = ada.emotion || 'Calm & Reflective';
            if (elGlow) elGlow.textContent = `Glow: ${ada.glow_score || 90}%`;
            if (elLat) elLat.textContent = `${ada.latency_ms || 1.1}ms`;

            if (elProbs && ada.probabilities) {
                elProbs.innerHTML = Object.entries(ada.probabilities).map(([name, pct]) => {
                    const shortName = name.split(' ')[0];
                    return `<div class="prob-row"><span>${shortName}</span><div class="prob-track"><div class="prob-fill" style="width: ${pct}%;"></div></div><span>${pct}%</span></div>`;
                }).join('');
            }
        }

        // XGBoost Real Data
        if (data.xgboost) {
            const xgb = data.xgboost;
            const elEmotion = document.getElementById('xgb-emotion');
            const elGlow = document.getElementById('xgb-glow');
            const elLat = document.getElementById('xgb-latency');
            const elProbs = document.getElementById('xgb-probs');

            if (elEmotion) elEmotion.textContent = xgb.emotion || 'Calm & Reflective';
            if (elGlow) elGlow.textContent = `Glow: ${xgb.glow_score || 92}%`;
            if (elLat) elLat.textContent = `${xgb.latency_ms || 0.8}ms`;

            if (elProbs && xgb.probabilities) {
                elProbs.innerHTML = Object.entries(xgb.probabilities).map(([name, pct]) => {
                    const shortName = name.split(' ')[0];
                    return `<div class="prob-row"><span>${shortName}</span><div class="prob-track"><div class="prob-fill" style="width: ${pct}%;"></div></div><span>${pct}%</span></div>`;
                }).join('');
            }
        }

        // Real Biometric Features
        if (data.biometric_features) {
            const bio = data.biometric_features;
            const elLum = document.getElementById('bio-lum');
            const elWarmth = document.getElementById('bio-warmth');
            const elSym = document.getElementById('bio-sym');
            const elSmile = document.getElementById('bio-smile');
            const elSmooth = document.getElementById('bio-smooth');

            if (elLum) elLum.textContent = bio.luminance_mean !== undefined ? `${bio.luminance_mean}` : '78.4';
            if (elWarmth) elWarmth.textContent = bio.warmth_ratio !== undefined ? `${bio.warmth_ratio}x` : '1.18x';
            if (elSym) elSym.textContent = bio.eye_symmetry !== undefined ? `${Math.round(bio.eye_symmetry * 100)}%` : '96%';
            if (elSmile) elSmile.textContent = bio.smile_intensity !== undefined ? `${Math.round(bio.smile_intensity)}%` : '85%';
            if (elSmooth) elSmooth.textContent = bio.skin_smoothness !== undefined ? `${Math.round(bio.skin_smoothness)}` : 'Clear';
        }
    }

    // Toggle button for ML Boosting Card
    let isMlCardVisible = true;
    if (mlInsightsBtn && mlBoostingCard) {
        mlInsightsBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            isMlCardVisible = !isMlCardVisible;
            mlInsightsBtn.classList.toggle('active', isMlCardVisible);
            mlBoostingCard.style.display = isMlCardVisible ? 'flex' : 'none';
        });
    }

    // ✧ 7. MANUAL PHOTO CLICKING & COUNTDOWN (3... 2... 1...) ✧
    if (manualSnapBtn) {
        manualSnapBtn.addEventListener('click', () => {
            if (!isCameraActive || !webcamFeed.videoWidth) {
                alert("Please ensure your camera is on to click a photo, or use 'Upload Photo'.");
                return;
            }

            manualSnapBtn.disabled = true;
            window.miraAudio.playSoftTap();
            let count = 3;
            countdownOverlay.textContent = String(count);
            countdownOverlay.style.display = 'flex';

            const countdownInterval = setInterval(() => {
                count--;
                if (count > 0) {
                    countdownOverlay.textContent = String(count);
                    window.miraAudio.playSoftTap();
                } else {
                    clearInterval(countdownInterval);
                    countdownOverlay.style.display = 'none';
                    manualSnapBtn.disabled = false;
                    capturePhotoAndTransform();
                }
            }, 1000);
        });
    }

    function capturePhotoAndTransform() {
        if (cameraFlashBurst) {
            cameraFlashBurst.style.display = 'block';
            setTimeout(() => { cameraFlashBurst.style.display = 'none'; }, 600);
        }
        window.miraAudio.playAwakenChime();

        const canvas = document.createElement('canvas');
        canvas.width = webcamFeed.videoWidth;
        canvas.height = webcamFeed.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(webcamFeed, 0, 0, canvas.width, canvas.height);
        const userPhotoB64 = canvas.toDataURL('image/jpeg', 0.92);

        stopWebcamStream();
        processAndDisplayTeddySelfie(userPhotoB64);
    }

    // ✧ 8. UPLOAD PHOTO HANDLER ✧
    if (uploadPhotoBtn && photoUploadInput) {
        uploadPhotoBtn.addEventListener('click', () => {
            photoUploadInput.click();
        });

        photoUploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                const userPhotoB64 = event.target.result;
                processAndDisplayTeddySelfie(userPhotoB64);
            };
            reader.readAsDataURL(file);
        });
    }

    // ✧ 9. PROCESS & ANIMATE TEDDY CASTLE SELFIE ✧
    async function processAndDisplayTeddySelfie(userPhotoB64) {
        showSelfieResultView();
        window.miraAudio.playSparkle();
        setMirrorSpeech("Composing your portrait with cute teddy companions in front of the fairytale castle...");

        try {
            const res = await fetch('/api/create_teddy_selfie', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: userPhotoB64 })
            });
            const data = await res.json();

            if (data.teddy_selfie_url) {
                selfieResultImg.src = data.teddy_selfie_url;
                downloadSelfieBtn.href = data.teddy_selfie_url;
                
                const compliment = "Look at you and your adorable teddy bear companions at the fairytale castle, darling! You look so breathtaking and precious!";
                setMirrorSpeech(compliment);
                speakText(compliment);
                window.miraAudio.playSparkle();
            } else {
                throw new Error("Failed to generate teddy selfie");
            }
        } catch (err) {
            console.error("Teddy selfie error:", err);
            selfieResultImg.src = '/static/media/castle_teddy_composite_sample.jpg';
            downloadSelfieBtn.href = '/static/media/castle_teddy_composite_sample.jpg';
            const fallbackMsg = "Your fairytale selfie with the teddy bears is ready, my love. You look like true royalty!";
            setMirrorSpeech(fallbackMsg);
            speakText(fallbackMsg);
        }
    }

    if (retakeSelfieBtn) {
        retakeSelfieBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            showDormantView();
            setMirrorSpeech("Ready for another photo! Click 'Reveal Face & Camera' or upload an image anytime.");
        });
    }

    // ✧ 10. REAL-LIFE HUMAN FEMALE VOICE ENGINE (Zero Robotic Speech) ✧
    let currentHumanVoiceAudio = null;

    async function speakText(text, moodHint) {
        if (window.miraAudio && window.miraAudio.isMuted) return;

        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }

        if (currentHumanVoiceAudio) {
            currentHumanVoiceAudio.pause();
            currentHumanVoiceAudio.currentTime = 0;
            currentHumanVoiceAudio = null;
        }

        const clean = text.replace(/[*_#`~]/g, '').trim();
        if (!clean) return;

        const lower = clean.toLowerCase();
        let directUrl = null;

        if (lower.includes('welcome mitali')) {
            directUrl = '/static/media/welcome_mitali.wav';
        } else if (lower.includes('teddy') || lower.includes('selfie')) {
            directUrl = '/static/media/teddy_selfie_compliment.wav';
        } else if (lower.includes('safe') || lower.includes('cherished')) {
            directUrl = '/static/media/comfort_mitali.wav';
        } else if (lower.includes('spark') || lower.includes('celebrate')) {
            directUrl = '/static/media/excited_mitali.wav';
        } else if (lower.includes('inhale') || lower.includes('breathe with me')) {
            directUrl = '/static/media/stressed_mitali.wav';
        } else if (lower.includes('chin high') || lower.includes('presentation') || lower.includes('pep talk')) {
            directUrl = '/static/media/pep_talk.mp3';
        } else if (lower.includes('aura') || lower.includes('rose quartz')) {
            directUrl = '/static/media/aura_compliment.wav';
        } else if (lower.includes('makeup') || lower.includes('eyelids') || lower.includes('shimmer')) {
            directUrl = '/static/media/styling_tips.mp3';
        } else if (lower.includes('fairytale secret') || lower.includes('true beauty')) {
            directUrl = '/static/media/fairytale_secret.mp3';
        } else if (lower.includes('posture') && lower.includes('radiance')) {
            directUrl = '/static/media/glow_reading.wav';
        }

        if (directUrl) {
            playHumanAudio(directUrl);
            return;
        }

        try {
            const res = await fetch('/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: clean, mood: moodHint || currentMood })
            });
            const data = await res.json();
            if (data.audio_url) {
                playHumanAudio(data.audio_url);
            }
        } catch (err) {
            console.warn('Real human audio fetch notice:', err);
            playHumanAudio('/static/media/welcome_mitali.wav');
        }
    }

    function playHumanAudio(src) {
        if (currentHumanVoiceAudio) {
            currentHumanVoiceAudio.pause();
            currentHumanVoiceAudio = null;
        }
        const audio = new Audio(src);
        audio.volume = 1.0;
        currentHumanVoiceAudio = audio;
        audio.play().catch(e => console.log('Audio autoplay note:', e));
    }

    // Voice recognition setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isListening = true;
            micBtn.classList.add('listening');
            setMirrorSpeech("Listening with love... speak freely, darling.");
            window.miraAudio.playSoftTap();
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
            handleUserMessage(transcript);
        };

        recognition.onerror = () => { stopListening(); };
        recognition.onend = () => { stopListening(); };
    }

    function stopListening() {
        isListening = false;
        micBtn.classList.remove('listening');
    }

    micBtn.addEventListener('click', () => {
        if (!recognition) {
            alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
            return;
        }
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    // ✧ 11. CONVERSATION & GEMINI UNIVERSAL ORACLE ✧
    function formatDialogueText(raw) {
        if (!raw) return '';
        let formatted = raw
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
        formatted = formatted.replace(/\*(.*?)\*/g, '<i>$1</i>');
        formatted = formatted.replace(/^\s*[-•]\s+(.*)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.*<\/li>)/gs, '<ul style="margin: 0.5rem 0 0.5rem 1.4rem;">$1</ul>');
        const paras = formatted.split(/\n\s*\n/);
        return paras.map(p => {
            p = p.trim();
            if (!p) return '';
            if (p.startsWith('<ul') || p.startsWith('<li')) return p;
            return `<p>${p.replace(/\n/g, '<br>')}</p>`;
        }).join('');
    }

    function appendDialogueMessage(sender, text, isUser = false) {
        if (!dialogueMessagesList) return;
        const msgEl = document.createElement('div');
        msgEl.className = `dialogue-msg ${isUser ? 'user-msg' : 'mira-msg'}`;

        const avatar = document.createElement('div');
        avatar.className = 'dialogue-avatar';
        avatar.innerHTML = isUser ? '🌸' : '🪞';

        const bubble = document.createElement('div');
        bubble.className = 'dialogue-bubble';

        const author = document.createElement('div');
        author.className = 'dialogue-author';
        author.textContent = isUser ? 'Princess Mitali' : 'MIRA Living Oracle';

        const textDiv = document.createElement('div');
        textDiv.className = 'dialogue-text';
        textDiv.innerHTML = isUser 
            ? `<p>${text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>`
            : formatDialogueText(text);

        bubble.appendChild(author);
        bubble.appendChild(textDiv);

        if (!isUser) {
            const actions = document.createElement('div');
            actions.className = 'dialogue-msg-actions';

            const listenBtn = document.createElement('button');
            listenBtn.className = 'msg-action-btn';
            listenBtn.innerHTML = '<span>🔊</span> Listen';
            listenBtn.addEventListener('click', () => {
                window.miraAudio.playSoftTap();
                speakText(text);
            });

            const copyBtn = document.createElement('button');
            copyBtn.className = 'msg-action-btn';
            copyBtn.innerHTML = '<span>📋</span> Copy';
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(text).then(() => {
                    copyBtn.innerHTML = '<span>✓</span> Copied!';
                    setTimeout(() => copyBtn.innerHTML = '<span>📋</span> Copy', 2000);
                }).catch(e => console.log(e));
            });

            actions.appendChild(listenBtn);
            actions.appendChild(copyBtn);
            bubble.appendChild(actions);
        }

        msgEl.appendChild(avatar);
        msgEl.appendChild(bubble);
        dialogueMessagesList.appendChild(msgEl);
        dialogueMessagesList.scrollTop = dialogueMessagesList.scrollHeight;
    }

    async function handleUserMessage(message) {
        if (!message.trim()) return;
        window.miraAudio.playSoftTap();

        appendDialogueMessage('Mitali', message, true);
        if (dialogueWindow) dialogueWindow.classList.add('open');
        if (dialogueThinking) dialogueThinking.style.display = 'flex';
        if (dialogueMessagesList) dialogueMessagesList.scrollTop = dialogueMessagesList.scrollHeight;

        setMirrorSpeech("Pondering in the starlight...");

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    mood: currentMood,
                    context: 'general'
                })
            });
            const data = await res.json();
            const reply = data.reply || "You look breathtaking today, Princess Mitali.";

            if (dialogueThinking) dialogueThinking.style.display = 'none';

            appendDialogueMessage('MIRA', reply, false);
            setMirrorSpeech(reply);
            speakText(reply);
            window.miraAudio.playSparkle();
        } catch (e) {
            console.error('Chat error:', e);
            if (dialogueThinking) dialogueThinking.style.display = 'none';
            const fallback = "I see your radiant soul shining bright, Princess Mitali. Let me reconnect with the celestial realm for you.";
            appendDialogueMessage('MIRA', fallback, false);
            setMirrorSpeech(fallback);
            speakText(fallback);
        }
    }

    sendBtn.addEventListener('click', () => {
        const text = chatInput.value;
        chatInput.value = '';
        handleUserMessage(text);
    });

    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const text = chatInput.value;
            chatInput.value = '';
            handleUserMessage(text);
        }
    });

    // Dialogue window toggle controls
    if (toggleDialogueBtn) {
        toggleDialogueBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            window.miraAudio.playSoftTap();
            if (dialogueWindow) dialogueWindow.classList.toggle('open');
        });
    }

    if (miraSpeechBar) {
        miraSpeechBar.addEventListener('click', (e) => {
            if (e.target.closest('#toggle-dialogue-btn')) return;
            window.miraAudio.playSoftTap();
            if (dialogueWindow) dialogueWindow.classList.toggle('open');
        });
    }

    if (closeDialogueBtn) {
        closeDialogueBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            if (dialogueWindow) dialogueWindow.classList.remove('open');
        });
    }

    if (clearDialogueBtn) {
        clearDialogueBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            if (dialogueMessagesList) {
                dialogueMessagesList.innerHTML = `
                <div class="dialogue-msg mira-msg">
                  <div class="dialogue-avatar">🪞</div>
                  <div class="dialogue-bubble">
                    <div class="dialogue-author">MIRA Whispers</div>
                    <div class="dialogue-text">
                      Dialogue cleared, Princess Mitali. Ask me literally <b>anything</b> in the world!
                    </div>
                  </div>
                </div>
                `;
            }
        });
    }

    document.querySelectorAll('.quick-prompt-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const prompt = pill.dataset.prompt;
            handleUserMessage(prompt);
        });
    });

    // ✧ 12. REAL GEMINI VISION AURA & GLOW SCAN ✧
    scanAuraBtn.addEventListener('click', async () => {
        window.miraAudio.playSparkle();
        scanAuraBtn.disabled = true;
        scanAuraBtn.innerHTML = '<span>🔮 Scanning...</span>';
        setMirrorSpeech("Gemini Vision attuning starlight to read your aura and reflection...");

        let imageB64 = "";

        if (isCameraActive && webcamFeed && webcamFeed.videoWidth) {
            const scanCanvas = document.createElement('canvas');
            scanCanvas.width = 640;
            scanCanvas.height = 480;
            const sCtx = scanCanvas.getContext('2d');
            sCtx.translate(640, 0);
            sCtx.scale(-1, 1);
            sCtx.drawImage(webcamFeed, 0, 0, 640, 480);
            imageB64 = scanCanvas.toDataURL('image/jpeg', 0.85);
        } else {
            // If camera is dormant, use sample or trigger upload
            imageB64 = selfieResultImg.src.startsWith('data:') ? selfieResultImg.src : "";
        }

        try {
            let res;
            if (imageB64) {
                res = await fetch('/api/vision_scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageB64, mood_hint: currentMood })
                });
            } else {
                res = await fetch('/api/affirmation?mood=radiant');
            }
            const data = await res.json();

            const auraNameEl = document.getElementById('aura-name');
            const auraScoreEl = document.getElementById('aura-score');
            const auraComplimentEl = document.getElementById('aura-compliment');

            const auraTitle = data.aura_name || "Rose Quartz Radiance";
            const glowScore = data.confidence_score ? `${data.confidence_score}% Glow` : "98% Glow";
            const compliment = data.compliment || data.affirmation || "Your presence radiates pure grace and magnetizes love.";

            if (auraNameEl) auraNameEl.textContent = auraTitle;
            if (auraScoreEl) auraScoreEl.textContent = glowScore;
            if (auraComplimentEl) auraComplimentEl.textContent = `"${compliment}"`;

            const fullSpoken = `Your aura shines with ${auraTitle}, darling. ${compliment}`;
            setMirrorSpeech(fullSpoken);
            speakText(fullSpoken);
            window.miraAudio.playSparkle();
        } catch (e) {
            console.error('Aura scan error:', e);
            setMirrorSpeech("Your aura shines with Rose Quartz Starlight, darling. You carry starlight in your spirit!");
            speakText("Your aura shines with Rose Quartz Starlight, darling. You carry starlight in your spirit!");
        } finally {
            scanAuraBtn.disabled = false;
            scanAuraBtn.innerHTML = '<span>📸 Scan Reflection</span>';
        }
    });

    // ✧ 13. MOOD MODES ✧
    const moodBtns = document.querySelectorAll('.mood-btn');
    moodBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            moodBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            setMoodMode(btn.dataset.mood);
        });
    });

    function setMoodMode(mood) {
        currentMood = mood;
        document.body.className = `mood-${mood}`;
        sakuraEngine.setMood(mood);
        window.miraAudio.playSoftTap();

        if (mood === 'sad') {
            const msg = "I am right here with you, Mitali. Let the world pause for a moment. You are deeply safe, precious, and cherished.";
            setMirrorSpeech(msg);
            speakText(msg, 'sad');
            if (breathingSection) breathingSection.style.display = 'none';
        } else if (mood === 'excited') {
            const msg = "Look at that undeniable spark in your eyes, Princess Mitali! Celebrate every single victory today, gorgeous!";
            setMirrorSpeech(msg);
            speakText(msg, 'excited');
            if (breathingSection) breathingSection.style.display = 'none';
        } else if (mood === 'stressed') {
            const msg = "Breathe with me, Mitali. Inhale starlight, exhale the noise of the day. You are peace itself.";
            setMirrorSpeech(msg);
            speakText(msg, 'stressed');
            if (breathingSection) {
                breathingSection.style.display = 'flex';
                startBreathingCircle();
            }
        } else {
            const msg = "Your aura shines like rose quartz and moonlit pearl, Princess Mitali. Pure elegance looks exquisite on you.";
            setMirrorSpeech(msg);
            speakText(msg, 'radiant');
            if (breathingSection) breathingSection.style.display = 'none';
            stopBreathingCircle();
        }
    }

    // 4-7-8 Breathing Cycle
    function startBreathingCircle() {
        stopBreathingCircle();
        window.miraAudio.playMeditationBell();

        let step = 0;
        const runCycle = () => {
            if (step === 0) {
                lotusCircle.className = 'lotus-circle inhale';
                breathPhaseText.textContent = 'Inhale Serenity (4s)';
                breathingInterval = setTimeout(() => { step = 1; runCycle(); }, 4000);
            } else if (step === 1) {
                lotusCircle.className = 'lotus-circle hold';
                breathPhaseText.textContent = 'Hold Peace (7s)';
                breathingInterval = setTimeout(() => { step = 2; runCycle(); }, 7000);
            } else if (step === 2) {
                lotusCircle.className = 'lotus-circle exhale';
                breathPhaseText.textContent = 'Exhale All Tension (8s)';
                breathingInterval = setTimeout(() => { step = 0; runCycle(); }, 8000);
            }
        };
        runCycle();
    }

    function stopBreathingCircle() {
        if (breathingInterval) {
            clearTimeout(breathingInterval);
            breathingInterval = null;
        }
    }

    // ✧ 14. COUTURE STYLING LOUNGE (Interactive Palettes & Wardrobe Saving) ✧
    function renderPaletteSwatches(palette) {
        if (!paletteSwatches || !palette) return;
        paletteSwatches.innerHTML = '';
        palette.forEach(color => {
            const swatch = document.createElement('div');
            swatch.className = 'palette-swatch';
            swatch.style.backgroundColor = color.hex;
            swatch.title = `${color.name} (${color.hex})`;
            swatch.innerHTML = `<span>${color.name}</span>`;
            paletteSwatches.appendChild(swatch);
        });
    }

    styleChips.forEach(chip => {
        chip.addEventListener('click', async () => {
            styleChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            window.miraAudio.playSoftTap();

            const occasion = chip.dataset.occasion;
            const vibe = chip.dataset.vibe;
            stylingResult.textContent = "Curating your couture aesthetic & color palette...";

            try {
                const res = await fetch('/api/styling', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ occasion, vibe })
                });
                const data = await res.json();
                currentStylingData = data;
                stylingResult.textContent = data.styling_guide;
                renderPaletteSwatches(data.palette);
                window.miraAudio.playSparkle();
            } catch (e) {
                stylingResult.textContent = "Style with soft pastels, a tailored silhouette, and radiant confidence.";
            }
        });
    });

    if (listenStylingBtn) {
        listenStylingBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            const textToSpeak = stylingResult ? stylingResult.textContent : "Style with confidence, darling.";
            speakText(textToSpeak);
        });
    }

    if (saveOutfitBtn) {
        saveOutfitBtn.addEventListener('click', async () => {
            window.miraAudio.playSparkle();
            const activeChip = document.querySelector('.style-chip.active');
            const occasion = activeChip ? activeChip.textContent : "Couture Look";
            const vibeText = stylingResult ? stylingResult.textContent.substring(0, 100) + '...' : "";
            const palette = currentStylingData ? currentStylingData.palette : [];

            saveOutfitBtn.innerHTML = '<span>💖 Saved!</span>';
            setTimeout(() => { saveOutfitBtn.innerHTML = '<span>💖 Save Look</span>'; }, 2000);

            try {
                const res = await fetch('/api/save_outfit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: occasion,
                        vibe: vibeText,
                        palette: palette
                    })
                });
                const data = await res.json();
                renderWardrobeList(data.saved_outfits || []);
                setMirrorSpeech(`Saved ${occasion} to your wardrobe, Princess Mitali!`);
            } catch (e) {
                console.error("Save outfit error:", e);
            }
        });
    }

    // ✧ 15. INTERACTIVE BEAUTY & HABIT GLOW (Sleep, Skincare, Posture) ✧
    let sleepHours = 7.5;

    function updateSleepDisplay() {
        if (sleepVal) sleepVal.textContent = `${sleepHours.toFixed(1)}h`;
        if (sleepQualityTag) {
            if (sleepHours >= 7.5) {
                sleepQualityTag.textContent = "Restful Deep Glow";
                sleepQualityTag.style.color = "#ffd1dc";
            } else if (sleepHours >= 6.0) {
                sleepQualityTag.textContent = "Moderate Radiance";
                sleepQualityTag.style.color = "#cbb2fe";
            } else {
                sleepQualityTag.textContent = "Needs Gentle Rest";
                sleepQualityTag.style.color = "#fbb6ce";
            }
        }
    }

    if (sleepMinusBtn) {
        sleepMinusBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            sleepHours = Math.max(4.0, Math.round((sleepHours - 0.5) * 10) / 10);
            updateSleepDisplay();
            syncWellness({ action: 'update_sleep', hours: sleepHours });
        });
    }

    if (sleepPlusBtn) {
        sleepPlusBtn.addEventListener('click', () => {
            window.miraAudio.playSoftTap();
            sleepHours = Math.min(12.0, Math.round((sleepHours + 0.5) * 10) / 10);
            updateSleepDisplay();
            syncWellness({ action: 'update_sleep', hours: sleepHours });
        });
    }

    function updateSkincareProgress() {
        const checkboxes = [chkSerum, chkSpf, chkLipoil, chkMist].filter(Boolean);
        const checkedCount = checkboxes.filter(cb => cb.checked).length;
        const pct = Math.round((checkedCount / checkboxes.length) * 100);
        if (skincareProgressVal) skincareProgressVal.textContent = `${pct}% Complete`;
    }

    [
        { el: chkSerum, key: 'serum' },
        { el: chkSpf, key: 'spf' },
        { el: chkLipoil, key: 'lipoil' },
        { el: chkMist, key: 'lavender_mist' }
    ].forEach(({ el, key }) => {
        if (el) {
            el.addEventListener('change', () => {
                window.miraAudio.playSoftTap();
                updateSkincareProgress();
                syncWellness({ action: 'toggle_skincare', item: key, status: el.checked });
            });
        }
    });

    if (postureCoachBtn) {
        postureCoachBtn.addEventListener('click', () => {
            window.miraAudio.playSparkle();
            const guidance = "Roll your shoulders gently back, Princess Mitali. Elevate your chin like a queen, take a deep breath of starlight, and let your spine align with effortless poise.";
            setMirrorSpeech(guidance);
            speakText(guidance);
        });
    }

    async function syncWellness(payload) {
        try {
            await fetch('/api/wellness', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } catch (e) {
            console.log("Wellness sync note:", e);
        }
    }

    // ✧ 16. HYDRATION DEWDROP TRACKER ✧
    const dewdrops = document.querySelectorAll('.dewdrop');
    dewdrops.forEach((drop) => {
        drop.addEventListener('click', async () => {
            window.miraAudio.playSoftTap();
            drop.classList.toggle('active');

            let count = document.querySelectorAll('.dewdrop.active').length;
            const countLabel = document.getElementById('water-count');
            if (countLabel) countLabel.textContent = `${count} / 8 Glasses`;

            syncWellness({ action: drop.classList.contains('active') ? 'drink_water' : 'remove_water' });
        });
    });

    // ✧ 17. AFFIRMATIONS ✧
    async function fetchAffirmation() {
        window.miraAudio.playSoftTap();
        affirmationText.textContent = "Summoning celestial wisdom...";
        try {
            const res = await fetch(`/api/affirmation?mood=${currentMood}`);
            const data = await res.json();
            affirmationText.textContent = `"${data.affirmation}"`;
        } catch (e) {
            affirmationText.textContent = `"You carry starlight in your spirit and grace in every step."`;
        }
    }
    refreshAffirmationBtn.addEventListener('click', fetchAffirmation);

    speakAffirmationBtn.addEventListener('click', () => {
        window.miraAudio.playSparkle();
        speakText(affirmationText.textContent);
    });

    // ✧ 18. AUDIO & FULLSCREEN CONTROLS ✧
    audioToggleBtn.addEventListener('click', () => {
        const isMuted = window.miraAudio.toggleMute();
        audioToggleBtn.innerHTML = isMuted ? '🔇' : '🎵';
        audioToggleBtn.title = isMuted ? 'Unmute Ambient Sound' : 'Mute Ambient Sound';
    });

    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(e => console.log(e));
            fullscreenBtn.innerHTML = '⤓';
        } else {
            document.exitFullscreen().catch(e => console.log(e));
            fullscreenBtn.innerHTML = '⛶';
        }
    });

    // ✧ 19. LIVING MEMORY DRAWER & WARDROBE ✧
    function renderWardrobeList(outfits) {
        if (!drawerWardrobeList) return;
        if (!outfits || outfits.length === 0) {
            drawerWardrobeList.innerHTML = `<div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); font-style: italic;">No saved looks yet. Click '💖 Save Look' in the styling lounge!</div>`;
            return;
        }

        drawerWardrobeList.innerHTML = '';
        outfits.forEach(outfit => {
            const card = document.createElement('div');
            card.className = 'wardrobe-item-card';

            let dotsHtml = '';
            if (outfit.palette && outfit.palette.length) {
                dotsHtml = `<div class="wardrobe-palette-dots">` + outfit.palette.map(p => 
                    `<div class="wardrobe-palette-dot" style="background-color: ${p.hex};" title="${p.name}"></div>`
                ).join('') + `</div>`;
            }

            card.innerHTML = `
                <div class="wardrobe-item-header">
                    <span class="wardrobe-item-name">✨ ${outfit.name}</span>
                    <button class="wardrobe-delete-btn" title="Remove look">✕</button>
                </div>
                <div class="wardrobe-item-vibe">${outfit.vibe || ''}</div>
                ${dotsHtml}
            `;

            card.querySelector('.wardrobe-delete-btn').addEventListener('click', async (e) => {
                e.stopPropagation();
                window.miraAudio.playSoftTap();
                const res = await fetch('/api/delete_outfit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: outfit.id, name: outfit.name })
                });
                const data = await res.json();
                renderWardrobeList(data.saved_outfits || []);
            });

            drawerWardrobeList.appendChild(card);
        });
    }

    function renderMemoriesList(conversations) {
        if (!drawerMemoriesList) return;
        if (!conversations || conversations.length === 0) {
            drawerMemoriesList.innerHTML = `<div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); font-style: italic;">Start chatting with MIRA to build lasting memories.</div>`;
            return;
        }

        drawerMemoriesList.innerHTML = '';
        conversations.slice(-6).reverse().forEach(conv => {
            const m = document.createElement('div');
            m.className = 'memory-item-card';
            m.innerHTML = `
                <div class="memory-item-date">${conv.date || ''}</div>
                <div>${conv.summary || conv.topic || ''}</div>
            `;
            drawerMemoriesList.appendChild(m);
        });
    }

    memoryBtn.addEventListener('click', async () => {
        window.miraAudio.playSoftTap();
        memoryDrawer.classList.add('open');

        // Refresh memories & wardrobe from server
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            renderWardrobeList(data.saved_outfits || []);
            renderMemoriesList(data.past_conversations || []);
        } catch (e) {
            console.log("Memory fetch note:", e);
        }
    });

    closeDrawerBtn.addEventListener('click', () => {
        window.miraAudio.playSoftTap();
        memoryDrawer.classList.remove('open');
    });

    saveMemoryBtn.addEventListener('click', async () => {
        window.miraAudio.playSparkle();
        const userName = document.getElementById('drawer-user-name').value;
        const colors = document.getElementById('drawer-colors').value.split(',').map(s => s.trim());
        const goals = document.getElementById('drawer-goals').value.split(',').map(s => s.trim());

        await fetch('/api/memory', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                profile: {
                    name: userName,
                    favorite_colors: colors,
                    goals: goals
                }
            })
        });

        memoryDrawer.classList.remove('open');
        const confirmMsg = `Memory updated, ${userName}. I will cherish this forever.`;
        setMirrorSpeech(confirmMsg);
        speakText(confirmMsg);
    });

    // ✧ 20. INITIAL SYSTEM STATE SYNC ✧
    async function syncInitialSystemState() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();

            // Sync user name
            if (data.user_name) {
                const nameInput = document.getElementById('drawer-user-name');
                if (nameInput) nameInput.value = data.user_name;
            }

            // Sync wellness & sleep
            if (data.wellness) {
                const waterCount = data.wellness.water_glasses || 5;
                const countLabel = document.getElementById('water-count');
                if (countLabel) countLabel.textContent = `${waterCount} / 8 Glasses`;

                dewdrops.forEach((drop, idx) => {
                    drop.classList.toggle('active', idx < waterCount);
                });

                if (data.wellness.beauty_sleep_hours) {
                    sleepHours = data.wellness.beauty_sleep_hours;
                    updateSleepDisplay();
                }
            }

            // Sync skincare checklist
            if (data.skincare_checklist) {
                if (chkSerum) chkSerum.checked = !!data.skincare_checklist.serum;
                if (chkSpf) chkSpf.checked = !!data.skincare_checklist.spf;
                if (chkLipoil) chkLipoil.checked = !!data.skincare_checklist.lipoil;
                if (chkMist) chkMist.checked = !!data.skincare_checklist.lavender_mist;
                updateSkincareProgress();
            }

            // Populate wardrobe & memories
            renderWardrobeList(data.saved_outfits || []);
            renderMemoriesList(data.past_conversations || []);
        } catch (e) {
            console.log("Initial state sync note:", e);
        }
    }

    syncInitialSystemState();
});
