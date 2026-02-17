import streamlit as st
import os
import base64
from PIL import Image
from main import process_files

st.set_page_config(page_title="CSA Mailer Control Center", page_icon="📧", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    .main-title {
        margin-bottom: 0px;
        padding-top: 0px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

LOGO_PATH = os.path.join(os.getcwd(), "CSA-RESEARCH.png")

col1, col2 = st.columns([0.2, 0.9])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=90)
    else:
        st.write("🏢")

with col2:
    st.markdown("<h1 class='main-title'>CSA Interviewer Performance Automation</h1>", unsafe_allow_html=True)

st.markdown("---")

survey_type = st.radio(
    "Select Survey Type:",
    ("FOLCAPI", "SPESE"),
    help="FOL files are read from data/folcapi/ and SPESE from data/spese/"
)

if survey_type == "FOLCAPI":
    target_dir = "data/folcapi/"
    file_prefix = "FOL"
else:
    target_dir = "data/spese/"
    file_prefix = "SPESE"

if st.button(f"🚀 Run {survey_type} Pipeline"):
    with st.status(f"Processing {survey_type}...", expanded=True) as status:
        st.write(f"🔍 Scanning directory: `{target_dir}`")
        
        try:
            process_files(directory=target_dir, file_prefix=file_prefix, report_type=file_prefix)
            status.update(label=f"{survey_type} Pipeline Completed!", state="complete", expanded=False)
            st.success(f"Emails sent! Audit trail updated in `logs/sent_history.log`")
            
        except Exception as e:
            st.error(f"Pipeline Failed: {e}")
            status.update(label="Error Occurred", state="error")

st.divider()
st.subheader("📊 Recent Execution Logs")
log_file = "logs/execution.log"

if os.path.exists(log_file):
    with open(log_file, "r") as f:
        log_lines = f.readlines()[-10:]
        st.code("".join(log_lines), language="text")
else:
    st.info("No logs found. Run a pipeline to generate activity history.")