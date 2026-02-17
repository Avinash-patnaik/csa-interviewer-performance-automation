import yaml
import os
from dotenv import load_dotenv

def load_all_configs():
    """Combines .env secrets and YAML settings into one dictionary."""
    # 1. Load Secrets from .env
    load_dotenv()
    
    # [cite_start]2. Load Structural Settings from YAML [cite: 2]
    config_path = os.path.join("config", "settings.yaml")
    with open(config_path, "r") as f:
        settings = yaml.safe_load(f)
    
    # 3. Merge them
    # [cite_start]We take the SMTP details directly from .env for security [cite: 1]
    settings['smtp_auth'] = {
        "user": os.getenv("SMTP_USER"),
        "pass": os.getenv("SMTP_PASSWORD"),
        "from": os.getenv("MAIL_FROM"),
        "server": os.getenv("SMTP_SERVER"),
        "port": int(os.getenv("SMTP_PORT", 587))
    }
    
    return settings