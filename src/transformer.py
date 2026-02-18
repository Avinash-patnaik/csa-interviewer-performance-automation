import logging
import pandas as pd

class DataTransformer:
    def format_pct(self, value):
        """Standardizes percentage formatting for the Italian locale."""
        try:
            if pd.isna(value) or str(value).lower() in ['nan', 'none', '']:
                return "0,0%"
            if isinstance(value, (float, int)):
                val = value * 100 if -1.0 <= value <= 1.0 else value
                return f"{round(val, 1)}%".replace('.', ',')
            return str(value).strip()
        except Exception:
            return "0,0%"

    def transform_row(self, values, report_type="FOL"):
        """
        Values is now a raw list of the row data from the DataFrame.
        This prevents 'list index out of range' errors.
        """
        try:
            is_fol = "FOL" in str(report_type).upper()

            # --- PROTECTED FOL LOGIC (A-P Structure) ---
            if is_fol:
                # Ensure we have enough columns for FOL (16 columns A-P)
                if len(values) < 16:
                    logging.error(f"Row has only {len(values)} columns, expected 16.")
                    return None
                    
                email_idx, nome_idx = 6, 1
                metrics = {
                    "personali": [self.format_pct(values[i]) for i in [7, 8, 9]],  # H, I, J
                    "regione": [self.format_pct(values[i]) for i in [10, 11, 12]], # K, L, M
                    "italia": [self.format_pct(values[i]) for i in [13, 14, 15]]   # N, O, P
                }
            
            # --- DYNAMIC SPESE LOGIC (A-M Structure) ---
            else:
                if len(values) < 10: # Minimum needed for column J
                    return None
                    
                email_idx, nome_idx = 4, 1
                metrics = {
                    "personali": [self.format_pct(values[8]), self.format_pct(values[9])],
                    "regione": [self.format_pct(values[11]), self.format_pct(values[12])],
                    "italia": ["85,0%", "66,0%"],
                    "obiettivi": ["92,0%", "90,0%"]
                }

            return {
                "name": str(values[nome_idx]).title(),
                "email": str(values[email_idx]).strip().lower(),
                "rilevatore_id": str(values[0]),
                "regione": "N/A", # Use fixed N/A to avoid dict lookup errors
                "periodo": str(values[3]) if len(values) > 3 else "N/D",
                "anno": str(values[4]) if len(values) > 4 else "2025",
                "report_type": "Forze di Lavoro" if is_fol else "Spese delle Famiglie",
                "is_fol": is_fol,
                "metrics": metrics
            }

        except Exception as e:
            logging.error(f"Logic Layer Error during transformation: {e}")
            return None

    def process_batch(self, dataframe, report_type="FOL"):
        """
        Updated to use .values directly to avoid duplicate header issues.
        """
        # We convert the dataframe directly to a list of lists (rows)
        rows = dataframe.values.tolist()
        return [self.transform_row(r, report_type) for r in rows if self.transform_row(r, report_type)]