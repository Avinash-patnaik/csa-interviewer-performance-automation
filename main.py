import sys
import os
import logging
import glob
import shutil
from src.bootstrap import config  
from src.reader import load_data     
from src.transformer import DataTransformer
from src.mailer import Mailer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    
    # Templates selection
    template_name = "folcapi_report.html" if "FOL" in report_type.upper() else "spese_report.html"

    for input_file in unprocessed_files:
        filename = os.path.basename(input_file)
        logging.info(f"📂 Processing file: {filename}")
        
        try:
            df = load_data(input_file)
            
            processed_records = transformer.process_batch(df, report_type=report_type)
            
            if not processed_records:
                stop_msg = f"STOPPED: No valid records/emails found in '{filename}'. Check column mapping."
                logging.error(f"🛑 {stop_msg}")
                raise ValueError(stop_msg)

            logging.info(f"📊 {len(processed_records)} records ready. Starting mailing...")

            # Email Dispatch
            success_count = 0
            for record in processed_records:
                if "@" not in str(record.get('email', '')):
                    logging.warning(f"Invalid email found: {record.get('email')}. Skipping row.")
                    continue

                context = {"user": record}
                if mailer.send_performance_email(record['email'], template_name, context):
                    success_count += 1
            
            logging.info(f"✅ Success: {success_count}/{len(processed_records)} emails sent.")

            # Safe Move/Archive
            new_filename = f"PROCESSED_{filename}"
            archive_path = os.path.join(archive_dir, new_filename)
            shutil.move(input_file, archive_path)
            logging.info(f"🔄 State Updated: File moved to {archive_path}")

        except Exception as e:
            logging.error(f"❌ Pipeline halted for {filename}: {str(e)}")
            raise e

if __name__ == "__main__":
    pass