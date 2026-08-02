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
""", unsafe_allow_html=True)

