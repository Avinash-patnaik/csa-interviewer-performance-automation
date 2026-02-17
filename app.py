import streamlit as st
import os
import pandas as pd
from main import process_files  # Importing the orchestrator logic

# Page Configuration
st.set_page_config(page_title="CSA Mailer Control Center", page_icon="📧")

st.title("🚀 CSA Interviewer Performance Automation")
st.markdown("Select the campaign type below to process Excel files and send emails.")

# 1. Selection UI
campaign_type = st.radio(
    "Select Campaign Type:",
    ("FOLCAPI", "SPESE"),
    help="This determines which files are scanned and which email template is used."
)

# 2. Folder Path Check
# As per your structure, we look into data/raw/ [cite: 2]
raw_path = "data/raw/"

if st.button(f"Run {campaign_type} Pipeline"):
    # Determine file prefix based on selection
    prefix = "FOL" if campaign_type == "FOLCAPI" else "SPESE"
    
    with st.status(f"Processing {campaign_type}...", expanded=True) as status:
        st.write("🔍 Scanning `data/raw/` for new files...")
        
        try:
            # Triggering the main processing logic 
            process_files(directory=raw_path, file_prefix=prefix, report_type=prefix)
            
            status.update(label=f"{campaign_type} Pipeline Completed!", state="complete", expanded=False)
            st.success(f"Emails sent! Check the logs/sent_history.log for details.") [cite: 3]
            
        except Exception as e:
            st.error(f"An error occurred during the process: {e}")
            status.update(label="Pipeline Failed", state="error")

# 3. Execution Logs Preview
st.divider()
st.subheader("📊 Recent Activity")
log_file = "logs/execution.log" [cite: 3]

if os.path.exists(log_file):
    with open(log_file, "r") as f:
        # Show last 15 lines of logs
        log_lines = f.readlines()[-15:]
        st.code("".join(log_lines), language="text")
else:
    st.info("No logs found. Run a pipeline to generate activity history.")