# 🤖 Bob - Unified AI Business Partner

**Professional AI agent for DiagnosticPro.io and business operations**

Bob is Jeremy Longshore's unified AI business partner, specializing in vehicle diagnostics, repair industry expertise, and strategic business support. Built with enterprise-grade reliability and professional communication.

---

## 🎯 What Bob Does

- **🔧 DiagnosticPro Expertise**: Vehicle diagnostic procedures and repair industry knowledge
- **🛡️ Customer Protection**: Helps prevent shop overcharges through accurate diagnostics  
- **💼 Business Strategy**: Leverages Jeremy's 15-year experience (BBI, trucking)
- **💬 Professional Communication**: Context-aware, business-appropriate responses
- **📚 Knowledge Integration**: Access to 970+ curated industry knowledge items

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Slack workspace with bot permissions
- ChromaDB knowledge base (optional for full features)

### Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/jeremylongshore/bobs-brain.git
   cd bobs-brain
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp config/.env.template config/.env
   # Edit config/.env with your Slack tokens
   ```

3. **Start Bob:**
   ```bash
   ./scripts/start_unified_bob_v2.sh
   ```

## 📱 Slack Configuration

1. **Create Slack App**: https://api.slack.com/apps
2. **Enable Socket Mode** with app-level token
3. **Bot Token Scopes**:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
   - `im:history`
4. **Install to workspace** and copy tokens to `.env`

## 🏗️ Architecture

```
Bob Unified Agent v2
├── 🧠 Smart Communication
│   ├── Duplicate response prevention
│   ├── Context-aware conversation memory
│   ├── Professional business tone
│   └── Jeremy-specific recognition
├── 📚 Knowledge Integration
│   ├── ChromaDB vector database (970+ items)
│   ├── DiagnosticPro procedures
│   ├── Repair industry expertise
│   └── Business strategy insights
├── 🔌 Slack Integration
│   ├── Socket Mode real-time connection
│   ├── Enterprise error handling
│   ├── Comprehensive logging
│   └── Health monitoring
└── 🛡️ Enterprise Features
    ├── Automatic backup systems
    ├── Rollback procedures
    ├── Professional monitoring
    └── Security best practices
```

## 💬 Communication Style

Bob communicates as Jeremy's strategic business partner:

- **For Jeremy**: Concise, context-aware responses ("Hey Jeremy!" vs full introductions)
- **For Team**: Professional DiagnosticPro expertise and guidance
- **Business Focus**: Repair industry disruption and customer protection
- **Strategic**: Leverages 15 years business experience (BBI, trucking)

## 🔧 Configuration

### Environment Variables
```bash
# Slack Integration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Knowledge Base (optional)
CHROMA_PERSIST_DIR=/path/to/knowledge/base

# Operational Settings
BOB_MODE=production
LOG_LEVEL=INFO
```

## 📊 Features

### ✅ Enhanced Communication (v2.0)
- **No Duplicate Responses**: Message ID tracking prevents double responses
- **Smart Greetings**: Context-aware hello responses (brief for repeated greetings)
- **Professional Tone**: Business partner communication style
- **Memory System**: Remembers recent conversations and context

### ✅ DiagnosticPro Integration
- **Industry Expertise**: Vehicle repair and diagnostic knowledge
- **Customer Protection**: Shop overcharge prevention focus
- **Business Context**: Jeremy's BBI and trucking experience
- **Strategic Support**: Multi-billion repair industry disruption

### ✅ Enterprise Reliability
- **Health Monitoring**: Automatic connection recovery
- **Comprehensive Logging**: Full operational visibility
- **Error Handling**: Graceful failure recovery
- **Backup Systems**: Complete system backup and rollback

## 🎯 Business Mission

> **DiagnosticPro.io**: Disrupting the multi-billion dollar repair industry by protecting customers from shop overcharges through accurate diagnostic procedures and transparent expertise.

Bob serves as Jeremy's AI business partner in this mission, providing:
- Technical diagnostic expertise
- Industry knowledge and insights  
- Strategic business support
- Professional customer communication

## 📈 Deployment

### Production Deployment
```bash
# Start Bob with monitoring
./scripts/start_unified_bob_v2.sh

# Check status
ps aux | grep bob_unified_v2
tail -f logs/bob_unified_v2.log
```

## 🛠️ Development

### Testing
```bash
# Run comprehensive tests
python3 src/bob_test_harness.py

# Validate code
python3 -m py_compile src/bob_unified_v2.py
```

## 🔒 Security

- **Token Management**: Environment-based secure token storage
- **Process Isolation**: Clean process separation and monitoring
- **Backup Systems**: Complete data backup and recovery procedures
- **Error Handling**: No sensitive data exposure in logs or errors

## 🤝 Support

**Primary Contact**: Jeremy Longshore - DiagnosticPro.io  
**Repository Issues**: https://github.com/jeremylongshore/bobs-brain/issues  
**Business Context**: Vehicle repair industry disruption and customer protection

---

## 🎉 Success Story

Bob has successfully consolidated Jeremy's fragmented AI implementations into one unified, professional business partner. From scattered Python files and duplicate processes to a single, enterprise-grade agent supporting DiagnosticPro.io's mission.

**Key Achievements**:
- ✅ Zero-downtime switchover from legacy systems
- ✅ 970+ knowledge items preserved and enhanced  
- ✅ Professional business communication established
- ✅ Enterprise reliability and monitoring implemented
- ✅ DiagnosticPro business context fully integrated

*Bob: From scattered fragments to unified excellence*

---

**Built with ❤️ for DiagnosticPro.io - Protecting customers through accurate diagnostics**
