# Action Plan for Brent Hunter - Workflow Improvements

## Executive Summary
This action plan addresses your two specific requirements for improving story traceability and selection transparency in the Daily Energizer workflow.

---

## Problem 1: Source Tracking

### The Issue
Currently impossible to trace which RSS feed a selected story came from, making it difficult to:
- Verify stories aren't hallucinated
- Identify problematic feeds (e.g., the eggplant cooking story)
- Remove feeds that don't align with the workflow's purpose

### Root Cause
RSS feed data loses its source identifier as it flows through the workflow nodes. Stories get combined without preserving their origin.

### Solution
Add a `source` field to each story that flows through the entire workflow:

1. **In each RSS Set Fields node**, add a new field:
   ```javascript
   source: "Good News Network"  // Or appropriate feed name
   ```

2. **In Select Story output**, include the source:
   ```json
   {
     "title": "exact title from RSS feed",
     "summary": "exact summary from RSS feed",
     "source": "Good News Network",
     "reason": "one sentence explaining selection",
     "story_number": 1,
     "hours_old": 24,
     "verification": "confirmed_from_list"
   }
   ```

---

## Problem 2: Scoring Visibility

### The Issue
Cannot see how the LLM scored each story, making it impossible to:
- Understand why one story was selected over another (skating vs 3D glue gun)
- Verify the scoring logic is working as intended
- Fine-tune selection criteria

### Root Cause
The Select Story node only outputs the winning story. The LLM calculates scores internally but doesn't share them.

### Solution
Modify the Select Story prompt to output ALL story scores:

**Updated Output Format:**
```json
{
  "selected_story": {
    "title": "Person Skates Across Country for Charity",
    "summary": "exact summary",
    "source": "Positive News UK",
    "story_number": 7,
    "hours_old": 24,
    "verification": "confirmed_from_list"
  },
  "scoring_breakdown": [
    {
      "story_number": 1,
      "title": "3D Glue Gun Printing Innovation",
      "source": "Good News Network",
      "emotional_impact": 3,
      "global_relevance": 5,
      "specificity": 4,
      "total_score": 12
    },
    {
      "story_number": 7,
      "title": "Person Skates Across Country for Charity",
      "source": "Positive News UK",
      "emotional_impact": 5,
      "global_relevance": 4,
      "specificity": 5,
      "total_score": 14
    }
    // ... all other stories
  ],
  "selection_reason": "Story 7 selected due to highest total score of 14"
}
```

---

## Implementation Steps

### Step 1: Add Source Tracking (Estimated: 30 minutes)
1. Edit each of the 10 RSS Set Fields nodes
2. Add `source` field with the feed name
3. Update Format Stories node to include source
4. Update Select Story prompt to preserve source

### Step 2: Add Scoring Visibility (Estimated: 20 minutes)
1. Update Select Story prompt to request full scoring breakdown
2. Modify Structured Output Parser to handle expanded JSON
3. Test with sample stories to verify scoring output

### Step 3: Testing (Estimated: 20 minutes)
1. Run workflow end-to-end
2. Verify source appears in final output
3. Confirm all story scores are visible
4. Check that selection logic matches highest score

---

## Benefits You'll Receive

1. **Complete Traceability**: Every story can be traced back to its RSS feed
2. **Feed Quality Control**: Easily identify and remove problematic feeds
3. **Selection Transparency**: See exactly why each story was chosen or rejected
4. **Fine-Tuning Capability**: Adjust prompts based on actual scoring patterns

---

## No Additional Changes

This plan addresses only your specific requests:
- Source tracking for each story
- Full scoring visibility for all stories

No additional features or complexity have been added.