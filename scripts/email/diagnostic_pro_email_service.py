#!/usr/bin/env python3
"""
Production-ready email service for Diagnostic Pro
Uses service account with domain-wide delegation
"""

import base64
import json
import os
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build


class DiagnosticProEmailService:
    """Production email service using Google Workspace service account"""

    def __init__(self, service_account_file: str = "/tmp/diagnostic-email-key.json"):
        """Initialize email service with service account"""

        self.service_account_file = service_account_file
        self.sender_email = "reports@diagnosticpro.io"
        self.scopes = ["https://www.googleapis.com/auth/gmail.send"]
        self.service = self._build_service()

    def _build_service(self):
        """Build Gmail service with domain-wide delegation"""

        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes, subject=self.sender_email
        )

        return build("gmail", "v1", credentials=credentials)

    def send_diagnostic_report(
        self, recipient: str, vehicle: Dict, issues: List[Dict], recommendations: List[str]
    ) -> bool:
        """Send a professional diagnostic report"""

        subject = f"Diagnostic Report - {vehicle.get('year')} {vehicle.get('make')} {vehicle.get('model')}"

        # Create HTML version
        html_body = self._create_html_report(vehicle, issues, recommendations)

        # Create text version
        text_body = self._create_text_report(vehicle, issues, recommendations)

        return self._send_email(recipient=recipient, subject=subject, text_body=text_body, html_body=html_body)

    def send_confirmation(self, recipient: str, submission_id: str) -> bool:
        """Send submission confirmation email"""

        subject = "Diagnostic Submission Received"

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2>Thank you for your submission!</h2>
              <p>We've received your diagnostic request and are processing it now.</p>

              <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Submission ID:</strong> {submission_id}</p>
                <p><strong>Status:</strong> Processing</p>
                <p><strong>Submitted:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
              </div>

              <p>You'll receive a detailed diagnostic report shortly.</p>

              <hr style="margin: 30px 0;">
              <p style="color: #6c757d; font-size: 12px;">
                Diagnostic Pro | support@diagnosticpro.io
              </p>
            </div>
          </body>
        </html>
        """

        text_body = f"""
        Thank you for your submission!

        We've received your diagnostic request and are processing it now.

        Submission ID: {submission_id}
        Status: Processing
        Submitted: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

        You'll receive a detailed diagnostic report shortly.

        - Diagnostic Pro Team
        """

        return self._send_email(recipient=recipient, subject=subject, text_body=text_body, html_body=html_body)

    def send_alert(self, recipient: str, alert_type: str, message: str, severity: str = "info") -> bool:
        """Send system alert email"""

        # Set colors based on severity
        colors = {"critical": "#dc3545", "warning": "#ffc107", "info": "#17a2b8", "success": "#28a745"}

        color = colors.get(severity, "#17a2b8")

        subject = f"[{alert_type.upper()}] Diagnostic Pro Alert"

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <div style="border-left: 4px solid {color}; padding-left: 15px;">
                <h2 style="color: {color};">System Alert: {alert_type}</h2>
              </div>

              <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Severity:</strong> {severity.upper()}</p>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
              </div>

              <div style="margin: 20px 0;">
                <p>{message}</p>
              </div>

              <hr style="margin: 30px 0;">
              <p style="color: #6c757d; font-size: 12px;">
                This is an automated alert from Diagnostic Pro System
              </p>
            </div>
          </body>
        </html>
        """

        text_body = f"""
        SYSTEM ALERT: {alert_type}
        Severity: {severity.upper()}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        {message}

        - Diagnostic Pro System
        """

        return self._send_email(recipient=recipient, subject=subject, text_body=text_body, html_body=html_body)

    def _create_html_report(self, vehicle: Dict, issues: List[Dict], recommendations: List[str]) -> str:
        """Create HTML version of diagnostic report"""

        issues_html = "".join(
            [f"<li><strong>{issue.get('code')}:</strong> {issue.get('description')}</li>" for issue in issues]
        )

        recommendations_html = "".join([f"<li>{rec}</li>" for rec in recommendations])

        return f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h1 style="color: #2c3e50;">🔧 Diagnostic Report</h1>

              <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Vehicle Information</h3>
                <table style="width: 100%;">
                  <tr><td><strong>Year:</strong></td><td>{vehicle.get('year', 'N/A')}</td></tr>
                  <tr><td><strong>Make:</strong></td><td>{vehicle.get('make', 'N/A')}</td></tr>
                  <tr><td><strong>Model:</strong></td><td>{vehicle.get('model', 'N/A')}</td></tr>
                  <tr><td><strong>VIN:</strong></td><td>{vehicle.get('vin', 'N/A')}</td></tr>
                  <tr><td><strong>Mileage:</strong></td><td>{vehicle.get('mileage', 'N/A')}</td></tr>
                </table>
              </div>

              <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>⚠️ Issues Detected</h3>
                <ul>{issues_html}</ul>
              </div>

              <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>✅ Recommendations</h3>
                <ol>{recommendations_html}</ol>
              </div>

              <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                <p style="color: #6c757d; font-size: 12px;">
                  Report generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br>
                  Diagnostic Pro | support@diagnosticpro.io
                </p>
              </div>
            </div>
          </body>
        </html>
        """

    def _create_text_report(self, vehicle: Dict, issues: List[Dict], recommendations: List[str]) -> str:
        """Create plain text version of diagnostic report"""

        issues_text = "\n".join([f"- {issue.get('code')}: {issue.get('description')}" for issue in issues])

        recommendations_text = "\n".join([f"{i+1}. {rec}" for i, rec in enumerate(recommendations)])

        return f"""
