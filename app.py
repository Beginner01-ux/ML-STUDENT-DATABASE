import streamlit as st
import pandas as pd
import re
import os
from PIL import Image
from html import escape
import streamlit.components.v1 as components

try:
    import zxingcpp
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Student Results Portal | ML",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== INJECT SPLIT-SCREEN LAYOUT & CONTINUOUS MOTION CHEMISTRY/PHONETICS CANVAS =====
split_layout_html = """
<script>
    (function() {
        const parentDoc = window.parent.document;
        const MOBILE_BREAKPOINT = 640;

        const mainBlock = parentDoc.querySelector('.main .block-container');
        if (mainBlock) {
            mainBlock.style.maxWidth = '100vw';
            mainBlock.style.padding = '0';
            mainBlock.style.margin = '0';
        }

        function isMobile() {
            return window.parent.innerWidth <= MOBILE_BREAKPOINT;
        }

        let canvas = parentDoc.getElementById('split-canvas-bg');
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'split-canvas-bg';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.zIndex = '0';
            canvas.style.pointerEvents = 'auto';
            parentDoc.body.style.backgroundColor = '#030712';
            parentDoc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            function applyResponsiveDimensions() {
                const mobile = isMobile();
                const widthFraction = mobile ? 1.0 : 0.5;
                const heightFraction = mobile ? 0.45 : 1.0;
                
                canvas.style.width = (widthFraction * 100) + 'vw';
                canvas.style.height = (heightFraction * 100) + 'vh';
                canvas.width = window.parent.innerWidth * widthFraction;
                canvas.height = window.parent.innerHeight * heightFraction;
                return mobile;
            }

            let currentMobile = applyResponsiveDimensions();

            function resize() {
                const mobile = isMobile();
                if (mobile !== currentMobile) {
                    currentMobile = mobile;
                    applyResponsiveDimensions();
                    entities.forEach(en => {
                        en.x = Math.random() * canvas.width;
                        en.y = Math.random() * canvas.height;
                    });
                } else {
                    applyResponsiveDimensions();
                }
            }
            window.parent.addEventListener('resize', resize);

            const entities = [];
            
            const atomTypes = [
                { symbol: 'H', valency: 1, color: '#38bdf8', mass: 1 },
                { symbol: 'O', valency: 2, color: '#f43f5e', mass: 16 },
                { symbol: 'C', valency: 4, color: '#a855f7', mass: 12 },
                { symbol: 'N', valency: 3, color: '#3b82f6', mass: 14 },
                { symbol: 'Na', valency: 1, color: '#eab308', mass: 23 },
                { symbol: 'Cl', valency: 1, color: '#22c55e', mass: 35 }
            ];

            const phoneticPairs = [
                { a: 's', b: 'h', result: 'sh' }, { a: 'c', b: 'h', result: 'ch' },
                { a: 'p', b: 'h', result: 'ph' }, { a: 't', b: 'h', result: 'th' },
                { a: 'w', b: 'h', result: 'wh' }, { a: 'q', b: 'u', result: 'qu' },
                { a: 'b', b: 'l', result: 'bl' }, { a: 'b', b: 'r', result: 'br' },
                { a: 'c', b: 'l', result: 'cl' }, { a: 'c', b: 'r', result: 'cr' },
                { a: 'd', b: 'r', result: 'dr' }, { a: 'f', b: 'l', result: 'fl' },
                { a: 'f', b: 'r', result: 'fr' }, { a: 'g', b: 'l', result: 'gl' },
                { a: 'g', b: 'r', result: 'gr' }, { a: 'p', b: 'l', result: 'pl' },
                { a: 'p', b: 'r', result: 'pr' }, { a: 's', b: 'c', result: 'sc' },
                { a: 's', b: 'k', result: 'sk' }, { a: 's', b: 'l', result: 'sl' },
                { a: 's', b: 'm', result: 'sm' }, { a: 's', b: 'n', result: 'sn' },
                { a: 's', b: 'p', result: 'sp' }, { a: 's', b: 't', result: 'st' },
                { a: 's', b: 'w', result: 'sw' }, { a: 't', b: 'r', result: 'tr' },
                { a: 't', b: 'w', result: 'tw' }, { a: 'e', b: 'e', result: 'ee' },
                { a: 'o', b: 'o', result: 'oo' }, { a: 'a', b: 'i', result: 'ai' },
                { a: 'e', b: 'a', result: 'ea' }, { a: 'o', b: 'u', result: 'ou' }
            ];

            const entityCount = 32;
            let pointer = { x: null, y: null, radius: 130, active: false };

            function updatePointerPosition(clientX, clientY) {
                const rect = canvas.getBoundingClientRect();
                const x = clientX - rect.left;
                const y = clientY - rect.top;
                if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
                    pointer.x = x;
                    pointer.y = y;
                    pointer.active = true;
                } else if (isMobile()) {
                    pointer.x = x;
                    pointer.y = y;
                    pointer.active = true;
                } else {
                    pointer.x = null;
                    pointer.y = null;
                    pointer.active = false;
                }
            }

            window.parent.addEventListener('mousemove', (e) => {
                updatePointerPosition(e.clientX, e.clientY);
            });

            window.parent.addEventListener('mouseleave', () => {
                pointer.x = null;
                pointer.y = null;
                pointer.active = false;
            });

            window.parent.addEventListener('touchstart', (e) => {
                if (e.touches.length > 0) {
                    updatePointerPosition(e.touches.get(0).clientX, e.touches.get(0).clientY);
                    triggerPulse(pointer.x, pointer.y);
                }
            }, { passive: true });

            window.parent.addEventListener('touchmove', (e) => {
                if (e.touches.length > 0) {
                    updatePointerPosition(e.touches.get(0).clientX, e.touches.get(0).clientY);
                }
            }, { passive: true });

            window.parent.addEventListener('touchend', () => {
                pointer.x = null;
                pointer.y = null;
                pointer.active = false;
            });

            window.parent.addEventListener('click', (e) => {
                updatePointerPosition(e.clientX, e.clientY);
                triggerPulse(pointer.x, pointer.y);
            });

            function triggerPulse(px, py) {
                if (px === null || py === null) return;
                entities.forEach(en => {
                    let dx = en.x - px;
                    let dy = en.y - py;
                    let dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 200) {
                        let angle = Math.atan2(dy, dx);
                        en.vx += Math.cos(angle) * 8;
                        en.vy += Math.sin(angle) * 8;
                    }
                });
            }

            class Entity {
                constructor() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    // Maintain continuous baseline velocity so motion never stops completely
                    const minSpeed = 0.8;
                    let angle = Math.random() * Math.PI * 2;
                    let speed = minSpeed + Math.random() * 1.2;
                    this.vx = Math.cos(angle) * speed;
                    this.vy = Math.sin(angle) * speed;
                    
                    this.category = Math.floor(Math.random() * 3);
                    this.radius = 12;

                    if (this.category === 0) {
                        let atom = atomTypes[Math.floor(Math.random() * atomTypes.length)];
                        this.baseSymbol = atom.symbol;
                        this.formula = atom.symbol;
                        this.color = atom.color;
                        this.valency = atom.valency;
                        this.boundAtoms = [];
                    } else if (this.category === 1) {
                        let pair = phoneticPairs[Math.floor(Math.random() * phoneticPairs.length)];
                        this.originalA = pair.a;
                        this.originalB = pair.b;
                        this.combinedText = pair.result;
                        this.text = this.originalA;
                        this.isCombined = false;
                    }
                }

                update() {
                    this.x += this.vx;
                    this.y += this.vy;

                    // Enforce a minimum perpetual velocity vector magnitude so motion never stops
                    let currentSpeed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
                    if (currentSpeed < 0.75) {
                        let boostAngle = Math.random() * Math.PI * 2;
                        this.vx += Math.cos(boostAngle) * 0.5;
                        this.vy += Math.sin(boostAngle) * 0.5;
                    }

                    // Damping with continuous energy floor
                    this.vx *= 0.998;
                    this.vy *= 0.998;

                    if (this.x < this.radius) { this.x = this.radius; this.vx = Math.abs(this.vx) + 0.5; }
                    if (this.x > canvas.width - this.radius) { this.x = canvas.width - this.radius; this.vx = -(Math.abs(this.vx) + 0.5); }
                    if (this.y < this.radius) { this.y = this.radius; this.vy = Math.abs(this.vy) + 0.5; }
                    if (this.y > canvas.height - this.radius) { this.y = canvas.height - this.radius; this.vy = -(Math.abs(this.vy) + 0.5); }

                    let logoCenterX = canvas.width / 2;
                    let logoCenterY = isMobile() ? canvas.height * 0.38 : canvas.height / 2;
                    let logoRadius = isMobile() ? 75 : 110;

                    let lDx = this.x - logoCenterX;
                    let lDy = this.y - logoCenterY;
                    let lDist = Math.sqrt(lDx * lDx + lDy * lDy);
                    let minAllowedDist = logoRadius + this.radius + 15;

                    if (lDist < minAllowedDist) {
                        let angle = Math.atan2(lDy, lDx);
                        this.x = logoCenterX + Math.cos(angle) * minAllowedDist;
                        this.y = logoCenterY + Math.sin(angle) * minAllowedDist;
                        this.vx += Math.cos(angle) * 1.2;
                        this.vy += Math.sin(angle) * 1.2;
                    }

                    if (pointer.x !== null && pointer.y !== null) {
                        let dx = pointer.x - this.x;
                        let dy = pointer.y - this.y;
                        let dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist < pointer.radius) {
                            let force = (pointer.radius - dist) / pointer.radius;
                            this.vx -= (dx / dist) * force * 0.15;
                            this.vy -= (dy / dist) * force * 0.15;
                        }
                    }
                }

                draw() {
                    ctx.save();
                    ctx.translate(this.x, this.y);

                    if (this.category === 0) {
                        let isCompound = this.boundAtoms && this.boundAtoms.length > 0;
                        let r = isCompound ? 18 : 13;
                        
                        ctx.beginPath();
                        ctx.arc(0, 0, r, 0, Math.PI * 2);
                        ctx.fillStyle = isCompound ? 'rgba(250, 204, 21, 0.95)' : (this.color || 'rgba(56, 189, 248, 0.9)');
                        ctx.shadowBlur = isCompound ? 15 : 6;
                        ctx.shadowColor = isCompound ? '#facc15' : (this.color || '#38bdf8');
                        ctx.fill();

                        ctx.font = 'bold 11px Space Grotesk, sans-serif';
                        ctx.fillStyle = isCompound ? '#000000' : '#ffffff';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(this.formula, 0, 1);
                    } else if (this.category === 1) {
                        ctx.font = 'bold 13px Space Mono, monospace';
                        ctx.fillStyle = this.isCombined ? 'rgba(250, 204, 21, 0.95)' : 'rgba(192, 132, 252, 0.9)';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(this.text, 0, 0);
                    } else {
                        ctx.beginPath();
                        ctx.arc(0, 0, 4, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(56, 189, 248, 0.95)';
                        ctx.shadowBlur = 8;
                        ctx.shadowColor = '#38bdf8';
                        ctx.fill();
                    }

                    ctx.restore();
                }
            }

            for (let i = 0; i < entityCount; i++) {
                entities.push(new Entity());
            }

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                let bgGrad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 10, canvas.width/2, canvas.height/2, Math.max(canvas.width, canvas.height));
                bgGrad.addColorStop(0, '#1e1b4b');
                bgGrad.addColorStop(1, '#030712');
                ctx.fillStyle = bgGrad;
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (let i = 0; i < entities.length; i++) {
                    entities[i].update();
                    entities[i].draw();

                    for (let j = i + 1; j < entities.length; j++) {
                        let dx = entities[i].x - entities[j].x;
                        let dy = entities[i].y - entities[j].y;
                        let dist = Math.sqrt(dx * dx + dy * dy);

                        if (dist < 28) {
                            let angle = Math.atan2(dy, dx);
                            let push = 0.8;
                            entities[i].vx += Math.cos(angle) * push;
                            entities[i].vy += Math.sin(angle) * push;
                            entities[j].vx -= Math.cos(angle) * push;
                            entities[j].vy -= Math.sin(angle) * push;
                        }

                        if (entities[i].category === 0 && entities[j].category === 0 && dist < 42) {
                            let a1 = entities[i];
                            let a2 = entities[j];
                            
                            if ((a1.boundAtoms.length === 0) && (a2.boundAtoms.length === 0)) {
                                let syms = [a1.baseSymbol, a2.baseSymbol].sort().join('');
                                if (syms === 'HO' || syms === 'H2O') {
                                    a1.boundAtoms.push(a2);
                                    a1.formula = 'H₂O';
                                    a2.formula = '';
                                } else if (syms === 'ClNa') {
                                    a1.boundAtoms.push(a2);
                                    a1.formula = 'NaCl';
                                    a2.formula = '';
                                } else if (syms === 'CO') {
                                    a1.boundAtoms.push(a2);
                                    a1.formula = 'CO';
                                    a2.formula = '';
                                } else if (a1.baseSymbol === a2.baseSymbol && a1.baseSymbol === 'H') {
                                    a1.boundAtoms.push(a2);
                                    a1.formula = 'H₂';
                                    a2.formula = '';
                                } else if (a1.baseSymbol === a2.baseSymbol && a1.baseSymbol === 'O') {
                                    a1.boundAtoms.push(a2);
                                    a1.formula = 'O₂';
                                    a2.formula = '';
                                }
                            } else if ((a1.boundAtoms.length > 0 && a1.boundAtoms.includes(a2)) || 
                                       (a2.boundAtoms.length > 0 && a2.boundAtoms.includes(a1))) {
                                a1.boundAtoms = [];
                                a1.formula = a1.baseSymbol;
                                a2.boundAtoms = [];
                                a2.formula = a2.baseSymbol;
                            }

                            if (a1.boundAtoms.includes(a2) || a2.boundAtoms.includes(a1)) {
                                ctx.beginPath();
                                ctx.moveTo(a1.x, a1.y);
                                ctx.lineTo(a2.x, a2.y);
                                ctx.strokeStyle = 'rgba(250, 204, 21, 0.8)';
                                ctx.lineWidth = 2.0;
                                ctx.stroke();
                            }
                        }

                        if (entities[i].category === 1 && entities[j].category === 1 && dist < 40) {
                            let p1 = entities[i];
                            let p2 = entities[j];
                            if (!p1.isCombined && !p2.isCombined) {
                                if ((p1.text === p1.originalA && p2.text === p2.originalA) ||
                                    (p1.text === p1.originalA && p2.text === p2.originalB) ||
                                    (p1.originalA === p2.originalA && p1.originalB === p2.originalB)) {
                                    p1.text = p1.combinedText;
                                    p1.isCombined = true;
                                    p2.text = p2.combinedText;
                                    p2.isCombined = true;
                                }
                            } else if (p1.isCombined && p2.isCombined) {
                                p1.text = p1.originalA;
                                p1.isCombined = false;
                                p2.text = p2.originalA;
                                p2.isCombined = false;
                            }
                        }

                        if (entities[i].category === 2 && entities[j].category === 2 && dist < 95) {
                            ctx.beginPath();
                            ctx.moveTo(entities[i].x, entities[i].y);
                            ctx.lineTo(entities[j].x, entities[j].y);
                            ctx.strokeStyle = `rgba(56, 189, 248, ${0.35 * (1 - dist / 95)})`;
                            ctx.lineWidth = 0.8;
                            ctx.stroke();
                        }
                    }
                }
                requestAnimationFrame(animate);
            }
            animate();
        }
    })();
</script>
"""
components.html(split_layout_html, height=0)

