# Daily Energizer Workflow - Manual Update Guide
**Date: 2025-09-12**

## Overview
This guide provides step-by-step instructions to manually update the Daily Energizer N8N workflow with two new features:
1. RSS Feed Source Tracking
2. Story Selection Scoring Visibility

---

## PART 1: RSS FEED SOURCE TRACKING

### Step 1: Update ALL 10 "Set RSS Fields" Nodes

You need to add a source field to each Set RSS Fields node. Open each node and add a new assignment:

#### Set RSS Fields (no number)
- **Name:** `source`
- **Value:** `Good News Network`
- **Type:** String

#### Set RSS Fields1
- **Name:** `source`
- **Value:** `Positive News UK`
- **Type:** String

#### Set RSS Fields2
- **Name:** `source`
- **Value:** `Sunny Skyz`
- **Type:** String

#### Set RSS Fields3
- **Name:** `source`
- **Value:** `The Optimist Daily`
- **Type:** String

#### Set RSS Fields4
- **Name:** `source`
- **Value:** `Good Good Good`
- **Type:** String

#### Set RSS Fields5
- **Name:** `source`
- **Value:** `Nice News`
- **Type:** String

#### Set RSS Fields6
- **Name:** `source`
- **Value:** `Epoch Times Bright`
- **Type:** String

#### Set RSS Fields7
- **Name:** `source`
- **Value:** `Reasons to Be Cheerful`
- **Type:** String

#### Set RSS Fields8
- **Name:** `source`
- **Value:** `YES! Magazine`
- **Type:** String

#### Set RSS Fields9
- **Name:** `source`
- **Value:** `Not All News is Bad!`
- **Type:** String

---

### Step 2: Update "Combine Stories" Function Node

1. Open the "Combine Stories" node
2. Find this code section:

```javascript
const formatted = stories.map((story, index) => {
  const hoursOld = story.hours_old || 'Unknown';
  return `Story ${index + 1}:
  Title: ${story.title}
  Summary: ${story.summary}
  Published: ${story.pubDate}
  Hours Old: ${hoursOld}`;
}).join('\n\n');
```

3. **REPLACE WITH:**

```javascript
const formatted = stories.map((story, index) => {
  const hoursOld = story.hours_old || 'Unknown';
  const source = story.source || 'Unknown Source';
  return `Story ${index + 1}:
  Title: ${story.title}
  Summary: ${story.summary}
  Published: ${story.pubDate}
  Hours Old: ${hoursOld}
  Source: ${source}`;
}).join('\n\n');
```

---

## PART 2: STORY SELECTION SCORING VISIBILITY

### Step 3: Update "Select Story" LLM Node - Two Options

⚠️ **IMPORTANT**: Due to N8N Cloud version 1.110.1 limitations with complex nested JSON, you have TWO options:

#### Option 1: WITHOUT Structured Output Parser (RECOMMENDED)

If you encounter "Model output doesn't fit required format" errors, REMOVE or DISCONNECT the Structured Output Parser node and use enhanced prompts for direct JSON output.

#### Option 2: WITH Structured Output Parser (If Compatible)

##### Part A: Update the Structured Output Parser Node

1. Find the **"Structured Output Parser"** node in your workflow (it should be connected to the Select Story node)
2. Open the Structured Output Parser node
3. Find the **"JSON Schema Example"** field
4. **DELETE everything in that field**
5. **PASTE this entire JSON example:**

```json
{
  "selected_story": {
    "title": "Example story title here",
    "summary": "Example story summary here",
    "source": "Example source here",
    "story_number": 1,
    "hours_old": 24,
    "emotional_impact": 5,
    "global_relevance": 5,
    "specificity": 5,
    "total_score": 15,
    "verification": "confirmed_from_list"
  },
  "selection_reason": "This story scored highest because it demonstrates incredible human resilience",
  "all_stories_scoring": [
    {
      "story_number": 1,
      "title": "Example story 1 title",
      "source": "Example source 1",
      "emotional_impact": 5,
      "global_relevance": 5,
      "specificity": 5,
      "total_score": 15,
      "hours_old": 24,
      "eligible": true
    },
    {
      "story_number": 2,
      "title": "Example story 2 title",
      "source": "Example source 2",
      "emotional_impact": 3,
      "global_relevance": 4,
      "specificity": 3,
      "total_score": 10,
      "hours_old": 36,
      "eligible": true
    }
  ]
}
```

6. Click **Save** on the Structured Output Parser node

##### Part B: Update the Select Story Node Prompt (FOR OPTION 2)

1. Open the **"Select Story"** node
2. Find the **"Prompt"** field
3. **DELETE everything in the Prompt field**
4. **PASTE this entire prompt:**

