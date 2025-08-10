#!/usr/bin/env python3
"""
Knowledge Loader Module for Bob Unified v2
Adds critical business knowledge to ChromaDB on startup
"""

import chromadb
from datetime import datetime
import hashlib

class KnowledgeLoader:
    """Loads critical business knowledge into Bob's brain"""
    
    def __init__(self, chroma_path='/home/jeremylongshore/bobs-brain/chroma_data'):
        """Initialize connection to existing ChromaDB"""
        self.client = chromadb.PersistentClient(path=chroma_path)
        try:
            self.collection = self.client.get_collection('bob_knowledge')
        except:
            self.collection = self.client.create_collection('bob_knowledge')
        
    def load_critical_knowledge(self):
        """Load critical business and technical knowledge"""
        
        # Critical knowledge documents
        knowledge_items = [
            {
                "id": "diagnosticpro_business_2025",
                "content": """DiagnosticPro Business Intelligence
                
                Company: Intent Solutions Inc
                Owner: Jeremy Longshore (15 years business experience - BBI, trucking)
                Platform: DiagnosticPro.io - Revolutionary AI Diagnostic Platform
                
                Revenue Model:
                - Equip Diag: $4.99 (Equipment Diagnosis)
                - Verify Quote: $4.99 (Quote Verification)
                - Get Help Now: $7.99 (Emergency Analysis)
                
                Market: Multi-billion dollar repair industry disruption
                Mission: Protect customers from repair overcharges through AI-powered diagnostics
                
                Technical Stack:
                - Frontend: SvelteKit, TailwindCSS, Contra color theme
                - Backend: Node.js, PostgreSQL, RESTful APIs
                - AI: OpenRouter GPT-4o Mini for diagnostic analysis
                - Deployment: Google Cloud Run with auto-scaling
                - Payment: Stripe integration with 3 service tiers
                
                Status: PRODUCTION READY - Generating revenue
                URL: https://diagnosticpro-mvp-970547573997.us-central1.run.app""",
                "metadata": {
                    "source": "DiagnosticPro documentation",
                    "type": "business_intelligence",
                    "priority": "critical",
                    "date": datetime.now().isoformat()
                }
            },
            {
                "id": "bob_architecture_2025",
                "content": """Bob AI Agent Architecture & Capabilities
                
                Bob Unified v2 - Professional Communication Edition
                
                Core Architecture:
                - LangChain ReAct Agent with step-by-step reasoning
                - Slack Socket Mode for real-time messaging
                - ChromaDB knowledge base (970+ items)
                - SQLite database (11 tables for conversation tracking)
                - Scrapy web scraping capabilities
                - Conversation memory with context awareness
                
                Key Features:
                - Duplicate message prevention via ID tracking
                - Smart greeting system (recognizes Jeremy)
                - Professional business communication style
                - Context-aware responses based on user history
                - Automatic knowledge base queries
                
                Process Management:
                - Graceful switchover from process 56701
                - Zero-downtime deployment strategy
                - Health monitoring every 60 seconds
                
                Location: /home/jeremylongshore/bob-consolidation/src/bob_unified_v2.py""",
                "metadata": {
                    "source": "Bob consolidation project",
                    "type": "technical_architecture",
                    "priority": "critical",
                    "date": datetime.now().isoformat()
                }
            },
            {
                "id": "bob_optimization_strategy_2025",
                "content": """Bob's 16GB RAM Optimization Strategy
                
                Local Model Configuration (13GB total):
                - qwen2.5-coder:14b (7.8GB) - Code generation for non-coders
                - mistral:7b (4.4GB) - Complex reasoning tasks
                - gemma:2b (1.7GB) - Quick responses
                - 1GB buffer for system stability
                
                Cloud AI Integration:
                - Claude CLI - Expert strategy and analysis (uses Jeremy's subscription)
                - Gemini CLI - Multimodal and research tasks (uses Jeremy's subscription)
                - LangChain automatic routing between all AI systems
                
                Business Intelligence Stack:
                - Airtable for structured business data
                - Google Docs/Sheets API for reports
                - Firebase/Supabase for real-time features
                - Make.com for workflow automation ($9/month)
                
                Research & Monitoring:
                - Brave Search API (2,000 free searches/month)
                - Scrapy for competitor analysis
                - Playwright for site automation
                - LangSmith for performance monitoring
                
                Total Cost: ~$9/month for integrations""",
                "metadata": {
                    "source": "Bob pimp-out conversation",
                    "type": "optimization_strategy",
                    "priority": "high",
                    "date": datetime.now().isoformat()
                }
            },
            {
                "id": "critical_dev_rules_2025",
                "content": """Critical Development Rules for AI Projects
                
                MANDATORY Git Workflow:
                1. NEVER commit directly to main branch
                2. ALWAYS create feature branches: feature/ai-agent-name
                3. NEVER use --no-verify flag (bypasses safety)
                4. ALWAYS run checks before committing:
                   - make lint-check
                   - make test
                   - pre-commit run --all-files
                
                AI Agent Safety:
                - Implement guardrails to prevent unintended actions
                - No unauthorized API calls
                - Use tracing tools (AgentOps) for behavior logging
                - Environment variables for all sensitive data
                - Never hard-code API keys or secrets
                
                Testing Requirements:
                - End-to-end Playwright tests in headless browser
                - Validate complete workflow (input → processing → output)
                - Test with real email: jeremylongshore@gmail.com
                - Verify data persistence to database
                
                Security Best Practices:
                - Save all data to designated database
                - API keys in environment variables only
                - No sensitive data in version control
                - Regular security audits""",
                "metadata": {
                    "source": "Critical development rules",
                    "type": "development_guidelines",
                    "priority": "critical",
                    "date": datetime.now().isoformat()
                }
            },
            {
                "id": "repair_industry_insights_2025",
                "content": """Repair Industry Disruption Strategy
                
                Industry Problems:
                - Widespread repair overcharging
                - Lack of transparency in diagnostics
                - Customers unable to verify repair necessity
                - Multi-billion dollar industry ripe for disruption
                
                DiagnosticPro Solution:
                - AI-powered diagnostic verification
                - Transparent pricing ($4.99-$7.99)
                - Expert analysis accessible to everyone
                - Protection from unnecessary repairs
                
                Jeremy's Business Experience:
                - 15 years in business (BBI, trucking industry)
                - Deep understanding of vehicle maintenance costs
                - Network in automotive and trucking sectors
                - Vision for industry transformation
                
                Competitive Advantages:
                - First-mover in AI diagnostic verification
                - Professional yet accessible pricing
                - Instant analysis (no waiting for mechanics)
                - Trust through transparency
                
                Growth Strategy:
                - Start with individual consumers
                - Expand to fleet management
                - Partner with insurance companies
                - Build repair shop network for honest mechanics""",
                "metadata": {
                    "source": "Business strategy documentation",
                    "type": "industry_analysis",
                    "priority": "high",
                    "date": datetime.now().isoformat()
                }
            }
        ]
        
        # Add knowledge to collection
        added_count = 0
        for item in knowledge_items:
            try:
                # Check if already exists to avoid duplicates
                existing = self.collection.get(ids=[item['id']])
                if not existing['ids']:
                    self.collection.add(
                        ids=[item['id']],
                        documents=[item['content']],
                        metadatas=[item['metadata']]
                    )
                    added_count += 1
            except Exception as e:
                print(f"Error adding {item['id']}: {e}")
        
        return added_count
    
    def get_knowledge_stats(self):
        """Get statistics about the knowledge base"""
        total_count = self.collection.count()
        
        # Sample query to verify knowledge
        sample_results = self.collection.query(
            query_texts=["DiagnosticPro business model"],
            n_results=1
        )
        
        return {
            'total_items': total_count,
            'sample_found': len(sample_results['documents'][0]) > 0 if sample_results['documents'] else False
        }

# Function to be called from Bob Unified
def ensure_knowledge_loaded():
    """Ensures critical knowledge is loaded into Bob's brain"""
    try:
        loader = KnowledgeLoader()
        added = loader.load_critical_knowledge()
        stats = loader.get_knowledge_stats()
        
        if added > 0:
            print(f"📚 Added {added} new knowledge items to Bob's brain")
        
        print(f"🧠 Bob's knowledge base: {stats['total_items']} total items")
        return stats['total_items']
        
    except Exception as e:
        print(f"⚠️ Knowledge loading error: {e}")
        return None

if __name__ == "__main__":
    # Test the knowledge loader
    print("🚀 Testing Bob Knowledge Loader...")
    total = ensure_knowledge_loaded()
    if total:
        print(f"✅ Knowledge loader working! Total items: {total}")
    else:
        print("❌ Knowledge loader failed")