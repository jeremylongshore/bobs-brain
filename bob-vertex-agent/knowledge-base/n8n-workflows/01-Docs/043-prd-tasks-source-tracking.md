# Tasks: RSS Feed Source Tracking Implementation

Based on PRD: RSS Feed Source Tracking for Daily Energizer

## Relevant Files

- `daily-energizer-workflow.json` - Main N8N workflow file containing all 70 nodes that need source tracking modifications
- `features/PRDs/source-tracking-prd.md` - Product requirements document for this feature
- `features/ADRs/adr-001-rss-source-tracking.md` - Architecture decision record for implementation approach
- `CLAUDE.md` - Workflow documentation that will need updates for source tracking patterns
- `features/requirements/BRENT-ACTION-PLAN.md` - Original client requirements documentation

### Notes

- All modifications will be made to the N8N workflow JSON file
- Source tracking must preserve existing anti-hallucination measures
- Testing should be performed in N8N interface after importing modified workflow
- Google Sheets integration will require additional column configuration

## Tasks

- [ ] 1.0 Analyze Current Workflow Structure and RSS Feed Nodes
  - [ ] 1.1 Load and examine the daily-energizer-workflow.json file structure
  - [ ] 1.2 Identify all 10 RSS Feed Read nodes and their corresponding Set RSS Fields nodes
  - [ ] 1.3 Map the data flow from RSS nodes through 48-hour filters to story combination
  - [ ] 1.4 Document current story object structure and field assignments
  - [ ] 1.5 Verify the names of all 10 RSS feeds for accurate source attribution

- [ ] 2.0 Implement Source Field Addition to RSS Set Fields Nodes
  - [ ] 2.1 Add source field to "Set RSS Fields" node (Good News Network) with value "Good News Network"
  - [ ] 2.2 Add source field to "Set RSS Fields1" node (Positive News UK) with value "Positive News UK"
  - [ ] 2.3 Add source field to "Set RSS Fields2" node (Sunny Skyz) with value "Sunny Skyz"
  - [ ] 2.4 Add source field to "Set RSS Fields3" node (The Optimist Daily) with value "The Optimist Daily"
  - [ ] 2.5 Add source field to "Set RSS Fields4" node (Good Good Good) with value "Good Good Good"
  - [ ] 2.6 Add source field to "Set RSS Fields5" node (Nice News) with value "Nice News"
  - [ ] 2.7 Add source field to "Set RSS Fields6" node (Epoch Times Bright) with value "Epoch Times Bright"
  - [ ] 2.8 Add source field to "Set RSS Fields7" node (Reasons to Be Cheerful) with value "Reasons to Be Cheerful"
  - [ ] 2.9 Add source field to "Set RSS Fields8" node (YES! Magazine) with value "YES! Magazine"
  - [ ] 2.10 Add source field to "Set RSS Fields9" node (Not All News is Bad!) with value "Not All News is Bad!"

- [ ] 3.0 Update Story Selection and Processing Nodes for Source Preservation
  - [ ] 3.1 Verify that 48-hour filter code nodes preserve the source field in story objects
  - [ ] 3.2 Update "Combine Stories" function node to include source field in formatted prompt text
  - [ ] 3.3 Modify "Select Story" LLM prompt to include source information in story evaluation
  - [ ] 3.4 Update Structured Output Parser JSON schema to include source field in output
  - [ ] 3.5 Verify source field flows correctly through "Set Today's Date" and "Write Article" nodes

- [ ] 4.0 Enhance Google Sheets Integration with Source Display
  - [ ] 4.1 Add source field to "Add Article and Story Centered Summary to Sheet" node column mapping
  - [ ] 4.2 Update Google Sheets schema configuration to include "Source" column
  - [ ] 4.3 Modify "Update Status, Image URL and Image Preview Formula to Sheet" to preserve source data
  - [ ] 4.4 Test Google Sheets integration to ensure source column populates correctly

- [ ] 5.0 Validate Source Tracking Throughout Workflow Execution
  - [ ] 5.1 Import modified workflow into N8N interface
  - [ ] 5.2 Execute workflow manually and verify source fields appear in all processing steps
  - [ ] 5.3 Check that selected story output includes correct source attribution
  - [ ] 5.4 Verify source information appears correctly in Google Sheets
  - [ ] 5.5 Test with multiple RSS feeds to ensure source accuracy across all feeds
  - [ ] 5.6 Validate that source tracking doesn't interfere with existing anti-hallucination measures

- [ ] 6.0 Update Documentation and Testing Procedures
  - [ ] 6.1 Update CLAUDE.md with source tracking implementation details
  - [ ] 6.2 Add source tracking validation steps to testing checklist
  - [ ] 6.3 Document source field structure and preservation requirements
  - [ ] 6.4 Create troubleshooting guide for source tracking issues
  - [ ] 6.5 Update workflow execution instructions to include source verification steps