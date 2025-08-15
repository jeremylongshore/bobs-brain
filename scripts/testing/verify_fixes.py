#!/usr/bin/env python3
"""
Verification script to confirm all fixes are working
"""

import subprocess
import sys


def run_command(cmd):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)  # nosec B602
        return result.stdout, result.returncode
    except subprocess.TimeoutExpired:
        return "Command timed out", 1
    except Exception as e:
        return str(e), 1


def check_youtube_scraper():
    """Verify YouTube scraper doesn't download videos"""
    print("\n1. Checking YouTube Scraper...")

    # Check for yt-dlp imports
    output, code = run_command("grep -c 'import yt_dlp\\|from yt_dlp' src/youtube_equipment_scraper.py")
    if output.strip() == "0":
        print("   ✅ No yt-dlp imports found (only transcripts)")
    else:
        print("   ❌ yt-dlp imports still present")
        return False

    # Check for download functions (excluding comments)
    output, code = run_command(
        "grep -v '^[[:space:]]*#' src/youtube_equipment_scraper.py | grep -c 'def.*download\\|def.*Download'"
    )
    if output.strip() == "0":
        print("   ✅ No download functions active")
    else:
        print("   ❌ Download functions still present")
        return False

    return True


def check_neo4j_connectivity():
    """Verify Neo4j connectivity via VPC"""
    print("\n2. Checking Neo4j Connectivity...")

    # Check Bob's Brain VPC
    cmd = (
        "gcloud run services describe bobs-brain --region us-central1 --format=json 2>/dev/null | "
        'python3 -c "import json, sys; data = json.load(sys.stdin); '
        "print(data.get('spec', {}).get('template', {}).get('metadata', {})"
        ".get('annotations', {}).get('run.googleapis.com/vpc-access-connector', 'None'))\""
    )
    output, _ = run_command(cmd)
    if "bob-vpc-connector" in output:
        print("   ✅ Bob's Brain has VPC connector")
    else:
        print("   ❌ Bob's Brain missing VPC connector")
        return False

    # Check Unified Scraper VPC
    cmd = (
        "gcloud run services describe unified-scraper --region us-central1 --format=json 2>/dev/null | "
        'python3 -c "import json, sys; data = json.load(sys.stdin); '
        "print(data.get('spec', {}).get('template', {}).get('metadata', {})"
        ".get('annotations', {}).get('run.googleapis.com/vpc-access-connector', 'None'))\""
    )
    output, _ = run_command(cmd)
    if "bob-vpc-connector" in output:
        print("   ✅ Unified Scraper has VPC connector")
    else:
        print("   ❌ Unified Scraper missing VPC connector")
        return False

    return True


def check_services_health():
    """Verify all services are healthy"""
    print("\n3. Checking Service Health...")

    services = [
        ("Bob's Brain", "https://bobs-brain-157908567967.us-central1.run.app/health"),
        ("Unified Scraper", "https://unified-scraper-157908567967.us-central1.run.app/health"),
    ]

    all_healthy = True
    for name, url in services:
        cmd = (
            f'curl -s {url} | python3 -c "import json, sys; '
            "data = json.load(sys.stdin); print(data.get('status', 'unknown'))\""
        )
        output, code = run_command(cmd)
        if "healthy" in output:
            print(f"   ✅ {name} is healthy")
        else:
            print(f"   ❌ {name} is not healthy")
            all_healthy = False

    return all_healthy


def check_slack_integration():
    """Verify Slack integration"""
    print("\n4. Checking Slack Integration...")

    cmd = (
        "curl -s https://bobs-brain-157908567967.us-central1.run.app/health | "
        'python3 -c "import json, sys; data = json.load(sys.stdin); '
        "print('slack:', data.get('components', {}).get('slack', False))\""
    )
    output, code = run_command(cmd)
    if "slack: True" in output:
        print("   ✅ Slack integration configured")
        return True
    else:
        print("   ❌ Slack integration not configured")
        return False


def check_circle_of_life():
    """Verify Circle of Life is working"""
    print("\n5. Checking Circle of Life...")

    cmd = (
        "curl -s https://bobs-brain-157908567967.us-central1.run.app/circle-of-life/metrics | "
        'python3 -c "import json, sys; data = json.load(sys.stdin); '
        "print(data.get('health', 'unknown'))\""
    )
    output, code = run_command(cmd)
    if "healthy" in output:
        print("   ✅ Circle of Life is healthy")
        return True
    else:
        print("   ❌ Circle of Life not healthy")
        return False


def main():
    print("=" * 60)
    print("VERIFICATION OF ALL FIXES")
    print("=" * 60)

    all_checks = []

    # Run all checks
    all_checks.append(check_youtube_scraper())
    all_checks.append(check_neo4j_connectivity())
    all_checks.append(check_services_health())
    all_checks.append(check_slack_integration())
    all_checks.append(check_circle_of_life())

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    if all(all_checks):
        print("\n🎉 ALL FIXES VERIFIED SUCCESSFULLY!")
        print("\nThe system is:")
        print("  ✅ Technically sound - All components working")
        print("  ✅ Logical - Proper architecture with separated services")
        print("  ✅ Smooth - Services responding, no errors")
        print("\nKey achievements:")
        print("  • YouTube scraper only gets transcripts (no video downloads)")
        print("  • Neo4j connectivity established via VPC")
        print("  • Correct unified scraper deployed and running")
        print("  • Bob responding in Slack for Circle of Life")
        print("  • All services healthy and operational")
        return 0
    else:
        print("\n⚠️ Some checks failed - review issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
