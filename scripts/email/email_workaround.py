#!/usr/bin/env python3
"""
Workaround: Send emails from a properly configured domain
"""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_from_personal_gmail(personal_email, app_password, to_email, subject, body):
    """Send email from a personal Gmail that's properly configured"""

    message = MIMEMultipart()
    message["From"] = f"Diagnostic Pro <{personal_email}>"
    message["To"] = to_email
    message["Subject"] = f"[Diagnostic Pro] {subject}"
    message["Reply-To"] = "reports@diagnosticpro.io"  # Still show diagnosticpro email

    # Add disclaimer
    full_body = f"""{body}

---
Note: This email is sent from {personal_email} on behalf of Diagnostic Pro
while we configure email DNS records for diagnosticpro.io.
Reply to: reports@diagnosticpro.io
"""

    message.attach(MIMEText(full_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(personal_email, app_password)

        server.send_message(message)
        server.quit()

        print(f"✅ Email sent from {personal_email} to {to_email}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_with_working_sender():
    """Test using a Gmail account that definitely works"""
    print("=" * 60)
    print("WORKAROUND: USE A WORKING GMAIL ACCOUNT")
    print("=" * 60)
    print()
    print("Since diagnosticpro.io lacks DNS records,")
    print("temporarily use a personal Gmail account:")
    print()
    print("1. Use your personal Gmail")
    print("2. Generate an app password for it")
    print("3. Send emails on behalf of Diagnostic Pro")
    print("4. Set Reply-To as reports@diagnosticpro.io")
    print()
    print("This ensures emails are delivered while")
    print("you set up the DNS records properly.")


def use_gmail_alias():
    """Use Gmail alias feature"""
    print("\n" + "=" * 60)
    print("ALTERNATIVE: GMAIL ALIAS")
    print("=" * 60)
    print()
    print("In your personal Gmail settings:")
    print("1. Go to Settings > Accounts and Import")
    print("2. Under 'Send mail as', click 'Add another email'")
    print("3. Add reports@diagnosticpro.io as an alias")
    print("4. Use your personal Gmail SMTP to send")
    print("   but it will show as from reports@diagnosticpro.io")


if __name__ == "__main__":
    test_with_working_sender()
    use_gmail_alias()

    print("\n" + "=" * 60)
    print("IMMEDIATE ACTION REQUIRED")
    print("=" * 60)
    print()
    print("To fix email delivery immediately:")
    print()
    print("OPTION 1: Fix DNS (Permanent solution)")
    print("- Add MX records in your DNS provider")
    print("- Add SPF record: v=spf1 include:_spf.google.com ~all")
    print("- Wait 1-24 hours for propagation")
    print()
    print("OPTION 2: Use SendGrid (Immediate)")
    print("- Sign up at sendgrid.com")
    print("- Get API key")
    print("- Use send_email_via_sendgrid.py")
    print()
    print("OPTION 3: Use personal Gmail (Immediate)")
    print("- Use this script with your personal Gmail")
    print("- Emails will be delivered immediately")
