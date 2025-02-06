import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from app.utils.llm_email_drafting import generate_email_body
from app.repositories.user_repository import get_user_email

# Replace with your OAuth2 credentials
CLIENT_ID = "360908048490-1a4v99b2vp422d8fkv0mdajdgf710k7l.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "1//04aEQGLbgvMFMCgYIARAAGAQSNwF-L9IrSuJTDoa_TYfTJStmjBycuMFRa-ZtaiC-Zh7rpam8WIqa_s58zxwxX66_VraNQP-bjrY"

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return build("gmail", "v1", credentials=creds)

def send_complaint_email(complaint, seller_email):
    """Send email using Gmail API"""
    email_body = generate_email_body(complaint)  # LLM-generated email content
    message = MIMEText(email_body)
    message["to"] = f"{seller_email}"
    message["subject"] = "Urgent: Buyer Complaint Regarding Product Issue"
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service = get_gmail_service()
    send_message = {"raw": raw}
    
    try:
        service.users().messages().send(userId="pavanshah280@gmail.com", body=send_message).execute()

        print(" Email sent successfully!")
    except Exception as e:
        print(f" Error sending email: {e}")
