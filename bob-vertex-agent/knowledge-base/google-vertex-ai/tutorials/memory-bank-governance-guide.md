# Memory Bank Governance Guide

**Source:** Google Cloud Platform - Vertex AI Memory Bank
**Topic:** Advanced governance features for Memory Bank
**Tutorial:** Get Started with Memory Bank Governance

## Overview

This guide demonstrates how to build customer support systems using Vertex AI Memory Bank's governance features, including data retention policies, audit trails, and regulatory compliance.

## Key Governance Features

### 1. Granular TTL (Time-To-Live)

Configure different retention periods for different types of data:

| Configuration | Duration | Use Case |
|--------------|----------|----------|
| `create_ttl` | 30 days (2592000s) | Manually created operational data |
| `generate_created_ttl` | 90 days (7776000s) | Newly extracted support memories |
| `generate_updated_ttl` | 365 days (31536000s) | Consolidated, validated account data |

**Implementation:**
```python
ttl_config = TtlConfig(
    granular_ttl_config=GranularTtlConfig(
        create_ttl="2592000s",           # 30 days
        generate_created_ttl="7776000s",  # 90 days
        generate_updated_ttl="31536000s", # 365 days
    )
)
```

### 2. Topic-Based Filtering

Memory Bank automatically categorizes memories using default managed topics:

| Topic | Description | Example |
|-------|-------------|---------|
| `USER_PERSONAL_INFO` | Personal details | "Customer name is Alex Chen" |
| `USER_PREFERENCES` | Preferences | "Prefers email communication" |
| `KEY_CONVERSATION_DETAILS` | Important outcomes | "Ticket #SUP-2024-0847 created" |
| `EXPLICIT_INSTRUCTIONS` | Direct requests | "Remember account number" |

**Filtering by topic:**
```python
def get_memories_by_topic(engine_name, topic_enum_value):
    all_memories = client.agent_engines.memories.list(name=engine_name)
    filtered = []

    for memory in all_memories:
        full_memory = client.agent_engines.memories.get(name=memory.name)
        for topic in full_memory.topics:
            if topic_enum_value in str(topic.managed_memory_topic):
                filtered.append(full_memory)
                break

    return filtered

# Example: Get all personal information
personal_info = get_memories_by_topic(
    agent_engine_name,
    "USER_PERSONAL_INFO"
)
```

### 3. Memory Revisions & Audit Trails

Every memory change creates an immutable revision snapshot:

**Revision Actions:**
- **CREATED**: First time memory was generated
- **UPDATED**: Memory was modified
- **DELETED**: Memory was removed

**List revision history:**
```python
revisions = client.agent_engines.memories.revisions.list(
    name=memory_name
)

for revision in revisions:
    print(f"Revision: {revision.name}")
    print(f"Fact: {revision.fact}")
    print(f"Created: {revision.create_time}")
    print(f"Labels: {revision.labels}")
```

**Retrieve specific revision (time-travel query):**
```python
specific_revision = client.agent_engines.memories.revisions.get(
    name=revision_name
)
```

### 4. Memory Rollback

Revert a memory to a previous state for compliance or error correction:

```python
# Rollback to previous revision
rollback_operation = client.agent_engines.memories.rollback(
    name=memory_name,
    target_revision_id=previous_revision_id
)

# Verify rollback
restored_memory = client.agent_engines.memories.get(name=memory_name)
print(f"Restored fact: {restored_memory.fact}")
```

### 5. Revision Labels

Track metadata about when and how memories were created:

```python
# Create memory with revision labels
operation = client.agent_engines.memories.generate(
    name=agent_engine_name,
    scope={"user_id": customer_id},
    direct_contents_source={...},
    config={
        "wait_for_completion": True,
        "revision_labels": {
            "data_source": "initial_preference",
            "verified": "true",
            "data_category": "personal_info"
        }
    }
)

# Filter revisions by labels
verified_revisions = client.agent_engines.memories.revisions.list(
    name=memory_name,
    config={"filter": 'labels.verified="true"'}
)
```

## Complete Workflow Example

### 1. Create Agent Engine with Governance

```python
# Configure Memory Bank with TTL governance
governance_config = MemoryBankConfig(
    similarity_search_config=SimilaritySearchConfig(
        embedding_model="text-embedding-005"
    ),
    generation_config=GenerationConfig(
        model="gemini-2.5-flash"
    ),
    ttl_config=TtlConfig(
        granular_ttl_config=GranularTtlConfig(
            create_ttl="2592000s",           # 30 days
            generate_created_ttl="7776000s",  # 90 days
            generate_updated_ttl="31536000s"  # 365 days
        )
    )
)

# Create Agent Engine
agent_engine = client.agent_engines.create(
    config={"context_spec": {"memory_bank_config": governance_config}}
)
```

### 2. Generate Memories from Conversation

```python
# Create session
session = client.agent_engines.sessions.create(
    name=agent_engine_name,
    user_id=customer_id
)

# Add conversation events
for turn in conversation:
    client.agent_engines.sessions.events.append(
        name=session.response.name,
        author=customer_id,
        config={
            "content": {
                "role": turn["role"],
                "parts": [{"text": turn["message"]}]
            }
        }
    )

# Generate memories from session
operation = client.agent_engines.memories.generate(
    name=agent_engine_name,
    vertex_session_source={"session": session.response.name},
    config={"wait_for_completion": True}
)
```

### 3. Query Memories with Governance

