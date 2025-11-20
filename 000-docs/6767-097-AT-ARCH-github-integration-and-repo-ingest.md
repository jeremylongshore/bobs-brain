# 6767-097-AT-ARCH-github-integration-and-repo-ingest.md

**Date Created:** 2025-11-20
**Category:** AT - Architecture & Technical
**Type:** ARCH - Architecture Document
**Status:** ACTIVE ✅

---

## Executive Summary

Implements **read-only GitHub integration** for the SWE pipeline, enabling Bob, the foreman, and iam-* agents to analyze real GitHub repositories while maintaining safety through read-only access.

---

## Purpose

Phase GH2 provides:
- **GitHub API Client:** Minimal, safe client for fetching repo contents
- **Pipeline Integration:** Automatic repo fetching when `repo_id` is provided
- **Safety Guarantees:** Read-only by design, no write operations
- **Registry Integration:** Uses repo registry from Phase GH1

---

## Architecture

### Components

```
┌─────────────────┐
│  Repo Registry  │ ← Phase GH1: config/repos.yaml
└────────┬────────┘
         │ repo_id → RepoConfig
         ↓
┌─────────────────┐
│ GitHub Client   │ ← Phase GH2: Read-only API
└────────┬────────┘
         │ GET /repos/.../git/trees/...
         │ GET /repos/.../contents/...
         ↓
┌─────────────────┐
│   RepoTree      │ → List of RepoFile objects
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ SWE Pipeline    │ → iam-* agents analyze
└─────────────────┘
```

### GitHub Client Location

**Module:** `agents/tools/github_client.py`

**Key Classes:**
- `GitHubClient` - Main API client
- `RepoFile` - File metadata
- `RepoTree` - Repository tree structure

---

## GitHub Client API

### Initialization

```python
from agents.tools.github_client import get_client

# Option 1: Use GITHUB_TOKEN from environment
client = get_client()

# Option 2: Explicit token
client = get_client(token="ghp_...")

# Option 3: No token (unauthenticated, rate-limited)
client = GitHubClient(token=None)
```

### List Repository Files

```python
files = client.list_repo_files(
    owner="jeremylongshore",
    repo="bobs-brain",
    ref="main",
    recursive=True,
    file_patterns=["*.py", "*.md"],
    exclude_patterns=["*.pyc", "__pycache__/*"],
    max_size_bytes=1048576  # 1MB per file
)

for file in files:
    print(f"{file.path} ({file.size} bytes)")
```

### Get File Content

```python
content = client.get_file_content(
    owner="jeremylongshore",
    repo="bobs-brain",
    path="README.md",
    ref="main"
)

print(content)
```

### Get Complete Repo Tree

```python
tree = client.get_repo_tree(
    owner="jeremylongshore",
    repo="bobs-brain",
    ref="main",
    file_patterns=["*.py", "*.yaml", "*.md"],
    exclude_patterns=["*__pycache__*"],
    max_file_size=1048576,      # 1MB per file
    max_total_size=10485760,    # 10MB total
    fetch_content=False         # Only metadata
)

print(f"Found {len(tree.files)} files")
print(f"Total size: {tree.total_size / 1024:.1f}KB")
```

---

## Pipeline Integration

### Automatic GitHub Fetching

The pipeline automatically fetches from GitHub when:
1. `repo_id` is provided and resolves to a GitHub repo
2. OR `github_owner`/`github_repo` are explicitly set

```python
from agents.iam_senior_adk_devops_lead.orchestrator import run_swe_pipeline
from agents.shared_contracts import PipelineRequest

# Use repo_id (recommended)
request = PipelineRequest(
    repo_hint="bobs-brain",
    repo_id="bobs-brain",  # Resolves to GitHub
    task_description="Audit ADK compliance",
    env="dev"
)

result = run_swe_pipeline(request)
```

### Pipeline Flow with GitHub

```
1. Resolve repo_id → GitHub owner/repo/ref
2. Initialize GitHub client
3. Fetch repo tree (filtered by registry settings)
4. Store file list in request.metadata
5. Pass to iam-adk for analysis
6. Continue with normal pipeline flow
```

### Example Output

