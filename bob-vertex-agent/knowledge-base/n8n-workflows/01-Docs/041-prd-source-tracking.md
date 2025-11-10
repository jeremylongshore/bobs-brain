<!-- Created: 2025-09-12T21:45:00Z -->

# PRD: RSS Feed Source Tracking for Daily Energizer

## Executive Summary

This PRD covers the implementation of comprehensive source tracking throughout the Daily Energizer N8N workflow, enabling complete traceability of every selected story back to its originating RSS feed. This enhancement addresses critical quality control needs by allowing administrators to verify story authenticity, identify problematic feeds, and maintain the integrity of the anti-hallucination system.

## Workflow Objectives

### Primary Automation Goals
- **Source Attribution**: Automatically track and preserve the RSS feed source for every story throughout the entire workflow
- **Hallucination Prevention**: Provide verifiable source information to confirm story authenticity and prevent fabricated content
- **Feed Quality Management**: Enable identification and removal of low-quality or inappropriate RSS feeds (e.g., cooking content in news feeds)

### Secondary Goals
- **Audit Trail Creation**: Maintain complete data lineage for compliance and quality assurance
- **Performance Monitoring**: Track feed reliability and content quality by source
- **Content Optimization**: Identify highest-performing feed sources for workflow enhancement

## User Experience Goals

### Target Users
- **Content Administrators**: Workflow managers who need to verify story authenticity and manage feed quality
- **Quality Assurance Teams**: Users responsible for maintaining content standards and preventing hallucinations
- **Workflow Developers**: Technical users who need to debug and optimize the content selection process

### User Journey
1. Administrator notices questionable content (e.g., "eggplant cooking" story)
2. Reviews workflow output with source tracking information
3. Identifies problematic RSS feed source
4. Makes informed decision to remove or modify feed configuration
5. Maintains high content quality and user trust

## Workflow Design

### Trigger Events
#### Primary Triggers
- **Manual Workflow Execution**: User-initiated article generation with full source tracking
- **Scheduled Execution**: Automated daily runs with source preservation throughout data flow

#### Secondary Triggers
- **Feed Quality Review**: Triggered when unusual content is detected for source investigation
- **Audit Requirements**: On-demand execution for compliance and quality verification

### Data Sources
#### Input Data
- **10 RSS Feeds**: Positive News UK, Good News Network, Sunny Skyz, The Optimist Daily, Good Good Good, Nice News, Epoch Times Bright, Reasons to Be Cheerful, YES! Magazine, Not All News is Bad!
- **Story Metadata**: Title, summary, publication date, and now source attribution
- **Workflow State**: Processing timestamps and node execution tracking

#### Data Processing Requirements
- **Source Preservation**: Maintain feed source through all transformation steps
- **Data Validation**: Ensure source field is never lost or corrupted during processing
- **Integrity Checking**: Verify story-to-source mapping remains accurate throughout workflow

## Workflow Logic

### Processing Steps
#### Step 1: RSS Feed Collection with Source Tagging
- **Input Sources**: Each of the 10 RSS feed nodes
- **Source Assignment**: Add explicit `source` field to every story in Set RSS Fields nodes
- **Data Validation**: Confirm source field exists and is populated for all stories

#### Step 2: Source Preservation Through Filtering
- **48-Hour Filtering**: Maintain source field through all date filtering operations
- **Duplicate Removal**: Preserve source information when removing duplicate stories
- **Story Combination**: Ensure source data flows correctly through merge operations

#### Step 3: Source-Aware Story Selection
- **LLM Input**: Include source information in story evaluation prompt
- **Selection Output**: Require selected story output to include verified source field
- **Verification**: Cross-reference selected story source with original feed data

### Decision Logic
#### Branching Conditions
- **Source Validation**: Verify source field exists before proceeding to next step
- **Feed Quality Assessment**: Flag feeds producing unusual content for review
- **Data Integrity**: Halt workflow if source tracking is compromised

#### Error Handling
- **Missing Source Data**: Alert administrators and halt processing
- **Source Mismatch**: Trigger verification failure and workflow stop
- **Feed Unavailability**: Log source unavailability but continue with available feeds

## Technical Requirements

### N8N Workflow Specifications
#### Workflow Architecture
- **Node Modifications**: Update all 10 Set RSS Fields nodes to include source attribution
- **Data Flow Enhancement**: Preserve source field through 70-node workflow
- **Output Schema Update**: Expand JSON output to include source information

