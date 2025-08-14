# \!/usr/bin/env python3
import random
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# Generate unique ID
unique_id = random.randint(10000, 99999)

sender = "reports@diagnosticpro.io"
password = "sfpi ihze imsx kkmc"
recipient = "jeremylongshore@gmail.com"

message = MIMEText(
    f"""
DIAGNOSTIC PRO TEST EMAIL #{unique_id}

This is test email #{unique_id} sent at {datetime.now()}

Please check:
1. Primary inbox
2. Promotions tab (if using Gmail)
3. Spam/Junk folder
4. All Mail folder

If you don't see this email, possible issues:
- Gmail may be filtering emails from new senders
- The recipient address might have a filter rule
- There might be a delay in delivery

Reply to this email or check if you received email #{unique_id}

- Diagnostic Pro System
"""
)

message["From"] = sender
message["To"] = recipient
message["Subject"] = f"Diagnostic Test #{unique_id} - {datetime.now().strftime('%I:%M %p')}"
message["Reply-To"] = sender

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)

    server.send_message(message)
    server.quit()

    print(f"✅ Email #{unique_id} sent successfully\!")
    print(f"   Subject: Diagnostic Test #{unique_id}")
    print(f"   Time: {datetime.now().strftime('%I:%M:%S %p')}")
    print()
    print("Please check:")
    print("1. Inbox")
    print("2. Promotions tab")
    print("3. Spam folder")
    print("4. All Mail")

except Exception as e:
    print(f"❌ Error: {e}")
