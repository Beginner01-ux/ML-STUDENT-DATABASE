import streamlit as st
import pandas as pd
import re
import os
from PIL import Image
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import streamlit.components.v1 as components

# ===== PAGE SETUP =====
st.set_page_config(page_title="Digital Report Card Portal", layout="centered")

# ===== FULL-PAGE FUTURISTIC EDUCATION BACKGROUND & OPTION B LOGO =====
custom_bg_and_header = """
<!DOCTYPE html>
<html>
<head>
<style>
    /* Full Page Background Canvas */
    #bgCanvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -999;
        background: radial-gradient(circle at center, #0f172a 0%, #05070a 100%);
    }

    /* Option B Logo: Glowing Ring Monogram */
    .header-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px 0 20px 0;
        text-align: center;
    }
    .ring-container {
        position: relative;
        width: 95px;
        height: 95px;
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .glowing-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 3px solid transparent;
        border-top-color: #d4af37;
        border-right-color: rgba(212, 175, 55, 0.25);
        animation: spinRing 3s linear infinite;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }
    .ring-inner {
        text-align: center;
    }
    .ring-ml {
        color: #d4af37;
        font-size: 32px;
        font-weight: 900;
        line-height: 1;
        letter-spacing: 1px;
    }
    .ring-sub {
        color: #94a3b8;
        font-size: 8px;
        letter-spacing: 2px;
        margin-top: 3px;
        font-weight: 600;
    }
    .portal-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 4px 0 2px 0;
        text-transform: uppercase;
    }
    .portal-subtitle {
        color: #d4af37;
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 600;
    }

    @keyframes spinRing {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
</head>
<body>
    <canvas id="bgCanvas"></canvas>

    <div class="header-box">
        <div class="ring-container">
            <div class="glowing-ring"></div>
            <div class="ring-inner">
                <div class="ring-ml">ML</div>
                <div class="ring-sub">MANISH LOHANA</div>
            </div>
        </div>
        <div class="portal-title">Student Results Portal</div>
        <div class="portal-subtitle">Govt Boys Higher Secondary School Tando Bago</div>
    </div>

    <script>
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);

        // Futuristic Education Floating Knowledge Nodes
        class CyberNode {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.radius = Math.random() * 2 + 1;
                this.vy = -(Math.random() * 0.6 + 0.2); // Ascending motion
                this.vx = (Math.random() - 0.5) * 0.4;
                this.alpha = Math.random() * 0.5 + 0.2;
            }
            update() {
                this.y += this.vy;
                this.x += this.vx;
                if (this.y < 0) this.y = canvas.height;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(212, 175, 55, ${this.alpha})`;
                ctx.shadowBlur = 10;
                ctx.shadowColor = "#d4af37";
                ctx.fill();
            }
        }

        for (let i = 0; i < 65; i++) {
            particles.push(new CyberNode());
        }

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();

                // Connect nearby nodes with digital knowledge circuits
                for (let j = i + 1; j < particles.length; j++) {
                    let dx = particles[i].x - particles[j].x;
                    let dy = particles[i].y - particles[j].y;
                    let dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 110) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(212, 175, 55, ${0.25 - dist / 440})`;
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(render);
        }
        render();
    </script>
</body>
</html>
"""
components.html(custom_bg_and_header, height=210)

# ===== HELPER FUNCTIONS =====
def validate_test_number(test_no):
    pattern = r'^[JFMASONDjfsond](1[0-2]|[1-9])-\d{2}-\d{2}$'
    return bool(re.match(pattern, test_no.strip()))

def decode_barcode_image(pil_image):
    """Extracts barcode text from PIL Image natively."""
    try:
        img_np = np.array(pil_image.convert('RGB'))
        decoded_objs = decode(img_np)
        if decoded_objs:
            return decoded_objs[0].data.decode("utf-8").strip()
    except Exception:
        pass
    return None

def format_percentage(val):
    """Converts 0.64 -> 64% cleanly."""
    try:
        f_val = float(str(val).replace('%', '').strip())
        if f_val <= 1.0:
            f_val = f_val * 100
        return f"{int(round(f_val))}%", f_val
    except:
        return "0%", 0.0

