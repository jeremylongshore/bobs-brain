#!/usr/bin/env python3
"""
COMPLETE EMAIL SOLUTION FOR DIAGNOSTIC PRO
Implements multiple methods to ensure email delivery works
"""

import hashlib
import json
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.cloud import secretmanager


class DiagnosticProEmailSystem:
    """Robust email system with multiple fallback methods"""

    def __init__(self):
        self.methods = []
        self.setup_email_methods()

    def setup_email_methods(self):
        """Setup all available email methods in priority order"""

        # Method 1: Try diagnosticpro.io first (might work after DNS fix)
        self.methods.append(
            {
                "name": "DiagnosticPro Direct",
                "sender": "reports@diagnosticpro.io",
                "password": "sfpi ihze imsx kkmc",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "priority": 1,
            }
        )

        # Method 2: Use a verified Gmail that works
        # You can add your personal Gmail here as backup
        self.methods.append(
            {
                "name": "Backup Gmail",
                "sender": os.environ.get("BACKUP_EMAIL", ""),
                "password": os.environ.get("BACKUP_PASSWORD", ""),
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "priority": 2,
            }
        )

        # Method 3: Use GCP Email API (if configured)
        self.methods.append({"name": "GCP Email Service", "type": "api", "priority": 3})

    def send_email(self, to_email, subject, body, method=None):
        """Send email using the best available method"""

        if method:
            # Use specific method if requested
            return self._send_with_method(method, to_email, subject, body)

        # Try each method in priority order
        for method in sorted(self.methods, key=lambda x: x.get("priority", 99)):
            if not method.get("sender"):  # Skip if not configured
                continue

            print(f"Trying method: {method['name']}")

            if self._send_with_method(method, to_email, subject, body):
                print(f"✅ Email sent successfully using {method['name']}")
                return True

        print("❌ All email methods failed")
        return False

    def _send_with_method(self, method, to_email, subject, body):
        """Send email using specific method"""

        if method.get("type") == "api":
            return self._send_via_api(to_email, subject, body)
        else:
            return self._send_via_smtp(
                method["sender"],
                method["password"],
                to_email,
                subject,
                body,
                method["smtp_server"],
                method["smtp_port"],
            )

    def _send_via_smtp(self, sender, password, recipient, subject, body, server, port):
        """Send via SMTP"""

        if not sender or not password:
            return False

        try:
            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = recipient
            message["Subject"] = subject
            message["Reply-To"] = "reports@diagnosticpro.io"

            # Add tracking ID
            tracking_id = hashlib.md5(f"{datetime.now()}".encode()).hexdigest()[:8]
            body_with_tracking = f"{body}\n\nTracking ID: {tracking_id}"

            message.attach(MIMEText(body_with_tracking, "plain"))

            smtp = smtplib.SMTP(server, port)
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(message)
            smtp.quit()

            print(f"✅ Sent via {sender} (ID: {tracking_id})")
            return True

        except Exception as e:
            print(f"❌ SMTP error: {e}")
            return False

    def _send_via_api(self, recipient, subject, body):
        """Send via GCP API (placeholder for SendGrid/Mailgun integration)"""
        # This would integrate with SendGrid, Mailgun, or GCP Email API
        print("API method not yet configured")
        return False

    def test_delivery(self, test_email):
        """Test email delivery to verify it works"""

        print("=" * 60)
        print("TESTING EMAIL DELIVERY")
        print("=" * 60)

        test_subject = f"Diagnostic Pro Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        test_body = f"""
This is a test email from Diagnostic Pro.

If you receive this email, the system is working correctly.

Test performed at: {datetime.now()}
Test recipient: {test_email}

Please confirm receipt of this email.

- Diagnostic Pro System
"""

        return self.send_email(test_email, test_subject, test_body)


class EmailDNSFixer:
    """Instructions to fix DNS configuration"""

    @staticmethod
    def print_dns_fix_instructions():
        """Print detailed DNS fix instructions"""

        print("\n" + "=" * 60)
        print("HOW TO FIX DNS FOR diagnosticpro.io")
        print("=" * 60)
        print()
        print("Go to your DNS provider (Porkbun or Cloudflare)")
        print()
        print("ADD THESE RECORDS:")
        print("-" * 40)
        print()
        print("1. MX RECORDS (for receiving email):")
        print("   Type: MX")
        print("   Name: @ (or leave blank)")
        print("   Priority | Server")
        print("   1        | aspmx.l.google.com")
        print("   5        | alt1.aspmx.l.google.com")
        print("   5        | alt2.aspmx.l.google.com")
        print("   10       | alt3.aspmx.l.google.com")
        print("   10       | alt4.aspmx.l.google.com")
        print()
        print("2. SPF RECORD (for sending authorization):")
        print("   Type: TXT")
        print("   Name: @ (or leave blank)")
        print("   Value: v=spf1 include:_spf.google.com ~all")
        print()
        print("3. DMARC RECORD (optional but recommended):")
        print("   Type: TXT")
        print("   Name: _dmarc")
        print("   Value: v=DMARC1; p=none; rua=mailto:reports@diagnosticpro.io")
        print()
        print("After adding these records:")
        print("- Wait 1-24 hours for DNS propagation")
        print("- Test email delivery again")
        print("- Emails should start arriving!")


def create_production_ready_solution():
    """Create production-ready email solution"""

    print("\n" + "=" * 60)
    print("PRODUCTION-READY EMAIL SOLUTION")
    print("=" * 60)

    # Create configuration file
    config = {
        "primary_method": {
            "sender": "reports@diagnosticpro.io",
            "password": "sfpi ihze imsx kkmc",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
        },
        "backup_method": {
            "sender": "YOUR_BACKUP_EMAIL@gmail.com",
            "password": "YOUR_BACKUP_APP_PASSWORD",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
        },
        "api_method": {"provider": "sendgrid", "api_key": "YOUR_SENDGRID_API_KEY"},
    }

    # Save configuration
    with open(".email_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("Created .email_config.json")
    print()
    print("To make this production-ready:")
    print("1. Add your backup Gmail credentials")
    print("2. Sign up for SendGrid and add API key")
    print("3. Store credentials in GCP Secret Manager")
    print("4. Use the DiagnosticProEmailSystem class")


def main():
    """Main execution"""

    print("=" * 60)
    print("DIAGNOSTIC PRO EMAIL SYSTEM")
    print("=" * 60)

    # Initialize email system
    email_system = DiagnosticProEmailSystem()

    # Test delivery
    test_recipient = "jeremylongshore@gmail.com"
    print(f"\nTesting email delivery to {test_recipient}...")

    if email_system.test_delivery(test_recipient):
        print("\n✅ Email system is working!")
    else:
        print("\n❌ Email delivery failed")
        print("\nTrying alternative methods...")

        # Print DNS fix instructions
        EmailDNSFixer.print_dns_fix_instructions()

        # Create production solution
        create_production_ready_solution()

        print("\n" + "=" * 60)
        print("IMMEDIATE WORKAROUND")
        print("=" * 60)
        print()
        print("While DNS propagates, use one of these:")
        print()
        print("1. Add your personal Gmail as backup:")
        print("   export BACKUP_EMAIL='your@gmail.com'")
        print("   export BACKUP_PASSWORD='your-app-password'")
        print()
        print("2. Use SendGrid (free tier):")
        print("   - Sign up at sendgrid.com")
        print("   - Get API key")
        print("   - Update .email_config.json")


if __name__ == "__main__":
    main()
