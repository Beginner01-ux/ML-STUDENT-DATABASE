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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== INJECT SPLIT-SCREEN LAYOUT & LEFT CANVAS =====
split_layout_html = """
<script>
    (function() {
        const parentDoc = window.parent.document;

        // Force Streamlit body to full-width split container
        const mainBlock = parentDoc.querySelector('.main .block-container');
        if (mainBlock) {
            mainBlock.style.maxWidth = '100vw';
            mainBlock.style.padding = '0';
            mainBlock.style.margin = '0';
        }

        // Create background canvas for Left 50% Visual Area
        let canvas = parentDoc.getElementById('split-canvas-bg');
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'split-canvas-bg';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '50vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '0';
            canvas.style.pointerEvents = 'none';
            canvas.style.background = 'radial-gradient(circle at 50% 50%, #1e1b4b 0%, #0f172a 100%)';
            parentDoc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.parent.innerWidth * 0.5;
                canvas.height = window.parent.innerHeight;
            }
            window.parent.addEventListener('resize', resize);
            resize();

            // Interactive 3D Molecules, Nodes, & Floating Academic Glyphs
            const elements = [];
            const glyphs = ['α', 'β', 'Ω', '∫', 'æ', 'θ', 'λ', '∑', 'ð'];
            const elementCount = 42;
            let mouse = { x: null, y: null, radius: 150 };

            window.parent.addEventListener('mousemove', (e) => {
                if (e.clientX <= window.parent.innerWidth * 0.5) {
                    mouse.x = e.clientX;
                    mouse.y = e.clientY;
                } else {
                    mouse.x = null;
                    mouse.y = null;
                }
            });

            class FloatingElement {
                constructor() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.vx = (Math.random() - 0.5) * 0.6;
                    this.vy = (Math.random() - 0.5) * 0.6;
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
                            this.x -= (dx / dist) * force * 2;
                            this.y -= (dy / dist) * force * 2;
                        }
                    }
                }

                draw() {
                    ctx.save();
                    ctx.translate(this.x, this.y);
                    ctx.rotate(this.angle);

                    if (this.type === 0) {
                        // Interactive Node
                        ctx.beginPath();
                        ctx.arc(0, 0, 3.5, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(250, 204, 21, 0.85)';
                        ctx.shadowBlur = 10;
                        ctx.shadowColor = '#facc15';
                        ctx.fill();
                    } else if (this.type === 1) {
                        // 3D Molecular Structure
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
                        // Floating Glyph
                        ctx.font = '14px Space Mono, monospace';
                        ctx.fillStyle = 'rgba(192, 132, 252, 0.7)';
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

                        if (dist < 110) {
                            ctx.beginPath();
                            ctx.moveTo(elements[i].x, elements[i].y);
                            ctx.lineTo(elements[j].x, elements[j].y);
                            ctx.strokeStyle = `rgba(250, 204, 21, ${0.15 * (1 - dist / 110)})`;
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
components.html(split_layout_html, height=0)

# ===== GLOBAL STYLING OVERRIDES =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

    /* Dark Theme Background */
    [data-testid="stAppViewContainer"] {
        background-color: #030712;
    }

    /* Left Hero Panel */
    .left-hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 85vh;
        text-align: center;
        padding: 40px;
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
        z-index: 2;
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

    /* Right Form Container Card */
    .right-portal-card {
        background: #0b1329;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        margin-top: 20px;
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

    /* Input Overrides */
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

# ===== A4 CERTIFICATE & MARKSHEET GENERATOR =====
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
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

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

            @media print {{
                html, body {{
                    background: #ffffff !important;
                    margin: 0 !important;
                }}
                .cert-container {{
                    box-shadow: none !important;
                    border: 3px solid #b45309 !important;
                    background: #090d16 !important;
                    width: 100% !important;
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
    components.html(certificate_html, height=540, scrolling=False)

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

