import re
import logging

class DataValidator:
    def __init__(self):
        self.email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def is_valid_email(self, email):
        if not email or str(email).lower() == 'nan':
            return False
        return re.match(self.email_regex, str(email).strip()) is not None

    def filter_valid_data(self, df):
        valid_rows = []
        for _, row in df.iterrows():
            rilevatore_id = row.get("Rilevatore")
            email = row.get("Email")

            if not rilevatore_id or str(rilevatore_id).lower() == 'nan':
                logging.error("Validation failed: Missing Rilevatore ID")
                continue

            if not self.is_valid_email(email):
                logging.error(f"Validation failed for ID {rilevatore_id}: Invalid Email '{email}'")
                continue

            valid_rows.append(row.to_dict())
            
        logging.info(f"Validation Complete: {len(valid_rows)} records passed.")
        return valid_rows