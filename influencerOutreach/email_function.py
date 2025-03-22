import os
import requests
import logging
from typing import Optional
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import utility functions
from influencerOutreach.utils import setup_logging, convert_to_serializable


# Initialize logger
log_file_path = setup_logging()
logger = logging.getLogger(__name__)

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
DEFAULT_RECIPIENT = "Zhang Yifan Jem <zhangjem321@gmail.com>"
DEFAULT_SUBJECT = "Message from LeadFetch Influencer Agent"
DEFAULT_FROM_EMAIL = "Mailgun Sandbox <postmaster@sandbox405609ba02c346768e9e41e94625d494.mailgun.org>"
MAILGUN_DOMAIN = "sandbox405609ba02c346768e9e41e94625d494.mailgun.org"

def send_simple_message(message: str, recipient: Optional[str] = None, subject: Optional[str] = None, from_email: Optional[str] = None):
    """
    Send an email message using Mailgun API.
    
    Args:
        message: The email message body
        recipient: The recipient email address (optional)
        subject: The email subject (optional)
        from_email: The sender email address (optional)
    
    Returns:
        Response object from the API request
    """
    if (MAILGUN_API_KEY == ''):
        logger.error("MAILGUN_API_KEY is not set")
        return None
        
    # Use provided values or defaults
    to_email = DEFAULT_RECIPIENT
    email_subject = subject or DEFAULT_SUBJECT
    sender = from_email or DEFAULT_FROM_EMAIL
    
    data = {
        "from": sender,
        "to": to_email,
        "subject": email_subject,
        "text": message
    }
    
    logger.info(f"Sending email with following payload: {data}")
    
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data=data
        )
        logger.info(f"Email sent with response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return None

# Example code for testing - uncomment to run
# if __name__ == "__main__":
#     send_simple_message(
#         message="Hi, here's your contract for the campaign!",
#         subject="Test Email from LeadFetch",
#         recipient="test@example.com"
#     )