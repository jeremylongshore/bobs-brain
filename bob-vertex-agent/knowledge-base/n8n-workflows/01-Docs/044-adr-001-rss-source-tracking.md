<!-- Created: 2025-09-12T21:50:00Z -->

# ADR-001: RSS Feed Source Tracking Implementation

## Status
**Accepted** - 2025-09-12

## Context

The Daily Energizer N8N workflow processes stories from 10 RSS feeds but lacks traceability to determine which feed each selected story originated from. This creates several critical problems:

1. **Hallucination Verification**: Impossible to verify that selected stories are real and came from legitimate RSS feeds
2. **Quality Control**: Cannot identify problematic feeds producing inappropriate content (e.g., cooking stories in news feeds)
3. **Feed Management**: No data-driven approach to evaluate and optimize RSS feed selection
4. **Audit Trail**: Missing essential information for content verification and workflow debugging

The client specifically encountered a "eggplant cooking" story and could not trace it back to its source feed, highlighting the urgent need for comprehensive source tracking throughout the workflow.

## Decision

Implement comprehensive RSS feed source tracking by adding a `source` field to every story object that is preserved throughout the entire 70-node workflow, from initial RSS collection through final article generation.

## Rationale

### Why This Solution?

This solution provides complete end-to-end traceability while maintaining the existing anti-hallucination system integrity. By adding source attribution at the earliest point (RSS Set Fields nodes) and preserving it through all transformations, we ensure every selected story can be verified against its original feed.

### Alternatives Considered

1. **Post-Processing Source Lookup**
   - Pros: Minimal workflow changes, retroactive source identification
   - Cons: Unreliable matching, potential for false positives, complex correlation logic
   - User Impact: Delayed source identification, potential accuracy issues
   - Workflow Impact: Additional complexity, performance overhead for lookups
   - Decision: Rejected due to reliability concerns and complexity

2. **Source Tracking in Final Nodes Only**
   - Pros: Minimal changes to core workflow, simple implementation
   - Cons: Cannot debug issues in intermediate steps, limited troubleshooting capability
   - User Impact: Limited visibility into workflow processing issues
   - Workflow Impact: Missing data for workflow optimization and debugging
   - Decision: Rejected due to insufficient debugging and quality control capabilities

3. **Comprehensive Source Tracking Throughout Workflow**
   - Pros: Complete traceability, excellent debugging, quality control, audit trail
   - Cons: Requires changes to multiple nodes, additional data storage
   - User Impact: Complete visibility and control over content sources
   - Workflow Impact: Minimal performance impact, enhanced debugging capabilities
   - Decision: Selected for superior traceability and quality control benefits

## Consequences

### User Experience Impact
- **Enhanced Trust**: Users can verify every story's authenticity through source attribution
- **Quality Control**: Administrators can identify and remove problematic feeds immediately
- **Transparency**: Complete visibility into content sourcing and selection decisions

### Workflow Performance Impact
- **Minimal Overhead**: Adding string source field has negligible impact on processing time
- **Enhanced Debugging**: Source information enables rapid identification of workflow issues
- **Improved Reliability**: Better error tracking and problem resolution capabilities

### Integration Impact
- **RSS Feed Processing**: All 10 Set RSS Fields nodes require source field addition
- **Google Sheets Output**: Additional column for source information display
- **LLM Processing**: Enhanced prompts to handle and preserve source data

### Maintenance Impact
- **Simplified Debugging**: Source tracking enables rapid issue identification and resolution
- **Quality Monitoring**: Ongoing feed performance evaluation and optimization
- **Future Expansion**: Framework for adding additional RSS feeds with proper tracking

## Implementation Notes

### N8N Workflow Requirements
- Modify all 10 Set RSS Fields nodes to include source assignment
- Ensure source field preservation through all filtering and processing nodes
- Update Select Story LLM prompt to include and output source information

### Workflow Changes
- **RSS Set Fields Nodes**: Add `source: "Feed Name"` assignment to each node
- **Combine Stories Node**: Verify source field preservation in story aggregation
- **Select Story Node**: Include source in JSON output schema and LLM prompt
- **Google Sheets Integration**: Add source column to article tracking spreadsheet

