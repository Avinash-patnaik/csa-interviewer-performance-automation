import streamlit as st
import os
from main import process_files

# Page Configuration
ICON_PATH = os.path.join(os.getcwd(), "csa-logo.ico")
st.set_page_config(
    page_title="CSA Mailer Control Center", 
    page_icon=ICON_PATH if os.path.exists(ICON_PATH) else "📧", 
    layout="wide"
)

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .stApp { background-color: #E3F2FD !important; }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }

    /* Global Text: Pure Black */
    html, body, [class*="st-"], p, h1, h2, h3, label, span {
        color: #000000 !important;
    }

    /* Survey Selection Text Sizes */
    [data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #004a99 !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    /* Containers: Grey with PURE BLACK Border */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #F5F5F5 !important; 
        border: 2px solid #000000 !important;
        border-radius: 15px !important;
        padding: 20px;
        min-height: 160px; 
    }

    /* TOGGLE COLOR EFFECT FOR BUTTON */
    div.stButton > button {
        background-color: #ADD8E6 !important;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid #004a99 !important;
        transition: all 0.3s ease;
        width: 100%;
        height: 4rem;
    }
    div.stButton > button:hover {
        background-color: #004a99 !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
    }

    /* Branding */
    .header-container { display: flex; flex-direction: column; align-items: center; text-align: center; }
    .thick-blue-line { height: 10px; background-color: #004a99; width: 100%; border-radius: 10px; margin: 5px 0; }
    .main-title { font-weight: 800; color: #004a99 !important; font-size: 3rem; margin-bottom: 0px !important; }
    
    hr { margin-top: 5px !important; margin-bottom: 10px !important; }
    .monitoring-flex-container {
        display: flex;
        flex-direction: row;
        justify-content: flex-start; /* Aligns items to the left */
        align-items: center;
        gap: 40px; /* Space between the items */
        background-color: #E0E0E0;
        padding: 15px 25px;
        border-radius: 8px;
        border-left: 8px solid #004a99;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 13px;
        width: 100%;
    }

    .monitoring-item {
        white-space: nowrap; /* Prevents text from wrapping to a new line */
    }

    .monitoring-label {
        color: #004a99;
        font-weight: bold;
        margin-right: 5px;
    }
    .log-container-box {
        background-color: #0A0A0A !important;
        border: 2px solid #333333;
        border-radius: 8px;
        padding: 15px;
        height: 250px;
        overflow-y: auto;

    #log-section .log-container-box, 
    #log-section .log-container-box * {
        font-size: 8px !important;
        line-height: 1.3 !important;
        /* Classic terminal font stack */
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        font-weight: 400 !important; /* Forces non-bold */
        letter-spacing: 0.5px !important;
    }

    .log-container-box {
        background-color: #0A0A0A !important;
        border: 2px solid #333333 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        height: 250px !important;
        overflow-y: auto !important;
    }

    .log-row {
        color: #00FF41 !important; 
        margin: 0 !important;
        padding: 1px 0 !important;
        display: block !important;
        border-bottom: 1px solid #1A1A1A !important;
        white-space: pre !important;
        font-weight: 300 !important; 
    }
    .folder-info-box {
        display: flex; 
        flex-wrap: wrap; 
        justify-content: space-between; 
        background-color: #E0E0E0;
        padding: 15px;
        border-radius: 8px;
        border-left: 8px solid #004a99;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        margin-top: 10px;
    }

    .info-item {
        margin-right: 20px; 
    }

    .info-item:last-child {
        margin-right: 20px; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
LOGO_PATH = os.path.join(os.getcwd(), "CSA-RESEARCH.png")
st.markdown('<div class="header-container">', unsafe_allow_html=True)
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=450)
st.markdown('<div class="thick-blue-line"></div>', unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>CSA - Sistema di Indicatori di Performance per i Rilevatori</h1>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Survey Selection 
with st.container(border=True):
    st.markdown("### 🛠️Survey Selection")
    survey_type = st.radio("Choose Type:", ("FOLCAPI", "SPESE"))
    
    # path mapping 
    target_dir = os.path.join("data", "folcapi") if survey_type == "FOLCAPI" else os.path.join("data", "spese")
    file_prefix = "FOL" if survey_type == "FOLCAPI" else "SPESE"

col1, col2 = st.columns([0.4, 1], gap="medium")

with col1:
    with st.container(border=True):
        st.markdown(f"### 🚀{survey_type} PIPELINE")
        if st.button(f"Run {survey_type} Pipeline"):
            with st.status("Processing...", expanded=True) as status:
                try: 
                    process_files(directory=target_dir, file_prefix=file_prefix, report_type=file_prefix)
                    status.update(label="Complete!", state="complete")
                    st.balloons()
                except Exception as e:
                    st.error(f"Pipeline Error: {e}")

with col2:
    with st.container(border=True):
        st.markdown("### 🔍 Monitoring Path")
        st.markdown(
            f"""
            <div class="monitoring-flex-container">
                <div class="monitoring-item">
                    <span class="monitoring-label">STATUS:</span> ACTIVE
                </div>
                <div class="monitoring-item">
                    <span class="monitoring-label">PATH:</span> /{target_dir}
                </div>
                <div class="monitoring-item">
                    <span class="monitoring-label">FILTER:</span> {file_prefix}*.xlsx
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
st.markdown('<div id="log-section">', unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("📊 Recent Execution Logs")
    log_path = os.path.join("logs", "execution.log") 
    
    if os.path.exists(log_path): 
        with open(log_path, "r", encoding="utf-8") as f:
            log_lines = f.readlines()[-25:] 
            
            log_html = '<div class="log-container-box">'
            for line in log_lines:
                log_html += f'<div class="log-row">{line.strip()}</div>'
            log_html += '</div>'
            
            st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.info("No logs found in logs/ directory.") 
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Refresh Logs"):
    st.rerun()