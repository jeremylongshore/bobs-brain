#!/usr/bin/env python3
"""
Find which email address works with domain delegation
"""

import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Email addresses to test - .io domain!
TEST_EMAILS = [
    "reports@diagnosticpro.io",
    "jeremy@diagnosticpro.io",
    "admin@diagnosticpro.io",
    "info@diagnosticpro.io",
    "noreply@diagnosticpro.io",
    "support@diagnosticpro.io",
    "hello@diagnosticpro.io",
]


def test_email(email):
    """Test if we can impersonate this email"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            subject=email,
        )

        service = build("gmail", "v1", credentials=credentials)

        # Try to get profile
        profile = service.users().getProfile(userId="me").execute()
        print(f"✅ SUCCESS: Can access {profile.get('emailAddress')}")
        print(f"   Messages: {profile.get('messagesTotal')}")
        return True

    except Exception as e:
        error_msg = str(e)
        if "Invalid email or User ID" in error_msg:
            print(f"❌ {email} - User doesn't exist")
        elif "invalid_grant" in error_msg:
            print(f"❌ {email} - No delegation permission")
        else:
            print(f"❌ {email} - {error_msg[:50]}")
        return False


def main():
    print("🔍 Testing which email addresses work with delegation")
    print("=" * 60)

    working_emails = []

    for email in TEST_EMAILS:
        if test_email(email):
            working_emails.append(email)

    print("\n" + "=" * 60)
    if working_emails:
        print(f"✅ Working emails: {', '.join(working_emails)}")
        print(f"\nUse this in your code:")
        print(f"DELEGATED_EMAIL = '{working_emails[0]}'")
    else:
        print("❌ No working emails found")
        print("\nThis means either:")
        print("1. The service account doesn't have domain-wide delegation")
        print("2. The email addresses don't exist in the workspace")
        print("3. The delegation wasn't configured for these emails")

        print("\nService Account Client ID for Google Workspace Admin:")
        print("103907537711085136705")


if __name__ == "__main__":
    main()
