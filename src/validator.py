import pandas as pd 

def validate_data(df, mode, config):

    required_columns = config['excel_columns'][mode].values()

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        
    email_col = config['excel_columns'][mode]['email']
    if not df[email_col].apply(lambda x: isinstance(x, str) and "@" in x).all():
        raise ValueError(f"Invalid email format in column: {email_col}")
    valid_rows = df[email_col].apply(lambda x: isinstance(x, str) and "@" in x)
    if not valid_rows.all():
        invalid_count = (~valid_rows).sum()
        raise ValueError(f"Found {invalid_count} invalid email(s) in column: {email_col}")
    
    return valid_rows