# ===== GLOBAL STYLING OVERRIDES =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

    @media print {
        .print-btn {
            display: none !important;
        }
    }

    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    [data-testid="stVerticalBlock"] {
        position: relative;
        z-index: 5;
    }

    .left-hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 85vh;
        text-align: center;
        padding: 40px;
        position: relative;
        z-index: 5;
    }

    @media (max-width: 640px) {
        .left-hero-container {
            min-height: 45vh;
            padding: 24px 16px 16px 16px;
        }
        .hero-circle-accent {
            width: 150px !important;
            height: 150px !important;
            margin-bottom: 14px !important;
        }
        .hero-logo-text {
            font-size: 48px !important;
        }
        .hero-title {
            font-size: 24px !important;
        }
        .hero-subtitle {
            font-size: 10px !important;
        }
    }

    .hero-circle-accent {
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 2px solid #facc15;
        box-shadow: 0 0 50px rgba(250, 204, 21, 0.25), inset 0 0 20px rgba(250, 204, 21, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 24px;
        z-index: 5;
    }

    .hero-logo-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 72px;
        font-weight: 700;
        color: #facc15;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(250, 204, 21, 0.4);
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px;
    }

    .right-portal-card {
        background: rgba(11, 19, 41, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);
        margin-top: 20px;
        position: relative;
        z-index: 10;
    }

    .form-header-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .form-header-sub {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 24px;
    }

    @media (max-width: 640px) {
        .right-portal-card {
            padding: 24px 18px;
            border-radius: 16px;
            margin-top: 12px;
            border-top: 2px solid rgba(250, 204, 21, 0.5);
        }
        .form-header-title { font-size: 20px; }
        .form-header-sub { font-size: 11px; margin-bottom: 16px; }
    }

    .stTextInput > div > div {
        background-color: #24304a !important;
        border: 1.5px solid rgba(250, 204, 21, 0.35) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4) !important;
    }

    .stTextInput input {
        font-size: 16px !important;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #facc15 !important;
        box-shadow: 0 0 12px rgba(250, 204, 21, 0.4) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.8);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 44px;
        display: flex;
        align-items: center;
    }

    .stTabs [aria-selected="true"] {
        background-color: #facc15 !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== UTILITY FUNCTIONS =====
def validate_test_number(test_no):
    pattern = r'^[JFMASONDjfmasond](1[0-2]|[1-9])-\d{2}-\d{2}$'
    return bool(re.match(pattern, test_no.strip()))

def decode_barcode_image(pil_image):
    if not BARCODE_AVAILABLE:
        return None
    try:
        results = zxingcpp.read_barcodes(pil_image)
        if results:
            return results[0].text.strip()
    except Exception:
        pass
    return None

def format_percentage(val):
    try:
        f_val = float(str(val).replace('%', '').strip())
        if f_val <= 1.0:
            f_val = f_val * 100
        f_val = max(0.0, min(100.0, f_val))
        return f"{int(round(f_val))}%", f_val
    except Exception:
        return "0%", 0.0

def get_excel_column(df, possible_names):
    normalized_cols = {c.lower().replace(' ', '').replace('_', ''): c for c in df.columns}
    for name in possible_names:
        key = name.lower().replace(' ', '').replace('_', '')
        if key in normalized_cols:
            return normalized_cols[key]
    return None

# ===== A4 CERTIFICATE & MARKSHEET GENERATOR =====
def generate_report_card(serial_no, test_no, student_data):
    name = escape(str(student_data.get('name', 'N/A')).strip())
    father_name = escape(str(student_data.get('father_name', 'N/A')).strip())
    roll_no = escape(str(student_data.get('roll_no', 'N/A')).strip())
    test_score = escape(str(student_data.get('test_score', '0')).strip())

    subject_raw = re.sub(r'\s+', ' ', str(student_data.get('subject', 'CHEMISTRY')).strip())
    subject = escape(subject_raw[:30])

    percentage_str, pct_num = format_percentage(student_data.get('percentage', '0'))
    cls = escape(str(student_data.get('class', 'X')).strip())
    section = escape(str(student_data.get('section', 'A')).strip()[:2])

    rank_raw = str(student_data.get('class_rank', 'N/A')).strip()
    rank_digits = re.search(r'\d+', rank_raw)
    rank = f"#{escape(rank_digits.group(0))}" if rank_digits else 'N/A'

    serial_no = escape(str(serial_no).strip())
    test_no = escape(str(test_no).strip())

    certificate_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                box-sizing: border-box;
            }}

            @media print {{
                .print-btn {{
                    display: none !important;
                }}
            }}

            @page {{
                size: A4 portrait;
                margin: 0;
            }}

            body {{
                background-color: transparent;
                font-family: 'Plus Jakarta Sans', sans-serif;
                margin: 0;
                padding: 0;
            }}

            .cert-container {{
                background: linear-gradient(145deg, #0b1329 0%, #030712 100%);
                color: #ffffff;
                width: 100%;
                border: 2px solid #ca8a04;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 25px 60px rgba(0,0,0,0.85);
            }}

            .cert-border-inner {{
                border: 1px solid rgba(234, 179, 8, 0.4);
                border-radius: 12px;
                padding: 16px;
                background: radial-gradient(circle at center, rgba(30, 41, 59, 0.2) 0%, rgba(3, 7, 18, 0.4) 100%);
            }}

            .cert-header {{
                text-align: center;
                border-bottom: 1px solid rgba(234, 179, 8, 0.2);
                padding-bottom: 12px;
                margin-bottom: 14px;
            }}

            .cert-crest {{
                width: 44px;
                height: 44px;
                border-radius: 50%;
                border: 1.5px solid #facc15;
                background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-family: 'Cinzel', serif;
                font-weight: 800;
                font-size: 18px;
                color: #facc15;
                margin-bottom: 6px;
            }}

            .institution-name {{
                font-family: 'Cinzel', serif;
                font-size: 11px;
                font-weight: 700;
                color: #facc15;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin: 0;
            }}

            .cert-title {{
                font-family: 'Cinzel', serif;
                font-size: 18px;
                font-weight: 900;
                color: #ffffff;
                margin-top: 4px;
            }}

            .student-section {{
                text-align: center;
                margin-bottom: 14px;
            }}

            .cert-presented-to {{
                font-size: 9px;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
            }}

            .student-name {{
                font-family: 'Cinzel', serif;
                font-size: 22px;
                font-weight: 800;
                color: #ffffff;
                margin: 4px 0;
            }}

            .student-sub {{
                color: #cbd5e1;
                font-size: 11px;
                font-weight: 600;
            }}

            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
                margin-bottom: 14px;
            }}

            .metric-box {{
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid rgba(234, 179, 8, 0.25);
                border-radius: 8px;
                padding: 8px 6px;
                text-align: center;
                min-width: 0;
            }}

            .metric-title {{
                font-size: 7.5px;
                color: #94a3b8;
                text-transform: uppercase;
                font-weight: 700;
            }}

            .metric-value {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 16px;
                font-weight: 700;
                color: #facc15;
                margin-top: 2px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}

            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                margin-bottom: 14px;
            }}

            .info-item {{
                background: rgba(30, 41, 59, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-left: 3px solid #facc15;
                padding: 6px 10px;
                border-radius: 6px;
            }}

            .info-label {{
                font-size: 7.5px;
                color: #64748b;
                text-transform: uppercase;
                font-weight: 700;
                display: block;
            }}

            .info-val {{
                font-size: 11px;
                color: #ffffff;
                font-weight: 700;
                margin-top: 2px;
            }}

            .cert-footer {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-top: 1px solid rgba(234, 179, 8, 0.2);
                padding-top: 12px;
            }}

            .official-seal {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}

            .seal-badge {{
                width: 36px;
                height: 36px;
                border-radius: 50%;
                border: 1.5px dashed #facc15;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #facc15;
                font-size: 14px;
                background: rgba(250, 204, 21, 0.1);
            }}

            .seal-text-title {{
                font-size: 10px;
                font-weight: 800;
                color: #ffffff;
            }}

            .seal-text-sub {{
                font-size: 8px;
                color: #22c55e;
                font-weight: 700;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
                color: #000000;
                border: none;
                padding: 10px 16px;
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700;
                font-size: 10px;
                border-radius: 8px;
                cursor: pointer;
                letter-spacing: 1px;
                text-transform: uppercase;
            }}
        </style>
    </head>
    <body>
        <div class="cert-container">
            <div class="cert-border-inner">
                <div class="cert-header">
                    <div class="cert-crest">ML</div>
                    <div class="institution-name">Govt Boys Higher Secondary School Tando Bago</div>
                    <div class="cert-title">Academic Progress Certificate</div>
                </div>

                <div class="student-section">
                    <div class="cert-presented-to">This Official Marksheet is Issued To</div>
                    <div class="student-name">{name}</div>
                    <div class="student-sub">Father's Name: {father_name} &nbsp;|&nbsp; Class {cls}-{section} &nbsp;|&nbsp; Seat No: {roll_no}</div>
                </div>

                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-title">Score</div>
                        <div class="metric-value">{test_score}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-title">Percentage</div>
                        <div class="metric-value">{percentage_str}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-title">Class Rank</div>
                        <div class="metric-value">{rank}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-title">Accuracy</div>
                        <div class="metric-value">{percentage_str}</div>
                    </div>
                </div>

                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">Evaluated Subject</span>
                        <span class="info-val">{subject}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Exam Session Code</span>
                        <span class="info-val">{test_no}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Book Serial Number</span>
                        <span class="info-val">{serial_no}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Verification Status</span>
                        <span class="info-val" style="color:#22c55e;">Authenticated</span>
                    </div>
                </div>

                <div class="cert-footer">
                    <div class="official-seal">
                        <div class="seal-badge">✓</div>
                        <div>
                            <div class="seal-text-title">Official Academic Seal</div>
                            <div class="seal-text-sub">Verified Digital Transcript</div>
                        </div>
                    </div>
                    <button class="print-btn" onclick="window.print()">️ Print / Save PDF Certificate</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(certificate_html, height=680, scrolling=True)

