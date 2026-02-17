import logging

class DataTransformer:
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
        
        self.spese_mapping = {
            "nazionale": {
                "completezza": "Tasso Complessivo Spese",
                "due_settimane": "Tasso Prime 2 Settimane Spese",
                "recapiti": "% Recapiti Spese"
            },
            "regionale": {
                "completezza": "% Tasso Regionale Spese",
                "due_settimane": "% Tasso Regionale 2 Settimane",
                "recapiti": "% Recapiti Regionali Spese"
            }
        }

    def format_pct(self, value):
        try:
            if value is None or str(value).lower() == 'nan':
                return "0%"
            if isinstance(value, (float, int)):
                if value <= 1.0:
                    return f"{round(value * 100, 1)}%"
                return f"{round(value, 1)}%"
            return str(value)
        except:
            return str(value)

    def transform_row(self, row, report_type="FOL"):
        try:
            transformed = {
                "rilevatore_id": row.get("Rilevatore"),
                "name": str(row.get("Nome Rilevatore", "")).title(),
                "email": str(row.get("Email", "")).strip().lower(),
                "regione": row.get("Regione", "N/A"),
                "periodo": row.get("periodo", "N/D"),
                "anno": row.get("Anno", "N/D"),
                "report_type": report_type.upper(),
                "metrics": {"nazionale": {}, "regionale": {}}
            }

            mapping = self.fol_mapping if "FOL" in report_type.upper() else self.spese_mapping 
            
            transformed["metrics"]["nazionale"] = {
                "completezza": self.format_pct(row.get(mapping["nazionale"]["completezza"])),
                "due_settimane": self.format_pct(row.get(mapping["nazionale"]["due_settimane"])),
                "recapiti": self.format_pct(row.get(mapping["nazionale"]["recapiti"]))
            }

            transformed["metrics"]["regionale"] = {
                "completezza": self.format_pct(row.get(mapping["regionale"]["completezza"])),
                "due_settimane": self.format_pct(row.get(mapping["regionale"]["due_settimane"])),
                "recapiti": self.format_pct(row.get(mapping["regionale"]["recapiti"]))
            }

            return transformed

        except Exception as e:
            logging.error(f"Error transforming row: {e}")
            return None

    def process_batch(self, dataframe, report_type="FOL"):
        raw_records = dataframe.to_dict(orient="records")
        clean_records = []
        for record in raw_records:
            clean_data = self.transform_row(record, report_type)
            if clean_data:
                clean_records.append(clean_data)
        return clean_records