# Tasks: Story Selection Scoring Visibility Implementation

Based on PRD: Story Selection Scoring Visibility for Daily Energizer

## Relevant Files

- `daily-energizer-workflow.json` - Main N8N workflow file containing Select Story LLM node and Structured Output Parser
- `features/PRDs/scoring-visibility-prd.md` - Product requirements document for this feature
- `features/ADRs/adr-002-scoring-visibility.md` - Architecture decision record for implementation approach
- `CLAUDE.md` - Workflow documentation that will need updates for scoring visibility patterns
- `features/requirements/BRENT-ACTION-PLAN.md` - Original client requirements documentation for scoring transparency

### Notes

- All modifications will be made to the N8N workflow JSON file
- Enhanced LLM prompts may increase processing time by 15-30 seconds
- Structured Output Parser schema must handle complex nested JSON for all story scores
- Google Sheets integration will require additional columns for scoring data display
- Testing should verify scoring accuracy and consistency across multiple executions

## Tasks

- [ ] 1.0 Analyze Current Story Selection Process and LLM Configuration
  - [ ] 1.1 Examine the current "Select Story" LLM node prompt structure and requirements
  - [ ] 1.2 Review the existing Structured Output Parser JSON schema for story selection
  - [ ] 1.3 Analyze current LLM output format and identify expansion points for scoring data
  - [ ] 1.4 Document current story evaluation criteria (emotional impact, global relevance, specificity)
  - [ ] 1.5 Identify performance baseline for current story selection processing time

- [ ] 2.0 Design Enhanced Scoring Output Schema and Data Structure
  - [ ] 2.1 Design JSON schema for comprehensive scoring breakdown of all stories
  - [ ] 2.2 Define scoring structure with individual criterion scores (1-5 scale)
  - [ ] 2.3 Plan nested JSON structure for selected_story and scoring_breakdown arrays
  - [ ] 2.4 Design selection_reason field format for clear decision explanation
  - [ ] 2.5 Validate schema compatibility with existing workflow data flow

- [ ] 3.0 Modify Select Story LLM Prompt for Comprehensive Scoring
  - [ ] 3.1 Enhance prompt to request evaluation of ALL stories, not just selection
  - [ ] 3.2 Add explicit scoring instructions for emotional impact (1-5) criteria
  - [ ] 3.3 Add explicit scoring instructions for global relevance (1-5) criteria
  - [ ] 3.4 Add explicit scoring instructions for specificity (1-5) criteria
  - [ ] 3.5 Include total score calculation and ranking requirements in prompt
  - [ ] 3.6 Add selection reasoning requirements for decision transparency
  - [ ] 3.7 Update prompt to maintain existing anti-hallucination measures

- [ ] 4.0 Update Structured Output Parser for Complex Scoring Data
  - [ ] 4.1 Replace existing JSON schema with comprehensive scoring schema
  - [ ] 4.2 Configure parser to handle nested scoring_breakdown array structure
  - [ ] 4.3 Add validation for required scoring fields (emotional_impact, global_relevance, specificity)
  - [ ] 4.4 Ensure parser handles variable number of stories in scoring breakdown
  - [ ] 4.5 Test JSON parsing with complex nested data structures

- [ ] 5.0 Enhance Google Sheets Integration with Scoring Columns
  - [ ] 5.1 Add scoring columns to "Add Article and Story Centered Summary to Sheet" node
  - [ ] 5.2 Configure column mapping for selected story scoring details
  - [ ] 5.3 Add comprehensive scoring breakdown display in separate columns or sheet
  - [ ] 5.4 Update "Update Status, Image URL and Image Preview Formula to Sheet" to include scoring
  - [ ] 5.5 Test Google Sheets integration with expanded scoring data

- [ ] 6.0 Validate Scoring Consistency and Performance Impact
  - [ ] 6.1 Import modified workflow into N8N interface for testing
  - [ ] 6.2 Execute workflow multiple times to verify scoring consistency
  - [ ] 6.3 Measure performance impact of enhanced scoring (target <30 second increase)
  - [ ] 6.4 Verify all stories receive complete scoring evaluation (emotional, global, specificity)
  - [ ] 6.5 Validate that highest-scored story is consistently selected
  - [ ] 6.6 Confirm scoring data displays correctly in Google Sheets
  - [ ] 6.7 Test edge cases (tie scores, stories with identical content, etc.)
  - [ ] 6.8 Verify scoring doesn't interfere with existing anti-hallucination measures