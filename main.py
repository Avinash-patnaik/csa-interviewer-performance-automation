import sys
import os
import logging
import glob
import shutil

# Ensure project root is in path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bootstrap import config  
from src.reader import load_data     
from src.transformer import DataTransformer
from src.mailer import Mailer

# Set up logging with UTF-8 support for Windows/Emojis
LOG_FILE = "logs/execution.log"
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'), 
        logging.StreamHandler()
    ]
)

def process_files(directory, file_prefix, report_type):
    """
    Orchestrator to scan, process, and archive survey files.
    Includes a Guard Clause to stop if no emails are parsed.
    """
    logging.info(f"🚀 Starting pipeline for {report_type} in {directory}")

    archive_dir = os.path.join(directory, "archive")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        logging.info(f"📁 Created archive directory: {archive_dir}")

    # Discovery: Find files not already processed
    pattern = os.path.join(directory, f"{file_prefix}*.xlsx")
    all_files = glob.glob(pattern)
    unprocessed_files = [
        f for f in all_files 
        if not os.path.basename(f).startswith("PROCESSED_")
    ]

    if not unprocessed_files:
        error_msg = f"No new files starting with '{file_prefix}' found in {directory}."
        logging.warning(f"⚠️ {error_msg}")
        raise Exception(error_msg)

    transformer = DataTransformer()
    mailer = Mailer(config)
    
    # Select template dynamically based on report_type
    template_name = "folcapi_report.html" if "FOL" in report_type.upper() else "spese_report.html"

    for input_file in unprocessed_files:
        filename = os.path.basename(input_file)
        logging.info(f"📂 Processing file: {filename}")
        
        try:
            # 1. Data Ingestion 
            df = load_data(input_file)
            
            # 2. Data Transformation
            processed_records = transformer.process_batch(df, report_type=report_type)
            
            # --- SENIOR GUARD CLAUSE: STOP IF NO EMAILS ---
            # This prevents the script from 'succeeding' with 0 emails
            if not processed_records:
                stop_msg = f"STOPPED: No valid records/emails found in '{filename}'. Check column mapping."
                logging.error(f"🛑 {stop_msg}")
                # Raising an error here skips the mailing and the archive step
                raise ValueError(stop_msg)

            logging.info(f"📊 {len(processed_records)} records ready. Starting mailing...")

            # 3. Email Dispatch
            success_count = 0
            for record in processed_records:
                # Basic validation: ensure email contains '@'
                if "@" not in str(record.get('email', '')):
                    logging.warning(f"Invalid email found: {record.get('email')}. Skipping row.")
                    continue

                context = {"user": record}
                if mailer.send_performance_email(record['email'], template_name, context):
                    success_count += 1
            
            logging.info(f"✅ Success: {success_count}/{len(processed_records)} emails sent.")

            # 4. Final Step: Safe Move/Archive
            # Only reached if the logic above succeeded without raising errors
            new_filename = f"PROCESSED_{filename}"
            archive_path = os.path.join(archive_dir, new_filename)
            shutil.move(input_file, archive_path)
            logging.info(f"🔄 State Updated: File moved to {archive_path}")

        except Exception as e:
            # Logs the error but leaves the file in the RAW folder for fixing
            logging.error(f"❌ Pipeline halted for {filename}: {str(e)}")
            raise e

if __name__ == "__main__":
    pass