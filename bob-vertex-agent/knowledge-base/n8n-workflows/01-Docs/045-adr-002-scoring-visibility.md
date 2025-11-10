<!-- Created: 2025-09-12T21:55:00Z -->

# ADR-002: Story Selection Scoring Visibility Implementation

## Status
**Accepted** - 2025-09-12

## Context

The Daily Energizer N8N workflow uses an LLM to select the most inspiring story from filtered RSS content, but the selection process is opaque. The current Select Story node only outputs the winning story without revealing how each story was evaluated or why one story was chosen over another.

This creates several critical problems:

1. **Selection Transparency**: Cannot understand why one story (e.g., skating story) was chosen over another (e.g., 3D glue gun story)
2. **Quality Validation**: No way to verify that the LLM's scoring logic aligns with content quality goals
3. **Prompt Optimization**: Cannot make data-driven improvements to selection prompts or criteria
4. **Decision Auditing**: Missing visibility into the evaluation process for quality assurance

The client specifically requested visibility into how stories are scored on emotional impact, global relevance, and specificity to understand and optimize the selection process.

## Decision

Implement comprehensive scoring visibility by modifying the Select Story LLM prompt to evaluate and output detailed scores for ALL stories, not just the selected winner, including individual criterion scores and selection reasoning.

## Rationale

### Why This Solution?

This solution provides complete transparency into the story selection process while maintaining the existing anti-hallucination system integrity. By expanding the LLM output to include comprehensive scoring data, administrators can validate, debug, and optimize the selection logic with data-driven insights.

### Alternatives Considered

1. **Separate Scoring Pass After Selection**
   - Pros: Minimal changes to existing selection logic, isolated scoring process
   - Cons: Additional LLM calls increase cost and execution time, potential score inconsistency
   - User Impact: Delayed insights, potentially inconsistent scoring
   - Workflow Impact: Significant performance overhead, complex error handling
   - Decision: Rejected due to cost and performance implications

2. **Limited Scoring for Top Stories Only**
   - Pros: Reduced complexity, lower computational overhead, focused insights
   - Cons: Incomplete picture of selection process, may miss edge cases in scoring
   - User Impact: Partial visibility into selection decisions
   - Workflow Impact: Moderate changes, limited debugging capability
   - Decision: Rejected due to incomplete transparency and limited optimization value

3. **Comprehensive Scoring for All Stories**
   - Pros: Complete transparency, excellent debugging, full optimization capability, audit trail
   - Cons: Larger LLM output, slightly increased processing time
   - User Impact: Complete visibility and control over selection process
   - Workflow Impact: Enhanced prompt complexity, manageable performance impact
   - Decision: Selected for superior transparency and optimization benefits

## Consequences

### User Experience Impact
- **Complete Transparency**: Users can see exactly how each story was evaluated and scored
- **Quality Validation**: Administrators can verify selection logic aligns with content goals
- **Optimization Capability**: Data-driven improvements to prompts and selection criteria

### Workflow Performance Impact
- **Moderate Overhead**: Enhanced LLM prompt processing adds 15-30 seconds to execution
- **Enhanced Debugging**: Scoring data enables rapid identification of selection issues
- **Improved Quality**: Better understanding leads to optimized selection outcomes

### Integration Impact
- **Select Story LLM Node**: Significantly enhanced prompt and expanded JSON output schema
- **Google Sheets Output**: Additional columns for comprehensive scoring display
- **Data Storage**: Increased data volume for complete scoring information

### Maintenance Impact
- **Simplified Optimization**: Scoring data enables targeted prompt improvements
- **Quality Monitoring**: Ongoing evaluation of selection effectiveness and consistency
- **Future Enhancement**: Framework for refining scoring criteria and weights

## Implementation Notes

### N8N Workflow Requirements
- Modify Select Story LLM prompt to request comprehensive scoring for all stories
- Update Structured Output Parser schema to handle expanded scoring data structure
- Ensure JSON output includes selected story plus complete scoring breakdown for all stories

### Workflow Changes
- **Select Story Node**: Enhanced prompt with detailed scoring requirements and expanded output format
- **Structured Output Parser**: Updated schema for nested scoring data structure
- **Google Sheets Integration**: Additional columns for scoring visibility and analysis
- **Data Flow**: Preserve all existing anti-hallucination measures while adding scoring transparency

### Dependencies
- OpenRouter LLM service capacity for enhanced prompt processing
- N8N JSON processing capability for complex nested data structures
- Google Sheets API capacity for additional scoring data columns

