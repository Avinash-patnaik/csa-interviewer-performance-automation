import pandas as pd
import logging
import os

def load_data(file_path):
    try:
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path, header=None)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, header=None)
        else:
            raise ValueError("Unsupported file format.")

        header_row_index = 0
        for i, row in df.iterrows():
            if "Rilevatore" in row.values:
                header_row_index = i
                break
        
        df.columns = df.iloc[header_row_index]
        df = df.iloc[header_row_index + 1:].reset_index(drop=True)
        df.columns = df.columns.str.strip()
        df = df.dropna(how='all') 
        df = df.loc[:, df.columns.notnull()]

        logging.info(f"Loaded {file_path} - Header at row {header_row_index}")
        return df

    except Exception as e:
        logging.error(f"Reader Error: {e}")
        raise