DIAGNOSTIC REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

VEHICLE INFORMATION:
- Year: {vehicle.get('year', 'N/A')}
- Make: {vehicle.get('make', 'N/A')}
- Model: {vehicle.get('model', 'N/A')}
- VIN: {vehicle.get('vin', 'N/A')}
- Mileage: {vehicle.get('mileage', 'N/A')}

ISSUES DETECTED:
{issues_text}

RECOMMENDATIONS:
{recommendations_text}

For questions, contact support@diagnosticpro.io
"""

    def _send_email(
        self,
        recipient: str,
        subject: str,
        text_body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List] = None,
    ) -> bool:
        """Send email using Gmail API"""

        try:
            if html_body:
                message = MIMEMultipart("alternative")
                message.attach(MIMEText(text_body, "plain"))
                message.attach(MIMEText(html_body, "html"))
            else:
                message = MIMEText(text_body)

            message["to"] = recipient
            message["from"] = self.sender_email
            message["subject"] = subject
            message["Reply-To"] = "support@diagnosticpro.io"

            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    # Implementation for attachments would go here
                    pass

            # Encode and send
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            body = {"raw": raw}

            result = self.service.users().messages().send(userId="me", body=body).execute()

            print(f"✅ Email sent to {recipient} (ID: {result['id']})")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Initialize service
    email_service = DiagnosticProEmailService()

    # Test diagnostic report
    vehicle = {"year": "2019", "make": "Ford", "model": "F-150", "vin": "1FTFW1E57KFC12345", "mileage": "45,000"}

    issues = [
        {"code": "P0301", "description": "Cylinder 1 Misfire Detected"},
        {"code": "P0171", "description": "System Too Lean (Bank 1)"},
    ]

    recommendations = [
        "Check and replace spark plugs if worn",
        "Inspect ignition coils for damage",
        "Clean or replace fuel injectors",
        "Check for vacuum leaks",
        "Replace air filter if dirty",
    ]

    # Send diagnostic report
    print("Sending diagnostic report...")
    email_service.send_diagnostic_report(
        recipient="jeremylongshore@gmail.com", vehicle=vehicle, issues=issues, recommendations=recommendations
    )

    # Send confirmation
    print("\nSending confirmation...")
    email_service.send_confirmation(recipient="jeremylongshore@gmail.com", submission_id="DIAG-2024-0812-001")

    # Send alert
    print("\nSending alert...")
    email_service.send_alert(
        recipient="jeremylongshore@gmail.com",
        alert_type="System Update",
        message="The diagnostic system has been updated with new fault codes for 2024 vehicles.",
        severity="info",
    )
