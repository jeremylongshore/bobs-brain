# 6767-096-DR-STND-repo-registry-and-target-selection.md

**Date Created:** 2025-11-20
**Category:** DR - Documentation & Reference
**Type:** STND - Standard
**Status:** ACTIVE ✅

---

## Executive Summary

Defines the **Repository Target Registry** - a centralized configuration system that allows Bob, the foreman, and the SWE pipeline to reference real GitHub repositories by logical IDs rather than hardcoded URLs.

---

## Purpose

The repo registry provides:
- **Centralized Configuration:** Single source of truth for target repositories
- **Logical Naming:** Use `repo_id` like "bobs-brain" instead of full GitHub URLs
- **Metadata Management:** Store tags, descriptions, branch defaults
- **Safety Controls:** Explicit write permission flags
- **Easy Expansion:** Add new repos with YAML entries

---

## Registry Location

**Config File:** `config/repos.yaml`
**Helper Module:** `agents/config/repos.py`

---

## Registry Format

### YAML Structure

```yaml
repos:
  - id: bobs-brain
    description: "Primary Bob/IAM department repo"
    github_owner: "jeremylongshore"
    github_repo: "bobs-brain"
    default_branch: "main"
    tags:
      - "adk"
      - "agents"
      - "core"
    allow_write: false

  - id: bobs-brain-sandbox
    description: "Sandbox test repo"
    github_owner: "jeremylongshore"
    github_repo: "bobs-brain-sandbox"
    default_branch: "main"
    tags:
      - "sandbox"
    allow_write: false

settings:
  default_allow_write: false
  require_explicit_write_permission: true
  github_api_rate_limit: 100
  analysis_file_patterns:
    - "*.py"
    - "*.yaml"
    - "*.md"
  max_file_size_bytes: 1048576  # 1MB
  max_total_size_bytes: 10485760  # 10MB
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique identifier (kebab-case) |
| `description` | str | Human-readable description |
| `github_owner` | str | GitHub username or org |
| `github_repo` | str | Repository name |
| `default_branch` | str | Default branch (usually "main") |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | list[str] | Category tags for filtering |
| `allow_write` | bool | Enable write operations (default: false) |

---

## Python API

### RepoConfig Dataclass

```python
@dataclass
class RepoConfig:
    id: str
    description: str
    github_owner: str
    github_repo: str
    default_branch: str
    tags: List[str]
    allow_write: bool

    @property
    def full_name(self) -> str:
        """Returns owner/repo format"""
        return f"{self.github_owner}/{self.github_repo}"

    @property
    def github_url(self) -> str:
        """Returns https://github.com/owner/repo"""
        return f"https://github.com/{self.full_name}"

    @property
    def api_url(self) -> str:
        """Returns API base URL"""
        return f"https://api.github.com/repos/{self.full_name}"
```

### Registry Functions

```python
from agents.config.repos import get_repo_by_id, list_repos

# Get specific repo
repo = get_repo_by_id("bobs-brain")
if repo:
    print(repo.full_name)  # jeremylongshore/bobs-brain
    print(repo.github_url)
    print(repo.default_branch)

# List all repos
all_repos = list_repos()

# Filter by tag
adk_repos = list_repos(tag="adk")
```

---

## Pipeline Integration

### PipelineRequest Updates

```python
@dataclass
class PipelineRequest:
    repo_hint: str  # Local path or fallback
    task_description: str
    env: Literal["dev", "staging", "prod"]

    # GitHub integration (Phase GH1+)
    repo_id: Optional[str] = None
    github_owner: Optional[str] = None
    github_repo: Optional[str] = None
    github_ref: Optional[str] = None
```

### Usage in Pipeline

```python
# Option 1: Use repo_id (recommended)
request = PipelineRequest(
    repo_hint="bobs-brain",  # Fallback
    repo_id="bobs-brain",    # Registry lookup
    task_description="Audit ADK compliance",
    env="dev"
)

# Option 2: Explicit GitHub details
request = PipelineRequest(
    repo_hint=".",
    github_owner="jeremylongshore",
    github_repo="bobs-brain",
    github_ref="feature/new-agent",
    task_description="Test new agent",
    env="dev"
)

# Run pipeline
result = run_swe_pipeline(request)
```

### Automatic Resolution

The pipeline automatically resolves `repo_id` to GitHub details:

```python
def run_swe_pipeline(request: PipelineRequest) -> PipelineResult:
    # Phase GH1: Resolve repo_id if provided
    if request.repo_id and not request.github_owner:
        repo_config = get_repo_by_id(request.repo_id)
        if repo_config:
            request.github_owner = repo_config.github_owner
            request.github_repo = repo_config.github_repo
            request.github_ref = request.github_ref or repo_config.default_branch
            # ... continue pipeline
