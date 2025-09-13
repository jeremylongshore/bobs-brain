# ADR-001: Multi-Branch Progressive Enhancement Architecture

**Date**: 2025-09-13
**Status**: Accepted

## Context

Bob's Brain started as a simple Slack bot template but evolved into a complex AI system with multiple integration points. Different users have vastly different needs - from beginners wanting a simple bot to enterprises needing production-scale systems. Managing this complexity in a single codebase would create confusion and maintenance challenges.

## Decision

We will maintain four distinct branches, each representing a different level of complexity and capability:

1. **main**: Simple template for beginners
2. **enhance-bob-graphiti**: Knowledge graph integration
3. **feature/graphiti-production**: Enterprise production system
4. **feature/bob-ferrari-final**: Complete holistic AI system

Each branch builds upon the previous, allowing users to choose their entry point based on expertise and requirements.

## Consequences

### Positive
- Users can start at their comfort level
- Clean separation of concerns per branch
- Easier to understand and maintain each version
- Progressive learning path from simple to complex
- No unnecessary complexity for basic use cases

### Negative
- Multiple branches to maintain
- Potential for drift between versions
- Need clear documentation on branch purposes
- Cherry-picking fixes across branches required

## Alternatives Considered

### Option 1: Single Branch with Feature Flags
- **Pros**: One codebase, configurable features
- **Cons**: Complex configuration, harder for beginners
- **Reason for rejection**: Too complex for new developers

### Option 2: Separate Repositories
- **Pros**: Complete isolation
- **Cons**: Difficult to share common code
- **Reason for rejection**: Loses the evolution story

### Option 3: Monorepo with Packages
- **Pros**: Shared dependencies, clean separation
- **Cons**: Complex build system
- **Reason for rejection**: Over-engineered for current needs

## Implementation

```bash
# Branch structure
main                        # Simple template (v1)
├── enhance-bob-graphiti    # + Neo4j/Graphiti (v2)
├── feature/graphiti-production  # + 40 scrapers/BigQuery (v3)
└── feature/bob-ferrari-final    # + Full integration (v4)

# User selection
git checkout main           # Beginners
git checkout enhance-bob-graphiti  # Intermediate
git checkout feature/graphiti-production  # Production
git checkout feature/bob-ferrari-final    # Everything
```

## References

- PRD-001: Simple Template Requirements
- PRD-002: Graphiti Integration Requirements
- PRD-003: Production System Requirements
- PRD-004: Ferrari Edition Requirements