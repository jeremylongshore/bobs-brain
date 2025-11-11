# A2A Peer Registry

**Last Updated:** 2025-11-11
**Status:** File-backed (Phase 5), Migrating to Firestore (Phase 6)

---

## Overview

The A2A (Agent-to-Agent) Peer Registry maintains a list of known A2A-compatible agents that Bob's Brain can discover and communicate with. This enables multi-agent orchestration and task delegation.

## Current Implementation (File-Backed)

### Storage
- **Location:** `a2a/peers.json`
- **Format:** JSON array of AgentCard objects
- **Environment Variable:** `A2A_REGISTRY_PATH` (default: `a2a/peers.json`)

### API Endpoint
```bash
GET /a2a/peers
```

**Response:**
```json
{
  "peers": [
    {
      "name": "Engineering Agent",
      "version": "1.0.0",
      "description": "Handles code review and testing",
      "skills": ["code_review", "testing"],
      "endpoint": "https://eng-agent.example.com",
      "card_url": "https://eng-agent.example.com/card",
      "capabilities": {
        "streaming": true
      }
    }
  ],
  "count": 1
}
```

### AgentCard Schema

Each peer is represented as an AgentCard with the following fields:

```json
{
  "name": "string (required)",
  "version": "string (required)",
  "description": "string (optional)",
  "skills": ["array of skill IDs"],
  "endpoint": "string (required) - Base URL for agent",
  "card_url": "string (optional) - URL to fetch AgentCard",
  "capabilities": {
    "streaming": "boolean - Supports streaming responses",
    "async": "boolean - Supports async execution"
  }
}
```

---

## Usage

### Querying Peers

**Example: List all peers**
```bash
curl -s http://localhost:8080/a2a/peers | jq
```

**Example: Find peer by skill**
```python
import requests

response = requests.get("http://localhost:8080/a2a/peers")
peers = response.json()["peers"]

# Find agents with "testing" skill
testing_agents = [p for p in peers if "testing" in p.get("skills", [])]
```

### Adding Peers (Manual - File-based)

1. Edit `a2a/peers.json`
2. Add new AgentCard entry
3. Restart gateway (or wait for hot-reload if enabled)

**Example:**
```json
{
  "name": "Monitoring Agent",
  "version": "1.0.0",
  "description": "Handles observability and alerting",
  "skills": ["monitoring", "alerting", "dashboards"],
  "endpoint": "https://monitor-agent.example.com",
  "card_url": "https://monitor-agent.example.com/card",
  "capabilities": {
    "streaming": false,
    "async": true
  }
}
```

---

## Future: Firestore Migration (Phase 6)

### Planned Architecture

**Storage:** Firestore collection `a2a_peers`

**Document Structure:**
```javascript
{
  id: "engineering-agent",
  name: "Engineering Agent",
  version: "1.0.0",
  endpoint: "https://eng-agent.example.com",
  registered_at: Timestamp,
  last_seen: Timestamp,
  status: "active" | "inactive",
  ...
}
```

**Benefits:**
- Real-time peer discovery
- Automatic health checking
- Dynamic registration/deregistration
- Multi-region replication
- No gateway restarts required

### API Extensions (Phase 6)

```bash
# Register new peer (authenticated)
POST /a2a/peers
{
  "name": "...",
  "endpoint": "...",
  ...
}

# Update peer status
PATCH /a2a/peers/{peer_id}

# Remove peer
DELETE /a2a/peers/{peer_id}

# Get peer by ID
GET /a2a/peers/{peer_id}

# Health check all peers
POST /a2a/peers/health
```

---

## A2A Protocol Compliance

Bob's Brain implements the A2A protocol for agent-to-agent communication:

### Discovery Endpoints
- `GET /card` - AgentCard metadata
- `GET /.well-known/agent-card.json` - Well-known discovery URI
- `GET /a2a/peers` - Peer registry (extension)

### Communication Endpoints
- `POST /invoke` - Synchronous invocation
- `POST /invoke/stream` - Streaming invocation

### AgentCard Format
```json
{
  "name": "Bob's Brain",
  "description": "A2A gateway to Vertex AI Reasoning Engine",
  "version": "5.0.0",
  "capabilities": {
    "streaming": true
  },
  "skills": [
    {
      "id": "get_time",
      "name": "Get Current Time",
      "description": "Returns current UTC time"
    }
  ]
}
```

---

## Testing

### Unit Tests
See `tests/integration/test_a2a_registry.py`

**Run tests:**
```bash
pytest tests/integration/test_a2a_registry.py -v
```

### Manual Testing

**1. Start gateway:**
```bash
uvicorn gateway.main:app --port 8080
```

**2. Query peers:**
```bash
curl http://localhost:8080/a2a/peers | jq
```

**3. Verify trace headers:**
```bash
curl -v http://localhost:8080/a2a/peers 2>&1 | grep X-Trace-Id
```

---

## Security Considerations

### Current (File-based)
- Read-only registry (no dynamic registration)
- No authentication required for /a2a/peers endpoint
- Peers are manually vetted before adding to registry

### Future (Firestore)
- Authentication required for write operations
- Peer verification via certificate/token
- Rate limiting on registration endpoints
- Automatic peer health checking and removal

---

## Operations

### Monitoring
- `/a2a/peers` endpoint included in synthetic checks
- Registry load failures logged (but non-fatal)
- Empty registry returns 200 with `{"peers": [], "count": 0}`

### Maintenance
- Review and update peer list quarterly
- Remove inactive peers
- Update peer capabilities as needed
- Test peer endpoints for availability

---

## References

- **A2A Protocol Spec:** [Google ADK A2A Documentation](https://github.com/google/adk-python)
- **Implementation:** `gateway/a2a_registry.py`
- **API Endpoint:** `gateway/main.py` (GET /a2a/peers)
- **Sample Peers:** `a2a/peers.json`
- **Tests:** `tests/integration/test_a2a_registry.py`

---

**Next Steps (Phase 6):**
1. Implement Firestore-backed registry
2. Add dynamic peer registration API
3. Implement peer health checking
4. Add authentication/authorization for write operations
5. Build peer discovery UI dashboard
