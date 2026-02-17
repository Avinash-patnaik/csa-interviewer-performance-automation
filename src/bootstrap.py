import os 
import sys
from dotenv import load_dotenv
import yaml


def load_config():

    load_dotenv()

    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)

    config['smtp']['user'] = os.getenv("SMTP_USER")
    config['smtp']['password'] = os.getenv("SMTP_PASSWORD")

    return config