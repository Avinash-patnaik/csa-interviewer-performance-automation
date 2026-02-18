import smtplib
import os
import logging
from email.message import EmailMessage
from email.utils import make_msgid # For unique image IDs
from jinja2 import Environment, FileSystemLoader

class Mailer:
    def __init__(self, config):
        """
        Initializes the Mailer with SMTP settings.
        """
        self.config = config['smtp_auth']

        # Presentation Layer - Templates
        template_dir = os.path.join(os.getcwd(), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # Path to the logo file
        self.logo_path = os.path.join(os.getcwd(), "CSA-RESEARCH.png")

    def send_performance_email(self, recipient, template_name, context):
        """Sends the email using CID embedding for maximum client compatibility."""
        try:
            # Generate a unique Content-ID for the image
            logo_cid = make_msgid()
            # Pass the CID to the template (removing the < > brackets for the src tag)
            context['logo_cid'] = logo_cid[1:-1]
            
            template = self.env.get_template(template_name)
            html_content = template.render(context)

            msg = EmailMessage()
            user = context.get('user', {})
            
            # MAINTAINED: Your specific subject and headers
            msg['Subject'] = f"Indagine {user.get('report_type')} - Indicatori di performance {user.get('periodo')} {user.get('anno')}"
            msg['From'] = self.config['from']
            msg['To'] = recipient
            
            # Text fallback
            msg.set_content("Per visualizzare questa comunicazione è necessario un client email compatibile con HTML.")
            
            # Add the HTML content
            msg.add_alternative(html_content, subtype='html')

            # IMAGE OPTIMIZATION: Attach image as a 'related' part
            # This is the industry standard for Gmail/Yahoo/Outlook compatibility
            if os.path.exists(self.logo_path):
                with open(self.logo_path, 'rb') as img:
                    # We add the image to the 'html' alternative part specifically
                    msg.get_payload()[1].add_related(
                        img.read(), 
                        maintype='image', 
                        subtype='png', 
                        cid=logo_cid
                    )

            # SMTP Execution
            with smtplib.SMTP(self.config['server'], self.config['port']) as server:
                server.starttls()
                server.login(self.config['user'], self.config['pass'])
                server.send_message(msg)
            
            logging.info(f"Email inviata con successo a: {recipient}") 
            return True

        except Exception as e:
            logging.error(f"Errore invio a {recipient}: {str(e)}") 
            return False