#### Integration Requirements
- **RSS Feed Processing**: Modified Set RSS Fields nodes with source assignment
- **Story Selection LLM**: Updated prompt to handle and output source data
- **Google Sheets Integration**: Expanded columns to display source information

### Performance Requirements
- **Processing Speed**: No significant impact on current 2-minute execution time
- **Throughput**: Handle same volume (100+ stories) with additional source metadata
- **Reliability**: Maintain 99%+ workflow success rate with enhanced data tracking
- **Scalability**: Support future expansion to additional RSS feeds

### Data Requirements
- **Input Data Format**: Add `source` string field to story objects
- **Output Data Format**: Include source in final article metadata and sheets
- **Data Persistence**: Store source information in Google Sheets for audit trail
- **Data Privacy**: No privacy concerns as source information is public RSS feed attribution

## User Experience Design

### Automation Transparency
- **Source Visibility**: Clear display of story source in Google Sheets output
- **Feed Performance**: Dashboard showing story selection rates by source
- **Quality Indicators**: Visual flags for feeds requiring review

### Control Options
- **Feed Management**: Administrative interface for enabling/disabling problem feeds
- **Source Filtering**: Option to exclude specific feeds from selection process
- **Quality Thresholds**: Configurable content quality standards by source

### Error Communication
- **Source Tracking Failures**: Immediate alerts when source data is lost
- **Feed Quality Issues**: Notifications when unusual content is detected
- **Verification Errors**: Clear reporting when source-story mismatches occur

## Success Metrics

### Automation Effectiveness
- **Source Tracking Accuracy**: Target 100% story-to-source attribution
- **Data Integrity**: Zero source data loss throughout workflow execution
- **Verification Success**: 100% successful source verification for selected stories

### User Experience Metrics
- **Administrator Efficiency**: Reduced time to identify problematic feeds
- **Quality Control Improvement**: Decreased occurrence of inappropriate content
- **Trust Metrics**: Increased confidence in story authenticity

### Business Impact Metrics
- **Content Quality**: Measurable improvement in story relevance and appropriateness
- **Feed Optimization**: Data-driven decisions for RSS feed management
- **Hallucination Prevention**: Zero instances of unverifiable content

## Implementation Phases

### Phase 1: Core Source Tracking
- Modify all 10 Set RSS Fields nodes to include source attribution
- Update Combine Stories node to preserve source data
- Test source preservation through 48-hour filters

### Phase 2: Selection Integration
- Update Select Story LLM prompt to handle source information
- Modify JSON output schema to include source field
- Implement source verification in workflow output

### Phase 3: Reporting & Management
- Add source columns to Google Sheets output
- Create source-based quality reporting
- Implement administrative feed management tools

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|---------|-------------|-------------------|
| Source data loss during processing | High | Low | Comprehensive testing, validation checks |
| Performance degradation | Medium | Low | Lightweight source field, performance monitoring |
| JSON schema complexity | Medium | Medium | Careful schema design, backward compatibility |
| LLM prompt reliability | Medium | Low | Extensive prompt testing, fallback handling |

## Integration Considerations

### External System Dependencies
- **RSS Feed Stability**: Ensure feed source names remain consistent
- **Google Sheets Capacity**: Additional column for source data
- **LLM Processing**: Enhanced prompts to handle source information

### N8N Environment Requirements
- **Node Compatibility**: Verify Set RSS Fields nodes support additional assignments
- **Memory Usage**: Minimal increase for source string storage
- **Processing Overhead**: Negligible impact on execution time

## Compliance & Privacy

### Data Privacy
- **Public Information**: RSS feed sources are public, no privacy concerns
- **Attribution Requirements**: Proper source attribution enhances transparency
- **Data Minimization**: Only necessary source information is stored

### Content Compliance
- **Source Attribution**: Proper attribution to original RSS feeds
- **Quality Standards**: Enhanced ability to maintain content quality
- **Audit Requirements**: Complete audit trail for content verification

## Related Documents

- **BRENT-ACTION-PLAN.md**: Original client requirements for source tracking
- **CLAUDE.md**: Workflow architecture and anti-hallucination system documentation
- **IMPLEMENTATION-GUIDE.md**: Technical implementation history and patterns

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-09-12 | Claude | Initial version based on client requirements |

---

<!-- Last Updated: 2025-09-12T21:45:00Z -->