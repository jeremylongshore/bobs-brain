#!/usr/bin/env python3
"""
Analyze Automation and Smart Insights Database Schemas
"""

import sqlite3
import json
from typing import Dict, List

def analyze_automation_db() -> Dict:
    """Analyze automation.db schema and data"""

    print('📋 AUTOMATION.DB SCHEMA ANALYSIS:')
    conn = sqlite3.connect('/home/jeremylongshore/.bob_brain/automation.db')
    cursor = conn.cursor()

    # Get table schema
    cursor.execute('PRAGMA table_info(automation_rules)')
    columns = cursor.fetchall()
    print('\nTable: automation_rules')
    for col in columns:
        pk_text = 'PRIMARY KEY' if col[5] else ''
        null_text = 'NOT NULL' if col[3] else 'NULL'
        print(f'  - {col[1]} ({col[2]}) {pk_text} {null_text}')

    # Get all rules with full data
    cursor.execute('SELECT * FROM automation_rules')
    rules = cursor.fetchall()
    print(f'\nRules Data ({len(rules)} rules):')

    rules_data = []
    for i, rule in enumerate(rules, 1):
        rule_data = {
            'id': rule[0],
            'name': rule[1],
            'trigger': rule[2],
            'action': rule[3],
            'config': rule[4],
            'active': rule[5],
            'created_at': rule[6],
            'last_run': rule[7],
            'execution_count': rule[8],
            'success_rate': rule[9]
        }
        rules_data.append(rule_data)

        print(f'  Rule {i}:')
        print(f'    ID: {rule[0]}')
        print(f'    Name: {rule[1]}')
        print(f'    Trigger: {rule[2]}')
        print(f'    Action: {rule[3]}')
        print(f'    Config: {rule[4]}')
        print(f'    Active: {rule[5]}')
        print(f'    Created: {rule[6]}')
        print(f'    Last Run: {rule[7]}')
        print(f'    Executions: {rule[8]}')
        print(f'    Success Rate: {rule[9]}')
        print()

    conn.close()
    return {'schema': columns, 'rules': rules_data}

def analyze_insights_db() -> Dict:
    """Analyze smart_insights.db schema and data"""

    print('🧠 SMART_INSIGHTS.DB SCHEMA ANALYSIS:')
    conn = sqlite3.connect('/home/jeremylongshore/.bob_brain/smart_insights.db')
    cursor = conn.cursor()

    # Get table schema
    cursor.execute('PRAGMA table_info(insights)')
    columns = cursor.fetchall()
    print('\nTable: insights')
    for col in columns:
        pk_text = 'PRIMARY KEY' if col[5] else ''
        null_text = 'NOT NULL' if col[3] else 'NULL'
        print(f'  - {col[1]} ({col[2]}) {pk_text} {null_text}')

    # Get all insights
    cursor.execute('SELECT * FROM insights')
    insights = cursor.fetchall()
    print(f'\nInsights Data ({len(insights)} insights):')

    insights_data = []
    for i, insight in enumerate(insights, 1):
        insight_data = {
            'id': insight[0],
            'type': insight[1],
            'title': insight[2],
            'description': insight[3],
            'confidence': insight[4],
            'importance': insight[5],
            'data_sources': insight[6],
            'actions': insight[7],
            'generated_at': insight[8],
            'user_feedback': insight[9]
        }
        insights_data.append(insight_data)

        print(f'  Insight {i}:')
        print(f'    ID: {insight[0]}')
        print(f'    Type: {insight[1]}')
        print(f'    Title: {insight[2]}')
        print(f'    Description: {insight[3][:100]}...')
        print(f'    Confidence: {insight[4]}')
        print(f'    Importance: {insight[5]}')
        print(f'    Data Sources: {insight[6]}')
        print(f'    Actions: {insight[7][:100]}...')
        print(f'    Generated: {insight[8]}')
        print(f'    User Feedback: {insight[9]}')
        print()

    conn.close()
    return {'schema': columns, 'insights': insights_data}