def generate_report_card(serial_no, test_no, student_data):
    name = student_data.get('name', 'N/A')
    roll_no = student_data.get('roll_no', 'N/A')
    test_score = student_data.get('test_score', '0')
    subject = student_data.get('subject', 'CHEMISTRY')
    percentage_str, pct_num = format_percentage(student_data.get('percentage', '0'))
    cls = student_data.get('class', 'X')
    rank = student_data.get('class_rank', 'N/A')
    section = student_data.get('section', 'N/A')

    card_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background-color: transparent;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 0;
                padding: 10px;
            }}
            
            /* Futuristic Hologram Reveal Animation */
            .report-card {{
                background: linear-gradient(160deg, #0f172a 0%, #030712 100%);
                color: #ffffff;
                width: 100%;
                max-width: 480px;
                border: 2px solid #d4af37;
                border-radius: 20px;
                padding: 25px;
                box-sizing: border-box;
                box-shadow: 0 0 35px rgba(212, 175, 55, 0.3);
                animation: holoGlow 1.2s ease-out;
            }}

            @keyframes holoGlow {{
                0% {{ opacity: 0; transform: scale(0.92) translateY(20px); filter: brightness(2); }}
                100% {{ opacity: 1; transform: scale(1) translateY(0); filter: brightness(1); }}
            }}

            .card-header {{
                text-align: center;
                border-bottom: 1px dashed rgba(212, 175, 55, 0.3);
                padding-bottom: 14px;
                margin-bottom: 20px;
            }}
            .card-title {{
                color: #d4af37;
                font-size: 19px;
                font-weight: 800;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            
            .gauge-container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 14px;
                padding: 18px;
                margin-bottom: 20px;
                border: 1px solid rgba(212, 175, 55, 0.2);
            }}
            .circle-gauge {{
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background: conic-gradient(#d4af37 {pct_num * 3.6}deg, #1e293b 0deg);
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 0 18px rgba(212, 175, 55, 0.4);
            }}
            .circle-inner {{
                width: 74px;
                height: 74px;
                background: #090d16;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .pct-text {{
                color: #ffffff;
                font-weight: 800;
                font-size: 18px;
            }}
            .pct-label {{
                color: #d4af37;
                font-size: 8px;
                letter-spacing: 1px;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-bottom: 20px;
            }}
            .info-item {{
                background: rgba(15, 23, 42, 0.8);
                padding: 12px;
                border-radius: 10px;
                border-left: 3px solid #d4af37;
            }}
            .label {{
                color: #94a3b8;
                font-size: 9px;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: block;
                margin-bottom: 3px;
            }}
            .value {{
                color: #ffffff;
                font-weight: 700;
                font-size: 14px;
            }}

            .analytics-box {{
                background: rgba(15, 23, 42, 0.8);
                padding: 14px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}
            .bar-container {{
                background: #1e293b;
                height: 12px;
                border-radius: 6px;
                overflow: hidden;
                margin-top: 8px;
            }}
            .bar-fill {{
                height: 100%;
                background: linear-gradient(90deg, #b8860b 0%, #d4af37 100%);
                width: {pct_num}%;
                border-radius: 6px;
                box-shadow: 0 0 10px #d4af37;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #d4af37 0%, #996515 100%);
                color: #000;
                border: none;
                padding: 14px 25px;
                font-size: 13px;
                font-weight: 800;
                border-radius: 10px;
                cursor: pointer;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                width: 100%;
                box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
            }}
            @media print {{
                .print-btn {{ display: none; }}
                body {{ background: black; }}
                .report-card {{ border: 2px solid #d4af37; box-shadow: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="report-card">
            <div class="card-header">
                <div class="card-title">OFFICIAL REPORT CARD</div>
                <div style="color: #94a3b8; font-size: 11px; margin-top: 3px;">MANISH LOHANA EDUCATION PORTAL</div>
            </div>

            <div class="gauge-container">
                <div>
                    <div style="color: #94a3b8; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">Subject</div>
                    <div style="color: #ffffff; font-size: 20px; font-weight: 800; text-transform: uppercase;">{subject}</div>
                    <div style="color: #d4af37; font-size: 12px; margin-top: 4px; font-weight: 700;">Class Rank: {rank}</div>
                </div>
                <div class="circle-gauge">
                    <div class="circle-inner">
                        <span class="pct-text">{percentage_str}</span>
                        <span class="pct-label">PERCENTAGE</span>
                    </div>
                </div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <span class="label">Book Serial No</span>
                    <span class="value">{serial_no}</span>
                </div>
                <div class="info-item">
                    <span class="label">Test Code</span>
                    <span class="value">{test_no}</span>
                </div>
                <div class="info-item">
                    <span class="label">Roll No</span>
                    <span class="value">{roll_no}</span>
                </div>
                <div class="info-item">
                    <span class="label">Student Name</span>
                    <span class="value">{name}</span>
                </div>
                <div class="info-item">
                    <span class="label">Test Score</span>
                    <span class="value">{test_score}</span>
                </div>
                <div class="info-item">
                    <span class="label">Class & Sec</span>
                    <span class="value">{cls} ({section})</span>
                </div>
            </div>

            <div class="analytics-box">
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; font-weight: 600;">
                    <span>SCORE ACCURACY METRIC</span>
                    <span style="color: #d4af37; font-weight: 800;">{percentage_str}</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill"></div>
                </div>
            </div>
            
            <button class="print-btn" onclick="window.print()">️ Print / Save Report Card</button>
        </div>
    </body>
    </html>
    """
    components.html(card_html, height=640)

# ===== MAIN APP FLOW =====
test_input = st.text_input("Enter Test Code:", placeholder="e.g., A4-25-01")

if test_input:
    cleaned_test = test_input.strip().upper()
    
    if validate_test_number(cleaned_test):
        file_name = f"{cleaned_test}.xlsx"
        
        if os.path.exists(file_name):
            st.success(f"✓ Test Session '{cleaned_test}' Active")
            
            # --- BARCODE SCANNER TABS ---
            scan_tab1, scan_tab2 = st.tabs([" Camera Scan", "️ Upload Image"])
            scanned_serial = ""

            with scan_tab1:
                cam_img = st.camera_input("Scan barcode using camera")
                if cam_img:
                    pil_img = Image.open(cam_img)
                    found_code = decode_barcode_image(pil_img)
                    if found_code:
                        scanned_serial = found_code
                        st.success(f"✓ Scanned Code: {scanned_serial}")
                    else:
                        st.warning("⚠️ No barcode detected in camera frame. Try adjusting distance.")

            with scan_tab2:
                uploaded_img = st.file_uploader("Upload barcode picture", type=["jpg", "jpeg", "png", "webp"])
                if uploaded_img:
                    pil_img = Image.open(uploaded_img)
                    found_code = decode_barcode_image(pil_img)
                    if found_code:
                        scanned_serial = found_code
                        st.success(f"✓ Scanned Code: {scanned_serial}")
                    else:
                        st.warning("⚠️ Could not read barcode from this image.")

            # Auto-fill scanned serial if available
            default_serial = scanned_serial if scanned_serial else ""
            serial_input = st.text_input("Enter or Scan Serial Number:", value=default_serial, placeholder="e.g., MGM75000002")
            
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

