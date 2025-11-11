<!-- Created: 2025-09-12T21:47:00Z -->

# PRD: Story Selection Scoring Visibility for Daily Energizer

## Executive Summary

This PRD covers the implementation of comprehensive scoring visibility for the Daily Energizer story selection process, exposing the LLM's evaluation criteria and decision-making logic. This enhancement enables administrators to understand why specific stories are chosen over others, validate the effectiveness of selection prompts, and fine-tune the scoring criteria to optimize content quality and relevance.

## Workflow Objectives

### Primary Automation Goals
- **Selection Transparency**: Expose detailed scoring breakdown for all evaluated stories, not just the selected winner
- **Quality Validation**: Provide visibility into emotional impact, global relevance, and specificity scores for each story
- **Decision Auditing**: Enable administrators to verify that the highest-scored story was correctly selected

### Secondary Goals
- **Prompt Optimization**: Enable data-driven improvements to LLM selection prompts and scoring criteria
- **Content Analysis**: Provide insights into story quality patterns and selection trends
- **Performance Tuning**: Support fine-tuning of scoring weights and selection logic

## User Experience Goals

### Target Users
- **Content Administrators**: Workflow managers who need to validate and optimize story selection quality
- **Editorial Teams**: Content curators who want to understand selection criteria and improve prompts
- **Workflow Developers**: Technical users who need to debug and enhance the selection algorithm

### User Journey
1. Administrator reviews selected story (e.g., skating vs. 3D glue gun story)
2. Examines detailed scoring breakdown for all evaluated stories
3. Analyzes why one story scored higher than another
4. Identifies potential improvements to scoring criteria or prompts
5. Makes data-driven adjustments to optimize future selections

## Workflow Design

### Trigger Events
#### Primary Triggers
- **Story Selection Execution**: Every time the Select Story LLM node executes during workflow runs
- **Manual Selection Review**: On-demand analysis of story selection decisions

#### Secondary Triggers
- **Quality Assurance Review**: Triggered when selection decisions seem suboptimal
- **Prompt Optimization Cycles**: Periodic review of scoring effectiveness for improvement

### Data Sources
#### Input Data
- **Filtered Stories**: All stories passing 48-hour freshness filter from 10 RSS feeds
- **Story Metadata**: Title, summary, publication date, hours old, and source information
- **Selection Criteria**: Emotional impact, global relevance, specificity scoring parameters

#### Data Processing Requirements
- **Comprehensive Scoring**: Evaluate ALL stories, not just select the winner
- **Score Calculation**: Generate numerical scores (1-5) for each of three criteria
- **Total Score Computation**: Calculate and display total scores for ranking transparency

## Workflow Logic

### Processing Steps
#### Step 1: Enhanced Story Evaluation
- **Input Processing**: Receive all filtered stories with complete metadata
- **Comprehensive Analysis**: Score EVERY story on all three criteria
- **Ranking Generation**: Calculate total scores and rank all stories

#### Step 2: Detailed Scoring Output
- **Score Documentation**: Record individual scores for emotional impact, global relevance, specificity
- **Selection Reasoning**: Provide clear explanation for why the highest-scored story was chosen
- **Comparative Analysis**: Show score differences between top-performing stories

#### Step 3: Structured Data Output
- **Selected Story Data**: Complete information about the winning story
- **Full Scoring Breakdown**: Detailed scores for ALL evaluated stories
- **Selection Justification**: Clear reasoning for the selection decision

### Decision Logic
#### Branching Conditions
- **Score Validation**: Ensure all stories receive valid scores (1-5 range)
- **Tie Breaking**: Handle cases where multiple stories have identical total scores
- **Quality Thresholds**: Flag selections where winning story has low absolute scores

#### Error Handling
- **Scoring Failures**: Retry scoring if any story lacks complete evaluation
- **Invalid Scores**: Alert administrators if scores are outside expected ranges
- **Selection Conflicts**: Handle edge cases where scoring logic produces unexpected results

## Technical Requirements

### N8N Workflow Specifications
#### Workflow Architecture
- **LLM Prompt Enhancement**: Expand Select Story prompt to request comprehensive scoring
- **JSON Schema Update**: Modify Structured Output Parser to handle expanded scoring data
- **Data Flow Preservation**: Maintain all existing anti-hallucination measures

#### Integration Requirements
- **Select Story LLM Node**: Enhanced prompt with detailed scoring requirements
- **Structured Output Parser**: Expanded schema for comprehensive scoring data
- **Google Sheets Integration**: Additional columns for scoring visibility

