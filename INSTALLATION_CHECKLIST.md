# Installation Checklist for Bob's Brain Graphiti Migration

## Current Status Check

### ✅ Already Installed:
```bash
# Python packages confirmed:
- graphiti-core==0.18.5     ✅ Installed
- google-cloud-firestore    ✅ Working
- slack-sdk                 ✅ Working
- vertexai                  ✅ Working
- chromadb                  ✅ Installed
```

### ❌ Not Installed Yet:
```bash
# Database:
- Neo4j database            ❌ Not running
- Docker (for Neo4j)        ❓ Check status
```

---

## 📦 COMPLETE INSTALLATION COMMANDS

### Step 1: Check Current Dependencies
```bash
# See what's installed
pip list | grep -E "graphiti|neo4j|firestore|slack|vertex"
```

### Step 2: Install/Update Python Packages
```bash
# Core Graphiti requirements
pip install --upgrade graphiti-core==0.18.5
pip install --upgrade neo4j==5.26.0

# Bob's Brain requirements
pip install --upgrade google-cloud-firestore==2.11.1
pip install --upgrade slack-sdk==3.31.0
pip install --upgrade vertexai==1.38.0
pip install --upgrade chromadb==0.5.0

# Optional but recommended
pip install --upgrade python-dotenv==1.0.1
pip install --upgrade tenacity==9.0.0
```

### Step 3: Install Docker (for Neo4j)
```bash
# Check if Docker is installed
docker --version

# If not installed:
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
# Log out and back in for group changes

# Verify Docker works
docker run hello-world
```

### Step 4: Install Neo4j via Docker
```bash
# Pull Neo4j image
docker pull neo4j:latest

# Create data directory
mkdir -p ~/neo4j/data ~/neo4j/logs ~/neo4j/import ~/neo4j/plugins

# Run Neo4j container
docker run -d \
  --name bob-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -v $HOME/neo4j/data:/data \
  -v $HOME/neo4j/logs:/logs \
  -v $HOME/neo4j/import:/import \
  -v $HOME/neo4j/plugins:/plugins \
  -e NEO4J_AUTH=neo4j/BobBrain2025 \
  --restart unless-stopped \
  neo4j:latest

# Check if running
docker ps | grep neo4j
```

### Step 5: Verify Neo4j Installation
```bash
# Wait 30 seconds for startup
sleep 30

# Check Neo4j browser
curl http://localhost:7474

# Test bolt connection
python3 -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'BobBrain2025'))
with driver.session() as session:
    result = session.run('RETURN 1 AS num')
    print('✅ Neo4j connected:', result.single()['num'])
driver.close()
"
```

### Step 6: Set Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export NEO4J_URI="bolt://localhost:7687"' >> ~/.bashrc
echo 'export NEO4J_USER="neo4j"' >> ~/.bashrc
echo 'export NEO4J_PASSWORD="BobBrain2025"' >> ~/.bashrc

# Reload
source ~/.bashrc

# Or create .env file
cat > ~/bobs-brain/.env.graphiti << EOF
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=BobBrain2025
EOF
```

---

## 🧪 VERIFICATION SCRIPT

Create and run this test:

```python
# verify_installation.py
import sys

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

print("=" * 50)
print("BOB'S BRAIN INSTALLATION CHECK")
print("=" * 50)

# Check Python packages
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

# Check Neo4j
if not check_neo4j():
    all_good = False

# Check Graphiti
if not check_graphiti():
    all_good = False

print("=" * 50)
if all_good:
    print("✅ ALL SYSTEMS GO! Ready for Graphiti migration")
else:
    print("❌ Some components missing. Run installation commands above")
```

---

## 🚀 QUICK INSTALL (ALL AT ONCE)

```bash
# Run this to install everything needed
cd ~/bobs-brain

# Python packages
pip install --upgrade \
  graphiti-core==0.18.5 \
  neo4j==5.26.0 \
  google-cloud-firestore==2.11.1 \
  slack-sdk==3.31.0 \
  vertexai==1.38.0 \
  chromadb==0.5.0 \
  python-dotenv==1.0.1 \
  tenacity==9.0.0

# Neo4j via Docker
docker pull neo4j:latest
docker run -d \
  --name bob-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/BobBrain2025 \
  --restart unless-stopped \
  neo4j:latest

# Wait for Neo4j to start
sleep 30

# Verify everything
python3 verify_installation.py
```

---

## 📊 Expected Result

After installation, you should see:
```
✅ graphiti-core installed
✅ neo4j installed
✅ google-cloud-firestore installed
✅ slack-sdk installed
✅ vertexai installed
✅ chromadb installed
✅ Neo4j connected and running
✅ Graphiti ready to use
==================================================
✅ ALL SYSTEMS GO! Ready for Graphiti migration
```