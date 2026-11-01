// ✧ MIRA Ethereal Fairytale Audio Synthesizer (Web Audio API) ✧
// Generates enchanted chimes, stardust arpeggios, and calming ambient soundscapes.

class MiraSoundEngine {
    constructor() {
        this.ctx = null;
        this.isMuted = false;
        this.ambientGain = null;
        this.ambientOscillators = [];
        this.isAmbientPlaying = false;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playAwakenChime() {
        this.init();
        if (this.isMuted) return;

        const now = this.ctx.currentTime;
        // Pentatonic enchanted scale (F# major / celestial): C#5, F#5, G#5, A#5, C#6, F#6
        const freqs = [554.37, 739.99, 830.61, 932.33, 1108.73, 1479.98];

        freqs.forEach((freq, index) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + index * 0.14);

            gain.gain.setValueAtTime(0.001, now + index * 0.14);
            gain.gain.exponentialRampToValueAtTime(0.22, now + index * 0.14 + 0.05);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + index * 0.14 + 1.8);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now + index * 0.14);
            osc.stop(now + index * 0.14 + 2.0);
        });
    }

    playSparkle() {
        this.init();
        if (this.isMuted) return;

        const now = this.ctx.currentTime;
        const freqs = [1046.50, 1318.51, 1567.98, 2093.00];
        
        freqs.forEach((freq, i) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq + Math.random() * 40, now + i * 0.06);

            gain.gain.setValueAtTime(0.001, now + i * 0.06);
            gain.gain.exponentialRampToValueAtTime(0.09, now + i * 0.06 + 0.03);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.06 + 0.6);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now + i * 0.06);
            osc.stop(now + i * 0.06 + 0.7);
        });
    }

    playSoftTap() {
        this.init();
        if (this.isMuted) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.exponentialRampToValueAtTime(440, now + 0.15);

        gain.gain.setValueAtTime(0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.18);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.2);
    }

    playMeditationBell() {
        this.init();
        if (this.isMuted) return;
        const now = this.ctx.currentTime;

        // Tibetan singing bowl frequency ~ 432 Hz + harmonics
        const harmonics = [
            { f: 432, g: 0.25, d: 4.5 },
            { f: 864, g: 0.12, d: 3.5 },
            { f: 1296, g: 0.05, d: 2.5 }
        ];

        harmonics.forEach(h => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(h.f, now);

            gain.gain.setValueAtTime(0.001, now);
            gain.gain.linearRampToValueAtTime(h.g, now + 0.08);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + h.d);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now);
            osc.stop(now + h.d + 0.5);
        });
    }

    toggleAmbientSoundscape(enable = null) {
        this.init();
        const shouldPlay = enable !== null ? enable : !this.isAmbientPlaying;

        if (!shouldPlay) {
            if (this.ambientGain) {
                this.ambientGain.gain.setTargetAtTime(0.0001, this.ctx.currentTime, 0.5);
                setTimeout(() => {
                    this.ambientOscillators.forEach(o => {
                        try { o.stop(); } catch (e) {}
                    });
                    this.ambientOscillators = [];
                }, 700);
            }
            this.isAmbientPlaying = false;
            return false;
        }

        // Dreamy ambient drone chords (F# major 9: F#2, C#3, G#3, A#3, F4)
        this.ambientGain = this.ctx.createGain();
        this.ambientGain.gain.setValueAtTime(0.001, this.ctx.currentTime);
        this.ambientGain.gain.linearRampToValueAtTime(0.12, this.ctx.currentTime + 3.0);
        this.ambientGain.connect(this.ctx.destination);

        const notes = [92.50, 138.59, 207.65, 233.08, 369.99];
        this.ambientOscillators = notes.map(freq => {
            const osc = this.ctx.createOscillator();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

            // Subtle vibrato/movement
            const lfo = this.ctx.createOscillator();
            const lfoGain = this.ctx.createGain();
            lfo.frequency.value = 0.15 + Math.random() * 0.1;
            lfoGain.gain.value = 1.2;
            lfo.connect(osc.frequency);
            lfo.start();

            osc.connect(this.ambientGain);
            osc.start();
            return osc;
        });

        this.isAmbientPlaying = true;
        return true;
    }

    toggleMute() {
        this.isMuted = !this.isMuted;
        if (this.isMuted && this.isAmbientPlaying) {
            this.toggleAmbientSoundscape(false);
        }
        return this.isMuted;
    }
}

window.miraAudio = new MiraSoundEngine();
