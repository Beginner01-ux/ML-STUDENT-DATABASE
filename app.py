import streamlit as st
import pandas as pd
import re
import os
from PIL import Image
from html import escape
import streamlit.components.v1 as components

# ===== OPTIONAL DEPENDENCY HANDLING =====
try:
    import zxingcpp
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False
    st.warning("⚠️ Barcode scanning disabled: zxingcpp not installed. Install with: pip install zxingcpp")

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="Student Results Portal | Official Examination Cell",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== OFFICIAL SEAL & VECTOR MARK =====
SVG_SEAL = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="width:100%; height:100%; max-width:110px; max-height:110px; display:block; margin:0 auto;">
  <circle cx="100" cy="100" r="90" fill="#0f172a" stroke="#38bdf8" stroke-width="4"/>
  <circle cx="100" cy="100" r="78" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4,4"/>
  <path d="M 100,45 L 125,85 L 100,125 L 75,85 Z" fill="#38bdf8"/>
  <polygon points="100,120 135,140 100,155 65,140" fill="#bae6fd"/>
</svg>
"""

# ===== CORE THEME & LAYOUT ENGINE =====
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #090d16;
        color: #f8fafc;
        font-family: system-ui, -apple-system, sans-serif;
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
    .portal-sidebar {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
        border-right: 1px solid #1e293b;
        min-height: 100vh;
        padding: 40px 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .portal-main-panel {
        background: #090d16;
        min-height: 100vh;
        padding: 40px;
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
        .portal-sidebar { min-height: auto; padding: 30px 16px; }
        .portal-main-panel { min-height: auto; padding: 30px 16px; }
    }
</style>
""", unsafe_allow_html=True)

# ===== VALIDATION & METADATA HANDLERS =====
def validate_test_number(test_no):
    """
    Enforces exact standard pattern: [JFMASONDjfmasond][1-12]-[YY]-[NN]
    FIXED: Added missing 'm' and 'a' to character class
    """
    pattern = r'^[JFMASONDjfmasond](1[0-2]|[1-9])-\d{2}-\d{2}$'
    return bool(re.match(pattern, test_no.strip()))

def decode_barcode_image(pil_image):
    """Decode barcode from PIL image, with graceful fallback if zxingcpp unavailable"""
    if not BARCODE_AVAILABLE:
        return None
    
    try:
        results = zxingcpp.read_barcodes(pil_image)
        if results:
            return results[0].text.strip()
    except Exception as e:
        st.warning(f"Barcode decode error: {str(e)}")
    return None

def normalize_percentage(val):
    """
    Convert value to percentage (0-100 range).
    FIXED: Clamped to 0-100 to prevent invalid CSS widths and progress bar overflow
    """
    try:
        f_val = float(str(val).replace('%', '').strip())
        # Auto-scale decimal percentages (0.75 → 75)
        if f_val <= 1.0:
            f_val *= 100
        # CRITICAL FIX: Clamp to valid percentage range
        f_val = max(0, min(100, f_val))
        return f"{int(round(f_val))}%"
    except (ValueError, AttributeError):
        return "0%"

def get_excel_column(df, possible_names):
    """
    Robustly find column by checking multiple naming variations.
    FIXED: Handles ColumnName, column_name, COLUMN NAME variations
    """
    normalized_cols = {col.lower().replace(' ', '').replace('_', ''): col for col in df.columns}
    
    for name in possible_names:
        normalized_name = name.lower().replace(' ', '').replace('_', '')
        if normalized_name in normalized_cols:
            return normalized_cols[normalized_name]
    return None

def load_excel_safe(filepath):
    """
    Safely load Excel file with error handling.
    FIXED: Handles missing files, corrupted sheets, encoding issues
    """
    try:
        if not os.path.exists(filepath):
            return None, f"File not found: {filepath}"
        
        df = pd.read_excel(filepath)
        
        if df.empty:
            return None, "Excel file is empty"
        
        # Normalize column names: strip whitespace, lowercase
        df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
        
        return df, None
    
    except pd.errors.EmptyDataError:
        return None, "Excel file contains no data"
    except pd.errors.ParserError:
        return None, "Could not parse Excel file (format corrupted?)"
    except Exception as e:
        return None, f"Unexpected error loading file: {str(e)}"