```
CRITICAL ANTI-HALLUCINATION REQUIREMENTS:

  YOU MUST FOLLOW THESE RULES OR THE SYSTEM WILL FAIL:
  1. You can ONLY select a story that is EXACTLY in the provided list
  2. You CANNOT create, modify, or reword ANY part of any story
  3. You MUST copy the title and summary EXACTLY as provided
  4. You MUST verify the story is less than 48 hours old
  5. If no stories meet ALL criteria, you MUST return an error
  6. You MUST score ALL stories, not just the selected one

  COMPREHENSIVE SCORING PROCESS:
  1. Read each story carefully
  2. Score EVERY story on ALL three criteria (even if >48 hours old):
     - Emotional Impact (1-5): How uplifting and inspiring?
     - Global Relevance (1-5): Universal appeal across cultures?
     - Specificity (1-5): Concrete details, names, places?
  3. Calculate total score for each story (sum of 3 criteria)
  4. Mark eligibility: true if <=48 hours old, false if older
  5. Select the ELIGIBLE story with highest total score
  6. Copy EXACT titles, summaries, and sources for ALL stories

  Stories to Evaluate:
 {{ $json.promptText }}

  OUTPUT FORMAT (MUST BE VALID JSON with ALL stories scored):
  {
    "selected_story": {
      "title": "exact title from the list",
      "summary": "exact summary from the list",
      "source": "exact source from the list",
      "story_number": 1,
      "hours_old": 24,
      "emotional_impact": 5,
      "global_relevance": 5,
      "specificity": 5,
      "total_score": 15,
      "verification": "confirmed_from_list"
    },
    "selection_reason": "one sentence explaining why this story scored highest among eligible stories",
    "all_stories_scoring": [
      {
        "story_number": 1,
        "title": "exact title from story 1",
        "source": "exact source from story 1",
        "emotional_impact": 5,
        "global_relevance": 5,
        "specificity": 5,
        "total_score": 15,
        "hours_old": 24,
        "eligible": true
      },
      {
        "story_number": 2,
        "title": "exact title from story 2",
        "source": "exact source from story 2",
        "emotional_impact": 3,
        "global_relevance": 4,
        "specificity": 3,
        "total_score": 10,
        "hours_old": 36,
        "eligible": true
      }
    ]
  }

  REMEMBER: You MUST include scoring for EVERY story in the all_stories_scoring array. Replace example values with actual scores and data. Any hallucination will cause system failure.

```

5. Click **Save** on the Select Story node

#### Option 1 Instructions: WITHOUT Structured Output Parser (RECOMMENDED)

If you're getting parser errors, follow these steps:

1. **Disconnect or Remove** the Structured Output Parser node
2. **Update the Select Story Node with Enhanced Prompts**:

**System Message:**
```
You are an AI assistant for "The Daily Energizer" with STRICT JSON output requirements.

CRITICAL OUTPUT RULES:
1. You MUST output ONLY valid JSON - no text before or after
2. You MUST include ALL required fields exactly as specified
3. You MUST NOT add any markdown formatting (no ```json blocks)
4. You MUST ensure proper JSON syntax with correct quotes and commas
5. You MUST score EVERY story in the provided list

Your response should be a single JSON object that can be directly parsed.

REQUIRED JSON STRUCTURE:
- selected_story: object with title, summary, source, story_number, hours_old, and all scores
- selection_reason: string explaining why this story won
- all_stories_scoring: array with scoring for EVERY story

Remember: Output ONLY the JSON object. No explanations, no formatting, just pure JSON.
```

**Main Prompt:**
```
CRITICAL ANTI-HALLUCINATION AND OUTPUT REQUIREMENTS:

YOU MUST FOLLOW THESE RULES OR THE SYSTEM WILL FAIL:
1. You can ONLY select a story that is EXACTLY in the provided list
2. You CANNOT create, modify, or reword ANY part of any story
3. You MUST copy the title and summary EXACTLY as provided
4. You MUST verify the story is less than 48 hours old
5. You MUST output ONLY valid JSON with no additional text
6. You MUST score ALL stories, not just the selected one

COMPREHENSIVE SCORING PROCESS:
Step 1: Read each story carefully
Step 2: Score EVERY story on ALL three criteria (even if >48 hours old):
   - Emotional Impact (1-5): How uplifting and inspiring?
   - Global Relevance (1-5): Universal appeal across cultures?
   - Specificity (1-5): Concrete details, names, places?
Step 3: Calculate total score for each story (sum of 3 criteria)
Step 4: Mark eligibility: true if <=48 hours old, false if older
Step 5: Select the ELIGIBLE story with highest total score
Step 6: Copy EXACT titles, summaries, and sources for ALL stories

Stories to Evaluate:
{{ $json.promptText }}

OUTPUT ONLY THIS EXACT JSON STRUCTURE (no text before or after):
{
  "selected_story": {
    "title": "[exact title from the list]",
    "summary": "[exact summary from the list]",
    "source": "[exact source from the list]",
    "story_number": [number],
    "hours_old": [number],
    "emotional_impact": [1-5],
    "global_relevance": [1-5],
    "specificity": [1-5],
    "total_score": [sum of 3 scores],
    "verification": "confirmed_from_list"
  },
  "selection_reason": "[one sentence explaining why this story scored highest among eligible stories]",
  "all_stories_scoring": [
    {
      "story_number": [number],
      "title": "[exact title]",
      "source": "[exact source]",
      "emotional_impact": [1-5],
      "global_relevance": [1-5],
      "specificity": [1-5],
      "total_score": [sum],
      "hours_old": [number],
      "eligible": [true/false]
    }
  ]
}

