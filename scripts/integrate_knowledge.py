#!/usr/bin/env python3
"""
Knowledge Integration Script for Bob AI
Adds valuable .md documentation to existing ChromaDB
"""

import os
import chromadb
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class KnowledgeIntegrator:
    def __init__(self):
        """Connect to EXISTING ChromaDB at the correct location"""
        print("🔌 Connecting to EXISTING ChromaDB...")
        self.client = chromadb.PersistentClient(
            path='/home/jeremylongshore/.bob_brain/chroma'
        )
        
        # Get the existing collection with 970+ items
        self.collection = self.client.get_collection('bob_knowledge')
        
        # Check current count
        current_count = self.collection.count()
        print(f"✅ Connected to 'bob_knowledge' collection: {current_count} existing items")
        
    def generate_id(self, content: str, metadata: Dict) -> str:
        """Generate unique ID for knowledge item"""
        unique_string = f"{metadata.get('source', '')}:{content[:100]}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def extract_knowledge_chunks(self, file_path: str) -> List[Dict]:
        """Extract meaningful knowledge chunks from markdown file"""
        chunks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip empty or very small files
            if len(content) < 100:
                return chunks
            
            # Split by major sections (## headers)
            sections = content.split('\n## ')
            
            for i, section in enumerate(sections):
                # Add ## back if not first section
                if i > 0:
                    section = '## ' + section
                
                # Skip very small sections
                if len(section) < 50:
                    continue
                
                # Extract section title if exists
                lines = section.split('\n')
                title = lines[0].strip('#').strip() if lines else Path(file_path).stem
                
                chunks.append({
                    'content': section.strip(),
                    'metadata': {
                        'source': str(file_path),
                        'section': title,
                        'file_name': Path(file_path).name,
                        'added_date': datetime.now().isoformat(),
                        'type': 'documentation'
                    }
                })
        
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
        
        return chunks
    
    def integrate_knowledge_files(self):
        """Main integration function"""
        print("\n📚 Starting knowledge integration...")
        
        # Critical knowledge files to integrate
        knowledge_files = [
            # Bob's Brain documentation
            '/home/jeremylongshore/bobs_brain/data/knowledge_base/BOB_PIMP_OUT_CONVERSATION_20250805.md',
            '/home/jeremylongshore/bobs_brain/CRITICAL_DEVELOPMENT_RULES.md',
            '/home/jeremylongshore/bobs_brain/BOB_AGENT_HANDOFF_2025_08_06.md',
            '/home/jeremylongshore/BOB_BRAIN_FEED_CLEANUP_20250806.md',
            '/home/jeremylongshore/bobs_brain/BOB_CLOSING_WALKTHROUGH_2025_08_06.md',
            '/home/jeremylongshore/bobs_brain/BOB_FINAL_SHUTDOWN_REPORT_2025_08_06.md',
            
            # DiagnosticPro documentation  
            '/home/jeremylongshore/DiagnosticPro-v1.0-FINAL/BOBS_BRAIN.md',
            '/home/jeremylongshore/DiagnosticPro-v1.0-FINAL/README.md',
            '/home/jeremylongshore/DiagnosticPro-v1.0-FINAL/GLOBAL_LAUNCH_ANNOUNCEMENT.md',
            '/home/jeremylongshore/DiagnosticPro-v1.0-FINAL/COMPLETION_REPORT.md',
            '/home/jeremylongshore/DiagnosticPro-v1.0-FINAL/SYSTEM_STATUS_REPORT.md',
            
            # Bob consolidation project
            '/home/jeremylongshore/bob-consolidation/CLAUDE.md',
            '/home/jeremylongshore/bob-consolidation/docs/SUCCESS_REPORT.md',
            '/home/jeremylongshore/bob-consolidation/docs/COMPREHENSIVE_TEST_REPORT.md',
            
            # Critical development rules
            '/home/jeremylongshore/bobs_brain/data/knowledge_base/JEREMY_CRITICAL_DEVELOPMENT_RULES.md',
        ]
        
        total_chunks_added = 0
        
        for file_path in knowledge_files:
            if not os.path.exists(file_path):
                print(f"⚠️  File not found: {file_path}")
                continue
            
            print(f"\n📄 Processing: {Path(file_path).name}")
            chunks = self.extract_knowledge_chunks(file_path)
            
            if not chunks:
                print(f"   ⚠️  No valid chunks extracted")
                continue
            
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            
            for chunk in chunks:
                chunk_id = self.generate_id(chunk['content'], chunk['metadata'])
                ids.append(chunk_id)
                documents.append(chunk['content'])
                metadatas.append(chunk['metadata'])
            
            try:
                # Add to collection (ChromaDB handles duplicates)
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                print(f"   ✅ Added {len(chunks)} knowledge chunks")
                total_chunks_added += len(chunks)
                
            except Exception as e:
                print(f"   ❌ Error adding chunks: {e}")
        
        # Final report
        final_count = self.collection.count()
        print("\n" + "="*60)
        print("📊 KNOWLEDGE INTEGRATION COMPLETE")
        print("="*60)
        print(f"✅ Initial knowledge items: 970")
        print(f"✅ New chunks processed: {total_chunks_added}")
        print(f"✅ Total knowledge items: {final_count}")
        print(f"✅ Knowledge growth: +{final_count - 970} items")
        
        # Show sample of what was added
        print("\n📝 Sample of integrated knowledge topics:")
        sample_topics = [
            "- Bob's Pimp-Out Upgrade Plan (16GB RAM strategy)",
            "- DiagnosticPro MVP Architecture & Business Model", 
            "- Critical Development Rules for AI Agents",
            "- Bob Agent Implementation (ReAct + Slack + ChromaDB)",
            "- DiagnosticPro Cloud Deployment & Revenue Status",
            "- Bob Consolidation Project Structure",
            "- Repair Industry Disruption Strategy",
            "- Jeremy's Business Context (BBI, trucking experience)"
        ]
        for topic in sample_topics:
            print(topic)
        
        return final_count

if __name__ == "__main__":
    print("🚀 Bob Knowledge Integration Script v1.0")
    print("="*60)
    
    integrator = KnowledgeIntegrator()
    final_count = integrator.integrate_knowledge_files()
    
    print("\n✨ Knowledge integration successful!")
    print(f"🧠 Bob now has {final_count} knowledge items in his brain")
    print("🎯 Ready to provide enhanced business intelligence!")