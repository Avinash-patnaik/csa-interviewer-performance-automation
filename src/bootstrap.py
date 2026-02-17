import yaml
import os
from dotenv import load_dotenv

def load_all_configs():
    """Combines .env secrets and YAML settings into one dictionary."""
    load_dotenv()

    config_path = os.path.join("config", "settings.yaml")
    with open(config_path, "r") as f:
        settings = yaml.safe_load(f)
    
    settings['smtp_auth'] = {
        "user": os.getenv("SMTP_USER"),
        "pass": os.getenv("SMTP_PASSWORD"),
        "from": os.getenv("MAIL_FROM"),
        "server": os.getenv("SMTP_SERVER"),
        "port": int(os.getenv("SMTP_PORT", 587))
    }
    
    return settings