CRITICAL REMINDERS:
- Output ONLY the JSON object above - no explanations
- Include scoring for EVERY story in all_stories_scoring
- Replace bracketed placeholders with actual values
- Ensure all string values are in quotes
- Ensure all number values are NOT in quotes
- Any hallucination will cause system failure
```

#### ⚠️ CRITICAL VERIFICATION for Step 3

**Choose Option 1 or Option 2 based on your N8N version:**
- **Option 1 (Without Parser)**: Recommended for N8N Cloud 1.110.1 or if you get parser errors
- **Option 2 (With Parser)**: Use if your N8N version supports complex nested JSON

**Test Point**: After completing Step 3, run a test of just the Select Story node to verify it outputs the new JSON structure with all stories scored.

---

### Step 4: Update "Write Article" Node

1. Open the "Write Article" node
2. In the Prompt field, find the section that starts with `IMPORTANT: You are writing about a REAL news story...`
3. **REPLACE THAT ENTIRE SECTION** with:

```
  IMPORTANT: You are writing about a REAL news story that happened {{ $('Select Story').item.json.output.selected_story.hours_old }} hours ago.
  Do NOT embellish or add details not in the provided summary.
  Use ONLY the information provided in the story summary.

  Selected Story (VERIFIED REAL):
  Title: {{ $('Select Story').item.json.output.selected_story.title }}
  Summary: {{ $('Select Story').item.json.output.selected_story.summary }}
  Published: {{ $('Select Story').item.json.output.selected_story.hours_old }} hours ago
  Source: {{ $('Select Story').item.json.output.selected_story.source }}
  Scores: Emotional Impact: {{ $('Select Story').item.json.output.selected_story.emotional_impact }}/5, Global Relevance: {{ $('Select Story').item.json.output.selected_story.global_relevance }}/5, Specificity: {{ $('Select Story').item.json.output.selected_story.specificity }}/5
  Total Score: {{ $('Select Story').item.json.output.selected_story.total_score }}/15
  Selection Reason: {{ $('Select Story').item.json.output.selection_reason }}
  Verification: {{ $('Select Story').item.json.output.selected_story.verification }}

  Now, using the above story, write the full Daily Energizer article (650-750 words max). Please follow the required section structure and tone
  guidelines to create one of the most uplifting, super-charged, inspiring and energizing articles ever!

  Don't ever use emojis!
```

---

### Step 5: Update "Add Article and Story Centered Summary to Sheet" Node

1. Open this Google Sheets node
2. In the Columns section, ADD these new column mappings (click Add Column for each):

#### New Column Mappings to Add:

| Column Name | Value |
|------------|-------|
| Source | `{{ $('Select Story').item.json.output.selected_story.source }}` |
| Emotional Impact Score | `{{ $('Select Story').item.json.output.selected_story.emotional_impact }}` |
| Global Relevance Score | `{{ $('Select Story').item.json.output.selected_story.global_relevance }}` |
| Specificity Score | `{{ $('Select Story').item.json.output.selected_story.specificity }}` |
| Total Score | `{{ $('Select Story').item.json.output.selected_story.total_score }}` |
| Selection Reason | `{{ $('Select Story').item.json.output.selection_reason }}` |
| All Stories Count | `{{ $('Select Story').item.json.output.all_stories_scoring.length }}` |
| All Stories Scoring | `{{ JSON.stringify($('Select Story').item.json.output.all_stories_scoring) }}` |

---

## ⚠️ CRITICAL NOTES

### Output Structure Changed
The Select Story node now returns a different structure:
- **OLD:** `output.title`, `output.summary`, etc.
- **NEW:** `output.selected_story.title`, `output.selected_story.summary`, etc.

### Testing Checkpoints
1. **After Step 3:** Test the workflow to verify the new JSON structure is returned
2. **After Step 4:** Verify the Write Article node can access the new fields
3. **After Step 5:** Confirm all data appears in Google Sheets

### Google Sheets Setup
Make sure your Google Sheet has columns for all the new fields:
- Source
- Emotional Impact Score
- Global Relevance Score
- Specificity Score
- Total Score
- Selection Reason
- All Stories Count
- All Stories Scoring

### Save Frequently
Save the workflow after completing each major step to avoid losing work.

---

## Summary of Changes

### RSS Feed Source Tracking
✅ Added source field to all 10 Set RSS Fields nodes
✅ Updated Combine Stories to include source in prompt
✅ Modified Select Story to output source field
✅ Updated Write Article to display source
✅ Added source column to Google Sheets

### Story Selection Scoring Visibility
✅ Modified Select Story to score ALL stories
✅ Changed output to include comprehensive scoring breakdown
✅ Updated Write Article to reference new structure
✅ Added 8 new scoring columns to Google Sheets
✅ Maintained all anti-hallucination measures

---

**End of Manual Update Guide**
**Date: 2025-09-12**