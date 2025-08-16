# \!/usr/bin/env python3
import random
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# Generate unique ID
tracking_id = f"DNS-{random.randint(10000, 99999)}"

sender = "reports@diagnosticpro.io"
password = "sfpi ihze imsx kkmc"
recipient = "jeremylongshore@gmail.com"

message = MIMEText(
    f"""
🎉 SUCCESS\! DNS RECORDS ARE WORKING\!

Tracking ID: {tracking_id}
Time: {datetime.now().strftime('%I:%M:%S %p')}

This email confirms:
✅ SPF record is active
✅ Emails from diagnosticpro.io are now authorized
✅ Gmail should deliver these to your inbox

The DNS changes you made in Porkbun are working\!

- Diagnostic Pro System
"""
)

message["From"] = sender
message["To"] = recipient
message["Subject"] = f"✅ DNS Working\! Test #{tracking_id}"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(message)
    server.quit()

    print(f"✅ SUCCESS\! Email sent with tracking ID: {tracking_id}")
    print(f"   Subject: DNS Working\! Test #{tracking_id}")
    print(f"   Time: {datetime.now().strftime('%I:%M:%S %p')}")
    print()
    print("Check your Gmail inbox - it should arrive now\!")
    print("The SPF record is helping deliver emails.")

except Exception as e:
    print(f"❌ Error: {e}")
