# Project Cleanup Plan - August 15, 2025

## Files to Move/Organize

### Test Files to Move to `/tests/`
- `test_graphiti_integration.py` (root) → `/tests/integration/`

### Agent Files in Root (Keep as Production)
- `clean_agent.py` - KEEP (current production local agent)
- `traced_agent_simple.py` - KEEP (production with tracing)

### Graphiti Files in `/src/` (Organize by Status)
**Production Ready:**
- `graphiti_production.py` - NEW production implementation with real Gemini
- `graphiti_error_tracking.py` - Production error handling

**Legacy/Reference (Move to archive):**
- `graphiti_integration.py` - Original attempt with fallbacks
- `graphiti_simple.py` - Simplified version without AI
- `graphiti_unified.py` - Intermediate attempt

## Cloud Run Services Status

### Essential Services (3) - KEEP RUNNING
1. **bobs-brain** - Main Bob assistant
2. **unified-scraper** - Data collection from 40+ sources
3. **circle-of-life-scraper** - MVP3 integration

### Non-Essential Services - CONSIDER REMOVAL
4. **startai-dashboard** - Separate project?
5. **startai-portfolio** - Separate project?
6. **website-form-integration** - Separate project?

## Proposed Actions

### 1. File Organization
```bash
# Create organized structure
mkdir -p tests/integration
mkdir -p archive/graphiti_attempts

# Move test files
mv test_graphiti_integration.py tests/integration/

# Archive old Graphiti attempts
mv src/graphiti_integration.py archive/graphiti_attempts/
mv src/graphiti_simple.py archive/graphiti_attempts/
mv src/graphiti_unified.py archive/graphiti_attempts/
```

### 2. Keep Production Files Clear
```
/src/
  graphiti_production.py     # PRODUCTION - Real Gemini implementation
  graphiti_error_tracking.py  # PRODUCTION - Error handling

/root/
  clean_agent.py             # PRODUCTION - Local Slack agent
  traced_agent_simple.py     # PRODUCTION - Agent with tracing
```

### 3. Documentation Updates Needed
- Update CLAUDE.md with final status
- Clear directory structure documentation
- GitHub commit with comprehensive notes

## Questions for Confirmation

1. **Should we archive the old Graphiti attempts?** (graphiti_integration.py, graphiti_simple.py, graphiti_unified.py)
   - They were learning steps but graphiti_production.py is the final version

2. **Should we keep the StartAI services running?**
   - They appear to be separate projects from Bob's Brain

3. **Is clean_agent.py the current production agent?**
   - If so, should remain in root for easy access

Please confirm before I proceed with cleanup.
