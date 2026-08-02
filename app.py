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
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Space+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
            }}

            body {{
                background-color: #07090e;
                font-family: 'Inter', system-ui, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 0;
                padding: 10px;
            }}
            
            .report-card {{
                background: #0d111a;
                color: #ffffff;
                width: 100%;
                max-width: 480px;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 24px;
                box-sizing: border-box;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
            }}

            .card-header {{
                text-align: left;
                border-bottom: 1px solid #1e293b;
                padding-bottom: 14px;
                margin-bottom: 18px;
            }}
            .sub-tag {{
                font-family: 'Space Mono', monospace;
                color: #eab308;
                font-size: 9px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            .main-name {{
                font-family: 'Playfair Display', Georgia, serif;
                color: #ffffff;
                font-size: 24px;
                font-weight: 700;
                margin: 4px 0;
            }}
            .school-tag {{
                color: #94a3b8;
                font-size: 11px;
            }}

            /* Top Banner Grid */
            .top-metrics {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-bottom: 18px;
            }}
            .metric-box {{
                background: #141b2d;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 12px;
            }}
            .m-label {{
                font-family: 'Space Mono', monospace;
                color: #94a3b8;
                font-size: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: block;
            }}
            .m-val {{
                color: #eab308;
                font-size: 22px;
                font-weight: 800;
                margin-top: 2px;
                font-family: 'Playfair Display', serif;
            }}

            /* Data Details Table */
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 18px;
            }}
            .info-item {{
                background: #111622;
                padding: 10px 12px;
                border-radius: 6px;
                border-left: 3px solid #eab308;
            }}
            .label {{
                font-family: 'Space Mono', monospace;
                color: #64748b;
                font-size: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
                display: block;
            }}
            .value {{
                color: #f8fafc;
                font-weight: 700;
                font-size: 13px;
                margin-top: 2px;
            }}

            /* Progress Bar */
            .analytics-box {{
                background: #111622;
                padding: 14px;
                border-radius: 8px;
                border: 1px solid #1e293b;
                margin-bottom: 20px;
            }}
            .bar-container {{
                background: #1e293b;
                height: 10px;
                border-radius: 5px;
                overflow: hidden;
                margin-top: 8px;
            }}
            .bar-fill {{
                height: 100%;
                background: linear-gradient(90deg, #ca8a04 0%, #facc15 100%);
                width: {pct_num}%;
            }}

            .print-btn {{
                background: #eab308;
                color: #000000;
                border: none;
                padding: 12px;
                font-weight: 800;
                border-radius: 6px;
                cursor: pointer;
                letter-spacing: 1px;
                text-transform: uppercase;
                width: 100%;
                font-size: 11px;
            }}

            /* Strict Print/PDF Color Preservation */
            @media print {{
                body {{
                    background-color: #07090e !important;
                }}
                .report-card {{
                    background: #0d111a !important;
                    border: 1px solid #1e293b !important;
                    box-shadow: none !important;
                }}
                .print-btn {{ display: none !important; }}
            }}
        </style>
    </head>
    <body>
        <div class="report-card">
            <div class="card-header">
                <span class="sub-tag">PROGRESS REPORT · EXAMINATION</span>
                <div class="main-name">{name}</div>
                <div class="school-tag">Class {cls} ({section}) · Roll No: {roll_no}</div>
            </div>

            <div class="top-metrics">
                <div class="metric-box">
                    <span class="m-label">TOTAL SCORE</span>
                    <div class="m-val">{test_score}</div>
                </div>
                <div class="metric-box">
                    <span class="m-label">PERCENTAGE</span>
                    <div class="m-val">{percentage_str}</div>
                </div>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <span class="label">SUBJECT</span>
                    <span class="value">{subject}</span>
                </div>
                <div class="info-item">
                    <span class="label">CLASS RANK</span>
                    <span class="value">{rank}</span>
                </div>
                <div class="info-item">
                    <span class="label">BOOK SERIAL NO</span>
                    <span class="value">{serial_no}</span>
                </div>
                <div class="info-item">
                    <span class="label">TEST CODE</span>
                    <span class="value">{test_no}</span>
                </div>
            </div>

            <div class="analytics-box">
                <div style="display: flex; justify-content: space-between; font-size: 10px; font-family: 'Space Mono', monospace;">
                    <span style="color: #94a3b8;">OVERALL PERFORMANCE</span>
                    <span style="color: #eab308; font-weight: 700;">{percentage_str}</span>
                </div>
                <div class="bar-container">
                    <div class="bar-fill"></div>
                </div>
            </div>
            
            <button class="print-btn" onclick="window.print()">️ Print / Save PDF</button>
        </div>
    </body>
    </html>
    """
    components.html(card_html, height=580)

