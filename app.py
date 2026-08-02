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

# ===== SVG LOGO DEFINITION =====
SVG_LOGO_CODE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 310" style="width:100%; height:100%; max-width:220px; max-height:220px;">
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

# ===== STYLES & DYNAMIC RESPONSIVE CANVAS BACKGROUND =====
st.markdown("""
<style>
    /* Reset Streamlit default padding & layout limits */
    .main .block-container {
        max-width: 100% !important;
        padding: 1rem 2rem !important;
        margin: 0 auto !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #030712;
        overflow-x: hidden;
    }

    /* Column Responsiveness Overrides */
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }

    /* Desktop View Layout */
    @media (min-width: 769px) {
        [data-testid="column"] {
            padding: 1rem !important;
        }
    }

    /* Mobile & Tablet Layout Adjustments (<768px) */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem 0.75rem !important;
        }

        /* Force columns to stack smoothly vertically on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 1rem !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            padding: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Inject Full-Viewport Responsive Particle Canvas
canvas_js = """
<script>
    (function() {
        const parentDoc = window.parent.document;
        let canvas = parentDoc.getElementById('responsive-hero-canvas');
        
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'responsive-hero-canvas';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '-1';
            canvas.style.pointerEvents = 'none';
            canvas.style.background = 'radial-gradient(circle at 30% 50%, #1e1b4b 0%, #030712 100%)';
            parentDoc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.parent.innerWidth;
                canvas.height = window.parent.innerHeight;
            }
            window.parent.addEventListener('resize', resize);
            resize();

            const elements = [];
            const glyphs = ['α', 'β', 'Ω', '∫', 'λ', 'π', 'Δ', '∑'];
            const count = window.parent.innerWidth < 768 ? 25 : 50;

            for (let i = 0; i < count; i++) {
                elements.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: (Math.random() - 0.5) * 0.5,
                    glyph: glyphs[Math.floor(Math.random() * glyphs.length)]
                });
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                elements.forEach(el => {
                    el.x += el.vx;
                    el.y += el.vy;
                    if (el.x < 0 || el.x > canvas.width) el.vx *= -1;
                    if (el.y < 0 || el.y > canvas.height) el.vy *= -1;
                    
                    ctx.font = '14px monospace';
                    ctx.fillStyle = 'rgba(250, 204, 21, 0.6)';
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

# ===== HELPER FUNCTIONS =====
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

# ===== PRINTABLE CERTIFICATE GENERATOR =====
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
            body {{ margin: 0; padding: 10px; font-family: system-ui, -apple-system, sans-serif; background: transparent; color: #fff; }}
            .cert-card {{ background: #0b1329; border: 2px solid #facc15; border-radius: 12px; padding: 20px; text-align: center; max-width: 100%; }}
            .logo-box {{ width: 65px; height: 65px; margin: 0 auto 10px auto; }}
            .title {{ font-size: clamp(14px, 3vw, 18px); font-weight: bold; color: #facc15; margin-top: 5px; }}
            .subtitle {{ font-size: clamp(9px, 2vw, 11px); color: #94a3b8; text-transform: uppercase; margin-bottom: 15px; }}
            .student-name {{ font-size: clamp(18px, 4vw, 24px); font-weight: bold; color: #fff; margin: 8px 0; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 8px; margin: 15px 0; }}
            .box {{ background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(250, 204, 21, 0.3); padding: 8px; border-radius: 8px; }}
            .val {{ font-size: 16px; font-weight: bold; color: #facc15; }}
            .lbl {{ font-size: 8px; color: #94a3b8; text-transform: uppercase; }}
            .btn {{ background: #facc15; color: #000; border: none; padding: 10px 18px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 10px; text-transform: uppercase; }}
            @media print {{
                body {{ background: #0b1329 !important; padding: 0 !important; }}
                .btn {{ display: none !important; }}
                .cert-card {{ height: 100vh; border-radius: 0; display: flex; flex-direction: column; justify-content: center; }}
            }}
        </style>
    </head>
    <body>
        <div class="cert-card">
            <div class="logo-box">{SVG_LOGO_CODE}</div>
            <div class="title">Govt Boys Higher Secondary School Tando Bago</div>
            <div class="subtitle">Academic Progress Certificate</div>
            <div class="student-name">{name}</div>
            <div style="font-size: 11px; color: #cbd5e1;">Father's Name: {father_name} | Class: {cls}-{section} | Seat No: {roll_no}</div>
            
            <div class="grid">
                <div class="box"><div class="lbl">Score</div><div class="val">{test_score}</div></div>
                <div class="box"><div class="lbl">Percentage</div><div class="val">{percentage_str}</div></div>
                <div class="box"><div class="lbl">Class Rank</div><div class="val">{rank}</div></div>
                <div class="box"><div class="lbl">Subject</div><div class="val" style="font-size:11px;">{subject}</div></div>
            </div>

            <div style="font-size: 10px; color: #64748b; margin-top: 10px;">Test Code: {test_no} | Serial: {serial_no}</div>
            <button class="btn" onclick="window.print()">️ Print / Save PDF Certificate</button>
        </div>
    </body>
    </html>
    """
    components.html(certificate_html, height=480, scrolling=False)

# ===== LAYOUT COLUMNS =====
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    hero_html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:15px; color:#ffffff; font-family:system-ui, sans-serif;">
        <div style="width:100%; max-width:180px; height:auto; margin-bottom:12px;">{SVG_LOGO_CODE}</div>
        <div style="font-size:clamp(18px, 3.5vw, 24px); font-weight:800; color:#ffffff;">Welcome to Student Portal</div>
        <div style="font-size:clamp(10px, 1.8vw, 12px); color:#94a3b8; letter-spacing:1px; text-transform:uppercase; margin-top:4px;">Govt Boys Higher Secondary School Tando Bago</div>
    </div>
    """
    components.html(hero_html, height=270)

with right_col:
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

