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

# ===== HIGH-DEFINITION GOLDEN LOGO (SVG) =====
SVG_LOGO_CODE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 310" style="width:100%; height:100%; max-width:180px; max-height:180px;">
  <defs>
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
    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  <polygon points="150,8 159,20 150,32 141,20" fill="url(#goldGradient)" filter="url(#goldGlow)"/>
  <path d="M 150,42 L 40,90 L 40,205 L 150,265 L 260,205 L 260,90 Z M 150,66 L 242,106 L 242,194 L 150,244 L 58,194 L 58,106 Z" 
        fill="url(#goldGradient)" fill-rule="evenodd" filter="url(#goldGlow)"/>
  <line x1="150" y1="42" x2="150" y2="244" stroke="url(#goldGradient)" stroke-width="4" stroke-linecap="round"/>
  <path d="M 72,110 L 96,110 L 96,178 L 115,142 L 132,178 L 132,110 L 145,110 L 145,198 L 132,198 L 115,164 L 98,198 L 72,198 Z" fill="url(#goldBright)"/>
  <path d="M 174,110 L 194,110 L 194,180 L 232,180 L 232,198 L 174,198 Z" fill="url(#goldBright)"/>
  <g transform="translate(150, 260) rotate(-28.5)">
    <text x="-95" y="15" font-family="sans-serif" font-weight="900" font-size="18" fill="#FFFFFF" letter-spacing="2">MANISH</text>
  </g>
  <g transform="translate(150, 260) rotate(28.5)">
    <text x="18" y="15" font-family="sans-serif" font-weight="900" font-size="18" fill="#FFFFFF" letter-spacing="2">LOHANA</text>
  </g>
