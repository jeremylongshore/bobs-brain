# bobs-brain

ADK agent with A2A identity and Vertex AI Memory Bank.

## Structure

```
.
├─ 000-docs/               # Documentation
├─ README.md               # This file
├─ requirements.txt        # Python dependencies
├─ main.py                 # FastAPI entry point
├─ Makefile                # dev, test, smoke
├─ .env.sample             # Environment template
├─ my_agent/               # Agent implementation
│  ├─ agent.py             # Runner + Memory Bank
│  ├─ a2a_manager.py       # AgentCard definition
│  ├─ tools.py             # Tool implementations
│  └─ prompts/system.md    # System prompt
├─ scripts/                # Automation scripts
│  ├─ run_local.sh         # Local development server
│  ├─ smoke_test.sh        # Health check validation
│  ├─ deploy_agent_engine.sh
│  └─ deploy_cloud_run.sh
├─ tests/                  # pytest suite
│  ├─ test_tools.py
│  └─ test_agent.py
├─ infra/terraform/        # Infrastructure as Code
│  ├─ envs/dev/            # Development environment
│  └─ modules/             # Reusable modules
│     ├─ project/          # API enablement
│     ├─ iam/              # Service accounts
│     ├─ artifact_registry/ # Docker registry
│     ├─ cloud_run/        # Cloud Run service
│     └─ agent_engine_bootstrap/ # Agent Engine deploy
└─ .github/workflows/      # CI/CD
   ├─ ci.yml               # pytest on push/PR
   └─ deploy.yml           # Deploy on tags
```

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.sample .env
# Edit .env with your PROJECT_ID, LOCATION, AGENT_ENGINE_ID

# 3. Run locally
make dev

# 4. Test endpoints
curl http://localhost:8080/_health
curl http://localhost:8080/

# 5. Run tests
make test

# 6. Smoke test
make smoke
```

## Terraform

```bash
cd infra/terraform/envs/dev
terraform init
terraform plan -var 'project_id=YOUR_PROJECT'
terraform apply -var 'project_id=YOUR_PROJECT'
```

## Endpoints

- `GET /_health` - Health check with X-Trace-Id header
- `GET /` - A2A AgentCard JSON
- `POST /invoke` - Execute agent (ADK routes)

## Documentation

See `000-docs/` for detailed documentation and after-action reports.
