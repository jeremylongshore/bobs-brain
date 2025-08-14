#!/usr/bin/env python3
"""
Direct Gmail API usage without domain-wide delegation
Using OAuth 2.0 flow for reports@diagnosticpro.io
"""

import base64
import json
import os
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def create_oauth_credentials():
    """Create OAuth 2.0 credentials for Gmail API"""

    # Create OAuth2 credentials configuration
    oauth_config = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
            "project_id": "diagnostic-pro-mvp",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "YOUR_CLIENT_SECRET",
            "redirect_uris": ["http://localhost"],
        }
    }

    print("=" * 60)
    print("OAUTH 2.0 CREDENTIAL SETUP")
    print("=" * 60)
    print("\nTo set up OAuth 2.0:")
    print("1. Go to: https://console.cloud.google.com/apis/credentials")
    print("2. Select project: diagnostic-pro-mvp")
    print("3. Click '+ CREATE CREDENTIALS' > OAuth client ID")
    print("4. Application type: Desktop app")
    print("5. Name: Bob's Brain Gmail")
    print("6. Download the JSON file")
    print("\nOr use the Gmail API Quickstart:")
    print("https://developers.google.com/gmail/api/quickstart/python")

    return oauth_config


def test_gmail_api():
    """Test Gmail API with proper OAuth"""

    print("\n" + "=" * 60)
    print("TESTING GMAIL API OPTIONS")
    print("=" * 60)

    print("\nYou have 3 options to send emails:")
    print()
    print("1. SMTP with App Password (Simplest)")
    print("   - Enable 2FA on reports@diagnosticpro.io")
    print("   - Generate App Password")
    print("   - Use gmail_smtp_setup.py")
    print()
    print("2. OAuth 2.0 Flow (Most Secure)")
    print("   - Create OAuth credentials in GCP")
    print("   - Authorize reports@diagnosticpro.io")
    print("   - Use gmail_oauth_setup.py")
    print()
    print("3. Service Account with Domain Delegation (Enterprise)")
    print("   - Already configured with Client ID: 103907537711085136705")
    print("   - Waiting for Google Workspace propagation")
    print()
    print("Which option would you like to proceed with?")
    print("I recommend starting with Option 1 (SMTP) as it's quickest.")


if __name__ == "__main__":
    test_gmail_api()

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("\nFor SMTP (Recommended for quick setup):")
    print("1. Log into reports@diagnosticpro.io")
    print("2. Enable 2-factor authentication")
    print("3. Generate App Password at: https://myaccount.google.com/apppasswords")
    print("4. Run: python3 gmail_smtp_setup.py")
    print("5. Enter the 16-character app password")
    print("\nFor OAuth 2.0:")
    print("1. Create OAuth 2.0 credentials in GCP Console")
    print("2. Download credentials.json")
    print("3. Run: python3 gmail_oauth_setup.py")
    print("4. Authorize in browser")
    print("\nFor Service Account (already configured):")
    print("- Wait for domain-wide delegation to propagate")
    print("- Run: python3 test_delegation_final.py")
