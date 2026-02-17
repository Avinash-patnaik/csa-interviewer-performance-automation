import pandas as pd
import os 
import logging

def load_data(file_path):
    """
    Reads an Excel or CSV file into a pandas DataFrame.
    Supports both .xlsx and .csv formats.
    """
    try:
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Only .xlsx and .csv are allowed.")
        
        logging.info(f"Loaded data from {file_path} with shape {df.shape}")

        df.columns = df.columns.str.strip()

        df = df.dropna(how='all') 

        logging.info(f"Data after cleaning has shape {df.shape}")

        return df

    except Exception as e:
            logging.error(f"Error loading data from {file_path}: {e}")
            raise
    
def get_rilevatore_email(df):
    """
    Extracts the email address of the Rilevatore from the DataFrame.        
    Assumes the email is in a column named 'Email' and that there is only one unique email per file.
    """
    return df.to_dict(orient="records")[0].get("Email", "").strip().lower()