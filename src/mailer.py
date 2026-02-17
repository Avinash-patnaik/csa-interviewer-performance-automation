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
        logo_path = os.path.join(os.getcwd(), "CSA-RESEARCH.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{encoded}"
        return None

    def send_performance_email(self, recipient, template_name, context):
        try:
            context['logo_base64'] = self.get_encoded_logo()

            template = self.env.get_template(template_name)
            html_content = template.render(context)

            msg = EmailMessage()
            msg['Subject'] = f"Performance Report - {context['user']['report_type']} - {context['user']['periodo']} {context['user']['anno']}"
            msg['From'] = self.config['from']
            msg['To'] = recipient
            msg.set_content("Please use an HTML compatible email client.")
            msg.add_alternative(html_content, subtype='html')

            with smtplib.SMTP(self.config['server'], self.config['port']) as server:
                server.starttls()
                server.login(self.config['user'], self.config['pass'])
                server.send_message(msg)
            
            logging.info(f"Email successfully sent to {recipient}")
            return True

        except Exception as e:
            logging.error(f"SMTP Error for {recipient}: {e}")
            return False