#!/usr/bin/env python3
"""
Alternative: Use SendGrid API for reliable email delivery
SendGrid handles DNS/reputation issues
"""

import json
import os
from datetime import datetime

import requests


def send_via_sendgrid(api_key, from_email, to_email, subject, body):
    """Send email using SendGrid API"""

    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email, "name": "Diagnostic Pro"},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 202:
        print(f"✅ Email sent via SendGrid to {to_email}")
        return True
    else:
        print(f"❌ SendGrid error: {response.status_code} - {response.text}")
        return False


def setup_sendgrid():
    """Setup instructions for SendGrid"""
    print("=" * 60)
    print("SENDGRID SETUP (IMMEDIATE SOLUTION)")
    print("=" * 60)
    print()
    print("SendGrid will deliver emails reliably without DNS setup:")
    print()
    print("1. Sign up for free at: https://sendgrid.com")
    print("   (100 emails/day free)")
    print()
    print("2. Get your API key from:")
    print("   Settings > API Keys > Create API Key")
    print()
    print("3. Verify your sender email")
    print()
    print("4. Use this script with your API key")
    print()
    print("Benefits:")
    print("✅ Works immediately")
    print("✅ No DNS configuration needed")
    print("✅ Better deliverability")
    print("✅ Email tracking and analytics")


if __name__ == "__main__":
    setup_sendgrid()

    # Example usage (need API key)
    # api_key = "YOUR_SENDGRID_API_KEY"
    # send_via_sendgrid(
    #     api_key,
    #     "reports@diagnosticpro.io",
    #     "jeremylongshore@gmail.com",
    #     "Test from SendGrid",
    #     "This should arrive!"
    # )
