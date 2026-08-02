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

# ===== OFFICIAL HD GOLDEN SHIELD SVG LOGO =====
SVG_LOGO_CODE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" style="width:100%; height:100%; max-width:160px; max-height:160px; display:block; margin:0 auto;">
  <defs>
    <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE55C" />
      <stop offset="50%" stop-color="#FACC15" />
      <stop offset="100%" stop-color="#854D0E" />
    </linearGradient>
    <linearGradient id="goldBright" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#A16207" />
      <stop offset="50%" stop-color="#FDE047" />
      <stop offset="100%" stop-color="#FEF08A" />
    </linearGradient>
    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  <path d="M 160,15 L 50,65 L 50,190 L 160,255 L 270,190 L 270,65 Z" fill="#0f172a" stroke="url(#goldGradient)" stroke-width="6" filter="url(#goldGlow)"/>
  <path d="M 160,28 L 63,73 L 63,182 L 160,238 L 257,182 L 257,73 Z" fill="none" stroke="url(#goldGradient)" stroke-width="2"/>
  <path d="M 95,110 L 115,110 L 115,170 L 132,138 L 150,170 L 150,110 L 168,110 L 168,190 L 150,190 L 132,158 L 115,190 L 95,190 Z" fill="url(#goldBright)"/>
  <path d="M 190,110 L 210,110 L 210,172 L 235,172 L 235,190 L 190,190 Z" fill="url(#goldBright)"/>
  <path d="M 30,225 L 290,225 L 270,275 L 50,275 Z" fill="url(#goldGradient)" stroke="#713F12" stroke-width="2"/>
  <text x="160" y="258" font-family="sans-serif" font-weight="900" font-size="20" fill="#0b1329" text-anchor="middle" letter-spacing="3">MANISH LOHANA</text>
</svg>
"""

# ===== STYLING & RESPONSIVE GRID CSS =====
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #0f172a;
        overflow-x: hidden;
    }
    .main .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        align-items: stretch !important;
    }
    .left-hero-panel {
        background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 100%);
        border-right: 1px solid rgba(250, 204, 21, 0.2);
        min-height: 100vh;
        padding: 40px 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #ffffff;
        position: relative;
        overflow: hidden;
    }
    .right-input-panel {
        background: #111827;
        min-height: 100vh;
        padding: 40px 30px;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        .left-hero-panel {
            min-height: auto;
            padding: 30px 15px;
        }
        .right-input-panel {
            min-height: auto;
            padding: 30px 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== LIGHTWEIGHT HTML5 CANVAS BACKGROUND (Molecules & Math Glyphs) =====
interactive_canvas_js = """
<script>
    (function() {
        const parentDoc = window.parent.document;
        let canvas = parentDoc.getElementById('portal-interactive-canvas');
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'portal-interactive-canvas';
            canvas.style.position = 'absolute';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            canvas.style.zIndex = '1';
            canvas.style.pointerEvents = 'none';
            
            const cols = parentDoc.querySelectorAll('[data-testid="column"]');
            if (cols.length > 0) {
                cols[0].style.position = 'relative';
                cols[0].style.overflow = 'hidden';
                cols[0].insertBefore(canvas, cols[0].firstChild);
            }

            const ctx = canvas.getContext('2d');
            function resizeCanvas() {
                if (cols.length > 0) {
                    canvas.width = cols[0].clientWidth;
                    canvas.height = cols[0].clientHeight;
                }
            }
            window.parent.addEventListener('resize', resizeCanvas);
            resizeCanvas();

            const particles = [];
            const symbols = ['H₂O', 'NaCl', 'CO₂', 'α', 'β', 'Ω', '∫', 'λ', 'π', 'Δ', 'C₆H₁₂O₆'];
            for (let i = 0; i < 20; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                    text: symbols[Math.floor(Math.random() * symbols.length)]
                });
            }

            function animateParticles() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                resizeCanvas();
                particles.forEach(p => {
                    p.x += p.vx;
                    p.y += p.vy;
                    if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                    if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                    
                    ctx.font = '12px sans-serif';
                    ctx.fillStyle = 'rgba(250, 204, 21, 0.2)';
                    ctx.fillText(p.text, p.x, p.y);
                });
                requestAnimationFrame(animateParticles);
            }
            animateParticles();
        }
    })();