### Migration Strategy
1. **Phase 1**: Develop and test enhanced LLM prompt with comprehensive scoring requirements
2. **Phase 2**: Update Structured Output Parser schema for expanded data structure
3. **Phase 3**: Enhance Google Sheets integration with scoring visualization columns
4. **Phase 4**: Validate scoring accuracy and consistency through complete workflow testing

## Success Metrics

### Workflow Performance Metrics
- Execution Success Rate: Maintain 99%+ with enhanced scoring implementation
- Processing Time: Allow for 15-30 second increase due to comprehensive scoring
- Resource Usage: Monitor memory usage for expanded JSON output processing

### User Experience Metrics
- Scoring Completeness: 100% of evaluated stories receive complete scoring breakdown
- Selection Validation: 100% verification that highest-scored story is selected
- Administrator Insight: 50%+ improvement in understanding of selection decisions

### System Integration Metrics
- Data Flow Accuracy: 100% accurate scoring data flow to Google Sheets
- JSON Processing Success: 100% successful parsing of complex scoring structure
- Error Rate: Zero scoring data corruption during workflow execution

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|---------|-------------|------------|
| LLM prompt complexity causing failures | High | Medium | Extensive prompt testing, fallback handling |
| JSON schema validation errors | Medium | Medium | Thorough schema design, comprehensive validation |
| Performance degradation | Medium | High | Optimize prompt efficiency, monitor execution time |
| Scoring inconsistency across runs | High | Low | Clear scoring criteria, prompt validation |

### N8N-Specific Risks
- **LLM Node Timeout**: Risk of enhanced prompts exceeding processing limits
- **JSON Processing Limits**: Risk of complex data structures causing parsing failures
- **Memory Usage**: Risk of expanded data causing workflow memory issues

## User Privacy & Security Considerations

### Data Privacy
- Scoring data contains no private user information
- Story evaluation based on public RSS content only
- Administrative access controls for scoring insights

### Security Implications
- Enhanced audit trail for content selection decisions
- Improved ability to detect and prevent inappropriate content selection
- Better content quality assurance through transparent evaluation process

### Compliance Requirements
- Complete audit trail for story selection decisions
- Enhanced accountability for content curation process
- Improved compliance with content quality standards

## N8N Implementation Details

### Required N8N Nodes
- Select Story LLM chain node (significantly enhanced prompt and output schema)
- Structured Output Parser (expanded schema for nested scoring data)
- Google Sheets append/update nodes (additional scoring columns)

### Enhanced Prompt Structure
```
SELECTION PROCESS WITH COMPREHENSIVE SCORING:
1. Evaluate each story on:
   - Emotional Impact (1-5): How uplifting and inspiring?
   - Global Relevance (1-5): Universal appeal across cultures?
   - Specificity (1-5): Concrete details, names, places?
2. Calculate total score for each story
3. Select highest-scored story
4. Output both selected story AND all scoring details

OUTPUT FORMAT:
{
  "selected_story": {
    "title": "winning story title",
    "summary": "winning story summary",
    [... other required fields]
  },
  "scoring_breakdown": [
    {
      "story_number": 1,
      "title": "story title",
      "source": "RSS feed name",
      "emotional_impact": 4,
      "global_relevance": 5,
      "specificity": 3,
      "total_score": 12
    },
    [... all other stories with complete scoring]
  ],
  "selection_reason": "Clear explanation of selection decision"
}
```

### Workflow Configuration
- Enhanced Select Story prompt with comprehensive scoring requirements
- Updated Structured Output Parser with nested JSON schema
- Google Sheets column configuration for scoring data display

### Testing Strategy
- Prompt testing with various story sets to ensure consistent scoring
- JSON schema validation for complex nested data structures
- End-to-end testing of scoring data flow from LLM to Google Sheets
- Performance testing to manage acceptable execution time increase

## Monitoring & Alerting

### Workflow Monitoring
- Scoring Completeness: Monitor for missing scores in any evaluated story
- Selection Accuracy: Verify highest-scored story is consistently selected
- JSON Processing: Alert on parsing failures for complex scoring data

### User Experience Monitoring
- Scoring Display: Monitor Google Sheets scoring columns for data accuracy
- Administrator Usage: Track usage of scoring insights for optimization
- Quality Metrics: Monitor improvements in selection quality based on scoring visibility

## Related Decisions

- PRD: Story Selection Scoring Visibility for Daily Energizer
- ADR-001: RSS Feed Source Tracking Implementation (companion decision)
- BRENT-ACTION-PLAN.md: Original client requirements for scoring visibility

## References

- [N8N LangChain Nodes Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [Daily Energizer Workflow Architecture](../CLAUDE.md)

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-09-12 | Claude | Initial version for story selection scoring visibility decision |

---

<!-- Last Updated: 2025-09-12T21:55:00Z -->