```

---

## Adding New Repositories

### Step 1: Update config/repos.yaml

```yaml
repos:
  - id: my-new-repo
    description: "My awesome project"
    github_owner: "myorg"
    github_repo: "my-repo"
    default_branch: "main"
    tags:
      - "python"
      - "api"
    allow_write: false
```

### Step 2: Test the Addition

```bash
# Verify registry loads
python3 agents/config/repos.py

# Test repo lookup
python3 -c "from agents.config.repos import get_repo_by_id; \
            repo = get_repo_by_id('my-new-repo'); \
            print(repo.full_name if repo else 'Not found')"
```

### Step 3: Use in Pipeline

```bash
python3 scripts/run_swe_pipeline_once.py \
  --repo-id my-new-repo \
  --task "Initial audit"
```

---

## Safety Features

### Read-Only by Default

All repos have `allow_write: false` by default. This prevents:
- Accidental issue creation
- Unwanted PR generation
- Direct pushes to branches

### Explicit Write Permission

To enable write operations (future):
1. Set `allow_write: true` in config
2. Ensure `GITHUB_TOKEN` has appropriate scopes
3. Add additional safeguards in code

### Validation

The registry validates:
- All required fields present
- IDs are unique
- File patterns are valid globs

---

## Configuration Settings

### File Analysis Settings

```yaml
settings:
  analysis_file_patterns:
    - "*.py"      # Python files
    - "*.yaml"    # Config files
    - "*.md"      # Documentation
    - "*.json"
    - "*.toml"

  analysis_exclude_patterns:
    - "*.pyc"
    - "__pycache__/*"
    - ".git/*"
    - "node_modules/*"
    - "venv/*"
```

### Size Limits

```yaml
settings:
  max_file_size_bytes: 1048576    # 1MB per file
  max_total_size_bytes: 10485760  # 10MB total per analysis
```

These limits prevent:
- Excessive API usage
- Memory exhaustion
- Slow analysis times

---

## Error Handling

### Repo Not Found

```python
repo = get_repo_by_id("nonexistent")
# Returns None (not an exception)

if not repo:
    print("⚠️ Repo not found in registry")
```

### Invalid Registry File

```python
try:
    registry = RepoRegistry()
except FileNotFoundError:
    print("❌ Registry file missing at config/repos.yaml")
except yaml.YAMLError as e:
    print(f"❌ Invalid YAML: {e}")
```

---

## Future Enhancements

### Phase GH2+ (Planned)
- **GitHub API Integration:** Fetch actual repo contents
- **Branch Discovery:** List available branches dynamically
- **Access Validation:** Check token permissions before operations

### Advanced Features (Future)
- **Team Permissions:** Map registry repos to team access levels
- **Multi-Org Support:** Support repos across multiple organizations
- **Private Repos:** Enhanced authentication for private repositories
- **Webhook Configuration:** Auto-update registry from GitHub events

---

## Examples

### List All ADK Repos

```python
from agents.config.repos import list_repos

adk_repos = list_repos(tag="adk")
for repo in adk_repos:
    print(f"- {repo.id}: {repo.full_name}")
```

### Check Write Permission

```python
from agents.config.repos import get_repo_by_id

repo = get_repo_by_id("bobs-brain")
if repo and not repo.allow_write:
    print("⚠️ Repo is read-only - no write operations allowed")
```

### Get All Tags

```python
from agents.config.repos import get_registry

registry = get_registry()
tags = registry.get_all_tags()
print(f"Available tags: {', '.join(tags)}")
```

---

## Testing

### Unit Tests

```bash
# Test registry loading
python3 -m pytest tests/test_repo_registry.py

# Test with specific repo
python3 -m pytest tests/test_repo_registry.py::test_get_bobs_brain
```

### Integration Tests

```bash
# Test pipeline with repo_id
python3 scripts/run_swe_pipeline_once.py \
  --repo-id bobs-brain \
  --task "Test registry integration" \
  --dry-run
```

---

## Related Documentation

- **Phase GH2:** `6767-097-AT-ARCH-github-integration-and-repo-ingest.md` (next)
- **Pipeline Architecture:** `6767-094-AT-ARCH-iam-swe-pipeline-orchestration.md`
- **Shared Contracts:** `agents/shared_contracts.py`

---

## Summary

The Repository Target Registry provides:
- ✅ Centralized repo configuration
- ✅ Logical naming via `repo_id`
- ✅ Safe defaults (read-only)
- ✅ Easy expansion via YAML
- ✅ Pipeline integration
- ✅ Future-ready for GitHub API integration

This foundation enables the SWE pipeline to operate on real GitHub repos while maintaining safety and flexibility.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-20
**Status:** Active
**Owner:** iam-senior-adk-devops-lead

---