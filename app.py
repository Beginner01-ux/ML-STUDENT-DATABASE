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

# ===== INJECT FULL-PAGE CANVAS & EXECUTIVE BRANDING DIRECTLY INTO PARENT DOM =====
parent_injection_code = """
<script>
    (function() {
        const parentDoc = window.parent.document;
        
        // Hide default Streamlit whitespace padding for true full-width feel
        const mainBlock = parentDoc.querySelector('.main .block-container');
        if (mainBlock) {
            mainBlock.style.paddingTop = '1.5rem';
            mainBlock.style.paddingBottom = '2rem';
            mainBlock.style.maxWidth = '600px';
        }

        // Create canvas on the PARENT body if it doesn't exist
        let canvas = parentDoc.getElementById('global-particle-canvas');
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'global-particle-canvas';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '-1';
            canvas.style.pointerEvents = 'none';
            canvas.style.background = '#06090e';
            parentDoc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.parent.innerWidth;
                canvas.height = window.parent.innerHeight;
            }
            window.parent.addEventListener('resize', resize);
            resize();

            const particles = [];
            const particleCount = Math.min(40, Math.floor(window.parent.innerWidth / 10));
            let mouse = { x: null, y: null, radius: 140 };

            window.parent.addEventListener('mousemove', (e) => {
                mouse.x = e.clientX;
                mouse.y = e.clientY;
            });

            window.parent.addEventListener('touchmove', (e) => {
                if(e.touches.length > 0) {
                    mouse.x = e.touches[0].clientX;
                    mouse.y = e.touches[0].clientY;
                }
            }, { passive: true });

            class Particle {
                constructor() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.vx = (Math.random() - 0.5) * 0.5;
                    this.vy = (Math.random() - 0.5) * 0.5;
                    this.radius = Math.random() * 1.6 + 1;
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
                    ctx.fillStyle = 'rgba(234, 179, 8, 0.75)';
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

                        if (dist < 115) {
                            ctx.beginPath();
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.strokeStyle = `rgba(234, 179, 8, ${0.2 * (1 - dist / 115)})`;
                            ctx.lineWidth = 0.6;
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
components.html(parent_injection_code, height=0)

# ===== EXECUTIVE BRANDING HEADER (NATIVE STREAMLIT COMPONENT) =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Playfair+Display:wght@700;800&family=Space+Mono:wght@700&family=Inter:wght@400;600&display=swap');

    .portal-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }

    /* Professional Executive Crest Logo */
    .brand-crest {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 72px;
        height: 72px;
        border-radius: 50%;
        border: 1.5px solid #eab308;
        background: radial-gradient(circle, rgba(30, 41, 59, 0.8) 0%, rgba(6, 9, 14, 0.95) 100%);
        box-shadow: 0 0 25px rgba(234, 179, 8, 0.25), inset 0 0 10px rgba(234, 179, 8, 0.15);
        margin-bottom: 12px;
    }

    .brand-initials {
        font-family: 'Cinzel', serif;
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(180deg, #ffffff 0%, #facc15 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
        line-height: 1;
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        color: #ffffff;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0 4px 12px rgba(0,0,0,0.9);
    }

    .sub-title {
        font-family: 'Space Mono', monospace;
        color: #eab308;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 6px;
        font-weight: 700;
    }
</style>

<div class="portal-header">
    <div class="brand-crest">
        <span class="brand-initials">ML</span>
    </div>
    <div class="main-title">Student Results Portal</div>
    <div class="sub-title">Govt Boys Higher Secondary School Tando Bago</div>
</div>
""", unsafe_allow_html=true)

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

# ===== FULL-PAGE DYNAMIC MARKSHEET GENERATOR =====
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
                margin: 0;
                padding: 0;
            }}

            .marksheet-card {{
                background: linear-gradient(165deg, #0e1422 0%, #070a12 100%);
                color: #ffffff;
                width: 100%;
                border: 1px solid #1e293b;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
            }}

            .card-top {{
                border-bottom: 1px solid #1e293b;
                padding-bottom: 14px;
                margin-bottom: 18px;
            }}

            .card-sub-title {{
                font-family: 'Space Mono', monospace;
                color: #eab308;
                font-size: 9px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}

            .student-headline {{
                font-family: 'Playfair Display', serif;
                font-size: 24px;
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
                gap: 10px;
                margin-bottom: 16px;
            }}

            .metric-card {{
                background: rgba(20, 27, 45, 0.7);
                border: 1px solid #1e293b;
                border-radius: 10px;
                padding: 12px;
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
                font-size: 24px;
                font-weight: 800;
                margin-top: 2px;
            }}

            .details-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                margin-bottom: 18px;
            }}

            .grid-item {{
                background: rgba(15, 22, 35, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-left: 3px solid #eab308;
                padding: 8px 10px;
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
                font-size: 12px;
                font-weight: 700;
                margin-top: 2px;
            }}

            .accuracy-section {{
                background: rgba(15, 22, 35, 0.8);
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 14px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 18px;
            }}

            .circular-gauge {{
                width: 65px;
                height: 65px;
                border-radius: 50%;
                background: conic-gradient(#facc15 {pct_num * 3.6}deg, #1e293b 0deg);
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .gauge-center {{
                width: 51px;
                height: 51px;
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
                font-size: 13px;
            }}

            .gauge-sub {{
                color: #eab308;
                font-size: 6.5px;
                font-family: 'Space Mono', monospace;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
                color: #000000;
                border: none;
                padding: 12px;
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
                <span class="card-sub-title">OFFICIAL ACADEMIC PROGRESS REPORT</span>
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
                    <div style="font-family: 'Space Mono', monospace; color: #94a3b8; font-size: 8.5px; text-transform: uppercase;">Performance Accuracy</div>
                    <div style="color: #ffffff; font-size: 15px; font-weight: 800; margin-top: 2px;">Subject Mastery Level</div>
                    <div style="color: #eab308; font-size: 10.5px; margin-top: 2px; font-weight: 600;">Status: Verified Record</div>
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
    components.html(card_html, height=560, scrolling=False)

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

