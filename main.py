import os
import logging
from datetime import datetime
from src.bootstrap import load_config, load_env
from src.reader import load_data
from src.validator import DataValidator
from src.transformer import DataTransformer
from src.mailer import Mailer

# Initialize Logging for the logic layer 
logging.basicConfig(
    filename='logs/execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_files(directory, file_prefix, report_type):
    """
    Main Pipeline Logic: Read -> Validate -> Transform -> Mail.
    This function is now the entry point for the Streamlit GUI.
    """
    load_env()
    config = load_config()
    
    validator = DataValidator()
    transformer = DataTransformer()
    mailer = Mailer(config) 

    target_files = [f for f in os.listdir(directory) if f.startswith(file_prefix)]
    
    if not target_files:
        logging.warning(f"No files found for {file_prefix} in {directory}")
        raise FileNotFoundError(f"No {file_prefix} files found in {directory}")

    for file_name in target_files:
        file_path = os.path.join(directory, file_name)
        logging.info(f"Processing: {file_name}")
        
        df = load_data(file_path)
        
        # 4. VALIDATE: Ensure emails and data are clean [cite: 5, 6]
        valid_rows = validator.filter_valid_data(df)
        
        # 5. TRANSFORM: Prepare metrics for the specific report type [cite: 4]
        clean_records = transformer.process_batch(valid_rows, report_type)
        
        # 6. MAIL: Send using templates 
        template = "fol_report.html" if report_type == "FOL" else "spese_report.html"
        
        for record in clean_records:
            success = mailer.send_performance_email(
                recipient=record['email'],
                template_name=template,
                context={'user': record}
            )
            
            if success:
                with open("logs/sent_history.log", "a") as f:
                    f.write(f"{datetime.now()}, {record['email']}, {file_name}\n")
        
    return True

if __name__ == "__main__":
    process_files(directory="data/raw/", file_prefix="FOL", report_type="FOL")