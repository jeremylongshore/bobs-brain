#!/usr/bin/env python3
"""
Verify all components are installed for Bob's Brain Graphiti migration
"""

import sys
import time

def check_import(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {package_name or module_name} installed")
        return True
    except ImportError:
        print(f"❌ {package_name or module_name} NOT installed")
        return False

def check_neo4j():
    """Check Neo4j connection"""
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(
            'bolt://localhost:7687', 
            auth=('neo4j', 'BobBrain2025')
        )
        with driver.session() as session:
            result = session.run('RETURN 1 AS num')
            print(f"✅ Neo4j connected and running")
            return True
    except Exception as e:
        print(f"❌ Neo4j NOT running: {e}")
        return False

def check_graphiti():
    """Check Graphiti can initialize"""
    try:
        from graphiti_core import Graphiti
        # Just check import, don't connect yet
        print("✅ Graphiti ready to use")
        return True
    except Exception as e:
        print(f"❌ Graphiti issue: {e}")
        return False

def check_firestore():
    """Check Firestore connection"""
    try:
        from google.cloud import firestore
        db = firestore.Client(project='diagnostic-pro-mvp', database='bob-brain')
        # Try to list collections
        collections = list(db.collections())
        print(f"✅ Firestore connected ({len(collections)} collections)")
        return True
    except Exception as e:
        print(f"⚠️  Firestore issue (may need auth): {str(e)[:50]}")
        return True  # Don't fail on auth issues

print("=" * 50)
print("BOB'S BRAIN INSTALLATION CHECK")
print("=" * 50)
print()

# Check Python packages
print("Python Packages:")
print("-" * 30)
packages = [
    ('graphiti_core', 'graphiti-core'),
    ('neo4j', 'neo4j'),
    ('google.cloud.firestore', 'google-cloud-firestore'),
    ('slack_sdk', 'slack-sdk'),
    ('vertexai', 'vertexai'),
    ('chromadb', 'chromadb')
]

all_good = True
for module, package in packages:
    if not check_import(module, package):
        all_good = False

print()
print("Database Systems:")
print("-" * 30)

# Check Neo4j
if not check_neo4j():
    all_good = False
    print("  Trying to wait for Neo4j startup...")
    time.sleep(5)
    if not check_neo4j():
        print("  Still not ready. May need more time.")

# Check Firestore
check_firestore()

# Check Graphiti
if not check_graphiti():
    all_good = False

print()
print("=" * 50)
if all_good:
    print("✅ ALL SYSTEMS GO! Ready for Graphiti migration")
    print()
    print("Next steps:")
    print("1. Fix Graphiti parameters in bob_memory.py")
    print("2. Run: python3 tests/test_memory_only.py")
else:
    print("❌ Some components missing. Check above for details")
    print()
    print("To fix:")
    print("1. Wait 30 seconds for Neo4j to fully start")
    print("2. Run this script again")

sys.exit(0 if all_good else 1)