### Dependencies
- N8N version compatibility with Set RSS Fields node enhancements
- Google Sheets API capacity for additional column data
- LLM service capability to handle enhanced prompts with source information

### Migration Strategy
1. **Phase 1**: Add source fields to all RSS Set Fields nodes
2. **Phase 2**: Update LLM prompts and JSON schema for source handling
3. **Phase 3**: Enhance Google Sheets integration with source display
4. **Phase 4**: Validate source tracking through complete workflow execution

## Success Metrics

### Workflow Performance Metrics
- Execution Success Rate: Maintain 99%+ with source tracking implementation
- Processing Time: No increase beyond 30 seconds to current execution time
- Resource Usage: Minimal memory increase for source string storage

### User Experience Metrics
- Source Tracking Accuracy: 100% of selected stories include verified source attribution
- Administrator Efficiency: 50%+ reduction in time to identify problematic feeds
- Quality Control Improvement: Measurable decrease in inappropriate content selection

### System Integration Metrics
- Integration Success Rate: 100% successful source data flow to Google Sheets
- Data Flow Accuracy: 100% source-to-story mapping accuracy throughout workflow
- Error Rate: Zero source data loss during workflow execution

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|---------|-------------|------------|
| Source data loss during processing | High | Low | Comprehensive testing, validation checks at each node |
| LLM prompt complexity | Medium | Medium | Careful prompt design, extensive testing with source data |
| JSON schema validation errors | Medium | Low | Thorough schema testing, backward compatibility validation |
| Performance degradation | Low | Low | Lightweight string field, performance monitoring |

### N8N-Specific Risks
- **Node Compatibility**: Risk of Set RSS Fields node limitations
- **Workflow Scalability**: Risk of source tracking affecting workflow performance
- **Integration Reliability**: Risk of source data corruption during processing

## User Privacy & Security Considerations

### Data Privacy
- RSS feed sources are public information, no privacy concerns
- Source attribution enhances transparency and accountability
- No personal or sensitive data involved in source tracking

### Security Implications
- Source tracking provides audit trail for content verification
- Enhanced ability to identify and block malicious or inappropriate feeds
- Improved content integrity and authenticity verification

### Compliance Requirements
- Proper attribution to original RSS feed sources
- Enhanced audit trail for content compliance verification
- Improved ability to meet content sourcing requirements

## N8N Implementation Details

### Required N8N Nodes
- 10 existing Set RSS Fields nodes (enhanced with source assignment)
- Existing Combine Stories function node (validated for source preservation)
- Select Story LLM chain node (enhanced prompt and output schema)
- Google Sheets append/update nodes (additional source column)

### Workflow Configuration
- Source field assignments in each RSS Set Fields node
- JSON schema updates in Structured Output Parser
- Google Sheets column configuration for source display

### Testing Strategy
- Unit testing of source field assignment in each RSS node
- Integration testing of source preservation through filtering nodes
- End-to-end testing of source tracking from RSS to final output
- Performance testing to ensure minimal impact on execution time

## Monitoring & Alerting

### Workflow Monitoring
- Source Field Validation: Monitor for missing or corrupted source data
- Processing Integrity: Alert on source data loss during workflow execution
- Selection Accuracy: Verify source attribution in final story selection

### User Experience Monitoring
- Source Display: Monitor Google Sheets source column for data accuracy
- Administrator Usage: Track source-based feed management decisions
- Quality Metrics: Monitor content quality improvements from source tracking

## Related Decisions

- PRD: RSS Feed Source Tracking for Daily Energizer
- BRENT-ACTION-PLAN.md: Original client requirements for source tracking
- CLAUDE.md: Workflow architecture and anti-hallucination system guidelines

## References

- [N8N Set Node Documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.set/)
- [Daily Energizer Workflow Implementation Guide](../IMPLEMENTATION-GUIDE.md)
- [Client Requirements Analysis](../BRENT-ACTION-PLAN.md)

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-09-12 | Claude | Initial version for RSS feed source tracking decision |

---

<!-- Last Updated: 2025-09-12T21:50:00Z -->