### Performance Requirements
- **Processing Speed**: Minimal impact on current execution time (target <30 second increase)
- **Throughput**: Handle comprehensive scoring for 50-100+ stories per execution
- **Reliability**: Maintain 99%+ workflow success rate with enhanced scoring output
- **Scalability**: Support scoring complexity without degrading system performance

### Data Requirements
- **Input Data Format**: Existing story structure with metadata
- **Output Data Format**: Expanded JSON with complete scoring breakdown for all stories
- **Data Persistence**: Store scoring data in Google Sheets for analysis and review
- **Data Integrity**: Ensure scoring accuracy and consistency across executions

## User Experience Design

### Automation Transparency
- **Scoring Dashboard**: Clear display of all story scores in Google Sheets
- **Selection Reasoning**: Visible justification for story selection decisions
- **Comparative Analysis**: Easy comparison between high-scoring stories

### Control Options
- **Scoring Criteria Review**: Administrative access to scoring methodology
- **Prompt Adjustment**: Ability to modify scoring weights and criteria
- **Quality Thresholds**: Configurable minimum score requirements

### Error Communication
- **Scoring Failures**: Clear alerts when comprehensive scoring fails
- **Quality Warnings**: Notifications when selected stories have unexpectedly low scores
- **Selection Anomalies**: Reports when scoring logic produces questionable results

## Success Metrics

### Automation Effectiveness
- **Scoring Completeness**: Target 100% of stories receive complete scoring evaluation
- **Selection Accuracy**: Verify highest-scored story is consistently selected
- **Data Quality**: Ensure all scores are within valid ranges (1-5) and properly justified

### User Experience Metrics
- **Administrator Insight**: Measurable improvement in selection decision understanding
- **Prompt Optimization**: Data-driven improvements to selection criteria and prompts
- **Quality Validation**: Increased confidence in story selection methodology

### Business Impact Metrics
- **Content Quality**: Improved story selection leading to higher user engagement
- **Editorial Efficiency**: Reduced time spent questioning selection decisions
- **System Optimization**: Data-driven improvements to selection algorithm

## Implementation Phases

### Phase 1: Enhanced Scoring Output
- Modify Select Story LLM prompt to request comprehensive scoring
- Update Structured Output Parser schema for expanded data
- Test scoring output for accuracy and completeness

### Phase 2: Data Integration
- Add scoring columns to Google Sheets output
- Implement scoring visualization and analysis tools
- Create administrative dashboard for scoring review

### Phase 3: Optimization Tools
- Develop prompt tuning tools based on scoring data
- Implement quality threshold monitoring
- Create automated scoring analysis and reporting

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|---------|-------------|-------------------|
| LLM prompt complexity | Medium | Medium | Careful prompt design, extensive testing |
| JSON schema complexity | Medium | Low | Structured schema design, validation |
| Performance degradation | Medium | Low | Optimize prompt efficiency, monitor execution time |
| Scoring inconsistency | High | Medium | Clear scoring criteria, prompt validation |

## Integration Considerations

### External System Dependencies
- **OpenRouter LLM Service**: Enhanced prompt processing capability
- **Google Sheets Integration**: Additional columns for comprehensive scoring data
- **N8N Processing Power**: Sufficient resources for expanded LLM operations

### N8N Environment Requirements
- **LLM Node Capacity**: Ability to handle larger, more complex prompts
- **JSON Processing**: Enhanced parsing for complex nested scoring data
- **Memory Usage**: Sufficient memory for comprehensive scoring output

## Compliance & Privacy

### Data Privacy
- **Scoring Transparency**: Scoring data contains no private user information
- **Content Analysis**: Story evaluation data is based on public RSS content
- **Administrative Access**: Scoring data available only to authorized personnel

### Content Compliance
- **Scoring Accuracy**: Ensure scoring criteria align with content quality standards
- **Selection Integrity**: Maintain fairness and consistency in story evaluation
- **Audit Trail**: Complete record of scoring decisions for quality assurance

## Related Documents

- **BRENT-ACTION-PLAN.md**: Original client requirements for scoring visibility
- **source-tracking-prd.md**: Companion PRD for source tracking implementation
- **CLAUDE.md**: Workflow architecture and LLM configuration guidelines

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-09-12 | Claude | Initial version based on client requirements |

---

<!-- Last Updated: 2025-09-12T21:47:00Z -->