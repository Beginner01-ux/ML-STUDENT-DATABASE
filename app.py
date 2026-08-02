import streamlit as st
import pandas as pd
import re
import os
from PIL import Image
import zxingcpp
import streamlit.components.v1 as components

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Student Results Portal | ML",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

    /* Fixed Fullscreen Canvas Background */
    #particle-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: auto;
    }

    /* Header Container Floating Above Canvas */
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

        // Mobile-Optimized Particle System
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
components.html(full_screen_bg_and_header, height=230)

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

# ===== HIGH-END ACADEMIC MARKSHEET GENERATOR =====
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

    card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Space+Mono:wght@400;700&family=Inter:wght@400;600;700;800&display=swap');

            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
                box-sizing: border-box;
            }}

            body {{
                background-color: transparent;
                font-family: 'Inter', system-ui, sans-serif;
                display: flex;
                justify-content: center;
                margin: 0;
                padding: 10px 0;
            }}

            .marksheet-card {{
                background: linear-gradient(165deg, #0e1422 0%, #070a12 100%);
                color: #ffffff;
                width: 100%;
                max-width: 520px;
                border: 1px solid #1e293b;
                border-radius: 16px;
                padding: 28px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
                position: relative;
            }}

            .card-top {{
                border-bottom: 1px solid #1e293b;
                padding-bottom: 16px;
                margin-bottom: 20px;
            }}

            .sub-title {{
                font-family: 'Space Mono', monospace;
                color: #eab308;
                font-size: 9px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}

            .student-headline {{
                font-family: 'Playfair Display', serif;
                font-size: 26px;
                font-weight: 900;
                color: #ffffff;
                margin: 4px 0 2px 0;
            }}

            .academic-meta {{
                color: #94a3b8;
                font-size: 11px;
                font-weight: 600;
            }}

            .metric-dashboard {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-bottom: 20px;
            }}

            .metric-card {{
                background: rgba(20, 27, 45, 0.7);
                border: 1px solid #1e293b;
                border-radius: 10px;
                padding: 14px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}

            .metric-label {{
                font-family: 'Space Mono', monospace;
                color: #64748b;
                font-size: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .metric-val {{
                font-family: 'Playfair Display', serif;
                color: #facc15;
                font-size: 26px;
                font-weight: 800;
                margin-top: 2px;
            }}

            .details-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 20px;
            }}

            .grid-item {{
                background: rgba(15, 22, 35, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-left: 3px solid #eab308;
                padding: 10px 12px;
                border-radius: 6px;
            }}

            .item-label {{
                font-family: 'Space Mono', monospace;
                color: #64748b;
                font-size: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: block;
            }}

            .item-val {{
                color: #ffffff;
                font-size: 13px;
                font-weight: 700;
                margin-top: 2px;
            }}

            .accuracy-section {{
                background: rgba(15, 22, 35, 0.8);
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 22px;
            }}

            .circular-gauge {{
                width: 72px;
                height: 72px;
                border-radius: 50%;
                background: conic-gradient(#facc15 {pct_num * 3.6}deg, #1e293b 0deg);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 15px rgba(250, 204, 21, 0.2);
            }}

            .gauge-center {{
                width: 58px;
                height: 58px;
                background: #080c14;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}

            .gauge-score {{
                color: #ffffff;
                font-weight: 800;
                font-size: 14px;
            }}

            .gauge-sub {{
                color: #eab308;
                font-size: 7px;
                font-family: 'Space Mono', monospace;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
                color: #000000;
                border: none;
                padding: 14px;
                font-family: 'Space Mono', monospace;
                font-weight: 700;
                font-size: 11px;
                border-radius: 8px;
                cursor: pointer;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                width: 100%;
                box-shadow: 0 4px 15px rgba(234, 179, 8, 0.3);
            }}

            @media print {{
                body {{
                    background-color: #06090e !important;
                }}
                .marksheet-card {{
                    background: #0e1422 !important;
                    border: 1px solid #1e293b !important;
                    box-shadow: none !important;
                }}
                .print-btn {{
                    display: none !important;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="marksheet-card">
            <div class="card-top">
                <span class="sub-title">OFFICIAL ACADEMIC PROGRESS REPORT</span>
                <div class="student-headline">{name}</div>
                <div class="academic-meta">Father's Name: {father_name} · Class {cls}-{section} · Seat No: {roll_no}</div>
            </div>

            <div class="metric-dashboard">
                <div class="metric-card">
                    <span class="metric-label">TOTAL SCORE OBTAINED</span>
                    <div class="metric-val">{test_score}</div>
                </div>
                <div class="metric-card">
                    <span class="metric-label">OVERALL PERCENTAGE</span>
                    <div class="metric-val">{percentage_str}</div>
                </div>
            </div>

            <div class="details-grid">
                <div class="grid-item">
                    <span class="item-label">EVALUATED SUBJECT</span>
                    <span class="item-val">{subject}</span>
                </div>
                <div class="grid-item">
                    <span class="item-label">CLASS RANK</span>
                    <span class="item-val">{rank}</span>
                </div>
                <div class="grid-item">
                    <span class="item-label">BOOK SERIAL NO</span>
                    <span class="item-val">{serial_no}</span>
                </div>
                <div class="grid-item">
                    <span class="item-label">EXAM SESSION CODE</span>
                    <span class="item-val">{test_no}</span>
                </div>
            </div>

            <div class="accuracy-section">
                <div>
                    <div style="font-family: 'Space Mono', monospace; color: #94a3b8; font-size: 9px; text-transform: uppercase;">Performance Accuracy</div>
                    <div style="color: #ffffff; font-size: 16px; font-weight: 800; margin-top: 2px;">Subject Mastery Level</div>
                    <div style="color: #eab308; font-size: 11px; margin-top: 2px; font-weight: 600;">Status: Verified Record</div>
                </div>
                <div class="circular-gauge">
                    <div class="gauge-center">
                        <span class="gauge-score">{percentage_str}</span>
                        <span class="gauge-sub">ACCURACY</span>
                    </div>
                </div>
            </div>

            <button class="print-btn" onclick="window.print()">️ Save PDF / Print Marksheet</button>
        </div>
    </body>
    </html>
    """
    components.html(card_html, height=620)

# ===== MAIN APPLICATION WORKFLOW =====
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

