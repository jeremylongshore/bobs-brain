# \!/usr/bin/env python3
"""
Check if email exists by trying different approaches
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build

print("Checking if reports@diagnosticpro.io exists...")
print("-" * 60)

# Try with different service account (Bob's Brain)
SERVICE_ACCOUNT_FILE = "/tmp/bob-service-key.json"

try:
    # Try Directory API to list users (if we have access)
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/admin.directory.user.readonly"]
    )

    # Try with domain-wide delegation to admin
    delegated = credentials.with_subject("jeremy@diagnosticpro.io")

    service = build("admin", "directory_v1", credentials=delegated)

    results = service.users().list(domain="diagnosticpro.io", maxResults=10).execute()

    users = results.get("users", [])

    print("✅ Users in diagnosticpro.io domain:")
    for user in users:
        email = user.get("primaryEmail", "")
        print(f"   - {email}")
        if email == "reports@diagnosticpro.io":
            print("     ^^^ FOUND reports@diagnosticpro.io\!")

    if not any(u.get("primaryEmail") == "reports@diagnosticpro.io" for u in users):
        print("\n⚠️  reports@diagnosticpro.io NOT FOUND in user list")
        print("   You may need to create this user in Google Workspace")

except Exception as e:
    print(f"Cannot check users directly: {str(e)[:100]}")
    print("\nTrying alternate method...")

    # Try simpler test - just see if we can delegate to jeremy@
    try:
        creds2 = service_account.Credentials.from_service_account_file(
            "/tmp/diagnostic-email-key.json",
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
            subject="jeremy@diagnosticpro.io",
        )

        service2 = build("gmail", "v1", credentials=creds2)
        profile = service2.users().getProfile(userId="me").execute()

        print(f"✅ Can access jeremy@diagnosticpro.io")
        print(f"   This means delegation IS configured for some users")
        print(f"   But reports@diagnosticpro.io might not exist")

    except Exception as e2:
        if "unauthorized_client" in str(e2):
            print("❌ Delegation not working for ANY user yet")
            print("   The Client ID needs to be added to Google Workspace Admin")
        else:
            print(f"❌ Error: {str(e2)[:100]}")
