#!/usr/bin/env python3
"""
Comprehensive email delivery diagnostic for diagnosticpro.io
"""

import json
import smtplib
import socket
import subprocess
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import dns.resolver


def check_dns_records(domain):
    """Check DNS records for email configuration"""
    print("\n" + "=" * 60)
    print(f"DNS RECORDS FOR {domain}")
    print("=" * 60)

    results = {"mx": None, "spf": None, "dkim": None, "dmarc": None}

    # Check MX records
    try:
        mx_records = dns.resolver.resolve(domain, "MX")
        mx_list = []
        for mx in mx_records:
            mx_list.append(f"{mx.preference} {mx.exchange}")
        results["mx"] = mx_list
        print(f"✅ MX Records: {', '.join(mx_list)}")
    except:
        print(f"❌ NO MX RECORDS - Cannot receive emails at @{domain}")
        results["mx"] = []

    # Check SPF record
    try:
        txt_records = dns.resolver.resolve(domain, "TXT")
        for txt in txt_records:
            txt_str = str(txt).strip('"')
            if "v=spf1" in txt_str:
                results["spf"] = txt_str
                print(f"✅ SPF Record: {txt_str}")
                break
        if not results["spf"]:
            print(f"❌ NO SPF RECORD - Emails may be marked as spam")
    except:
        print(f"❌ NO SPF RECORD - Emails will likely be rejected")

    # Check DMARC record
    try:
        dmarc_records = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        for txt in dmarc_records:
            txt_str = str(txt).strip('"')
            if "v=DMARC1" in txt_str:
                results["dmarc"] = txt_str
                print(f"✅ DMARC Record: {txt_str}")
                break
        if not results["dmarc"]:
            print(f"⚠️  No DMARC record found")
    except:
        print(f"⚠️  No DMARC record (optional but recommended)")

    return results


def test_smtp_connection(server, port, username, password):
    """Test SMTP connection and authentication"""
    print("\n" + "=" * 60)
    print("SMTP CONNECTION TEST")
    print("=" * 60)

    try:
        print(f"Connecting to {server}:{port}...")
        smtp = smtplib.SMTP(server, port)
        smtp.set_debuglevel(0)

        print("Starting TLS...")
        smtp.starttls()

        print(f"Authenticating as {username}...")
        smtp.login(username, password)

        print("✅ SMTP connection successful")
        smtp.quit()
        return True
    except Exception as e:
        print(f"❌ SMTP error: {e}")
        return False


def send_test_with_headers(recipient, sender, password):
    """Send test email with proper headers"""
    print("\n" + "=" * 60)
    print("SENDING TEST EMAIL WITH HEADERS")
    print("=" * 60)

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = f"Diagnostic Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    message["Reply-To"] = sender
    message["Return-Path"] = sender
    message["Message-ID"] = f"<{datetime.now().timestamp()}@diagnosticpro.io>"
    message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    body = f"""
    This is a test email from Diagnostic Pro.

    Sent at: {datetime.now()}
    From: {sender}
    To: {recipient}

    If you receive this, the email system is working.

    - Diagnostic Pro System
    """

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)

        # Get envelope info
        refused = server.send_message(message)

        server.quit()

        if refused:
            print(f"⚠️  Some recipients refused: {refused}")
        else:
            print(f"✅ Email accepted by Gmail SMTP")
            print(f"   Message-ID: {message['Message-ID']}")

        return True
    except Exception as e:
        print(f"❌ Failed to send: {e}")
        return False


def check_gmail_api_alternative():
    """Check if Gmail API would work better"""
    print("\n" + "=" * 60)
    print("GMAIL API ALTERNATIVE")
    print("=" * 60)

    print("Gmail API might work better because:")
    print("1. It bypasses SMTP delivery issues")
    print("2. It uses OAuth2 authentication")
    print("3. It's native to Google Workspace")
    print()
    print("To use Gmail API:")
    print("1. Enable Gmail API in GCP Console")
    print("2. Create OAuth2 credentials")
    print("3. Use the gmail_oauth_setup.py script")