```python
# Retrieve memories by scope
results = client.agent_engines.memories.retrieve(
    name=agent_engine_name,
    scope={"user_id": customer_id}
)

# Filter by topic
personal_info = get_memories_by_topic(
    agent_engine_name,
    "USER_PERSONAL_INFO"
)

# Check TTL expiration
for memory in results:
    print(f"Memory: {memory.memory.fact}")
    print(f"Expires: {memory.memory.expire_time}")
```

### 4. Audit and Compliance Queries

```python
# Get complete revision history for compliance
def generate_audit_report(memory_name):
    revisions = client.agent_engines.memories.revisions.list(
        name=memory_name
    )

    report = []
    for revision in revisions:
        report.append({
            "revision_id": revision.name.split("/")[-1],
            "fact": revision.fact,
            "created": revision.create_time,
            "labels": revision.labels,
            "expire_time": revision.expire_time
        })

    return report

# Answer compliance question: "What did you have about me on March 20th?"
def get_data_at_timestamp(memory_name, target_timestamp):
    revisions = client.agent_engines.memories.revisions.list(
        name=memory_name
    )

    # Find revision active at target_timestamp
    for revision in reversed(list(revisions)):
        if revision.create_time <= target_timestamp:
            return revision

    return None
```

## Best Practices

### Data Retention Strategy

1. **Temporary operational data** - 30 days (manual creates)
   - Support tickets, temporary notes
   - Use `create_ttl`

2. **Support memories** - 90 days (new generations)
   - Customer service interactions
   - Use `generate_created_ttl`

3. **Account data** - 365 days (consolidated/updated)
   - Verified customer information
   - Use `generate_updated_ttl`

### Topic Organization

- Use default managed topics for standard categorization
- Filter by `USER_PERSONAL_INFO` for GDPR/privacy requests
- Filter by `USER_PREFERENCES` for preference management
- Filter by `KEY_CONVERSATION_DETAILS` for support history

### Revision Tracking

1. **Always use revision labels** when generating memories:
   ```python
   "revision_labels": {
       "data_source": "customer_portal",
       "verified": "true",
       "department": "customer_support",
       "timestamp": datetime.now().isoformat()
   }
   ```

2. **Implement audit logging** for all memory operations:
   - Log memory creation/update/delete
   - Track who made changes (user_id)
   - Record reason for change

3. **Regular compliance checks**:
   - Verify TTL expirations working correctly
   - Check revision history completeness
   - Validate data retention policies

### Rollback Procedures

Only rollback when:
- Incorrect consolidation occurred
- Data quality issues detected
- Compliance requires reverting to known-good state

**Never rollback:**
- To hide legitimate data changes
- Without proper authorization
- During active customer interactions

## Compliance Use Cases

### GDPR Right to Erasure

```python
# Delete all memories for a user
results = client.agent_engines.memories.retrieve(
    name=agent_engine_name,
    scope={"user_id": customer_id}
)

for result in results:
    client.agent_engines.memories.delete(
        name=result.memory.name
    )

# Verify deletion with revision history
# (revisions preserved for audit trail)
```

### GDPR Right to Access

```python
# Get all data about a user
all_memories = client.agent_engines.memories.retrieve(
    name=agent_engine_name,
    scope={"user_id": customer_id}
)

# Include revision history for complete picture
data_export = []
for memory in all_memories:
    revisions = client.agent_engines.memories.revisions.list(
        name=memory.memory.name
    )

    data_export.append({
        "current": memory.memory.fact,
        "created": memory.memory.create_time,
        "expires": memory.memory.expire_time,
        "history": [
            {
                "fact": rev.fact,
                "timestamp": rev.create_time
            }
            for rev in revisions
        ]
    })
```

### Data Retention Compliance

```python
# Verify TTL compliance
def check_ttl_compliance(agent_engine_name):
    all_memories = client.agent_engines.memories.list(
        name=agent_engine_name
    )

    issues = []
    for memory in all_memories:
        full_memory = client.agent_engines.memories.get(
            name=memory.name
        )

        # Check if expiration is set
        if not full_memory.expire_time:
            issues.append(f"Memory {memory.name} has no TTL")

        # Check if expiration is within policy
        # (your policy checks here)

    return issues
```

## Configuration Reference

### SDK Imports

```python
from vertexai import types

# Basic configuration
MemoryBankConfig = types.ReasoningEngineContextSpecMemoryBankConfig
SimilaritySearchConfig = types.ReasoningEngineContextSpecMemoryBankConfigSimilaritySearchConfig
GenerationConfig = types.ReasoningEngineContextSpecMemoryBankConfigGenerationConfig

# Governance configuration
TtlConfig = types.ReasoningEngineContextSpecMemoryBankConfigTtlConfig
GranularTtlConfig = types.ReasoningEngineContextSpecMemoryBankConfigTtlConfigGranularTtlConfig
CustomizationConfig = types.MemoryBankCustomizationConfig
MemoryTopic = types.MemoryBankCustomizationConfigMemoryTopic
```

### Environment Setup

```python
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"

client = vertexai.Client(
    project=PROJECT_ID,
    location=LOCATION
)
```

## Resources

- [Memory Bank Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank)
- [Agent Engine Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine)
- [Vertex AI SDK Documentation](https://cloud.google.com/python/docs/reference/aiplatform/latest)

---

**Last Updated:** 2025-11-10
**SDK Version:** google-cloud-aiplatform >= 1.123.0
**Status:** Production-ready governance features
