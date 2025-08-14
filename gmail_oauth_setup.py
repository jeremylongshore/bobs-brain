#!/usr/bin/env python3
"""
Gmail OAuth 2.0 Setup for sending emails
This will open a browser for authentication
"""

import base64
import os
import pickle
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth scope for sending emails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def authenticate_gmail():
    """Authenticate and return Gmail service"""
    creds = None

    # Token file stores the user's access and refresh tokens
    token_file = "token.pickle"

    # Check if we have saved credentials
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create OAuth2 flow
            # You'll need to create OAuth 2.0 credentials in GCP Console first
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES  # Download this from GCP Console
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def send_email(service, to_email, subject, body):
    """Send an email using the Gmail API"""
    try:
        message = MIMEText(body)
        message["to"] = to_email
        message["subject"] = subject

        # Encode the message
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the message
        result = service.users().messages().send(userId="me", body={"raw": raw}).execute()

        print(f"✅ Email sent successfully! Message ID: {result['id']}")
        return result

    except Exception as error:
        print(f"❌ An error occurred: {error}")
        return None


def main():
    print("=" * 60)
    print("GMAIL OAUTH 2.0 SETUP")
    print("=" * 60)
    print()
    print("Prerequisites:")
    print("1. Go to GCP Console > APIs & Services > Credentials")
    print("2. Create OAuth 2.0 Client ID (Desktop application)")
    print("3. Download the credentials as 'credentials.json'")
    print("4. Place it in this directory")
    print()

    if not os.path.exists("credentials.json"):
        print("❌ credentials.json not found!")
        print("   Please download OAuth 2.0 credentials from GCP Console")
        return

    print("Authenticating with Gmail...")
    service = authenticate_gmail()

    print("\nSending test email...")
    result = send_email(
        service,
        "jeremylongshore@gmail.com",
        "✅ Bob's Brain Gmail OAuth Working!",
        """
        This email was sent using Gmail OAuth 2.0 authentication.

        Bob's Brain can now send emails through your Workspace Gmail!

        - Bob's Brain System
        """,
    )

    if result:
        print("\n🎉 Success! OAuth authentication is working.")
        print("   The token has been saved for future use.")


if __name__ == "__main__":
    main()
