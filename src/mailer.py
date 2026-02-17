import smtplib
import os
import base64
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import logging

class Mailer:
    def __init__(self, config):
        self.config = config['smtp_auth']
        template_dir = os.path.join(os.getcwd(), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def get_encoded_logo(self):
        # Adjusted to match your specific filename: CSA-RESEARCH.png
        logo_path = os.path.join(os.getcwd(), "CSA-RESEARCH.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{encoded}"
        return None

    def send_performance_email(self, recipient, template_name, context):
        try:
            user = context['user']
            context['logo_base64'] = self.get_encoded_logo()

            template = self.env.get_template(template_name)
            html_content = template.render(context)

            msg = EmailMessage()
            
            # Specific Subject Format: Indagine Forze di Lavoro - Indicatori di performance Trimestre 4 2025
            msg['Subject'] = f"Indagine {user['report_type']} - Indicatori di performance {user['periodo']} {user['anno']}"
            
            msg['From'] = self.config['from']
            msg['To'] = recipient
            msg.set_content("Contenuto HTML non supportato.")
            msg.add_alternative(html_content, subtype='html')

            with smtplib.SMTP(self.config['server'], self.config['port']) as server:
                server.starttls()
                server.login(self.config['user'], self.config['pass'])
                server.send_message(msg)
            
            logging.info(f"Email inviata con successo a: {recipient}")
            return True

        except Exception as e:
            logging.error(f"Errore SMTP per {recipient}: {e}")
            return False