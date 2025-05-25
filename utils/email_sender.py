import os
import smtplib
import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
import json

load_dotenv()

logger = logging.getLogger(__name__)

class EmailSender:
    """Send results via email"""
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_email = os.getenv("SMTP_EMAIL")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.recipient = os.getenv("RECIPIENT_EMAIL", "bilalrahib8work@gmail.com")
    
    async def send_results(self, email_data: Dict[str, Any], attachments: List[Dict[str, Any]]):
        """Send results email with attachments"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_email
            msg['To'] = self.recipient
            msg['Subject'] = f"Agentic Loop Content Generation - Task {email_data['task_id']}"
            
            # Create email body
            body = self._create_email_body(email_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Add attachments
            for attachment in attachments:
                self._add_attachment(msg, attachment)
            
            # Send email
            await self._send_email(msg)
            
            logger.info(f"Results email sent successfully to {self.recipient}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
    
    def _create_email_body(self, email_data: Dict[str, Any]) -> str:
        """Create HTML email body"""
        status_color = "green" if email_data["status"] == "completed" else "red"
        
        errors_section = ""
        if email_data.get("errors"):
            errors_list = "".join([
                f"<li><strong>{error['phase']}</strong>: {error['error']}</li>"
                for error in email_data["errors"]
            ])
            errors_section = f"""
            <h3>Errors Encountered:</h3>
            <ul style="color: red;">
                {errors_list}
            </ul>
            """
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .header {{ background-color: #f4f4f4; padding: 20px; border-radius: 5px; }}
                .status {{ color: {status_color}; font-weight: bold; }}
                .section {{ margin: 20px 0; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Agentic Loop Content Generation Report</h2>
                <p><strong>Task ID:</strong> {email_data['task_id']}</p>
                <p><strong>Status:</strong> <span class="status">{email_data['status'].upper()}</span></p>
                <p><strong>Start Time:</strong> {email_data.get('start_time', 'N/A')}</p>
                <p><strong>End Time:</strong> {email_data.get('end_time', 'N/A')}</p>
            </div>
            
            <div class="section">
                <h3>Generated Content:</h3>
                <p>Please find the generated content in the attached JSON files:</p>
                <ul>
                    <li>Blog Posts (3 articles)</li>
                    <li>Twitter Content (12 tweets)</li>
                    <li>LinkedIn Posts (6 posts)</li>
                </ul>
            </div>
            
            {errors_section}
            
            <div class="footer">
                <p><em>This is an automated email from Agentic Loop Content Automation System.</em></p>
                <p><em>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            </div>
        </body>
        </html>
        """
        
        return body
    
    def _add_attachment(self, msg: MIMEMultipart, attachment: Dict[str, Any]):
        """Add attachment to email"""
        try:
            part = MIMEApplication(
                attachment['content'].encode('utf-8'),
                Name=attachment['filename']
            )
            part['Content-Disposition'] = f'attachment; filename="{attachment["filename"]}"'
            msg.attach(part)
        except Exception as e:
            logger.error(f"Failed to add attachment {attachment['filename']}: {str(e)}")
    
    async def _send_email(self, msg: MIMEMultipart):
        """Send email via SMTP"""
        if not self.smtp_email or not self.smtp_password:
            logger.warning("Email credentials not configured. Skipping email send.")
            return
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_email, self.smtp_password)
            
            await asyncio.to_thread(
                server.send_message,
                msg
            )
            
            server.quit()
        except Exception as e:
            logger.error(f"SMTP error: {str(e)}")
            raise