</script>
"""
components.html(interactive_canvas_js, height=0)

# ===== HELPER UTILITIES =====
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
        return f"{int(round(f_val))}%"
    except Exception:
        return "0%"

# ===== PRINT-READY A4 CERTIFICATE WITH GRAPHS =====
def generate_report_card(serial_no, test_no, student_data):
    name = student_data.get('name', 'N/A')
    father_name = student_data.get('father_name', 'N/A')
    roll_no = student_data.get('roll_no', 'N/A')
    test_score = student_data.get('test_score', '0')
    subject = student_data.get('subject', 'CHEMISTRY')
    percentage_str = format_percentage(student_data.get('percentage', '0'))
    cls = student_data.get('class', 'X')
    rank = student_data.get('class_rank', 'N/A')
    section = student_data.get('section', 'A')

    certificate_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
            @page {{ size: A4 portrait; margin: 0; }}
            body {{ margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; background: #0b1329; color: #fff; }}
            .cert-page {{ 
                width: 210mm; 
                height: 297mm; 
                max-width: 100%;
                margin: 0 auto;
                background: linear-gradient(135deg, #0b1329 0%, #1e1b4b 100%);
                border: 4px solid #facc15; 
                padding: 40px; 
                display: flex; 
                flex-direction: column; 
                justify-content: space-between;
            }}
            .header {{ text-align: center; }}
            .school-title {{ font-size: 15px; font-weight: bold; color: #facc15; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; }}
            .cert-title {{ font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 5px; }}
            .student-info-box {{ background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(250, 204, 21, 0.3); border-radius: 12px; padding: 18px; text-align: center; margin: 15px 0; }}
            .student-name {{ font-size: 26px; font-weight: bold; color: #facc15; margin-bottom: 5px; }}
            .student-details {{ font-size: 13px; color: #cbd5e1; }}
            .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 15px 0; }}
            .metric-card {{ background: rgba(30, 41, 59, 0.9); border: 1px solid #facc15; border-radius: 10px; padding: 12px; text-align: center; }}
            .metric-val {{ font-size: 20px; font-weight: bold; color: #facc15; }}
            .metric-lbl {{ font-size: 9px; color: #94a3b8; text-transform: uppercase; margin-top: 4px; }}
            .graph-section {{ background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 15px; border: 1px solid rgba(255,255,255,0.1); margin: 10px 0; }}
            .graph-title {{ font-size: 13px; font-weight: bold; color: #facc15; margin-bottom: 10px; text-transform: uppercase; }}
            .bar-container {{ background: #334155; border-radius: 6px; height: 16px; width: 100%; overflow: hidden; }}
            .bar-fill {{ background: linear-gradient(90deg, #eab308, #facc15); height: 100%; width: {percentage_str}; border-radius: 6px; }}
            .footer-info {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #64748b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 12px; }}
            .print-btn {{ background: #facc15; color: #000; border: none; padding: 12px 25px; font-weight: bold; border-radius: 8px; cursor: pointer; text-transform: uppercase; font-size: 13px; display: block; width: 100%; margin-top: 12px; }}
            @media print {{
                body {{ background: #0b1329 !important; }}
                .print-btn {{ display: none !important; }}
                .cert-page {{ border: none; height: 100vh; width: 100vw; padding: 20px; }}
            }}
        </style>
    </head>
    <body>
        <div class="cert-page">
            <div class="header">
                {SVG_LOGO_CODE}
                <div class="school-title">Govt Boys Higher Secondary School Tando Bago</div>
                <div class="cert-title">Academic Progress Certificate</div>
            </div>
            <div class="student-info-box">
                <div class="student-name">{name}</div>
                <div class="student-details">Father's Name: <b>{father_name}</b> &nbsp;|&nbsp; Class: <b>{cls}-{section}</b> &nbsp;|&nbsp; Roll No: <b>{roll_no}</b></div>
            </div>
            <div class="metrics-grid">
                <div class="metric-card"><div class="metric-val">{test_score}</div><div class="metric-lbl">Total Score</div></div>
                <div class="metric-card"><div class="metric-val">{percentage_str}</div><div class="metric-lbl">Percentage</div></div>
                <div class="metric-card"><div class="metric-val">#{rank}</div><div class="metric-lbl">Class Rank</div></div>
                <div class="metric-card"><div class="metric-val" style="font-size: 14px; padding-top: 4px;">{subject}</div><div class="metric-lbl">Subject</div></div>
            </div>
            <div class="graph-section">
                <div class="graph-title">Performance Accuracy Graph ({percentage_str})</div>
                <div class="bar-container"><div class="bar-fill"></div></div>
            </div>
            <div>
                <div class="footer-info">
                    <span>Test Code: <b>{test_no}</b></span>
                    <span>Serial: <b>{serial_no}</b></span>
                    <span>Verified Official Document</span>
                </div>
                <button class="print-btn" onclick="window.print()">️ Download Full-Page A4 PDF Certificate</button>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(certificate_html, height=720, scrolling=False)

# ===== MAIN APPLICATION LAYOUT =====
left_col, right_col = st.columns([1, 1], gap="small")

with left_col:
    st.markdown('<div class="left-hero-panel">', unsafe_allow_html=True)
    st.markdown(f'<div style="position:relative; z-index:2; width:100%;">{SVG_LOGO_CODE}</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:clamp(22px, 3.5vw, 32px); font-weight:800; margin:20px 0 5px 0; position:relative; z-index:2;">Student Results Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:clamp(10px, 1.8vw, 12px); letter-spacing:1.5px; text-transform:uppercase; color:#facc15; font-weight:700; position:relative; z-index:2; margin:0;">Govt Boys Higher Secondary School Tando Bago</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="right-input-panel">', unsafe_allow_html=True)
    st.subheader("Search Student Record")
    st.caption("Enter exam details to view academic progress certificate")

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
                            st.warning("⚠️ No barcode detected.")

                with scan_tab2:
                    uploaded_img = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "webp"])
                    if uploaded_img:
                        pil_img = Image.open(uploaded_img)
                        found_code = decode_barcode_image(pil_img)
                        if found_code:
                            scanned_serial = found_code
                            st.success(f"✓ Detected: {scanned_serial}")
                        else:
                            st.warning("⚠️ Could not read barcode.")

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
                                student_row = {k: ("N/A" if pd.isna(v) else str(v).strip()) for k, v in raw_row.items()}
                                generate_report_card(serial_no=cleaned_serial, test_no=cleaned_test, student_data=student_row)
                            else:
                                st.error(f"❌ Serial Number '{cleaned_serial}' not found in Test {cleaned_test}.")
                        else:
                            st.error("❌ Excel file missing 'serial_number' column header.")
                    except Exception as e:
                        st.error(f"Error reading spreadsheet: {e}")
            else:
                st.error(f"❌ Test file '{file_name}' not found.")
        else:
            st.error("❌ Invalid Test Code format! Use format like: A4-25-01")

    st.markdown('</div>', unsafe_allow_html=True)

