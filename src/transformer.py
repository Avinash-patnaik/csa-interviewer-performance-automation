import logging
import pandas as pd

class DataTransformer:
    def format_pct(self, value):
        try:
            if pd.isna(value) or str(value).lower() in ['nan', 'none', '']:
                return "0,0%"
            if isinstance(value, (float, int)):
                val = value * 100 if -1.0 <= value <= 1.0 else value
                return f"{round(val, 1)}%".replace('.', ',')
            return str(value).strip()
        except:
            return "0,0%"

    def transform_row(self, row, report_type="FOL"):
        try:
            values = list(row.values())
            email_idx = 6 
            is_fol = "FOL" in str(report_type).upper()

            rilevatore_id = str(values[0]) if len(values) > 0 else "N/D"
            nome = str(values[1]).title() if len(values) > 1 else "Rilevatore"
            periodo = str(values[3]) if len(values) > 3 else "N/D"
            anno = str(values[4]) if len(values) > 4 else "N/D"

            def get_block(start_offset):
                idx_list = [email_idx + start_offset, 
                            email_idx + start_offset + 1, 
                            email_idx + start_offset + 2]
                vals = []
                for idx in idx_list:
                    if idx < len(values):
                        vals.append(self.format_pct(values[idx]))
                    else:
                        vals.append("0,0%")
                return vals if is_fol else [vals[0], vals[2]]

            transformed = {
                "rilevatore_id": rilevatore_id,
                "name": nome,
                "email": str(values[email_idx]).strip().lower(),
                "regione": str(row.get("Regione", "N/A")).upper(),
                "periodo": periodo,
                "anno": anno,
                "report_type": "Forze di Lavoro" if is_fol else "Spese",
                "is_fol": is_fol,
                "metrics": {
                    "personali": get_block(1),
                    "regione": get_block(4),
                    "italia": get_block(7)
                }
            }
            return transformed
        except Exception as e:
            logging.error(f"Error: {e}")
            return None

    def process_batch(self, dataframe, report_type="FOL"):
        records = dataframe.to_dict(orient="records")
        return [self.transform_row(r, report_type) for r in records if self.transform_row(r, report_type)]