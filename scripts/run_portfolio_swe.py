#!/usr/bin/env python3
"""
Portfolio SWE CLI - Run multi-repo quality audits from command line

Usage:
    python3 scripts/run_portfolio_swe.py
    python3 scripts/run_portfolio_swe.py --repos bobs-brain,diagnosticpro
    python3 scripts/run_portfolio_swe.py --mode dry-run --output report.json
    python3 scripts/run_portfolio_swe.py --repos all --markdown report.md

Environment:
    Run from repo root directory
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add agents to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from iam_senior_adk_devops_lead.portfolio_orchestrator import (
    run_portfolio_swe,
    get_portfolio_local_repos,
    get_portfolio_repos_by_tag
)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run SWE pipeline across multiple repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run on all local repos (default)
  %(prog)s

  # Run on specific repos
  %(prog)s --repos bobs-brain,diagnosticpro

  # Run on all repos with a specific tag
  %(prog)s --tag adk

  # Run in dry-run mode
  %(prog)s --mode dry-run

  # Save JSON output
  %(prog)s --output portfolio-report.json

  # Generate markdown report
  %(prog)s --markdown portfolio-report.md

  # Combine options
  %(prog)s --repos bobs-brain --mode dry-run --output report.json --markdown report.md
        """
    )

    parser.add_argument(
        "--repos",
        type=str,
        default=None,
        help='Repo IDs to audit (comma-separated) or "all". If not specified, runs on all local repos.'
    )

    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Filter repos by tag (e.g., 'adk', 'production'). Cannot be used with --repos."
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["preview", "dry-run", "create"],
        default="preview",
        help="Pipeline mode: preview (default), dry-run (show what would happen), create (actually create issues)"
    )

    parser.add_argument(
        "--task",
        type=str,
        default="Portfolio quality audit",
        help="Task description for the audit"
    )

    parser.add_argument(
        "--env",
        type=str,
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Environment: dev (default), staging, prod"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save JSON results to file (e.g., portfolio-report.json)"
    )

    parser.add_argument(
        "--markdown",
        type=str,
        default=None,
        help="Generate markdown report to file (e.g., portfolio-report.md)"
    )

    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run repos in parallel (future enhancement, not yet implemented)"
    )

    return parser.parse_args()


