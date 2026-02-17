import logging

class DataTransformer:
    """
    Handles the mapping and sanitization of raw Excel/CSV data 
    into a structured format for email templates.
    """
    
    def __init__(self):
        self.fol_mapping = {
            "nazionale": {
                "completezza": "Tasso di completezza complessivo",
                "due_settimane": "Tasso completezza interviste complete nelle prime due settimane",
                "recapiti": "% Recapiti telefonici inseriti"
            },
            "regionale": {
                "completezza": "% Tasso di completezza complessivo FOL",
                "due_settimane": "% Tasso  di completezza prime due settimane FOL",
                "recapiti": "% Recapiti telefonici inseriti FOL"
            }
        }

    def transform_row(self, row, report_type="FOL"):
        """
        Transforms a single row (dictionary) from the pandas reader into a 
        structured dictionary for the Jinja2 templates.
        """
        try:
            transformed = {
                "rilevatore_id": row.get("Rilevatore"),
                "name": str(row.get("Nome Rilevatore", "")).title(),
                "email": row.get("Email", "").strip().lower(),
                "regione": row.get("Regione", "N/A"),
                "report_type": report_type.upper(),
                "metrics": {}
            }

            mapping = self.fol_mapping 
            
            transformed["metrics"]["nazionale"] = {
                "completezza": row.get(mapping["nazionale"]["completezza"], "0%"),
                "due_settimane": row.get(mapping["nazionale"]["due_settimane"], "0%"),
                "recapiti": row.get(mapping["nazionale"]["recapiti"], "0%")
            }

            transformed["metrics"]["regionale"] = {
                "completezza": row.get(mapping["regionale"]["completezza"], "0%"),
                "due_settimane": row.get(mapping["regionale"]["due_settimane"], "0%"),
                "recapiti": row.get(mapping["regionale"]["recapiti"], "0%")
            }

            return transformed

        except Exception as e:
            logging.error(f"Error transforming row for {row.get('Email')}: {e}")
            return None

    def process_batch(self, dataframe, report_type="FOL"):
        """
        Converts an entire dataframe into a list of clean, email-ready dictionaries.
        """
        raw_records = dataframe.to_dict(orient="records")
        clean_records = []

        for record in raw_records:
            clean_data = self.transform_row(record, report_type)
            if clean_data:
                clean_records.append(clean_data)
        
        return clean_records