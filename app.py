import streamlit as st
import os
import logging
from main import process_files

ICON_PATH = os.path.join(os.getcwd(), "csa-logo.ico")

# Page Configuration
st.set_page_config(
    page_title="CSA Mailer Control Center", 
    page_icon=ICON_PATH if os.path.exists(ICON_PATH) else "📧", 
    layout="wide"
)

st.markdown(
    """
    <style>
    /* Center the main container */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        width: 100%;
        margin-top: -50px; /* Adjust top padding */
    }
    
    .logo-img {
        margin-bottom: 20px;
    }

    .thick-blue-line {
        height: 8px; /* Extra thick */
        background-color: #004a99;
        width: 100%; /* Line spans 100% of the screen width */
        border-radius: 5px;
        margin-bottom: 20px;
    }

    .main-title {
        font-weight: 800;
        color: #004a99;
        font-size: 3rem;
        letter-spacing: -1px;
    }
    
    /* Standard Streamlit adjustments */
    .stRadio > label {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

LOGO_PATH = os.path.join(os.getcwd(), "CSA-RESEARCH.png")

st.markdown('<div class="header-container">', unsafe_allow_html=True)
if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=300) 
else:
    st.markdown("## 🏢 CSA RESEARCH")

st.markdown('<div class="thick-blue-line"></div>', unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>CSA Interviewer Performance Automation</h1>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# Pipeline Selection Layer
survey_type = st.radio(
    "Select Survey Type:",
    ("FOLCAPI", "SPESE"),
    help="FOL files are read from data/folcapi/ and SPESE from data/spese/"
)

# Mapping to correct directory structure 
if survey_type == "FOLCAPI":
    target_dir = os.path.join("data", "folcapi")
    file_prefix = "FOL"
    report_label = "Forze di Lavoro (FOL)"
else:
    target_dir = os.path.join("data", "spese")
    file_prefix = "SPESE"
    report_label = "Spese delle Famiglie (SPESE)"

# Execution Section
st.subheader(f"Pipeline Management: {report_label}")
col_btn, col_info = st.columns([0.3, 0.7])

with col_btn:
    run_pressed = st.button(f"🚀 Run {survey_type} Pipeline", use_container_width=True)

with col_info:
    st.info(f"Directory: `{target_dir}/` | Prefix: `{file_prefix}*.xlsx`")

if run_pressed:
    with st.status(f"Processing {survey_type}...", expanded=True) as status:
        st.write(f"🔍 Scanning directory for new files...")
        
        try:
            process_files(
                directory=target_dir, 
                file_prefix=file_prefix, 
                report_type=file_prefix
            )
            
            status.update(label=f"{survey_type} Pipeline Completed!", state="complete", expanded=False)
            st.success(f"Successfully processed and archived files in `{target_dir}/archive/`")
            st.balloons()
            
        except Exception as e:
            st.error(f"Pipeline Failed: {str(e)}")
            status.update(label="Error Occurred", state="error")

# Logging & Audit Trail Section
st.divider()
st.subheader("📊 Recent Execution Logs")

log_file = "logs/execution.log"

if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        log_lines = f.readlines()[-15:]
        st.code("".join(log_lines), language="text")
    
    if st.button("Clear View Log"):
        st.rerun()
else:
    st.info("No logs found. Execution history will appear here after the first run.")

# Footer
st.markdown(
    """
    <div style='text-align: center; color: #b2bec3; padding-top: 50px;'>
        <small>© 2026 CSA Research - Data Engineering Pipeline</small>
    </div>
    """, 
    unsafe_allow_html=True
)