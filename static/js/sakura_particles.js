// ✧ MIRA Aesthetic Sakura & Stardust Particle Engine ✧
// Features 3D fluttering cherry blossoms, stardust bokeh, and mood-adaptive physics.

class SakuraEngine {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        this.petals = [];
        this.stars = [];
        this.maxPetals = 45;
        this.maxStars = 60;
        this.currentMood = 'radiant';
        this.wind = 0.5;
        this.mouseX = window.innerWidth / 2;
        this.mouseY = window.innerHeight / 2;

        this.init();
    }

    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
            this.wind = (e.clientX - window.innerWidth / 2) / 600;
        });

        // Initialize petals
        for (let i = 0; i < this.maxPetals; i++) {
            this.petals.push(this.createPetal(true));
        }

        // Initialize stardust
        for (let i = 0; i < this.maxStars; i++) {
            this.stars.push(this.createStar());
        }

        this.animate = this.animate.bind(this);
        requestAnimationFrame(this.animate);
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createPetal(randomY = false) {
        const colors = [
            'rgba(255, 183, 197, ', // Light Sakura Pink
            'rgba(255, 209, 220, ', // Pastel Rose
            'rgba(230, 204, 255, ', // Lavender Mist
            'rgba(255, 230, 240, '  // Pearl White-Pink
        ];
        return {
            x: Math.random() * this.canvas.width,
            y: randomY ? Math.random() * this.canvas.height : -20,
            size: Math.random() * 12 + 8,
            speedY: Math.random() * 1.2 + 0.8,
            speedX: Math.random() * 0.8 - 0.4,
            rotation: Math.random() * 360,
            rotSpeed: (Math.random() - 0.5) * 2,
            flip: Math.random() * Math.PI,
            flipSpeed: Math.random() * 0.03 + 0.01,
            colorBase: colors[Math.floor(Math.random() * colors.length)],
            alpha: Math.random() * 0.5 + 0.35
        };
    }

    createStar() {
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            size: Math.random() * 2.2 + 0.5,
            alpha: Math.random(),
            speed: Math.random() * 0.02 + 0.005,
            direction: Math.random() > 0.5 ? 1 : -1
        };
    }

    setMood(mood) {
        this.currentMood = mood;
        if (mood === 'excited') {
            this.maxPetals = 70;
            while (this.petals.length < this.maxPetals) {
                this.petals.push(this.createPetal(false));
            }
        } else if (mood === 'sad') {
            this.maxPetals = 25;
        } else {
            this.maxPetals = 45;
        }
    }

    drawPetal(p) {
        this.ctx.save();
        this.ctx.translate(p.x, p.y);
        this.ctx.rotate((p.rotation * Math.PI) / 180);
        this.ctx.scale(Math.cos(p.flip), 1);

        // Petal shape
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.bezierCurveTo(p.size / 2, -p.size / 2, p.size, p.size / 4, 0, p.size);
        this.ctx.bezierCurveTo(-p.size, p.size / 4, -p.size / 2, -p.size / 2, 0, 0);
        
        let color = p.colorBase + p.alpha + ')';
        if (this.currentMood === 'sad') {
            color = `rgba(180, 195, 235, ${p.alpha * 0.8})`;
        } else if (this.currentMood === 'excited') {
            color = `rgba(255, 195, 170, ${p.alpha * 1.1})`;
        }

        this.ctx.fillStyle = color;
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = 'rgba(255, 192, 203, 0.4)';
        this.ctx.fill();
        this.ctx.restore();
    }

    drawStar(s) {
        this.ctx.save();
        s.alpha += s.speed * s.direction;
        if (s.alpha >= 1) {
            s.alpha = 1;
            s.direction = -1;
        } else if (s.alpha <= 0.1) {
            s.alpha = 0.1;
            s.direction = 1;
        }

        let starColor = `rgba(255, 255, 255, ${s.alpha * 0.85})`;
        if (this.currentMood === 'sad') {
            starColor = `rgba(190, 210, 255, ${s.alpha * 0.7})`;
        } else if (this.currentMood === 'excited') {
            starColor = `rgba(255, 235, 180, ${s.alpha * 0.9})`;
        }

        this.ctx.fillStyle = starColor;
        this.ctx.shadowBlur = 8;
        this.ctx.shadowColor = 'rgba(255, 255, 255, 0.8)';
        this.ctx.beginPath();
        this.ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.restore();
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Update and draw stars
        for (let s of this.stars) {
            this.drawStar(s);
        }

        // Update and draw petals
        for (let i = 0; i < this.petals.length; i++) {
            let p = this.petals[i];
            p.y += p.speedY;
            p.x += p.speedX + this.wind;
            p.rotation += p.rotSpeed;
            p.flip += p.flipSpeed;

            if (p.y > this.canvas.height + 30 || p.x < -30 || p.x > this.canvas.width + 30) {
                this.petals[i] = this.createPetal(false);
            } else {
                this.drawPetal(p);
            }
        }

        requestAnimationFrame(this.animate);
    }
}

window.SakuraEngine = SakuraEngine;