def explain_get_er_done_support():
    """Explain how automation and insights support Bob's 'get er done' tasks"""

    print("🎯 HOW AUTOMATION & INSIGHTS SUPPORT BOB'S 'GET ER DONE' TASKS:")
    print("=" * 70)

    print("\n📱 AUTOMATION RULES (2 rules):")
    print("1. Memory Optimization Rule:")
    print("   - Trigger: memory_high (80% threshold)")
    print("   - Action: optimize_memory")
    print("   - Purpose: Automatically free memory when VM gets full")
    print("   - 'Get Er Done': Prevents system slowdowns without manual intervention")

    print("\n2. Daily Insights Generation:")
    print("   - Trigger: new_day")
    print("   - Action: generate_insights")
    print("   - Purpose: Automatically analyze patterns and suggest optimizations")
    print("   - 'Get Er Done': Proactive recommendations without being asked")

    print("\n🧠 SMART INSIGHTS (3 insights):")
    print("1. Peak Usage Pattern:")
    print("   - Insight: You're most active around 2PM")
    print("   - Actions: Schedule important tasks during peak hours")
    print("   - 'Get Er Done': Optimize timing for maximum efficiency")

    print("\n2. AI Model Preference:")
    print("   - Insight: 'ai_routed' used most frequently (5 times)")
    print("   - Actions: Pre-load this model, optimize memory allocation")
    print("   - 'Get Er Done': Faster responses by predicting model needs")

    print("\n3. Memory Optimization Opportunity:")
    print("   - Insight: Only 0% memory used, can load additional models")
    print("   - Actions: Pre-load models, enable more AI systems")
    print("   - 'Get Er Done': Maximize system capabilities proactively")

    print("\n🚀 FIRESTORE MIGRATION VALUE:")
    print("- Automation rules → /bob_automation collection")
    print("- Smart insights → /bob_insights collection")
    print("- Alice can access these for enhanced collaboration")
    print("- Bob's 'get er done' intelligence becomes shared with Alice")

def generate_firestore_schemas():
    """Generate Firestore collection schemas for migration"""

    print("\n🔥 FIRESTORE MIGRATION SCHEMAS:")
    print("=" * 50)

    automation_schema = {
        "collection": "/bob_automation/{rule_id}",
        "schema": {
            "rule_id": "string (unique identifier)",
            "name": "string (human readable name)",
            "trigger_condition": "string (when to execute)",
            "action_type": "string (what to do)",
            "configuration": "map (JSON config object)",
            "active": "boolean (enabled/disabled)",
            "created_at": "timestamp",
            "last_executed_at": "timestamp (nullable)",
            "execution_count": "number",
            "success_rate": "number (0.0 - 1.0)",
            "metadata": {
                "priority": "string (low/medium/high)",
                "category": "string (performance/maintenance/optimization)",
                "agent_permissions": "array (which agents can trigger)"
            }
        }
    }

    insights_schema = {
        "collection": "/bob_insights/{insight_id}",
        "schema": {
            "insight_id": "string (unique identifier)",
            "type": "string (pattern/optimization/recommendation)",
            "title": "string (short description)",
            "description": "string (detailed explanation)",
            "confidence": "number (0.0 - 1.0)",
            "importance": "string (low/medium/high/critical)",
            "data_sources": "array (where insight came from)",
            "recommended_actions": "array (what user should do)",
            "generated_at": "timestamp",
            "expires_at": "timestamp (optional)",
            "user_feedback": "number (optional rating)",
            "status": "string (new/acknowledged/implemented/dismissed)",
            "metadata": {
                "category": "string (performance/cost/security/usage)",
                "affected_systems": "array (which components)",
                "estimated_impact": "string (time/cost savings)"
            }
        }
    }

    print("📋 Automation Rules Schema:")
    print(json.dumps(automation_schema, indent=2))

    print("\n🧠 Smart Insights Schema:")
    print(json.dumps(insights_schema, indent=2))

if __name__ == "__main__":
    print("🔍 AUTOMATION & INSIGHTS DATABASE ANALYSIS")
    print("=" * 60)

    # Analyze databases
    automation_data = analyze_automation_db()
    insights_data = analyze_insights_db()

    # Explain business value
    explain_get_er_done_support()

    # Generate Firestore schemas
    generate_firestore_schemas()

    print(f"\n✅ Analysis Complete:")
    print(f"   - {len(automation_data['rules'])} automation rules analyzed")
    print(f"   - {len(insights_data['insights'])} smart insights analyzed")
    print(f"   - Migration schemas generated for Firestore")
