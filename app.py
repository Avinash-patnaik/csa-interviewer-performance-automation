import streamlit as st
import os
import pandas as pd
from main import process_files  

st.set_page_config(page_title="CSA Mailer Control Center", page_icon="📧")

st.title("🚀 CSA Interviewer Performance Automation")
st.markdown("Select the campaign type below to process Excel files and send emails.")

campaign_type = st.radio(
    "Select Campaign Type:",
    ("FOLCAPI", "SPESE"),
    help="This determines which files are scanned and which email template is used."
)

raw_path = "data/raw/"

if st.button(f"Run {campaign_type} Pipeline"):
    prefix = "FOL" if campaign_type == "FOLCAPI" else "SPESE"
    
    with st.status(f"Processing {campaign_type}...", expanded=True) as status:
        st.write(f"🔍 Scanning `{raw_path}` for new files...")
        
        try:
            process_files(directory=raw_path, file_prefix=prefix, report_type=prefix)
            
            status.update(label=f"{campaign_type} Pipeline Completed!", state="complete", expanded=False)
            st.success("Emails sent! Check the `logs/sent_history.log` for details.")
            
        except Exception as e:
            st.error(f"An error occurred during the process: {e}")
            status.update(label="Pipeline Failed", state="error")

st.divider()
st.subheader("📊 Recent Activity")
log_file = "logs/execution.log"

if os.path.exists(log_file):
    with open(log_file, "r") as f:
        log_lines = f.readlines()[-15:]
        st.code("".join(log_lines), language="text")
else:
    st.info("No logs found. Run a pipeline to generate activity history.")