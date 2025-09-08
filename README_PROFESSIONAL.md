# 🤖 Bob's Brain - Evolution of an AI Business Partner

[![CI Pipeline](https://github.com/jeremylongshore/bobs-brain/actions/workflows/ci.yml/badge.svg)](https://github.com/jeremylongshore/bobs-brain/actions)
[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](VERSIONS.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **A showcase of AI agent evolution**: From simple CLI assistant to enterprise-grade Slack bot

Bob's Brain demonstrates the progressive development of an AI business partner, featuring multiple versions that showcase different architectural approaches and capabilities. Perfect for developers looking to understand AI agent development patterns.

## 🎯 What is Bob?

Bob is Jeremy Longshore's AI business partner for **DiagnosticPro.io**, specializing in:
- 🔧 Vehicle diagnostic expertise
- 🛡️ Customer protection from shop overcharges
- 💼 Strategic business support
- 📚 970+ curated industry knowledge items

## 🚀 Quick Start

### Option 1: Interactive Version Selector
```bash
# Clone the repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Run the interactive selector
./scripts/version-selector.py
```

### Option 2: Direct Version Access
```bash
# Run Basic Bob (v1)
cd versions/v1-basic && python3 run_bob.py

# Run Unified Bob (v2 - Production)
cd versions/v2-unified && ./start_unified_bob_v2.sh
```

### Option 3: Docker
```bash
# Run any version in Docker
docker-compose up bob-v1  # Basic Bob
docker-compose up bob-v2  # Unified Bob
```

## 📚 Available Versions

| Version | Description | Key Features | Status |
|---------|-------------|--------------|--------|
| **v1-basic** | Simple CLI Assistant | Local ChromaDB, Basic Chat | ✅ Stable |
| **v2-unified** | Enterprise Slack Bot | Slack Integration, Memory System | ✅ Production |

[View detailed version history →](VERSIONS.md)

## 🏗️ Repository Structure

```
bobs-brain/
├── versions/               # All Bob versions
│   ├── v1-basic/          # Simple CLI version
│   ├── v2-unified/        # Production Slack bot
│   └── current/           # Symlink to latest
├── .github/workflows/      # CI/CD pipelines
├── scripts/               
│   └── version-selector.py # Interactive version selector
├── tests/                  # Comprehensive test suite
├── docs/                   # Extended documentation
└── examples/               # Usage examples
```

## 🔧 Installation

### Prerequisites
- Python 3.10+
- pip or conda
- (Optional) Docker & Docker Compose
- (Optional) Slack workspace for v2

### Basic Setup
```bash
# Install base requirements
pip install -r requirements.txt

# For specific version requirements
pip install -r versions/v1-basic/requirements.txt  # For v1
pip install -r versions/v2-unified/requirements.txt # For v2
```

### Environment Configuration
```bash
# Copy template
cp .env.template .env

# Edit with your configuration
nano .env
```

Required for v2-unified:
- `SLACK_BOT_TOKEN`: Your Slack bot token
- `SLACK_APP_TOKEN`: Your Slack app token

## 🎓 Learning Path

This repository serves as an educational resource for AI agent development:

### Beginner: Start with v1-basic
- Understand core conversation loop
- Learn ChromaDB integration
- Explore command patterns

### Intermediate: Move to v2-unified  
- Study Slack integration patterns
- Implement message deduplication
- Add conversation memory

### Advanced: Extend and Customize
- Create your own version
- Implement new features
- Contribute improvements

## 🧪 Development

### Running Tests
```bash
# All tests
make test

# Specific version tests
pytest tests/v1-basic/
pytest tests/v2-unified/
```

### Code Quality
```bash
# Run all checks
make safe-commit

# Individual checks
make lint-check
make test
```

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📖 Documentation

- [Version History](VERSIONS.md) - Detailed changelog
- [Development Guide](CLAUDE.md) - For Claude Code users
- [API Reference](docs/api.md) - Technical documentation
- [Deployment Guide](docs/deployment.md) - Production setup

## 🚢 Deployment Options

### Local Development
```bash
./scripts/version-selector.py
```

### Docker Deployment
```bash
docker-compose up
```

### Cloud Deployment
- Google Cloud Run ready (v2)
- Kubernetes manifests available
- Auto-scaling configured

## 🔒 Security

- Environment-based configuration
- No hardcoded secrets
- Automated security scanning via GitHub Actions
- Regular dependency updates

## 📊 Features by Version

### v1-basic ✅
- CLI interface
- ChromaDB knowledge base
- Basic commands
- Local execution

### v2-unified ✅
- Slack Socket Mode
- Duplicate prevention
- Conversation memory
- Professional tone
- Enterprise logging
- 970+ knowledge items

## 🤝 Support & Community

- **Issues**: [GitHub Issues](https://github.com/jeremylongshore/bobs-brain/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jeremylongshore/bobs-brain/discussions)
- **Contact**: Jeremy Longshore - DiagnosticPro.io

## 📈 Roadmap

- [ ] v3.0: Cloud Native with Kubernetes
- [ ] v4.0: LangChain ReAct Integration
- [ ] v5.0: Multi-modal Capabilities
- [ ] v6.0: Distributed Architecture

## 🙏 Acknowledgments

- DiagnosticPro.io team
- Open source community
- ChromaDB for vector storage
- Slack for excellent APIs

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

<p align="center">
  <strong>Bob's Brain</strong><br>
  <em>From simple assistant to enterprise AI partner</em><br>
  <br>
  Built with ❤️ for <a href="https://diagnosticpro.io">DiagnosticPro.io</a><br>
  Protecting customers through accurate diagnostics
</p>