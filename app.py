import streamlit as st
import pandas as pd
import re
import os
from PIL import Image
import zxingcpp
import streamlit.components.v1 as components

# ===== PAGE SETUP =====
st.set_page_config(page_title="Digital Report Card Portal", layout="centered")

# ===== ULTRA-LIGHTWEIGHT GPU-ACCELERATED HEADER & BACKGROUND =====
custom_bg_and_header = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background: #070a0f;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        overflow: hidden;
    }

    /* Lightweight CSS Ambient Radial Glows */
    .bg-glow-1 {
        position: fixed;
        top: -100px;
        left: 50%;
        transform: translateX(-50%);
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .header-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px 10px;
        text-align: center;
    }

    /* CSS Animated Glowing Ring (0% CPU Load) */
    .logo-container {
        position: relative;
        width: 90px;
        height: 90px;
        margin-bottom: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .glowing-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 2px solid transparent;
        border-top-color: #d4af37;
        border-right-color: rgba(212, 175, 55, 0.3);
        animation: spinRing 4s linear infinite;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.25);
    }

    .ring-inner {
        text-align: center;
    }

    .ring-ml {
        color: #d4af37;
        font-size: 30px;
        font-weight: 900;
        line-height: 1;
        letter-spacing: 1px;
    }

    .ring-sub {
        color: #94a3b8;
        font-size: 8px;
        letter-spacing: 2px;
        margin-top: 4px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .portal-title {
        color: #ffffff;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 6px 0 2px 0;
        text-transform: uppercase;
    }

    .portal-subtitle {
        color: #d4af37;
        font-size: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 600;
        opacity: 0.9;
    }

    @keyframes spinRing {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
</head>
<body>
    <div class="bg-glow-1"></div>
    <div class="header-box">
        <div class="logo-container">
            <div class="glowing-ring"></div>
            <div class="ring-inner">
                <div class="ring-ml">ML</div>
                <div class="ring-sub">MANISH LOHANA</div>
            </div>
        </div>
        <div class="portal-title">Student Results Portal</div>
        <div class="portal-subtitle">Govt Boys Higher Secondary School Tando Bago</div>
    </div>
</body>
</html>
"""
components.html(custom_bg_and_header, height=200)

# ===== HELPER FUNCTIONS =====
def validate_test_number(test_no):
    pattern = r'^[JFMASONDjfsond](1[0-2]|[1-9])-\d{2}-\d{2}$'
    return bool(re.match(pattern, test_no.strip()))

def decode_barcode_image(pil_image):
    """Fast barcode reading via C++ zxing engine."""
    try:
        results = zxingcpp.read_barcodes(pil_image)
        if results:
            return results[0].text.strip()
    except Exception:
        pass
    return None

def format_percentage(val):
    """Converts raw numerical decimal/percentage to clean display format."""
    try:
        f_val = float(str(val).replace('%', '').strip())
        if f_val <= 1.0:
            f_val = f_val * 100
        return f"{int(round(f_val))}%", f_val
    except Exception:
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
                font-family: 'Segoe UI', system-ui, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 0;
                padding: 5px;
            }}
            
            .report-card {{
                background: linear-gradient(160deg, #0e1524 0%, #05080f 100%);
                color: #ffffff;
                width: 100%;
                max-width: 460px;
                border: 1px solid #d4af37;
                border-radius: 16px;
                padding: 22px;
                box-sizing: border-box;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            }}

            .card-header {{
                text-align: center;
                border-bottom: 1px dashed rgba(212, 175, 55, 0.3);
                padding-bottom: 12px;
                margin-bottom: 16px;
            }}
            .card-title {{
                color: #d4af37;
                font-size: 18px;
                font-weight: 800;
                letter-spacing: 1.5px;
                text-transform: uppercase;
            }}
            
            .gauge-container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 16px;
                border: 1px solid rgba(212, 175, 55, 0.15);
            }}
            .circle-gauge {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: conic-gradient(#d4af37 {pct_num * 3.6}deg, #1e293b 0deg);
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .circle-inner {{
                width: 66px;
                height: 66px;
                background: #080c14;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .pct-text {{
                color: #ffffff;
                font-weight: 800;
                font-size: 16px;
            }}
            .pct-label {{
                color: #d4af37;
                font-size: 7px;
                letter-spacing: 1px;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 16px;
            }}
            .info-item {{
                background: rgba(15, 23, 42, 0.6);
                padding: 10px;
                border-radius: 8px;
                border-left: 3px solid #d4af37;
            }}
            .label {{
                color: #94a3b8;
                font-size: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: block;
                margin-bottom: 2px;
            }}
            .value {{
                color: #ffffff;
                font-weight: 700;
                font-size: 13px;
            }}

            .analytics-box {{
                background: rgba(15, 23, 42, 0.6);
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 16px;
            }}
            .bar-container {{
                background: #1e293b;
                height: 10px;
                border-radius: 5px;
                overflow: hidden;
                margin-top: 6px;
            }}
            .bar-fill {{
                height: 100%;
                background: #d4af37;
                width: {pct_num}%;
                border-radius: 5px;
            }}

            .print-btn {{
                background: linear-gradient(135deg, #d4af37 0%, #a67c1e 100%);
                color: #000;
                border: none;
                padding: 12px;
                font-size: 12px;
                font-weight: 800;
                border-radius: 8px;
                cursor: pointer;
                letter-spacing: 1px;
                text-transform: uppercase;
                width: 100%;
            }}
            @media print {{
                .print-btn {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="report-card">
            <div class="card-header">
                <div class="card-title">OFFICIAL REPORT CARD</div>
                <div style="color: #94a3b8; font-size: 10px; margin-top: 2px;">MANISH LOHANA EDUCATION PORTAL</div>
            </div>

            <div class="gauge-container">
                <div>
                    <div style="color: #94a3b8; font-size: 9px; text-transform: uppercase; letter-spacing: 1px;">Subject</div>
                    <div style="color: #ffffff; font-size: 18px; font-weight: 800; text-transform: uppercase;">{subject}</div>
                    <div style="color: #d4af37; font-size: 11px; margin-top: 2px; font-weight: 700;">Class Rank: {rank}</div>
                </div>
                <div class="circle-gauge">
                    <div class="circle-inner">
                        <span class="pct-text">{percentage_str}</span>
                        <span class="pct-label">SCORE</span>
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
                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; font-weight: 600;">
                    <span>PERFORMANCE ACCURACY</span>
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
    components.html(card_html, height=580)

# ===== MAIN APP FLOW =====
test_input = st.text_input("Enter Test Code:", placeholder="e.g., A4-25-01")

if test_input:
    cleaned_test = test_input.strip().upper()
    
    if validate_test_number(cleaned_test):
        file_name = f"{cleaned_test}.xlsx"
        
        if os.path.exists(file_name):
            st.success(f"✓ Test Session '{cleaned_test}' Active")
            
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
                        st.warning("⚠️ No barcode detected in frame.")

            with scan_tab2:
                uploaded_img = st.file_uploader("Upload barcode picture", type=["jpg", "jpeg", "png", "webp"])
                if uploaded_img:
                    pil_img = Image.open(uploaded_img)
                    found_code = decode_barcode_image(pil_img)
                    if found_code:
                        scanned_serial = found_code
                        st.success(f"✓ Scanned Code: {scanned_serial}")
                    else:
                        st.warning("⚠️ Could not read barcode from image.")

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

