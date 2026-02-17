import os
import logging
import pandas as pd
from src.bootstrap import load_config
from src.reader import load_data
from src.validator import DataValidator
from src.transformer import DataTransformer
from src.mailer import Mailer

logging.basicConfig(
    filename='logs/execution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_files(directory, file_prefix, report_type):
    config = load_config()
    validator = DataValidator()
    transformer = DataTransformer()
    mailer = Mailer(config)

    files = [f for f in os.listdir(directory) if f.startswith(file_prefix)]
    
    if not files:
        raise FileNotFoundError(f"No files found with prefix {file_prefix}")

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        df = load_data(file_path)
        valid_rows = validator.filter_valid_data(df)
        clean_records = transformer.process_batch(pd.DataFrame(valid_rows), report_type)

        template = "folcapi_report.html" if "FOL" in report_type.upper() else "spese_report.html"

        for record in clean_records:
            success = mailer.send_performance_email(record['email'], template, {'user': record})
            if success:
                with open('logs/sent_history.log', 'a') as f:
                    f.write(f"{record['rilevatore_id']},{record['email']},{report_type}\n")