# 🧠 Bob's Brain - AI-Powered Assistant Ecosystem

[![CI/CD](https://github.com/jeremylongshore/bobs-brain/workflows/CI/badge.svg)](https://github.com/jeremylongshore/bobs-brain/actions)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue?logo=github)](https://jeremylongshore.github.io/bobs-brain)
[![Cloud Run](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Slack](https://img.shields.io/badge/Slack-Integration-4A154B?logo=slack&logoColor=white)](https://slack.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributors Welcome](https://img.shields.io/badge/contributors-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

> An intelligent AI assistant that learns, remembers, and evolves through continuous interaction. Built with Google Gemini 2.5 Flash, Neo4j graph database, and enterprise-grade cloud infrastructure.

## 🌟 Features

- **🤖 Advanced AI**: Powered by Google Gemini 2.5 Flash with intelligent response generation
- **🧠 Persistent Memory**: Full conversation recall with Neo4j graph database
- **📱 Slack Integration**: Native Slack bot with real-time messaging
- **🔄 Continuous Learning**: Circle of Life feedback loop for model improvement
- **📊 Data Collection**: Automated scraping from 40+ technical sources
- **☁️ Cloud-Native**: Deployed on Google Cloud Run with auto-scaling
- **💰 Cost-Efficient**: < $30/month operational costs with $2,251+ GCP credits
- **🔒 Enterprise Security**: VPC networking, secret management, and access controls

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Platform account
- Slack workspace and app tokens

### Local Development

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SLACK_BOT_TOKEN=xoxb-your-token-here
export GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
export PROJECT_ID=your-gcp-project-id

# Run Bob's Brain
python src/bob_brain_v5.py
```

### Production Deployment

```bash
# Deploy to Google Cloud Run
make deploy

# Or manually:
gcloud run deploy bobs-brain \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --vpc-connector bob-vpc-connector \
  --vpc-egress private-ranges-only
```

## 🏗️ Architecture

```mermaid
graph TB
    A[Slack Interface] --> B[Bob's Brain Service]
    B --> C[Gemini 2.5 Flash]
    B --> D[Neo4j Graph DB]
    B --> E[BigQuery Analytics]

    F[Unified Scraper] --> G[40+ Data Sources]
    F --> E
    F --> H[Circle of Life Learning]

    B --> I[MVP3 Diagnostic Platform]
    H --> B

    subgraph "Google Cloud Platform"
        B
        D
        E
        F
    end
```

### Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Engine** | Google Gemini 2.5 Flash | Natural language processing |
| **Graph Database** | Neo4j 5.20 | Knowledge relationships & memory |
| **Data Warehouse** | BigQuery | Analytics & ML training |
| **Message Bus** | Slack API | User interaction interface |
| **Web Framework** | Flask + Gunicorn | REST API server |
| **Container Runtime** | Google Cloud Run | Serverless deployment |

## 📚 Documentation

> **🌐 [Complete Documentation Site](https://jeremylongshore.github.io/bobs-brain)** - Comprehensive guides for all branches and use cases

### Key Documentation
- [**Branch Guide**](docs/BRANCH_GUIDE.md) - Navigate between different project branches and versions
- [**Contributing Guide**](CONTRIBUTING.md) - How to contribute to the project
- [**Architecture Guide**](docs/ARCHITECTURE.md) - System design and component overview
- [**Deployment Guide**](docs/DEPLOYMENT.md) - Production deployment instructions
- [**API Reference**](docs/API.md) - REST endpoint documentation
- [**Security Guide**](docs/SECURITY.md) - Security best practices

## 🛠️ Development

### Available Commands

```bash
# Development workflow
make lint-check     # Run code linting
make test          # Execute test suite
make type-check    # Type checking with mypy
make security-check # Security scanning
make safe-commit   # Run all checks before commit

# Deployment
make deploy        # Deploy to Cloud Run
make test-health   # Test health endpoints

# Monitoring
make logs          # View application logs
make metrics       # Display system metrics
```

### Project Structure

```
bobs-brain/
├── src/                    # Production source code
│   ├── bob_brain_v5.py    # Main AI assistant service
│   ├── circle_of_life.py  # Learning pipeline
│   └── unified_scraper.py # Data collection
├── scripts/               # Automation scripts
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .github/               # GitHub workflows
└── requirements.txt       # Python dependencies
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Integration tests
python scripts/testing/test_complete_flow.py
```

## 📊 System Status

### Health Indicators
- ✅ **Services**: 3/3 healthy (bobs-brain, unified-scraper, circle-of-life)
- ✅ **Uptime**: 99.95% (target: 99.9%)
- ✅ **Response Time**: 1.8s avg (target: <2s)
- ✅ **Cost**: $28/month (target: <$30)
- ✅ **Learning**: Active continuous improvement

### Key Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Response Time | 1.8s | <2s | ✅ |
| Data Collection | 120/day | 100+/day | ✅ |
| Error Rate | 0.3% | <1% | ✅ |
| Learning Rate | Continuous | Daily | ✅ |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `make test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Areas We Need Help

- 🧠 **AI/ML Engineers**: Enhance learning algorithms and model fine-tuning
- 🌐 **Web Scrapers**: Add new data sources and improve extraction accuracy
- 🔧 **DevOps Engineers**: Optimize cloud infrastructure and monitoring
- 📝 **Technical Writers**: Improve documentation and user guides
- 🧪 **QA Engineers**: Expand test coverage and automation

## 📋 Roadmap

### Current Phase: Production Optimization
- ✅ Core AI functionality
- ✅ Slack integration
- ✅ Data collection pipeline
- ✅ Cloud deployment

### Next Phase: Advanced Features
- [ ] Multi-tenant architecture
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Custom model training

### Future Vision
- [ ] Voice interaction
- [ ] Predictive maintenance
- [ ] IoT device integration
- [ ] Enterprise marketplace

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/jeremylongshore/bobs-brain/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jeremylongshore/bobs-brain/discussions)
- **Documentation**: [Project Wiki](https://github.com/jeremylongshore/bobs-brain/wiki)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- **Google Cloud Platform** for enterprise infrastructure
- **Anthropic Claude** for development assistance
- **Open Source Community** for foundational libraries
- **Contributors** who make this project possible

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/jeremylongshore/bobs-brain?style=social)
![GitHub forks](https://img.shields.io/github/forks/jeremylongshore/bobs-brain?style=social)
![GitHub issues](https://img.shields.io/github/issues/jeremylongshore/bobs-brain)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jeremylongshore/bobs-brain)

---

<div align="center">
  <strong>Built with ❤️ by the Bob's Brain community</strong>
</div>