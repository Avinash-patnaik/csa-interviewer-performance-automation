import smtplib
import os 
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape

class Mailer:
    """
    Handles email composition and sending using SMTP.
    Uses Jinja2 templates for dynamic content generation.
    Configuration is loaded from the bootstrap settings.
    """
    def __init__(self, config):
        self.smtp_user = config['smtp_auth']['user']
        self.smtp_pass = config['smtp_auth']['pass']
        self.smtp_server = config['smtp_auth']['server']
        self.smtp_port = config['smtp_auth']['port']
        self.mail_from = config['smtp_auth']['from']
        
        # Setup Jinja2 Environment for templates
        self.jinja_env = Environment(loader=FileSystemLoader('templates'),
                                        autoescape=select_autoescape(['html', 'xml']))
        
    def send_performance_email(self, recipient, template_name, context):
        """
        Composes and sends an email based on the provided template and context.
        Returns True if successful, False otherwise.
        """
        try:
            # Load and render the template with context
            template = self.jinja_env.get_template(template_name)
            html_content = template.render(context)
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.mail_from
            msg['To'] = recipient
            msg['Subject'] = f"Report Performance {context['user']['report_type']} - {context['user']['name']}"
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            
            logging.info(f"Email sent to {recipient}")
            return True
        
        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {e}")
            return False