import re
import logging

class DataValidator:
    """
    Quality Assurance Layer: Validates the integrity of the 
    Excel/CSV data before it is processed.
    """
    
    def __init__(self):
        self.email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        self.required_columns = [
            "Rilevatore", 
            "Nome Rilevatore", 
            "Email",
            "Tasso di completezza complessivo"
        ]

    def is_valid_email(self, email):
        """Checks if the email string follows a standard format."""
        if not email or not isinstance(email, str):
            return False
        return re.match(self.email_regex, email.strip()) is not None

    def validate_row(self, row):
        """
        Validates a single row for missing critical data.
        Returns (True, None) if valid, (False, error_message) otherwise.
        """
        for col in self.required_columns:
            if col not in row or str(row[col]).strip() == "" or row[col] is None:
                return False, f"Missing required column: {col}"

        email = str(row["Email"]).strip()
        if not self.is_valid_email(email):
            return False, f"Invalid email format: {email}"

        if "%" not in str(row.get("% Tasso di completezza complessivo FOL", "")):
            logging.warning(f"Row for {email} might have unformatted metrics.")

        return True, None

    def filter_valid_data(self, dataframe):
        """
        Processes a dataframe and returns only the rows that pass validation.
        Logs any failures to the execution logs[cite: 3].
        """
        valid_records = []
        invalid_count = 0
        
        records = dataframe.to_dict(orient="records")
        for record in records:
            is_valid, error = self.validate_row(record)
            if is_valid:
                valid_records.append(record)
            else:
                invalid_count += 1
                logging.error(f"Validation failed for Rilevatore {record.get('Rilevatore')}: {error}")
        
        logging.info(f"Validation Complete: {len(valid_records)} passed, {invalid_count} failed.")
        return valid_records