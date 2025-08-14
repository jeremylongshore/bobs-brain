#!/usr/bin/env python3
"""
Gmail SMTP Setup with App Password
Simpler approach using SMTP
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass


def send_email_smtp(sender_email, app_password, to_email, subject, body):
    """Send email using Gmail SMTP with app password"""

    # Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    port = 587  # For TLS

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    try:
        # Create SMTP session
        print(f"Connecting to {smtp_server}:{port}...")
        server = smtplib.SMTP(smtp_server, port)

        # Enable security
        server.starttls()

        # Login
        print(f"Logging in as {sender_email}...")
        server.login(sender_email, app_password)

        # Send email
        text = message.as_string()
        server.sendmail(sender_email, to_email, text)

        # Terminate session
        server.quit()

        print(f"✅ Email sent successfully to {to_email}!")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed!")
        print("   Make sure you're using an App Password, not your regular password")
        print("   Generate one at: https://myaccount.google.com/apppasswords")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def save_app_password(email, password):
    """Save app password securely (in production, use proper secret management)"""
    env_file = ".env.gmail"
    with open(env_file, "w") as f:
        f.write(f"GMAIL_ADDRESS={email}\n")
        f.write(f"GMAIL_APP_PASSWORD={password}\n")
    os.chmod(env_file, 0o600)  # Restrict permissions
    print(f"✅ Credentials saved to {env_file}")


def load_app_password():
    """Load saved credentials"""
    env_file = ".env.gmail"
    if os.path.exists(env_file):
        creds = {}
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    creds[key] = value
        return creds.get("GMAIL_ADDRESS"), creds.get("GMAIL_APP_PASSWORD")
    return None, None


def main():
    print("=" * 60)
    print("GMAIL SMTP SETUP WITH APP PASSWORD")
    print("=" * 60)
    print()
    print("To use Gmail SMTP, you need an App Password:")
    print("1. Enable 2-factor authentication on your Google account")
    print("2. Go to: https://myaccount.google.com/apppasswords")
    print("3. Select 'Mail' and generate a password")
    print("4. Use that 16-character password here (not your regular password)")
    print()

    # Try to load saved credentials
    saved_email, saved_password = load_app_password()

    if saved_email and saved_password:
        print(f"Found saved credentials for {saved_email}")
        use_saved = input("Use saved credentials? (y/n): ").lower() == "y"
        if use_saved:
            sender_email = saved_email
            app_password = saved_password
        else:
            sender_email = input("Enter your Gmail address: ")
            app_password = getpass("Enter your App Password: ")
    else:
        sender_email = input("Enter your Gmail address: ")
        app_password = getpass("Enter your App Password (16 characters): ")

    # Test sending email
    print("\nSending test email...")
    success = send_email_smtp(
        sender_email,
        app_password,
        "jeremylongshore@gmail.com",
        "✅ Bob's Brain SMTP Working!",
        """
        This email was sent using Gmail SMTP with an App Password.

        Bob's Brain can now send emails through Gmail!

        Configuration:
        - SMTP Server: smtp.gmail.com
        - Port: 587 (TLS)
        - Authentication: App Password

        - Bob's Brain System
        """,
    )

    if success:
        print("\n🎉 Success! SMTP authentication is working.")

        # Offer to save credentials
        if not (saved_email and saved_password):
            save = input("\nSave credentials for future use? (y/n): ").lower() == "y"
            if save:
                save_app_password(sender_email, app_password)


if __name__ == "__main__":
    main()
