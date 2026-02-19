import logging
import pandas as pd

class DataTransformer:
    def __init__(self):
        # Mappings 
        self.COMMON_MAP = {
            "id": 0, "nome": 1, "regione": 2, 
            "sv": 3, "email": 4, "periodo": 5, "anno": 6
        }

        self.METRIC_MAP = {
            "FOL": {
                "label": "Forze di Lavoro",
                "personale": [7, 8, 9],    
                "regione": [10, 11, 12],
                "italia": [13, 14, 15]
            },
            "SPESE": {
                "label": "Spese delle Famiglie",
                "personale": [7, 8],     
                "regione": [9, 10],
                "italia": [11, 12]
            }
        }

    def format_pct(self, value):
        """Standardizes percentage formatting for Italian business locale (comma decimal)."""
        try:
            if pd.isna(value) or str(value).lower() in ['nan', 'none', '', 'n/d']:
                return "0,0%"
            
            # data conversion from float to percentage
            if isinstance(value, (float, int)):
                val = value * 100 if -1.0 <= value <= 1.0 else value
                return f"{round(val, 1)}%".replace('.', ',')
            
            return str(value).strip().replace('.', ',')
        except Exception:
            return "0,0%"

    def transform_row(self, row_values, report_type="FOL"):
        """
        Processes a single row into a standardized dictionary.
        """
        try:
            r_type = "FOL" if "FOL" in str(report_type).upper() else "SPESE"
            m_cfg = self.METRIC_MAP[r_type]
            c_cfg = self.COMMON_MAP

            email_val = str(row_values[c_cfg["email"]]).strip().lower()
            if "@" not in email_val:
                return None
            
            metrics = {
                "personali": [self.format_pct(row_values[i]) for i in m_cfg["personale"]],
                "regione":   [self.format_pct(row_values[i]) for i in m_cfg["regione"]],
                "italia":    [self.format_pct(row_values[i]) for i in m_cfg["italia"]]
            }

            return {
                "id": str(row_values[c_cfg["id"]]),         
                "name": str(row_values[c_cfg["nome"]]).title(),
                "email": email_val,
                "regione": str(row_values[c_cfg["regione"]]).upper(),
                "periodo": str(row_values[c_cfg["periodo"]]),
                "anno": str(row_values[c_cfg["anno"]]),
                "report_type": m_cfg["label"],            
                "is_fol": r_type == "FOL",
                "metrics": metrics
            }

        except (IndexError, KeyError) as e:
            logging.error(f"Row structure error in {report_type}: {e}")
            return None

    def process_batch(self, dataframe, report_type="FOL"):
        """Entry point for the pipeline to process an entire sheet."""
        rows = dataframe.values.tolist()
        return [self.transform_row(r, report_type) for r in rows if self.transform_row(r, report_type)]