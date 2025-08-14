#!/usr/bin/env python3
"""
Verify startaitools.com domain for Cloud Run
"""

import subprocess
import time

def verify_domain():
    print("🔍 Attempting to verify startaitools.com...")
    
    # Try to create mapping which will trigger verification need
    result = subprocess.run([
        "gcloud", "beta", "run", "domain-mappings", "create",
        "--service", "startai-portfolio",
        "--domain", "www.startaitools.com",
        "--region", "us-central1",
        "--project", "bobs-house-ai"
    ], capture_output=True, text=True)
    
    print("Output:", result.stdout)
    print("Error:", result.stderr)
    
    if "verified" in result.stderr.lower():
        print("\n⚠️  Domain needs verification")
        print("\n📝 Please add this TXT record to your DNS:")
        print("Type: TXT")
        print("Host: @ (or root)")
        print("Value: google-site-verification=<code from Search Console>")
        print("\nThen visit: https://search.google.com/search-console/")
    
    return result

if __name__ == "__main__":
    verify_domain()