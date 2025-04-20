import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Union
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_emails(email_list: List[Dict[str, Union[str, List[str]]]]) -> None:
    """
    Send emails to a list of recipients using Google SMTP server.
    
    Args:
        email_list (List[Dict[str, Union[str, List[str]]]]): List of dictionaries containing email details.
            Each dictionary should have:
            - 'email': Receiver's email address (string) or list of email addresses
            - 'subject': Email subject
            - 'body': Email body content
    
    Returns:
        None
    """
    # Get email credentials from environment variables
    sender_email = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not sender_email or not password:
        raise ValueError("Gmail credentials not found in environment variables")
    
    # Create SMTP session
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable TLS encryption
        
        # Login to the server
        server.login(sender_email, password)
        
        # Send each email
        for email_data in email_list:
            # Convert single email to list for uniform handling
            recipients = email_data['email'] if isinstance(email_data['email'], list) else [email_data['email']]
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipients)  # Join multiple recipients with commas
            msg['Subject'] = email_data['subject']
            
            # Attach the body
            msg.attach(MIMEText(email_data['body'], 'plain'))
            
            # Send the email
            server.send_message(msg)
            print(f"Email sent successfully to: {', '.join(recipients)}")
        
        # Close the server connection
        server.quit()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage with both single and multiple recipients
    email_list = [
        {
            'email': ['rajs02073@gmail.com', 'ashishiitdelhi2021@gmail.com'],
            'subject': 'Test Email to Multiple Recipients',
            'body': 'This is a test email sent to multiple recipients.'
        },
        {
            'email': 'ashishsingh.iitd2021@gmail.com',
            'subject': 'Test Email to Single Recipient',
            'body': 'This is a test email sent to a single recipient.'
        }
    ]

    send_emails(email_list)
