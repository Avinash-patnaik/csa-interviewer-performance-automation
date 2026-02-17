import streamlit as st
import os
from main import process_files  # Importing the orchestrator logic


st.set_page_config(page_title="CSA Mailer Control Center", page_icon="📧")

st.title("🚀 CSA Interviewer Performance Automation")
st.markdown("Select the campaign type to process files from their specific folders.")

campaign_type = st.radio(
    "Select Campaign Type:",
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