# ===== SECURE CERTIFICATE RENDERING ENGINE =====
def render_certificate(serial_no, test_no, data):
    """
    Render certificate with HTML-escaped user data.
    FIXED: Escaped all user-controlled strings to prevent XSS
    """
    # Extract and sanitize all data fields
    name = escape(str(data.get('name', 'N/A')))
    father_name = escape(str(data.get('father_name', 'N/A')))
    roll_no = escape(str(data.get('roll_no', 'N/A')))
    score = escape(str(data.get('test_score', '0')))
    subject = escape(str(data.get('subject', 'General Evaluation')))
    percentage = normalize_percentage(data.get('percentage', '0'))  # Returns safe percentage
    cls = escape(str(data.get('class', 'N/A')))
    rank = escape(str(data.get('class_rank', 'N/A')))
    section = escape(str(data.get('section', 'A')))

    # Extract numeric value from percentage for progress bar width
    pct_num = int(percentage.rstrip('%'))

    cert_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
            @page {{ size: A4 portrait; margin: 0; }}
            body {{ margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; background: #020617; color: #f8fafc; }}
            .page-container {{
                width: 210mm;
                height: 297mm;
                max-width: 100%;
                margin: 0 auto;
                background: linear-gradient(135deg, #090d16 0%, #1e1b4b 100%);
                border: 3px solid #38bdf8;
                padding: 40px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            .cert-header {{ text-align: center; }}
            .org-title {{ font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 2px; margin-top: 10px; }}
            .doc-title {{ font-size: 24px; font-weight: 800; color: #ffffff; margin-top: 6px; }}
            
            .identity-box {{ background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0; }}
            .student-name {{ font-size: 26px; font-weight: 700; color: #38bdf8; margin-bottom: 6px; word-break: break-word; }}
            .student-sub {{ font-size: 13px; color: #94a3b8; }}
            
            .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }}
            .metric-card {{ background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 14px; text-align: center; }}
            .metric-val {{ font-size: 20px; font-weight: 700; color: #38bdf8; word-break: break-word; }}
            .metric-lbl {{ font-size: 9px; color: #64748b; text-transform: uppercase; margin-top: 4px; }}
            
            .analytics-box {{ background: rgba(15, 23, 42, 0.5); border: 1px solid #1e293b; border-radius: 10px; padding: 18px; margin: 15px 0; }}
            .analytics-label {{ font-size: 12px; font-weight: 600; color: #cbd5e1; margin-bottom: 8px; text-transform: uppercase; }}
            .progress-track {{ background: #1e293b; border-radius: 4px; height: 12px; width: 100%; overflow: hidden; }}
            .progress-fill {{ background: linear-gradient(90deg, #0284c7, #38bdf8); height: 100%; width: {pct_num}%; border-radius: 4px; transition: width 0.3s ease; }}
            
            .footer-meta {{ display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #64748b; border-top: 1px solid #1e293b; padding-top: 15px; flex-wrap: wrap; gap: 8px; }}
            .print-action-btn {{ background: #38bdf8; color: #020617; border: none; padding: 12px; font-weight: 700; border-radius: 6px; cursor: pointer; text-transform: uppercase; font-size: 13px; width: 100%; margin-top: 15px; }}
            
            @media print {{
                body {{ background: #020617 !important; }}
                .print-action-btn {{ display: none !important; }}
                .page-container {{ border: none; height: 100vh; width: 100vw; padding: 20px; }}
            }}
        </style>
    </head>
    <body>
        <div class="page-container">
            <div class="cert-header">
                {SVG_SEAL}
                <div class="org-title">Official Academic Evaluation Cell</div>
                <div class="doc-title">Certificate of Performance</div>
            </div>
            
            <div class="identity-box">
                <div class="student-name">{name}</div>
                <div class="student-sub">Father's Name: <b>{father_name}</b> &nbsp;|&nbsp; Class: <b>{cls}-{section}</b> &nbsp;|&nbsp; Roll No: <b>{roll_no}</b></div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card"><div class="metric-val">{score}</div><div class="metric-lbl">Total Score</div></div>
                <div class="metric-card"><div class="metric-val">{percentage}</div><div class="metric-lbl">Accuracy</div></div>
                <div class="metric-card"><div class="metric-val">#{rank}</div><div class="metric-lbl">Class Rank</div></div>
                <div class="metric-card"><div class="metric-val" style="font-size:13px; padding-top:4px;">{subject}</div><div class="metric-lbl">Subject</div></div>
            </div>
            
            <div class="analytics-box">
                <div class="analytics-label">Performance Metric Rating ({percentage})</div>
                <div class="progress-track"><div class="progress-fill"></div></div>
            </div>
            
            <div>
                <div class="footer-meta">
                    <span>Test Code: <b>{escape(test_no)}</b></span>
                    <span>Serial No: <b>{escape(serial_no)}</b></span>
                    <span>Status: Verified Record</span>
                </div>
                <button class="print-action-btn" onclick="window.print()">🖨️ Download Printable A4 Report PDF</button>
            </div>
        </div>
    </body>
    </html>
    """
    # Use full height to render complete A4 certificate + scrolling for mobile
    components.html(cert_html, height=1400, scrolling=True)

# ===== STRUCTURAL CONTAINER VIEW =====
sidebar_col, main_col = st.columns([1, 1], gap="small")

with sidebar_col:
    st.markdown('<div class="portal-sidebar">', unsafe_allow_html=True)
    st.markdown(SVG_SEAL, unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 24px; font-weight: 800; margin: 16px 0 6px 0;">Evaluation Portal</h2>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 12px; color: #64748b; letter-spacing: 1px; text-transform: uppercase; margin: 0;">Secure Metadata Indexing Unit</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main_col:
    st.markdown('<div class="portal-main-panel">', unsafe_allow_html=True)
    st.subheader("Record Identification Lookup")
    st.caption("Provide metadata identifiers to access verified evaluation sheets.")

    # Primary Metadata Input: Test Code
    test_code_input = st.text_input("Enter Test Code:", placeholder="e.g., A4-25-01")

    if test_code_input:
        cleaned_test = test_code_input.strip().upper()
        
        if validate_test_number(cleaned_test):
            target_file = f"{cleaned_test}.xlsx"
            
            if os.path.exists(target_file):
                st.success(f"✓ Validated Session Index: {cleaned_test}")
                
                # Secondary Metadata Input: Barcode / Serial Acquisition
                input_tabs = st.tabs(["📷 Camera Scanner", "🖼️ File Upload", "⌨️ Direct Serial"])
                captured_serial = ""

                with input_tabs[0]:
                    if BARCODE_AVAILABLE:
                        cam_frame = st.camera_input("Capture Barcode Tag")
                        if cam_frame:
                            decoded = decode_barcode_image(Image.open(cam_frame))
                            if decoded:
                                captured_serial = decoded
                                st.success(f"✓ Barcode Read Successfully: {captured_serial}")
                            else:
                                st.warning("⚠️ No valid barcode found in camera frame.")
                    else:
                        st.info("Camera barcode scanning not available. Use file upload or manual entry.")

                with input_tabs[1]:
                    uploaded_file = st.file_uploader("Upload Barcode Image", type=["jpg", "jpeg", "png", "webp"])
                    if uploaded_file:
                        if BARCODE_AVAILABLE:
                            decoded = decode_barcode_image(Image.open(uploaded_file))
                            if decoded:
                                captured_serial = decoded
                                st.success(f"✓ Barcode Extracted Successfully: {captured_serial}")
                            else:
                                st.warning("⚠️ Failed to parse barcode from uploaded image.")
                        else:
                            st.warning("⚠️ Barcode scanning unavailable. Please use direct serial entry.")

                with input_tabs[2]:
                    st.info("Manual serial code entry enabled below.")

                # Serial Number Metadata Field
                serial_box_value = captured_serial if captured_serial else ""
                serial_number_input = st.text_input("Enter or Confirm Serial Number:", value=serial_box_value, placeholder="e.g., MGM75000002")

                if serial_number_input:
                    cleaned_serial = serial_number_input.strip().upper()
                    
                    # FIXED: Use robust Excel loading with error handling
                    df_records, load_error = load_excel_safe(target_file)
                    
                    if load_error:
                        st.error(f"❌ Error loading evaluation repository: {load_error}")
                    else:
                        # FIXED: Robust column name matching
                        serial_col = get_excel_column(df_records, ['serial_number', 'serialnumber', 'serial no', 'serial'])
                        
                        if serial_col is None:
                            st.error(f"❌ Target spreadsheet format invalid: Cannot find 'serial_number' column. Available columns: {', '.join(df_records.columns)}")
                        else:
                            match_row = df_records[df_records[serial_col].astype(str).str.strip().str.upper() == cleaned_serial]
                            
                            if not match_row.empty:
                                raw_data_dict = match_row.iloc[0].to_dict()
                                sanitized_data = {
                                    k: ("N/A" if pd.isna(v) else str(v).strip()) 
                                    for k, v in raw_data_dict.items()
                                }
                                
                                render_certificate(
                                    serial_no=cleaned_serial,
                                    test_no=cleaned_test,
                                    data=sanitized_data
                                )
                            else:
                                st.error(f"❌ Serial Number '{cleaned_serial}' not indexed under session {cleaned_test}.")
            else:
                st.error(f"❌ Target session file '{target_file}' not found in current directory. Please upload the Excel file for test {cleaned_test}.")
        else:
            st.error("❌ Invalid Test Code syntax! Expected format: [Month Letter][1-12]-[YY]-[NN]\nExamples: A4-25-01, J12-26-15, D6-25-03")

    st.markdown('</div>', unsafe_allow_html=True)