</svg>
"""

# ===== RESPONSIVE SPLIT-SCREEN STYLES =====
st.markdown("""
<style>
    /* Global Layout Settings */
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

    /* Left Panel (Vibrant Hero Theme inspired by reference design) */
    .left-panel-container {
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
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

    /* Right Panel (Dark Functional Input Theme) */
    .right-panel-container {
        background: #111827;
        min-height: 100vh;
        padding: 40px 30px;
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* Responsive Mobile Overrides */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        .left-panel-container {
            min-height: auto;
            padding: 30px 15px;
        }
        .right-panel-container {
            min-height: auto;
            padding: 30px 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== INTERACTIVE FLOATING CANVAS BACKGROUND (Left Panel Physics) =====
canvas_js = """
<script>
    (function() {
        const parentDoc = window.parent.document;
        let canvas = parentDoc.getElementById('interactive-hero-canvas');
        
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'interactive-hero-canvas';
            canvas.style.position = 'absolute';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            canvas.style.zIndex = '1';
            canvas.style.pointerEvents = 'none';
            
            // Find left column container to append canvas into
            const cols = parentDoc.querySelectorAll('[data-testid="column"]');
            if (cols.length > 0) {
                cols[0].style.position = 'relative';
                cols[0].style.overflow = 'hidden';
                cols[0].insertBefore(canvas, cols[0].firstChild);
            }

            const ctx = canvas.getContext('2d');

            function resize() {
                if (cols.length > 0) {
                    canvas.width = cols[0].clientWidth;
                    canvas.height = cols[0].clientHeight;
                }
            }
            window.parent.addEventListener('resize', resize);
            resize();

            const elements = [];
            const glyphs = ['α', 'β', 'Ω', '∫', 'λ', 'π', 'Δ', '∑', 'H₂O', 'NaCl'];
            for (let i = 0; i < 30; i++) {
                elements.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.8,
                    vy: (Math.random() - 0.5) * 0.8,
                    glyph: glyphs[Math.floor(Math.random() * glyphs.length)]
                });
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                resize();
                elements.forEach(el => {
                    el.x += el.vx;
                    el.y += el.vy;
                    if (el.x < 0 || el.x > canvas.width) el.vx *= -1;
                    if (el.y < 0 || el.y > canvas.height) el.vy *= -1;
                    
                    ctx.font = '13px sans-serif';
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
                    ctx.fillText(el.glyph, el.x, el.y);
                });
                requestAnimationFrame(draw);
            }
            draw();
        }
    })();
</script>
"""
components.html(canvas_js, height=0)

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
        return f"{int(round(f_val))}%"
    except Exception:
        return "0%"

# ===== MODERN A4 FULL-PAGE CERTIFICATE / MARKSHEET (PDF PRINT READY) =====
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

    # Parse numeric score for graph visualization bar
    try:
        numeric_score = float(str(test_score).split('/')[0])
    except:
        numeric_score = 75.0

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
                position: relative;
            }}
            .header {{ text-align: center; }}
            .logo-box {{ width: 85px; height: 85px; margin: 0 auto 10px auto; }}
            .school-title {{ font-size: 16px; font-weight: bold; color: #facc15; text-transform: uppercase; letter-spacing: 1px; }}
            .cert-title {{ font-size: 24px; font-weight: 800; color: #ffffff; margin-top: 5px; }}
            
            .student-info-box {{ background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(250, 204, 21, 0.3); border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0; }}
            .student-name {{ font-size: 28px; font-weight: bold; color: #facc15; margin-bottom: 5px; }}
            .student-details {{ font-size: 13px; color: #cbd5e1; }}

            .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
            .metric-card {{ background: rgba(30, 41, 59, 0.9); border: 1px solid #facc15; border-radius: 10px; padding: 15px; text-align: center; }}
            .metric-val {{ font-size: 22px; font-weight: bold; color: #facc15; }}
            .metric-lbl {{ font-size: 10px; color: #94a3b8; text-transform: uppercase; margin-top: 4px; }}

            /* Data Visualization Graph Elements */
            .graph-section {{ background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); margin: 15px 0; }}
            .graph-title {{ font-size: 14px; font-weight: bold; color: #facc15; margin-bottom: 12px; text-transform: uppercase; }}
            .bar-container {{ background: #334155; border-radius: 6px; height: 18px; width: 100%; overflow: hidden; position: relative; }}
            .bar-fill {{ background: linear-gradient(90deg, #eab308, #facc15); height: 100%; width: {percentage_str}; border-radius: 6px; }}

            .footer-info {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #64748b; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px; }}
            .print-btn {{ background: #facc15; color: #000; border: none; padding: 12px 25px; font-weight: bold; border-radius: 8px; cursor: pointer; text-transform: uppercase; font-size: 14px; display: block; width: 100%; margin-top: 15px; }}
            
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
                <div class="logo-box">{SVG_LOGO_CODE}</div>
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
                <div class="metric-card"><div class="metric-val" style="font-size: 15px; padding-top: 4px;">{subject}</div><div class="metric-lbl">Subject</div></div>
            </div>

            <div class="graph-section">
                <div class="graph-title">Performance Accuracy Graph ({percentage_str})</div>
                <div class="bar-container">
                    <div class="bar-fill"></div>
                </div>
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

# ===== MAIN SPLIT-SCREEN LAYOUT COLUMNS =====
left_col, right_col = st.columns([1, 1], gap="small")

# --- LEFT PANEL (Hero Branding & Interactive Canvas) ---
with left_col:
    st.markdown("""
    <div class="left-panel-container">
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="width:100%; display:flex; justify-content:center; position:relative; z-index:2; margin-bottom: 15px;">
        {SVG_LOGO_CODE}
    </div>
    <h1 style="font-size:clamp(24px, 4vw, 36px); font-weight:800; margin:10px 0; position:relative; z-index:2;">Welcome to Student Portal</h1>
    <p style="font-size:clamp(11px, 2vw, 13px); letter-spacing:1.5px; text-transform:uppercase; opacity:0.9; position:relative; z-index:2;">Govt Boys Higher Secondary School Tando Bago</p>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL (Functional Data Entry & Workflow) ---
with right_col:
    st.markdown('<div class="right-panel-container">', unsafe_allow_html=True)
    
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
                st.error(f"❌ Test file '{file_name}' not found.")
        else:
            st.error("❌ Invalid Test Code format! Use format like: A4-25-01")

    st.markdown('</div>', unsafe_allow_html=True)

