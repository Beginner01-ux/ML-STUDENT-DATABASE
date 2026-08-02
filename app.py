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

# ===== INJECT FULL-SCREEN INTERACTIVE CANVAS (MOLECULES, NODES & GLYPHS) =====
canvas_html = """
<script>
    (function() {
        const parentDoc = window.parent.document;
        
        // Optimize container layout
        const mainBlock = parentDoc.querySelector('.main .block-container');
        if (mainBlock) {
            mainBlock.style.paddingTop = '1.5rem';
            mainBlock.style.paddingBottom = '2rem';
            mainBlock.style.maxWidth = '680px';
        }

        // Create canvas on the parent document body
        let canvas = parentDoc.getElementById('interactive-bg-canvas');
        if (!canvas) {
            canvas = parentDoc.createElement('canvas');
            canvas.id = 'interactive-bg-canvas';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '-1';
            canvas.style.pointerEvents = 'none';
            canvas.style.background = 'radial-gradient(circle at 50% 30%, #0f172a 0%, #020617 100%)';
            parentDoc.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.parent.innerWidth;
                canvas.height = window.parent.innerHeight;
            }
            window.parent.addEventListener('resize', resize);
            resize();

            // Interactive Elements: Nodes, Molecules, and Phonetic/Language Glyphs
            const elements = [];
            const glyphs = ['α', 'β', 'Ω', '∫', 'æ', 'θ', 'λ', '∑', 'ð'];
            const elementCount = 35;
            let mouse = { x: null, y: null, radius: 150 };

            window.parent.addEventListener('mousemove', (e) => {
                mouse.x = e.clientX;
                mouse.y = e.clientY;
            });

            class FloatingElement {
                constructor() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.vx = (Math.random() - 0.5) * 0.5;
                    this.vy = (Math.random() - 0.5) * 0.5;
                    this.size = Math.random() * 14 + 10;
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
                        ctx.beginPath();
                        ctx.arc(0, 0, 3, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(234, 179, 8, 0.8)';
                        ctx.shadowBlur = 8;
                        ctx.shadowColor = '#eab308';
                        ctx.fill();
                    } else if (this.type === 1) {
                        ctx.beginPath();
                        ctx.arc(0, 0, 4, 0, Math.PI * 2);
                        ctx.fillStyle = 'rgba(244, 63, 94, 0.85)';
                        ctx.fill();

                        for (let i = 0; i < 3; i++) {
                            let bAngle = (i * Math.PI * 2 / 3);
                            let bx = Math.cos(bAngle) * 12;
                            let by = Math.sin(bAngle) * 12;

                            ctx.beginPath();
                            ctx.moveTo(0, 0);
                            ctx.lineTo(bx, by);
                            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                            ctx.lineWidth = 1;
                            ctx.stroke();

                            ctx.beginPath();
                            ctx.arc(bx, by, 2.5, 0, Math.PI * 2);
                            ctx.fillStyle = 'rgba(56, 189, 248, 0.8)';
                            ctx.fill();
                        }
                    } else {
                        ctx.font = '13px Space Mono, monospace';
                        ctx.fillStyle = 'rgba(168, 85, 247, 0.6)';
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
                            ctx.strokeStyle = `rgba(234, 179, 8, ${0.12 * (1 - dist / 110)})`;
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
components.html(canvas_html, height=0)

# ===== ULTRA-MODERN GLASSMORPHIC HEADER =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .header-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }

    .brand-crest {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 76px;
        height: 76px;
        border-radius: 50%;
        background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
        border: 2px solid #facc15;
        box-shadow: 0 0 25px rgba(250, 204, 21, 0.3);
        margin-bottom: 14px;
    }

    .brand-initials {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #facc15;
        letter-spacing: 1px;
    }

    .portal-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .portal-subtitle {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 6px;
    }

    /* Input overrides */
    .stTextInput > div > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
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

<div class="header-card">
    <div class="brand-crest">
        <span class="brand-initials">ML</span>
    </div>
    <div class="portal-title">Student Results Portal</div>
    <div class="portal-subtitle">Govt Boys Higher Secondary School Tando Bago</div>
</div>
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
                display: flex;
                justify-content: center;
            }}

            /* Certificate Frame Dimensions optimized for A4 / Screen */
            .cert-container {{
                background: linear-gradient(145deg, #0b1329 0%, #030712 100%);
                color: #ffffff;
                width: 100%;
                max-width: 650px;
                border: 2px solid #ca8a04;
                border-radius: 16px;
                padding: 24px;
                position: relative;
                box-shadow: 0 25px 60px rgba(0,0,0,0.85);
                overflow: hidden;
            }}

            /* Decorative Gold Foil Double Border */
            .cert-border-inner {{
                border: 1px solid rgba(234, 179, 8, 0.4);
                border-radius: 12px;
                padding: 20px;
                position: relative;
                background: radial-gradient(circle at center, rgba(30, 41, 59, 0.2) 0%, rgba(3, 7, 18, 0.4) 100%);
            }}

            .cert-header {{
                text-align: center;
                border-bottom: 1px solid rgba(234, 179, 8, 0.2);
                padding-bottom: 16px;
                margin-bottom: 20px;
            }}

            .cert-crest {{
                width: 50px;
                height: 50px;
                border-radius: 50%;
                border: 1.5px solid #facc15;
                background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-family: 'Cinzel', serif;
                font-weight: 800;
                font-size: 20px;
                color: #facc15;
                box-shadow: 0 0 15px rgba(250, 204, 21, 0.25);
                margin-bottom: 8px;
            }}

            .institution-name {{
                font-family: 'Cinzel', serif;
                font-size: 13px;
                font-weight: 700;
                color: #facc15;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin: 0;
            }}

            .cert-title {{
                font-family: 'Cinzel', serif;
                font-size: 22px;
                font-weight: 900;
                color: #ffffff;
                letter-spacing: 1.5px;
                margin-top: 4px;
            }}

            .student-section {{
                text-align: center;
                margin-bottom: 20px;
            }}

            .cert-presented-to {{
                font-size: 10px;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 2px;
                font-weight: 600;
            }}

            .student-name {{
                font-family: 'Cinzel', serif;
                font-size: 26px;
                font-weight: 800;
                color: #ffffff;
                margin: 6px 0;
                background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            .student-sub {{
                color: #e2e8f0;
                font-size: 12px;
                font-weight: 600;
            }}

            /* Academic Metric Grid */
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
                margin-bottom: 20px;
            }}

            .metric-box {{
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid rgba(234, 179, 8, 0.25);
                border-radius: 10px;
                padding: 10px 8px;
                text-align: center;
            }}

            .metric-title {{
                font-size: 8px;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 700;
            }}

            .metric-value {{
                font-family: 'Space Grotesk', sans-serif;
                font-size: 18px;
                font-weight: 700;
                color: #facc15;
                margin-top: 2px;
            }}

            /* Detailed Table Grid */
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 20px;
            }}

            .info-item {{
                background: rgba(30, 41, 59, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-left: 3px solid #facc15;
                padding: 8px 12px;
                border-radius: 6px;
            }}

            .info-label {{
                font-size: 8px;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 700;
                display: block;
            }}

            .info-val {{
                font-size: 12px;
                color: #ffffff;
                font-weight: 700;
                margin-top: 2px;
            }}

            /* Seal & Verification Section */
            .cert-footer {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-top: 1px solid rgba(234, 179, 8, 0.2);
                padding-top: 16px;
            }}

            .official-seal {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .seal-badge {{
                width: 44px;
                height: 44px;
                border-radius: 50%;
                border: 2px dashed #facc15;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #facc15;
                font-size: 18px;
                background: rgba(250, 204, 21, 0.1);
            }}

            .seal-text-title {{
                font-size: 11px;
                font-weight: 800;
                color: #ffffff;
            }}

            .seal-text-sub {{
                font-size: 9px;
                color: #22c55e;
                font-weight: 700;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #facc15 0%, #ca8a04 100%);
                color: #000000;
                border: none;
                padding: 12px 20px;
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700;
                font-size: 11px;
                border-radius: 10px;
                cursor: pointer;
                letter-spacing: 1px;
                text-transform: uppercase;
                box-shadow: 0 4px 15px rgba(250, 204, 21, 0.3);
            }}

            /* PRINT SPECIFIC STYLES TO TARGET A4 PDF DOWNLOAD PERFECTLY */
            @media print {{
                html, body {{
                    background: #ffffff !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }}
                .cert-container {{
                    box-shadow: none !important;
                    border: 3px solid #b45309 !important;
                    background: #090d16 !important;
                    width: 100% !important;
                    max-width: 100% !important;
                    page-break-inside: avoid !important;
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
    components.html(certificate_html, height=620, scrolling=False)

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

