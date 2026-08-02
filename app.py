# ===== 100% FULL-SCREEN INTERACTIVE BACKGROUND & 3D LOGO HEADER =====
full_screen_bg_and_header = """
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@800&family=Playfair+Display:wght@700;800&family=Space+Mono:wght@700&family=Inter:wght@400;600;800&display=swap');

    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background: #06090e;
        overflow: hidden;
        font-family: 'Inter', system-ui, sans-serif;
    }

    #particle-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: auto;
    }

    .header-container {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 25px 15px 10px 15px;
        text-align: center;
        pointer-events: none;
        perspective: 1000px;
    }

    /* 3D Glass Emblem Base */
    .logo-3d-wrapper {
        position: relative;
        width: 95px;
        height: 95px;
        margin-bottom: 12px;
        transform-style: preserve-3d;
        transform: rotateX(15deg) rotateY(-8deg);
        transition: transform 0.5s ease;
    }

    /* 3D Drop Shadow Base Layer */
    .logo-3d-shadow {
        position: absolute;
        width: 100%;
        height: 100%;
        background: rgba(234, 179, 8, 0.15);
        border-radius: 22px;
        transform: translateZ(-18px) scale(0.92);
        filter: blur(8px);
    }

    /* Glassmorphism Back Plate */
    .logo-3d-backplate {
        position: absolute;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-radius: 22px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        transform: translateZ(0px);
    }

    /* Floating Gold Rim Frame */
    .logo-3d-frame {
        position: absolute;
        top: 6px;
        left: 6px;
        right: 6px;
        bottom: 6px;
        border-radius: 16px;
        border: 2px solid #eab308;
        box-shadow: 0 0 15px rgba(234, 179, 8, 0.4), inset 0 0 10px rgba(234, 179, 8, 0.2);
        transform: translateZ(12px);
    }

    /* Raised Metallic 3D Monogram */
    .logo-3d-content {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transform: translateZ(25px);
    }

    .ml-text-3d {
        font-family: 'Cinzel', serif;
        font-size: 34px;
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #facc15 65%, #ca8a04 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
        line-height: 1;
        letter-spacing: 1.5px;
    }

    .ml-sub-3d {
        font-family: 'Space Mono', monospace;
        font-size: 7px;
        color: #eab308;
        letter-spacing: 2px;
        margin-top: 3px;
        text-transform: uppercase;
        font-weight: 700;
    }

    .portal-title {
        font-family: 'Playfair Display', serif;
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 8px 0 2px 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }

    .portal-subtitle {
        font-family: 'Space Mono', monospace;
        color: #eab308;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.95;
    }
</style>
</head>
<body>
    <canvas id="particle-canvas"></canvas>
    
    <div class="header-container">
        <div class="logo-3d-wrapper">
            <div class="logo-3d-shadow"></div>
            <div class="logo-3d-backplate"></div>
            <div class="logo-3d-frame"></div>
            <div class="logo-3d-content">
                <div class="ml-text-3d">ML</div>
                <div class="ml-sub-3d">LOHANA</div>
            </div>
        </div>
        <div class="portal-title">Student Results Portal</div>
        <div class="portal-subtitle">Govt Boys Higher Secondary School Tando Bago</div>
    </div>

    <script>
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        const particles = [];
        const particleCount = Math.min(35, Math.floor(window.innerWidth / 12));
        let mouse = { x: null, y: null, radius: 120 };

        window.addEventListener('mousemove', (e) => {
            mouse.x = e.x;
            mouse.y = e.y;
        });

        window.addEventListener('touchmove', (e) => {
            if(e.touches.length > 0) {
                mouse.x = e.touches[0].clientX;
                mouse.y = e.touches[0].clientY;
            }
        }, { passive: true });

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.6;
                this.vy = (Math.random() - 0.5) * 0.6;
                this.radius = Math.random() * 1.8 + 1;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;

                if (mouse.x !== null) {
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < mouse.radius) {
                        let force = (mouse.radius - dist) / mouse.radius;
                        this.x -= (dx / dist) * force * 2;
                        this.y -= (dy / dist) * force * 2;
                    }
                }
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = '#eab308';
                ctx.fill();
            }
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();

                for (let j = i + 1; j < particles.length; j++) {
                    let dx = particles[i].x - particles[j].x;
                    let dy = particles[i].y - particles[j].y;
                    let dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 110) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(234, 179, 8, ${0.25 * (1 - dist / 110)})`;
                        ctx.lineWidth = 0.7;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();
    </script>
</body>
</html>
"""

