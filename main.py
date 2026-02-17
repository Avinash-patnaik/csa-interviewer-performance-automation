import os
import logging
import pandas as pd
from datetime import datetime
from src.bootstrap import load_config
from src.mailer import Mailer
from src.transformer import DataTransformer

def process_files(directory, file_prefix, report_type):
    config = load_config()
    transformer = DataTransformer()
    mailer = Mailer(config)
    
    log_file = "logs/execution.log"
    os.makedirs("logs", exist_ok=True)

    files = [f for f in os.listdir(directory) if f.startswith(file_prefix)]
    
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        df = pd.read_excel(file_path, header=1)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.dropna(how='all')
        
        clean_records = transformer.process_batch(df, report_type)
        template = "folcapi_report.html" if "FOL" in report_type.upper() else "spese_report.html"

        for record in clean_records:
            success = mailer.send_performance_email(
                recipient=record['email'], 
                template_name=template, 
                context={'user': record}
            )
            
            if success:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] SUCCESS: Email inviata a {record['name']} (ID: {record['rilevatore_id']}) - {record['email']}\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                print(log_entry.strip())
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_entry = f"[{timestamp}] ERROR: Invio fallito per {record['name']} - {record['email']}\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(error_entry)