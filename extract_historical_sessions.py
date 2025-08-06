#!/usr/bin/env python3
"""
Extract additional historical context from old Claude sessions
and add any missing knowledge to Bob's Brain
"""

import chromadb
from datetime import datetime


def extract_historical_knowledge():
    """Extract historical session knowledge that might be missing"""

    print("🧠 Extracting historical session knowledge for Bob's Brain...")

    # Connect to Bob's brain
    client = chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma')
    collection = client.get_collection('bob_knowledge')

    # Additional historical context that might be missing
    historical_knowledge = [
        {
            "content": "HISTORICAL SESSION CONTEXT: Previous Claude sessions (PID 1409, 16145) from August 5th involved intensive Beast Mode architecture development, including tmux session management, CrewAI payment integration (60% complete), LangChain voice recording (45% complete), AutoGen mobile testing (30% complete), and comprehensive system coordination through Bob's House MCP headquarters.",
            "metadata": {
                "type": "historical_session",
                "date": "2025-08-05",
                "source": "previous_claude_sessions",
                "priority": "CONTEXT"
            }
        },
        {
            "content": "BEAST MODE SYSTEM ARCHITECTURE: 8-session tmux system with beast-central (Mission Control), beast-crewai (Payment), beast-langchain (Voice), beast-autogen (Mobile), beast-langgraph (State), beast-brain (Knowledge), beast-mvp2 (AI Coordination), beast-wtf (Emergency). Emergency commands: 'wtf' for disaster recovery, 'beast-mode' for system startup, 'tmux ls' for session listing.",
            "metadata": {
                "type": "system_architecture",
                "source": "emergency_briefing",
                "components": "tmux_beast_mode",
                "status": "HISTORICAL"
            }
        },
        {
            "content": "JEREMY'S BACKGROUND PROFILE: Restaurant industry expert (BBI Bloomin' Brands background) + Trucking business owner. Vision: AI-powered repair revolution (fix anything from phones to spaceships). Personality: Direct, no-nonsense, results-oriented entrepreneur. Current focus evolved from MS Pacman themed DiagnosticPro MVP 2.0 to today's breakthrough production-ready system.",
            "metadata": {
                "type": "user_profile",
                "subject": "Jeremy",
                "source": "emergency_briefing",
                "priority": "PERSONAL_CONTEXT"
            }
        },
        {
            "content": "DEVELOPMENT EVOLUTION: DiagnosticPro evolved from Beast Mode architecture (August 3-5) with multiple AI teams (CrewAI payment 60%, LangChain voice 45%, AutoGen mobile 30%) to today's (August 6) breakthrough single unified system with OpenRouter GPT-4o Mini, dual email delivery, and production Cloud Run deployment. Development rules maintained: never localhost, never main branch, professional standards only.",
            "metadata": {
                "type": "project_evolution",
                "project": "DiagnosticPro",
                "timespan": "2025-08-03_to_2025-08-06",
                "status": "EVOLUTION_COMPLETE"
            }
        },
        {
            "content": "HISTORICAL URLS AND DEPLOYMENTS: Previous system included https://bobs-brain-central-157908567967.us-central1.run.app (Bob's Brain Cloud), https://bobs-ai-house-157908567967.us-central1.run.app (Bob's House AI), and early DiagnosticPro staging. These evolved into today's single production deployment at https://diagnosticpro-mvp-970547573997.us-central1.run.app with unified architecture.",
            "metadata": {
                "type": "deployment_history",
                "project": "DiagnosticPro_Evolution",
                "urls": "historical_deployments",
                "status": "SUPERSEDED"
            }
        }
    ]

    # Add each piece of historical knowledge
    added_count = 0
    for i, knowledge in enumerate(historical_knowledge):
        knowledge_id = f"historical_session_extract_{datetime.now().strftime('%Y%m%d')}_{i+1}"

        try:
            # Check if similar content already exists
            existing = collection.query(
                query_texts=[knowledge["content"][:100]],
                n_results=1
            )

            # Only add if not already present
            if not existing['documents'] or not existing['documents'][0]:
                collection.add(
                    documents=[knowledge["content"]],
                    metadatas=[knowledge["metadata"]],
                    ids=[knowledge_id]
                )
                print(f"✅ Added historical knowledge: {knowledge['metadata']['type']}")
                added_count += 1
            else:
                print(f"⏭️ Skipped (already exists): {knowledge['metadata']['type']}")

        except Exception as e:
            print(f"⚠️ Warning adding historical knowledge {i+1}: {e}")

    # Final status
    total_items = collection.count()
    print(f"\n🧠 Bob's brain now contains {total_items} knowledge items")
    print(f"📈 Added {added_count} new historical items from previous Claude sessions")

    return added_count > 0


if __name__ == "__main__":
    print("🔍 Extracting historical session knowledge from previous Claude sessions...")
    success = extract_historical_knowledge()
    if success:
        print("\n✅ Historical session context successfully integrated into Bob's Brain!")
    else:
        print("\n✅ Bob already has all historical session context!")