def suggest_fixes(dns_results):
    """Suggest fixes based on DNS results"""
    print("\n" + "=" * 60)
    print("RECOMMENDED FIXES")
    print("=" * 60)

    fixes_needed = []

    if not dns_results["mx"]:
        fixes_needed.append("ADD MX RECORDS")
        print("\n1. ADD MX RECORDS (CRITICAL):")
        print("   Go to your DNS provider (Porkbun/Cloudflare)")
        print("   Add these MX records for diagnosticpro.io:")
        print("   - 1 aspmx.l.google.com")
        print("   - 5 alt1.aspmx.l.google.com")
        print("   - 5 alt2.aspmx.l.google.com")
        print("   - 10 alt3.aspmx.l.google.com")
        print("   - 10 alt4.aspmx.l.google.com")

    if not dns_results["spf"]:
        fixes_needed.append("ADD SPF RECORD")
        print("\n2. ADD SPF RECORD (CRITICAL):")
        print("   Add this TXT record to diagnosticpro.io:")
        print("   v=spf1 include:_spf.google.com ~all")

    if not dns_results["dmarc"]:
        fixes_needed.append("ADD DMARC RECORD")
        print("\n3. ADD DMARC RECORD (Recommended):")
        print("   Add this TXT record to _dmarc.diagnosticpro.io:")
        print("   v=DMARC1; p=none; rua=mailto:reports@diagnosticpro.io")

    print("\n4. CONSIDER DKIM (Optional but helpful):")
    print("   In Google Workspace Admin:")
    print("   - Go to Apps > Google Workspace > Gmail")
    print("   - Click 'Authenticate email'")
    print("   - Generate DKIM key")
    print("   - Add the provided TXT record to your DNS")

    return fixes_needed


def test_alternative_recipients():
    """Test sending to different email providers"""
    print("\n" + "=" * 60)
    print("TESTING ALTERNATIVE RECIPIENTS")
    print("=" * 60)

    print("Since jeremylongshore@gmail.com isn't receiving emails,")
    print("try sending to:")
    print("1. A different Gmail address")
    print("2. An Outlook/Hotmail address")
    print("3. A Yahoo address")
    print("4. A corporate email address")
    print()
    print("This will help identify if it's a recipient-specific issue")


def main():
    print("=" * 60)
    print("EMAIL DELIVERY DIAGNOSTIC FOR DIAGNOSTICPRO.IO")
    print("=" * 60)

    domain = "diagnosticpro.io"
    sender = "reports@diagnosticpro.io"
    password = "sfpi ihze imsx kkmc"
    recipient = "jeremylongshore@gmail.com"

    # Step 1: Check DNS
    dns_results = check_dns_records(domain)

    # Step 2: Test SMTP
    smtp_ok = test_smtp_connection("smtp.gmail.com", 587, sender, password)

    # Step 3: Send test email
    if smtp_ok:
        send_test_with_headers(recipient, sender, password)

    # Step 4: Suggest fixes
    fixes = suggest_fixes(dns_results)

    # Step 5: Alternative approaches
    check_gmail_api_alternative()
    test_alternative_recipients()

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)

    if fixes:
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        for fix in fixes:
            print(f"   - {fix}")
        print("\nEmails are being sent but likely rejected due to missing DNS records.")
        print("Gmail accepts them initially but then filters them as suspicious.")
    else:
        print("\n✅ DNS configuration looks good")
        print("If emails still aren't arriving, check:")
        print("1. Recipient's spam filters")
        print("2. Google Workspace email routing rules")
        print("3. Try sending to a different email address")


if __name__ == "__main__":
    # Install required module if needed
    try:
        import dns.resolver
    except ImportError:
        print("Installing dnspython...")
        import subprocess

        subprocess.run(["pip", "install", "dnspython"], capture_output=True)
        import dns.resolver

    main()
