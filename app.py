import streamlit as st
import pandas as pd
import re
import os
from PIL import Image
import zxingcpp
import streamlit.components.v1 as components

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Student Results Portal | Manish Lohana",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== INLINE SVG VECTOR LOGO (MANISH LOHANA CREST) =====
MANISH_LOHANA_SVG_LOGO = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 310" class="vector-logo-svg">
  <defs>
    <!-- Metallic Gold Gradient -->
    <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF099" />
      <stop offset="30%" stop-color="#FACC15" />
      <stop offset="70%" stop-color="#EAB308" />
      <stop offset="100%" stop-color="#A16207" />
    </linearGradient>
    
    <linearGradient id="goldBright" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#CA8A04" />
      <stop offset="50%" stop-color="#FDE047" />
      <stop offset="100%" stop-color="#FEF08A" />
    </linearGradient>

    <!-- Subtle Glow Filter -->
    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Top Diamond Finial Accent -->
  <polygon points="150,8 159,20 150,32 141,20" fill="url(#goldGradient)" filter="url(#goldGlow)"/>

  <!-- Main Outer Book/Shield Frame -->
  <path d="M 150,42 
           L 40,90 
           L 40,205 
           L 150,265 
           L 260,205 
           L 260,90 
           Z 
           M 150,66 
           L 242,106 
           L 242,194 
           L 150,244 
           L 58,194 
           L 58,106 
           Z" 
        fill="url(#goldGradient)" 
        fill-rule="evenodd" filter="url(#goldGlow)"/>

  <!-- Central Vertical Spine Line -->
  <line x1="150" y1="42" x2="150" y2="244" stroke="url(#goldGradient)" stroke-width="4" stroke-linecap="round"/>

  <!-- Left Inner "M" Geometry -->
  <path d="M 72,110 L 96,110 L 96,178 L 115,142 L 132,178 L 132,110 L 145,110 L 145,198 L 132,198 L 115,164 L 98,198 L 72,198 Z" 
        fill="url(#goldBright)"/>

  <!-- Right Inner "L" Geometry -->
  <path d="M 174,110 L 194,110 L 194,180 L 232,180 L 232,198 L 174,198 Z" 
        fill="url(#goldBright)"/>

  <!-- Angled Text "MANISH" (Left Lower Frame) -->
  <g transform="translate(150, 260) rotate(-28.5)">
    <text x="-95" y="15" 
          font-family="'Space Grotesk', 'Arial Black', sans-serif" 
          font-weight="900" 
          font-size="18" 
          fill="#FFFFFF" 
          letter-spacing="2">MANISH</text>
  </g>

  <!-- Angled Text "LOHANA" (Right Lower Frame) -->
  <g transform="translate(150, 260) rotate(28.5)">
    <text x="18" y="15" 
          font-family="'Space Grotesk', 'Arial Black', sans-serif" 
          font-weight="900" 
          font-size="18" 
          fill="#FFFFFF" 
          letter-spacing="2">LOHANA</text>
  </g>