def export_json(result, output_path: str):
    """Export portfolio result to JSON file."""
    print(f"\n📄 Exporting JSON to {output_path}...")

    # Convert result to JSON-serializable dict
    output = {
        "portfolio_run_id": result.portfolio_run_id,
        "timestamp": result.timestamp.isoformat(),
        "duration_seconds": result.portfolio_duration_seconds,
        "summary": {
            "total_repos_analyzed": result.total_repos_analyzed,
            "total_repos_skipped": result.total_repos_skipped,
            "total_repos_errored": result.total_repos_errored,
            "total_issues_found": result.total_issues_found,
            "total_issues_fixed": result.total_issues_fixed,
            "fix_rate": (result.total_issues_fixed / result.total_issues_found * 100)
                        if result.total_issues_found > 0 else 0.0
        },
        "issues_by_severity": result.issues_by_severity,
        "issues_by_type": result.issues_by_type,
        "repos_by_issue_count": result.repos_by_issue_count,
        "repos_by_compliance_score": result.repos_by_compliance_score,
        "repos": [
            {
                "repo_id": r.repo_id,
                "display_name": r.display_name,
                "status": r.status,
                "duration_seconds": r.duration_seconds,
                "issues_found": r.issues_found,
                "issues_fixed": r.issues_fixed,
                "error_message": r.error_message
            }
            for r in result.repos
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ JSON exported to {output_path}")


def export_markdown(result, output_path: str):
    """Export portfolio result to Markdown file."""
    print(f"\n📄 Generating Markdown report to {output_path}...")

    lines = []
    lines.append(f"# Portfolio SWE Audit Report")
    lines.append(f"")
    lines.append(f"**Portfolio Run ID:** `{result.portfolio_run_id}`")
    lines.append(f"**Date:** {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Duration:** {result.portfolio_duration_seconds:.2f} seconds")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # Summary
    lines.append(f"## Summary")
    lines.append(f"")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Repos Analyzed | {result.total_repos_analyzed} |")
    lines.append(f"| Repos Skipped | {result.total_repos_skipped} |")
    lines.append(f"| Repos Errored | {result.total_repos_errored} |")
    lines.append(f"| Total Issues | {result.total_issues_found} |")
    lines.append(f"| Issues Fixed | {result.total_issues_fixed} |")
    fix_rate = (result.total_issues_fixed / result.total_issues_found * 100) if result.total_issues_found > 0 else 0.0
    lines.append(f"| Fix Rate | {fix_rate:.1f}% |")
    lines.append(f"")

    # Issues by severity
    if result.issues_by_severity:
        lines.append(f"## Issues by Severity")
        lines.append(f"")
        lines.append(f"| Severity | Count |")
        lines.append(f"|----------|-------|")
        for severity in ["critical", "high", "medium", "low", "info"]:
            count = result.issues_by_severity.get(severity, 0)
            if count > 0:
                lines.append(f"| {severity.title()} | {count} |")
        lines.append(f"")

    # Issues by type
    if result.issues_by_type:
        lines.append(f"## Issues by Type")
        lines.append(f"")
        lines.append(f"| Type | Count |")
        lines.append(f"|------|-------|")
        for issue_type, count in sorted(result.issues_by_type.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"| {issue_type} | {count} |")
        lines.append(f"")

    # Repos by issue count
    if result.repos_by_issue_count:
        lines.append(f"## Repositories by Issue Count")
        lines.append(f"")
        lines.append(f"| Rank | Repository | Issues |")
        lines.append(f"|------|------------|--------|")
        for i, (repo_id, issue_count) in enumerate(result.repos_by_issue_count, 1):
            lines.append(f"| {i} | {repo_id} | {issue_count} |")
        lines.append(f"")

    # Repos by compliance
    if result.repos_by_compliance_score:
        lines.append(f"## Repositories by Compliance Score")
        lines.append(f"")
        lines.append(f"| Rank | Repository | Compliance |")
        lines.append(f"|------|------------|------------|")
        for i, (repo_id, compliance_score) in enumerate(result.repos_by_compliance_score, 1):
            lines.append(f"| {i} | {repo_id} | {compliance_score:.2f} |")
        lines.append(f"")

    # Per-repo details
    lines.append(f"## Per-Repository Results")
    lines.append(f"")
    for repo_result in result.repos:
        icon = "✅" if repo_result.status == "completed" else "⏭️" if repo_result.status == "skipped" else "❌"
        lines.append(f"### {icon} {repo_result.display_name} (`{repo_result.repo_id}`)")
        lines.append(f"")
        lines.append(f"**Status:** {repo_result.status.upper()}")
        lines.append(f"**Duration:** {repo_result.duration_seconds:.2f}s")
        if repo_result.status == "completed":
            lines.append(f"**Issues Found:** {repo_result.issues_found}")
            lines.append(f"**Issues Fixed:** {repo_result.issues_fixed}")
        elif repo_result.status == "error":
            lines.append(f"**Error:** {repo_result.error_message}")
        lines.append(f"")

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✅ Markdown report generated at {output_path}")


def main():
    """Main CLI entry point."""
    args = parse_args()

    # Validate arguments
    if args.repos and args.tag:
        print("❌ Error: Cannot specify both --repos and --tag")
        sys.exit(1)

    # Determine repo list
    repo_ids = None
    if args.tag:
        print(f"🏷️  Filtering repos by tag: {args.tag}")
        repo_ids = get_portfolio_repos_by_tag(args.tag)
        if not repo_ids:
            print(f"⚠️  No repos found with tag '{args.tag}'")
            sys.exit(0)
    elif args.repos:
        if args.repos.lower() == "all":
            print("📋 Running on all local repos")
            repo_ids = None  # Let orchestrator handle it
        else:
            repo_ids = [r.strip() for r in args.repos.split(",")]
            print(f"📋 Running on specified repos: {', '.join(repo_ids)}")

    # Run portfolio audit
    result = run_portfolio_swe(
        repo_ids=repo_ids,
        mode=args.mode,
        task=args.task,
        env=args.env,
        parallel=args.parallel
    )

    # Export results if requested
    if args.output:
        export_json(result, args.output)

    if args.markdown:
        export_markdown(result, args.markdown)

    # Exit with appropriate code
    if result.total_repos_errored > 0:
        print("\n⚠️  Some repos had errors. Check output above.")
        sys.exit(1)
    elif result.total_repos_analyzed == 0:
        print("\n⚠️  No repos were analyzed.")
        sys.exit(0)
    else:
        print(f"\n✅ Portfolio audit complete!")
        sys.exit(0)


if __name__ == "__main__":
    main()
