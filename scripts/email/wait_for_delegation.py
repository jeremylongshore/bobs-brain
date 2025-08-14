#!/usr/bin/env python3
"""
Wait for domain-wide delegation to become active
"""

import base64
import time
from datetime import datetime
from email.mime.text import MIMEText

from google.oauth2 import service_account
from googleapiclient.discovery import build


def test_delegation():
    """Test if delegation is working"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            "/tmp/diagnostic-email-key.json",
            scopes=["https://www.googleapis.com/auth/gmail.send"],
            subject="reports@diagnosticpro.io",
        )

        service = build("gmail", "v1", credentials=credentials)

        # Create test message
        message = MIMEText("Domain-wide delegation is now active! Bob's Brain can send emails.")
        message["to"] = "jeremylongshore@gmail.com"
        message["from"] = "reports@diagnosticpro.io"
        message["subject"] = "✅ Bob's Brain Email System Active!"

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        body = {"raw": raw}

        result = service.users().messages().send(userId="me", body=body).execute()
        return True, f"Message sent! ID: {result['id']}"

    except Exception as e:
        return False, str(e)[:100]


def main():
    print("=" * 60)
    print("WAITING FOR DOMAIN-WIDE DELEGATION TO ACTIVATE")
    print("=" * 60)
    print("Client ID: 103907537711085136705")
    print("Email: reports@diagnosticpro.io")
    print("Press Ctrl+C to stop")
    print()

    attempt = 0
    start_time = time.time()

    while True:
        attempt += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        elapsed = int(time.time() - start_time)

        print(f"[{current_time}] Attempt {attempt} (elapsed: {elapsed}s)...", end=" ")

        success, message = test_delegation()

        if success:
            print(f"✅ SUCCESS!")
            print(f"\n🎉 DELEGATION IS ACTIVE!")
            print(f"   {message}")
            print(f"   Email sent from reports@diagnosticpro.io to jeremylongshore@gmail.com")
            break
        else:
            if "unauthorized_client" in message:
                print(f"⏳ Not ready yet")
            else:
                print(f"❌ Error: {message}")

        # Wait 30 seconds before next attempt
        time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped by user")
