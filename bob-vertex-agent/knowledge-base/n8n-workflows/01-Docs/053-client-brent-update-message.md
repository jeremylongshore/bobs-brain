# Message for Brent - Workflow Updates Needed
**Date: 2025-09-12**

Hi Brent,

I've successfully tested the RSS Feed Source Tracking and Story Selection Scoring Visibility features on my local copy. Since the workflow is shared from your account, I need you to make these updates on your end.

## Quick Updates Needed (5-10 minutes)

### 1. Google Sheets - Add New Columns
Please add these columns to your Daily Energizer Google Sheet:
- **Source** (for RSS feed tracking)
- **Emotional Impact Score** (1-5 rating)
- **Global Relevance Score** (1-5 rating)
- **Specificity Score** (1-5 rating)
- **Total Score** (sum of 3 scores)
- **Selection Reason** (why story was chosen)
- **All Stories Count** (number evaluated)
- **All Stories Scoring** (detailed JSON data)

### 2. Select Story Node - Remove Output Parser
Due to N8N Cloud version limitations with complex JSON:
1. Open the **Select Story** node
2. **Disconnect or remove** the Structured Output Parser (it's causing the format errors)
3. The enhanced prompts I've provided will handle JSON formatting directly

### 3. Update "Add Article and Story Centered Summary to Sheet" Node
Add these column mappings in the Google Sheets node:

| Column Name | Value to Paste |
|------------|----------------|
| Source | `{{ $('Select Story').item.json.output.selected_story.source }}` |
| Emotional Impact Score | `{{ $('Select Story').item.json.output.selected_story.emotional_impact }}` |
| Global Relevance Score | `{{ $('Select Story').item.json.output.selected_story.global_relevance }}` |
| Specificity Score | `{{ $('Select Story').item.json.output.selected_story.specificity }}` |
| Total Score | `{{ $('Select Story').item.json.output.selected_story.total_score }}` |
| Selection Reason | `{{ $('Select Story').item.json.output.selection_reason }}` |
| All Stories Count | `{{ $('Select Story').item.json.output.all_stories_scoring.length }}` |
| All Stories Scoring | `{{ JSON.stringify($('Select Story').item.json.output.all_stories_scoring) }}` |

## What This Gives You
- **Full transparency** on which RSS feed each story comes from
- **Detailed scoring breakdown** for ALL evaluated stories (not just the winner)
- **Decision reasoning** for why each story was selected
- **Quality metrics** to optimize story selection over time

## Important Note
The workflow is already updated with the enhanced prompts and source tracking. You just need to:
1. Add the Google Sheets columns
2. Disconnect the output parser (it's incompatible with the complex JSON)
3. Update the Sheets node with the new mappings

Let me know if you need any clarification or run into issues!

Best,
Jeremy

**Date: 2025-09-12**