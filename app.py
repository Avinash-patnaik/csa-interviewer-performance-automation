import streamlit as st
import os
from PIL import Image
from main import process_files  


st.set_page_config(page_title="CSA Mailer Control Center", page_icon="📧")

LOGO_PATH = os.path.join(os.getcwd(), "CSA-RESEARCH.png")

col1, col2 = st.columns([0.1, 0.9])

with col1:
    if os.path.exists(LOGO_PATH):
        logo_img = Image.open(LOGO_PATH)
        st.image(logo_img, width=100)
    else:
        st.write("🏢") # Fallback if logo is missing

with col2:
    st.title("CSA Interviewer Performance Automation")
st.markdown("Select the survey type to process files from their specific folders.")

campaign_type = st.radio(
    "Select Survey Type:",
    ("FOLCAPI", "SPESE"),
    help="FOL files are read from data/folcapi/ and SPESE from data/spese/"
)

if campaign_type == "FOLCAPI":
    target_dir = "data/folcapi/"
    file_prefix = "FOL"
else:
    target_dir = "data/spese/"
    file_prefix = "SPESE"

if st.button(f"Run {campaign_type} Pipeline"):
    with st.status(f"Processing {campaign_type}...", expanded=True) as status:
        st.write(f"🔍 Searching in `{target_dir}` for files starting with `{file_prefix}`...")
        
        try:
            process_files(directory=target_dir, file_prefix=file_prefix, report_type=file_prefix)
            
            status.update(label=f"{campaign_type} Pipeline Completed!", state="complete", expanded=False)
            st.success(f"Emails sent successfully! Review `logs/sent_history.log`.")
            
        except Exception as e:
            st.error(f"Pipeline Error: {e}")
            status.update(label="Pipeline Failed", state="error")

st.divider()
st.subheader("📊 Recent Activity")
log_file = "logs/execution.log"

if os.path.exists(log_file):
    with open(log_file, "r") as f:
        log_lines = f.readlines()[-10:]
        st.code("".join(log_lines), language="text")
else:
    st.info("No logs found. Run a pipeline to generate activity history.")