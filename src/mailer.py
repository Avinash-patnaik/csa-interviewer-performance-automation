import smtplib
import os
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import logging

class Mailer:
    def __init__(self, config):
        self.config = config['smtp_auth']
        template_dir = os.path.join(os.getcwd(), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def send_performance_email(self, recipient, template_name, context):
        try:
            template = self.env.get_template(template_name)
            html_content = template.render(context)

            msg = EmailMessage()
            msg['Subject'] = f"Performance Report - {context['user']['report_type']}"
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