</svg>
"""

# ===== INJECT DYNAMIC RESPONSIVE CANVAS SCRIPT =====
responsive_canvas_html = """
<script>
    (function() {
        const parentDoc = window.parent.document;

        // Force Streamlit body to dynamic responsive container
        const mainBlock = parentDoc.querySelector('.main .block-container');
        if (mainBlock) {
            mainBlock.style.maxWidth = '100vw';
            mainBlock.style.padding = '0';
            mainBlock.style.margin = '0';
        }

        // Background canvas for interactive left side floating particles & nodes
        let canvas = parentDoc.getElementById('responsive-canvas-bg');
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'responsive-canvas-bg';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.zIndex = '0';
            canvas.style.pointerEvents = 'none';
            canvas.style.background = 'radial-gradient(circle at 50% 50%, #1e1b4b 0%, #0f172a 100%)';
            parentDoc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            function resize() {
                const width = window.parent.innerWidth;
                if (width > 768) {
                    canvas.width = width * 0.5; // Exactly left 50% on Desktop
                } else {
                    canvas.width = width;       // 100% full width on Mobile
                }
                canvas.height = window.parent.innerHeight;
            }
            window.parent.addEventListener('resize', resize);
            resize();

            // Interactive Floating Physics Elements (Glyphs & Molecular Nodes)
            const elements = [];
            const glyphs = ['α', 'β', 'Ω', '∫', 'æ', 'θ', 'λ', '∑', 'ð', 'π', 'Δ'];
            const elementCount = 42;
            let mouse = { x: null, y: null, radius: 140 };

            window.parent.addEventListener('mousemove', (e) => {
                mouse.x = e.clientX;
                mouse.y = e.clientY;
            });

            class FloatingElement {
                constructor() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.vx = (Math.random() - 0.5) * 0.7;
                    this.vy = (Math.random() - 0.5) * 0.7;
                    this.type = Math.floor(Math.random() * 3);
                    this.glyph = glyphs[Math.floor(Math.random() * glyphs.length)];
                    this.angle = Math.random() * Math.PI * 2;
                    this.spin = (Math.random() - 0.5) * 0.02;
                }

                update() {
                    this.x += this.vx;
                    this.y += this.vy;
                    this.angle += this.spin;

                    if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                    if (this.y < 0 || this.y > canvas.height) this.vy *= -1;

                    if (mouse.x !== null) {
                        let dx = mouse.x - this.x;
                        let dy = mouse.y - this.y;
                        let dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist < mouse.radius) {
                            let force = (mouse.radius - dist) / mouse.radius;
                            this.x -= (dx / dist) * force * 2.5;
                            this.y -= (dy / dist) * force * 2.5;
                        }
                    }
                }

                draw() {
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    ctx.rotate(this.angle);

                    if (this.type === 0) {
                        ctx.beginPath();
                        ctx.arc(0, 0, 3.5, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(250, 204, 21, 0.85)';
                        ctx.shadowBlur = 10;
                        ctx.shadowColor = '#facc15';
                        ctx.fill();
                    } else if (this.type === 1) {
                        ctx.beginPath();
                        ctx.arc(0, 0, 4.5, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(244, 63, 94, 0.9)';
                        ctx.fill();

                        for (let i = 0; i < 3; i++) {
                            let bAngle = (i * Math.PI * 2 / 3);
                            let bx = Math.cos(bAngle) * 14;
                            let by = Math.sin(bAngle) * 14;

                            ctx.beginPath();
                            ctx.moveTo(0, 0);
                            ctx.lineTo(bx, by);
                            ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
                            ctx.lineWidth = 1;
                            ctx.stroke();

                            ctx.beginPath();
                            ctx.arc(bx, by, 2.5, 0, Math.PI * 2);
                            ctx.fillStyle = 'rgba(56, 189, 248, 0.85)';
                            ctx.fill();
                        }
                    } else {
                        ctx.font = '15px Space Mono, monospace';
                        ctx.fillStyle = 'rgba(192, 132, 252, 0.75)';
                        ctx.fillText(this.glyph, 0, 0);
                    }

                    ctx.restore();
                }
            }

            for (let i = 0; i < elementCount; i++) {
                elements.push(new FloatingElement());
            }

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                for (let i = 0; i < elements.length; i++) {
                    elements[i].update();
                    elements[i].draw();

                    for (let j = i + 1; j < elements.length; j++) {
                        let dx = elements[i].x - elements[j].x;
                        let dy = elements[i].y - elements[j].y;
                        let dist = Math.sqrt(dx * dx + dy * dy);

                        if (dist < 100) {
                            ctx.beginPath();
                            ctx.moveTo(elements[i].x, elements[i].y);
                            ctx.lineTo(elements[j].x, elements[j].y);
                            ctx.strokeStyle = `rgba(250, 204, 21, ${0.15 * (1 - dist / 100)})`;
                            ctx.lineWidth = 0.5;
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
components.html(responsive_canvas_html, height=0)

# ===== GLOBAL RESPONSIVE STYLING (CSS) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@600;700;900&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #030712;
        overflow-x: hidden;
    }

    /* Left Interactive Hero Panel Container */
    .left-hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 85vh;
        text-align: center;
        padding: 20px;
        position: relative;
        z-index: 1;
    }

    /* Dynamic Vector Logo Box */
    .logo-hero-box {
        width: 220px;
        height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 24px;
        filter: drop-shadow(0px 10px 25px rgba(250, 204, 21, 0.35));
        transition: transform 0.3s ease;
    }

    .logo-hero-box:hover {
        transform: scale(1.06);
    }

    .vector-logo-svg {
        width: 100%;
        height: 100%;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 6px;
    }

    /* Right Portal Search Card */
    .right-portal-card {
        background: #0b1329;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        margin-top: 20px;
        position: relative;
        z-index: 1;
    }

    .form-header-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .form-header-sub {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 20px;
    }

    /* Custom Input Controls */
    .stTextInput > div > div {
        background-color: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #facc15 !important;
        box-shadow: 0 0 12px rgba(250, 204, 21, 0.25) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background-color: #facc15 !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* Mobile Responsive Rules */
    @media screen and (max-width: 768px) {
        .left-hero-container {
            min-height: auto;
            padding: 20px 10px 10px 10px;
        }

        .logo-hero-box {
            width: 150px;
            height: 150px;
            margin-bottom: 14px;
        }

        .hero-title {
            font-size: 20px;
        }

        .hero-subtitle {
            font-size: 10px;
        }

        .right-portal-card {
            padding: 18px 14px;
            margin-top: 10px;
        }

        #responsive-canvas-bg {
            width: 100vw !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== UTILITY FUNCTIONS =====
def validate_test_number(test_no):
    pattern = r'^[JFMASONDjfsond](1[0-2]|[1-9])-\d{2}-\d{2}$'
    return bool(re.match(pattern, test_no.strip()))

def decode_barcode_image(pil_image):
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
        return f"{int(round(f_val))}%", f_val
    except Exception:
        return "0%", 0.0

# ===== A4 CERTIFICATE & FULL-PAGE MARKSHEET GENERATOR =====
def generate_report_card(serial_no, test_no, student_data):
    name = student_data.get('name', 'N/A')
    father_name = student_data.get('father_name', 'N/A')
    roll_no = student_data.get('roll_no', 'N/A')
    test_score = student_data.get('test_score', '0')
    subject = student_data.get('subject', 'CHEMISTRY')
    percentage_str, pct_num = format_percentage(student_data.get('percentage', '0'))
    cls = student_data.get('class', 'X')
    rank = student_data.get('class_rank', 'N/A')
    section = student_data.get('section', 'A')

    certificate_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;900&display=swap');

            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                box-sizing: border-box;
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
                padding: 24px;
                box-shadow: 0 25px 60px rgba(0,0,0,0.85);
            }}

            .cert-border-inner {{
                border: 1px solid rgba(234, 179, 8, 0.4);
                border-radius: 12px;
                padding: 20px;
                background: radial-gradient(circle at center, rgba(30, 41, 59, 0.25) 0%, rgba(3, 7, 18, 0.45) 100%);
            }}

            .cert-header {{
                text-align: center;
                border-bottom: 1px solid rgba(234, 179, 8, 0.25);
                padding-bottom: 14px;
                margin-bottom: 16px;
            }}

            .cert-crest-svg {{
                width: 65px;
                height: 65px;
                margin: 0 auto 6px auto;
            }}

            .institution-name {{
                font-family: 'Cinzel', serif;
                font-size: 12px;
                font-weight: 700;
                color: #facc15;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin: 0;
            }}

            .cert-title {{
                font-family: 'Cinzel', serif;
                font-size: 20px;
                font-weight: 900;
                color: #ffffff;
                margin-top: 4px;
                letter-spacing: 0.5px;
            }}

            .student-section {{
                text-align: center;
                margin-bottom: 18px;
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
                font-size: 24px;
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
                gap: 10px;
                margin-bottom: 18px;
            }}

            .metric-box {{
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(234, 179, 8, 0.3);
                border-radius: 10px;
                padding: 10px 6px;
                text-align: center;
            }}

            .metric-title {{
                font-size: 8px;
                color: #94a3b8;
                text-transform: uppercase;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}

            .metric-value {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 18px;
                font-weight: 700;
                color: #facc15;
                margin-top: 4px;
            }}

            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 18px;
            }}

            .info-item {{
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-left: 4px solid #facc15;
                padding: 8px 12px;
                border-radius: 8px;
            }}

            .info-label {{
                font-size: 8px;
                color: #64748b;
                text-transform: uppercase;
                font-weight: 700;
                display: block;
            }}

            .info-val {{
                font-size: 12px;
                color: #ffffff;
                font-weight: 700;
                margin-top: 2px;
            }}

            .cert-footer {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-top: 1px solid rgba(234, 179, 8, 0.25);
                padding-top: 14px;
            }}

            .official-seal {{
                display: flex;
                align-items: center;
                gap: 10px;
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
                font-size: 8.5px;
                color: #22c55e;
                font-weight: 700;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
                color: #000000;
                border: none;
                padding: 10px 18px;
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 800;
                font-size: 11px;
                border-radius: 8px;
                cursor: pointer;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                box-shadow: 0 4px 14px rgba(250, 204, 21, 0.3);
            }}

            /* FULL-PAGE PRINT SPECIFICATIONS */
            @media print {{
                html, body {{
                    background: #ffffff !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    height: 100vh !important;
                }}
                .cert-container {{
                    box-shadow: none !important;
                    border: 4px solid #b45309 !important;
                    background: #080d1a !important;
                    width: 100% !important;
                    height: 100vh !important;
                    border-radius: 0 !important;
                    display: flex !important;
                    flex-direction: column !important;
                    justify-content: center !important;
                }}
                .print-btn {{
                    display: none !important;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="cert-container">
            <div class="cert-border-inner">
                <div class="cert-header">
                    <div class="cert-crest-svg">
                        {MANISH_LOHANA_SVG_LOGO}
                    </div>
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
    components.html(certificate_html, height=580, scrolling=False)

# ===== MAIN WEBPAGE COLUMNS =====
left_col, right_col = st.columns([1, 1], gap="medium")

with left_col:
    st.markdown(f"""
    <div class="left-hero-container">
        <div class="logo-hero-box">
            {MANISH_LOHANA_SVG_LOGO}
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

    test_input = st.text_input("Enter Test Code:", placeholder="e.g., A4-25-01")

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
                        else:
                            st.warning("⚠️ No barcode detected in frame.")

                with scan_tab2:
                    uploaded_img = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "webp"])
                    if uploaded_img:
                        pil_img = Image.open(uploaded_img)
                        found_code = decode_barcode_image(pil_img)
                        if found_code:
                            scanned_serial = found_code
                            st.success(f"✓ Detected: {scanned_serial}")
                        else:
                            st.warning("⚠️ Could not read barcode from image.")

                default_serial = scanned_serial if scanned_serial else ""
                serial_input = st.text_input("Enter or Confirm Serial Number:", value=default_serial, placeholder="e.g., MGM75000002")
                
                if serial_input:
                    cleaned_serial = serial_input.strip().upper()
                    
                    try:
                        df = pd.read_excel(file_name)
                        df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
                        
                        if 'serial_number' in df.columns:
                            result = df[df['serial_number'].astype(str).str.strip().str.upper() == cleaned_serial]
                            
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
                            st.error("❌ Excel file missing 'serial_number' column header.")
                    except Exception as e:
                        st.error(f"Error reading spreadsheet: {e}")
            else:
                st.error(f"❌ Test file '{file_name}' not found in repository.")
        else:
            st.error("❌ Invalid Test Code format! Use format like: A4-25-01, J6-26-01")

