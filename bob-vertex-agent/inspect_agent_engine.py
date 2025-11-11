#!/usr/bin/env python3
"""
Comprehensive inspection of Bob's Brain Agent Engine deployment.

This script validates:
1. Agent Engine runtime health and configuration
2. A2A protocol compliance
3. Query method availability (ADK vs standard Agent Engine)
4. Code Execution Sandbox settings
5. Memory Bank configuration
6. Deployment method validation
"""

import json
import os
import sys
from typing import Any, Dict, List

import google.auth
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines


def inspect_agent_engine_deployment(
    project_id: str, location: str, reasoning_engine_id: str
) -> Dict[str, Any]:
    """
    Comprehensive inspection of Agent Engine deployment.

    Returns inspection report covering:
    - Runtime configuration
    - Agent health status
    - Available methods (critical for ADK agents!)
    - A2A protocol compliance
    - Code Execution settings
    - Memory Bank configuration
    - Security posture
    """

    print(f"\n{'='*80}")
    print(f"🔍 INSPECTING AGENT ENGINE DEPLOYMENT")
    print(f"{'='*80}\n")

    print(f"📋 Target Information:")
    print(f"   Project ID: {project_id}")
    print(f"   Location: {location}")
    print(f"   Reasoning Engine ID: {reasoning_engine_id}")
    print()

    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    inspection_report = {
        "project_id": project_id,
        "location": location,
        "reasoning_engine_id": reasoning_engine_id,
        "deployment_type": None,
        "runtime_checks": {},
        "method_checks": {},
        "a2a_compliance": {},
        "security_checks": {},
        "issues": [],
        "recommendations": []
    }

    try:
        # Get Reasoning Engine instance
        print("📡 Retrieving Agent Engine instance...")
        remote_agent = reasoning_engines.ReasoningEngine(reasoning_engine_id)
        print("✅ Successfully connected to Agent Engine\n")

        # 1. CRITICAL: Check Available Methods (ADK vs Standard)
        print(f"\n{'='*80}")
        print("🔧 METHOD AVAILABILITY CHECK (CRITICAL FOR ADK AGENTS)")
        print(f"{'='*80}\n")

        available_methods = dir(remote_agent)

        # Filter to only relevant methods (exclude private/dunder)
        public_methods = [m for m in available_methods if not m.startswith('_')]

        print(f"📋 Public methods available ({len(public_methods)}):")
        for method in sorted(public_methods):
            print(f"   - {method}")
        print()

        # Check for critical methods
        critical_methods = {
            "query": "query" in public_methods,
            "send_message": "send_message" in public_methods,
            "search_memory": "search_memory" in public_methods or "async_search_memory" in public_methods,
            "get_session": "get_session" in public_methods or "async_get_session" in public_methods,
            "list_sessions": "list_sessions" in public_methods or "async_list_sessions" in public_methods,
            "delete_session": "delete_session" in public_methods or "async_delete_session" in public_methods,
            "register_feedback": "register_feedback" in public_methods,
        }

        inspection_report["method_checks"] = {
            "available_methods": public_methods,
            "critical_methods": critical_methods,
            "has_query_method": critical_methods["query"],
            "has_send_message_method": critical_methods["send_message"],
            "has_memory_methods": critical_methods["search_memory"],
            "has_session_methods": critical_methods["get_session"],
        }

        print("🔍 Critical Method Status:")
        for method, available in critical_methods.items():
            status = "✅" if available else "❌"
            print(f"   {status} {method}: {'Available' if available else 'NOT FOUND'}")
        print()

        # Determine deployment type based on available methods
        if critical_methods["query"]:
            deployment_type = "Standard Agent Engine (has query method)"
        elif critical_methods["send_message"]:
            deployment_type = "ADK Agent (use send_message, NOT query)"
        else:
            deployment_type = "Unknown (no standard query methods found)"

        inspection_report["deployment_type"] = deployment_type

        print(f"📊 Deployment Type: {deployment_type}\n")

        # 2. Test Query Capabilities
        print(f"\n{'='*80}")
        print("🧪 TESTING QUERY CAPABILITIES")
        print(f"{'='*80}\n")

        test_query = "Hello, this is a health check. Please respond with 'OK'."

        try:
            if critical_methods["query"]:
                print("Testing with query() method...")
                response = remote_agent.query(input=test_query)
                print(f"✅ query() method works")
                print(f"   Response: {response}\n")
                inspection_report["runtime_checks"]["query_method_works"] = True
            elif critical_methods["send_message"]:
                print("Testing with send_message() method...")
                response = remote_agent.send_message(message=test_query)
                print(f"✅ send_message() method works")
                print(f"   Response: {response}\n")
                inspection_report["runtime_checks"]["send_message_works"] = True
            else:
                print("❌ No standard query method found")
                inspection_report["issues"].append(
                    "No query() or send_message() method available"
                )
        except Exception as e:
            print(f"❌ Query test failed: {e}\n")
            inspection_report["issues"].append(f"Query method failed: {str(e)}")

        # 3. A2A Protocol Compliance Check
        print(f"\n{'='*80}")
        print("🔗 A2A PROTOCOL COMPLIANCE CHECK")
        print(f"{'='*80}\n")

        # Check if agent exposes A2A methods
        a2a_methods = [
            "get_agent_card",
            "send_task",
            "get_task_status",
            "list_capabilities",
        ]

        a2a_compliance = {}
        for method in a2a_methods:
            available = method in public_methods
            a2a_compliance[method] = available
            status = "✅" if available else "❌"
            print(f"   {status} {method}: {'Available' if available else 'Not found'}")

        print()

        if not any(a2a_compliance.values()):
            print("ℹ️  A2A Protocol methods not detected in Agent Engine interface.")
            print("   A2A compliance may be implemented at application layer (app/a2a_tools.py)")
            print()

        inspection_report["a2a_compliance"] = a2a_compliance

        # 4. Memory Bank Configuration Check
        print(f"\n{'='*80}")
        print("💾 MEMORY BANK CONFIGURATION")
        print(f"{'='*80}\n")

        if critical_methods["search_memory"]:
            print("✅ Memory Bank methods detected")
            print("   Available memory methods:")
            memory_methods = [m for m in public_methods if 'memory' in m.lower() or 'session' in m.lower()]
            for method in memory_methods:
                print(f"   - {method}")
            print()
            inspection_report["runtime_checks"]["memory_bank_enabled"] = True
        else:
            print("ℹ️  Memory Bank methods not detected")
            print("   Agent may be stateless (no conversation memory)")
            print()
            inspection_report["runtime_checks"]["memory_bank_enabled"] = False

        # 5. Code Execution Sandbox Check
        print(f"\n{'='*80}")
        print("🔒 CODE EXECUTION SANDBOX")
        print(f"{'='*80}\n")

        # Check if agent has code execution tools
        try:
            # Try to inspect agent configuration (if available)
            if hasattr(remote_agent, 'get_config'):
                config = remote_agent.get_config()
                print(f"Agent Configuration: {json.dumps(config, indent=2)}")
                inspection_report["runtime_checks"]["config"] = config
            else:
                print("ℹ️  Agent configuration not directly accessible via API")
        except Exception as e:
            print(f"ℹ️  Could not retrieve agent configuration: {e}")

        print()

        # 6. Generate Recommendations
        print(f"\n{'='*80}")
        print("💡 RECOMMENDATIONS")
        print(f"{'='*80}\n")

        recommendations = []

        if not critical_methods["query"] and critical_methods["send_message"]:
            recommendations.append(
                "🔧 CRITICAL: Use send_message() instead of query() for ADK agents"
            )
            recommendations.append(
                "   Update slack-webhook/main.py to use remote_agent.send_message(message=user_message)"
            )

        if not critical_methods["query"] and not critical_methods["send_message"]:
            recommendations.append(
                "⚠️  WARNING: No standard query methods found. Agent may need re-deployment."
            )

        if not inspection_report["runtime_checks"].get("memory_bank_enabled"):
            recommendations.append(
                "ℹ️  Consider enabling Memory Bank for conversation history tracking"
            )

        if not any(a2a_compliance.values()):
            recommendations.append(
                "ℹ️  A2A Protocol methods not exposed. Verify app/a2a_tools.py implementation."
            )

        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

        inspection_report["recommendations"] = recommendations

    except Exception as e:
        print(f"\n❌ CRITICAL ERROR during inspection: {e}")
        inspection_report["issues"].append(f"Inspection failed: {str(e)}")
        import traceback
        traceback.print_exc()

    # Final Summary
    print(f"\n{'='*80}")
    print("📊 INSPECTION SUMMARY")
    print(f"{'='*80}\n")

    print(f"Deployment Type: {inspection_report['deployment_type']}")
    print(f"Issues Found: {len(inspection_report['issues'])}")
    print(f"Recommendations: {len(inspection_report['recommendations'])}")
    print()

    if inspection_report["issues"]:
        print("⚠️  Issues:")
        for issue in inspection_report["issues"]:
            print(f"   - {issue}")
        print()

    return inspection_report


def main():
    """Main entry point."""

    # Get credentials and project
    credentials, project_id = google.auth.default()

    # Agent Engine configuration
    location = "us-central1"
    reasoning_engine_id = "5828234061910376448"

    # Check if project override provided
    if len(sys.argv) > 1:
        project_id = sys.argv[1]

    if not project_id:
        print("❌ ERROR: Could not determine GCP project ID")
        print("   Set via: export GOOGLE_CLOUD_PROJECT=bobs-brain")
        print("   Or pass as argument: python inspect_agent_engine.py bobs-brain")
        sys.exit(1)

    # Run inspection
    report = inspect_agent_engine_deployment(
        project_id=project_id,
        location=location,
        reasoning_engine_id=reasoning_engine_id
    )

    # Save report to file
    report_file = "agent_engine_inspection_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n💾 Full report saved to: {report_file}\n")

    # Exit with error code if issues found
    if report["issues"]:
        sys.exit(1)
    else:
        print("✅ Inspection completed successfully\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