```
✓ Resolved repo_id 'bobs-brain' to jeremylongshore/bobs-brain

🐙 Fetching repository from GitHub...
✓ Fetched 197 files (5834.6KB total)

📊 STEP 1: ANALYSIS
[iam-adk] Analyzing repo: jeremylongshore/bobs-brain (197 files from GitHub)
...
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | No | Personal access token (higher rate limits) |

### Rate Limits

| Authentication | Requests/Hour |
|----------------|---------------|
| Unauthenticated | 60 |
| Authenticated | 5,000 |

### Registry Settings

From `config/repos.yaml`:

```yaml
settings:
  github_api_rate_limit: 100

  analysis_file_patterns:
    - "*.py"
    - "*.yaml"
    - "*.md"
    - "*.json"

  analysis_exclude_patterns:
    - "*.pyc"
    - "__pycache__/*"
    - ".git/*"
    - "node_modules/*"

  max_file_size_bytes: 1048576    # 1MB
  max_total_size_bytes: 10485760  # 10MB
```

---

## Safety Features

### Read-Only Operations

The GitHub client ONLY supports:
- ✅ GET requests (list files, get content)
- ❌ POST/PUT/PATCH/DELETE (blocked by design)

### No Writes

The client **cannot**:
- Create issues
- Create PRs
- Push code
- Modify branches
- Change settings

### Error Handling

```python
from agents.tools.github_client import (
    GitHubAuthError,
    GitHubRateLimitError,
    GitHubClientError
)

try:
    files = client.list_repo_files(...)
except GitHubAuthError:
    print("⚠️ Authentication failed - check GITHUB_TOKEN")
except GitHubRateLimitError as e:
    print(f"⚠️ Rate limit exceeded: {e}")
except GitHubClientError as e:
    print(f"⚠️ GitHub API error: {e}")
```

---

## Testing

### Unit Tests (Mocked)

```bash
# Run all tests (no token needed)
python3 -m pytest tests/test_github_client.py -v

# Results: 12 passed, 3 skipped
```

### Live Tests (Optional)

```bash
# Requires GITHUB_TOKEN and RUN_LIVE_TESTS=1
export GITHUB_TOKEN="ghp_..."
export RUN_LIVE_TESTS=1

python3 -m pytest tests/test_github_client.py -v
```

### Make Targets

```bash
# Test GitHub client
make test-github-client

# Test pipeline with GitHub
python3 scripts/run_swe_pipeline_once.py \
  --repo-id bobs-brain \
  --task "Test GitHub integration"
```

---

## Performance

### Metrics

| Operation | Time | API Calls |
|-----------|------|-----------|
| List files | ~500ms | 1 |
| Get file content | ~300ms | 1 per file |
| Get tree (197 files) | ~800ms | 1 (no content) |
| Get tree (with content) | ~60s | 1 + N |

### Optimization

**Fetch metadata only (fast):**
```python
tree = client.get_repo_tree(
    fetch_content=False  # ✅ Fast: 1 API call
)
```

**Fetch with content (slow):**
```python
tree = client.get_repo_tree(
    fetch_content=True  # ⚠️ Slow: 1 + N API calls
)
```

---

## Future Enhancements (Phase GH3+)

### Phase GH3 (Next)
- **Issue Creation:** Draft GitHub issues from IssueSpec
- **Preview Mode:** Show what would be created without creating

### Later Phases
- **Write Operations:** Enable with safety controls
- **PR Creation:** Automated fix PRs
- **Branch Management:** Create feature branches
- **Webhooks:** Real-time updates from GitHub

---

## Troubleshooting

### "No GITHUB_TOKEN provided"

**Solution:** Set environment variable
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### "Rate limit exceeded"

**Cause:** Unauthenticated requests limited to 60/hour

**Solutions:**
1. Add GITHUB_TOKEN (increases to 5000/hour)
2. Wait for rate limit reset
3. Use caching for repeated analysis

### "Authentication failed"

**Causes:**
- Invalid token
- Expired token
- Insufficient scopes

**Solution:** Generate new token at https://github.com/settings/tokens
- Required scope: `repo` (or `public_repo` for public only)

---

## Related Documentation

- **Phase GH1:** `6767-096-DR-STND-repo-registry-and-target-selection.md`
- **Phase GH3:** `6767-098-AT-ARCH-iam-issue-github-draft-flow.md` (next)
- **Pipeline Architecture:** `6767-094-AT-ARCH-iam-swe-pipeline-orchestration.md`

---

## Summary

Phase GH2 provides:
- ✅ Read-only GitHub API client
- ✅ Automatic repo fetching in pipeline
- ✅ Registry-driven file filtering
- ✅ Comprehensive error handling
- ✅ Safe by design (no writes)
- ✅ Tested with mocked and live tests

The SWE pipeline can now analyze real GitHub repositories while maintaining safety through read-only access.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-20
**Status:** Active
**Owner:** iam-senior-adk-devops-lead

---