# ===== 50/50 SPLIT SCREEN LAYOUT =====
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.markdown("""
    <div class="left-hero-container">
        <div class="hero-circle-accent">
            <span class="hero-logo-text">ML</span>
        </div>
        <div class="hero-title">Welcome to Student Portal</div>
        <div class="hero-subtitle">Govt Boys Higher Secondary School Tando Bago</div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class="right-portal-card">
        <div class="form-header-title">Search Student Record</div>
        <div class="form-header-sub">Please enter exam details to view academic progress certificate</div>
    </div>
    """, unsafe_allow_html=True)

    test_input = st.text_input(
        "Enter Test Code:",
        placeholder="e.g., A4-25-01",
        help="Format: [Month Letter][1-12]-[Year]-[Number] — e.g. A4-25-01 for April, test 4, 2025, sheet 01"
    )

    if test_input:
        cleaned_test = test_input.strip().upper()
        
        if validate_test_number(cleaned_test):
            file_name = f"{cleaned_test}.xlsx"
            
            if os.path.exists(file_name):
                st.success(f"✓ Active Exam Session: {cleaned_test}")
                
                scan_tab1, scan_tab2 = st.tabs([" Camera Scan", "️ Upload Picture"])
                scanned_serial = ""

                with scan_tab1:
                    cam_img = st.camera_input("Scan Barcode")
                    if cam_img:
                        pil_img = Image.open(cam_img)
                        found_code = decode_barcode_image(pil_img)
                        if found_code:
                            scanned_serial = found_code
                            st.success(f"✓ Detected: {scanned_serial}")
                        elif not BARCODE_AVAILABLE:
                            st.warning("⚠️ Barcode scanning is unavailable right now. Please type the serial number below instead.")
                        else:
                            st.warning("⚠️ No barcode detected in frame. Try moving closer or improving lighting, or type it below.")

                with scan_tab2:
                    uploaded_img = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "webp"])
                    if uploaded_img:
                        pil_img = Image.open(uploaded_img)
                        found_code = decode_barcode_image(pil_img)
                        if found_code:
                            scanned_serial = found_code
                            st.success(f"✓ Detected: {scanned_serial}")
                        elif not BARCODE_AVAILABLE:
                            st.warning("⚠️ Barcode scanning is unavailable right now. Please type the serial number below instead.")
                        else:
                            st.warning("⚠️ Could not read barcode from image. Try a clearer photo, or type it below.")

                default_serial = scanned_serial if scanned_serial else ""
                serial_input = st.text_input(
                    "Enter or Confirm Serial Number:",
                    value=default_serial,
                    placeholder="e.g., MGM75000002",
                    help="Printed on the exam booklet's barcode label. Not case-sensitive."
                )
                
                if serial_input:
                    cleaned_serial = serial_input.strip().upper()
                    
                    try:
                        df = pd.read_excel(file_name)
                        df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')

                        serial_col = get_excel_column(df, ['serial_number', 'serialnumber', 'serial no', 'serial'])

                        if serial_col:
                            result = df[df[serial_col].astype(str).str.strip().str.upper() == cleaned_serial]
                            
                            if len(result) > 0:
                                raw_row = result.iloc[0].to_dict()
                                student_row = {
                                    k: ("N/A" if pd.isna(v) else str(v).strip()) 
                                    for k, v in raw_row.items()
                                }
                                
                                generate_report_card(
                                    serial_no=cleaned_serial,
                                    test_no=cleaned_test,
                                    student_data=student_row
                                )
                            else:
                                st.error(f"❌ Serial Number '{cleaned_serial}' not found in Test {cleaned_test}.")
                        else:
                            st.error(f"❌ Excel file missing a recognizable serial number column. Found columns: {', '.join(df.columns)}")
                    except Exception as e:
                        st.error(f"Error reading spreadsheet: {e}")
            else:
                st.error(f"❌ Test file '{file_name}' not found in repository.")
        else:
            st.error("❌ Invalid Test Code format! Use format like: A4-25-01, J6-26-01")

