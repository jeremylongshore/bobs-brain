# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

N8N workflow automation for generating **daily inspirational articles** from positive news RSS feeds with comprehensive anti-hallucination measures, full scoring transparency, and automated image generation.

## Critical Workflow Architecture

### Core Workflow Files
- **`The Daily Energizer Article and Image Generator V4.json`** - Latest version with enhanced features
  - Direct import into N8N platform for execution
  - Contains 4-layer anti-hallucination system
  - Full scoring visibility for all evaluated stories
  - Automated image generation and Google Sheets integration
  - Enhanced article processing with story-centered summaries
- **`The Daily Energizer Article and Image Generator V3.json`** - Previous stable version (2,513 lines, 86KB)
- **`The Daily Energizer Article and Image Generator V2-Jeremy.json`** - Legacy version (83KB)

### V4 Enhanced Data Flow Pipeline
1. **RSS Collection** → 10 positive news feeds fetch stories with source tracking
2. **Date Filtering** → Removes stories older than 48 hours (prevents old content)
3. **Story Deduplication** → Remove Duplicates node prevents repeated stories
4. **Story Selection** → Enhanced LLM scores ALL stories on 3 criteria, selects highest
5. **Verification** → Validates selected story exists in source list
6. **Article Generation** → Creates full article with verified story and source attribution
7. **Summary Generation** → Creates story-centered summary (200 words max)
8. **Image Processing** → Generates images and converts shareable URLs to direct URLs
9. **Google Sheets Integration** → Updates spreadsheet with article, image, and review status

## N8N Commands

```bash
# Import V4 workflow (latest version)
n8n import:workflow --input="The Daily Energizer Article and Image Generator V4.json"

# Import V3 workflow (stable fallback)
n8n import:workflow --input="The Daily Energizer Article and Image Generator V3.json"

# Execute workflow (requires workflow ID from N8N)
n8n execute --id=[workflow-id]

# Export updated workflow
n8n export:workflow --id=[workflow-id] --output="The Daily Energizer Article and Image Generator V4.json"

# Validate workflow JSON structure
jq . "The Daily Energizer Article and Image Generator V4.json" > /dev/null && echo "Valid JSON"
```

## Critical Anti-Hallucination System (ALL 4 LAYERS REQUIRED)

### Layer 1: Date Filtering
- 10 Filter nodes enforce 48-hour freshness
- Formula: `Math.floor((Date.now() - new Date($json.pubDate).getTime()) / (1000 * 60 * 60))`
- Stories > 48 hours automatically dropped

### Layer 2: Verification Node
- Cross-references selected story with source list
- Returns: 'passed', 'partial', or 'failed'
- Workflow halts on failure

### Layer 3: LLM Prompt Hardening
- Explicit anti-hallucination instructions
- Required JSON output with verification field
- Structured scoring for all stories

### Layer 4: Temperature Zero
- All 3 GPT-4o-mini nodes at deterministic setting
- Ensures consistent, non-creative output

## Critical Development Rules

### NEVER Modify These Settings
- **Temperature** must remain at 0 in all LLM nodes
- **Date filters** must remain at 48 hours
- **Verification node** must never be bypassed
- **Source tracking** must be preserved through workflow

### Node Variable Syntax (N8N Specific)
```javascript
// CORRECT - Always use N8N helpers
const stories = $input.first().json.stories;
const allItems = $input.all();
const currentData = $json;

// INCORRECT - Will cause undefined variable errors
const stories = items[0].json.stories;  // DO NOT USE
const data = items.json;                 // DO NOT USE
```

## Current Feature Implementation

### RSS Feed Source Tracking
Each of the 10 RSS feeds has a source identifier:
- Good News Network
- Positive News UK
- Sunny Skyz
- The Optimist Daily
- Good Good Good
- Nice News
- Epoch Times Bright
- Reasons to Be Cheerful
- YES! Magazine
- Not All News is Bad!

### Scoring System (3 Criteria)
All stories are scored on:
1. **Emotional Impact** (1-5): How uplifting and inspiring
2. **Global Relevance** (1-5): Universal appeal across cultures
3. **Specificity** (1-5): Concrete details, names, places
4. **Total Score**: Sum of all three (3-15 range)

## Expected Output Format

### Select Story Node Output
```json
{
  "selected_story": {
    "title": "exact title from RSS feed",
    "summary": "exact summary from RSS feed",
    "source": "RSS feed name",
    "story_number": 1,
    "hours_old": 24,
    "emotional_impact": 5,
    "global_relevance": 4,
    "specificity": 5,
    "total_score": 14,
    "verification": "confirmed_from_list"
  },
  "selection_reason": "explanation of why selected",
  "all_stories_scoring": [
    // Scoring for ALL evaluated stories
  ]
}
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Referenced node doesn't exist" | Verify node connections and use `$input.first()` syntax |
| JSON parsing errors | Check Structured Output Parser schema or use direct JSON output |
| Old stories appearing | Confirm all 10 date filter nodes are active |
| Hallucinated content | Verify all LLM nodes have temperature = 0 |
| Format Stories node failure | Use `$input.first().json.stories` not `items[0]` |
| Parser format errors | Consider removing Structured Output Parser for direct JSON |

## Testing Requirements

Before deployment verify:
- [ ] All RSS feeds return data successfully
- [ ] Date filters remove stories > 48 hours old
- [ ] Story selection outputs valid JSON with all fields
- [ ] Selected story exists in original feed list
- [ ] All stories receive scoring (not just winner)
- [ ] Article uses only provided information
- [ ] All 3 LLM nodes show temperature: 0
- [ ] Source tracking preserved through workflow
- [ ] Google Sheets receives all scoring data

## Manual Update Procedures

### Modifying RSS Feed Sources
1. Update corresponding "Set RSS Fields" node with new source name
2. Verify source flows through to Google Sheets
3. Test complete workflow end-to-end

### Adjusting Scoring Criteria
1. Modify Select Story prompt with new criteria
2. Update Structured Output Parser schema (if used)
3. Add corresponding Google Sheets columns
4. Test scoring output structure

### N8N Version Compatibility
- **N8N Cloud 1.110.1**: May require removing Structured Output Parser for complex JSON
- **Alternative**: Use enhanced prompts for direct JSON output without parser

## Development Workflow

### Common Tasks
```bash
# Check workflow status
make status

# Validate JSON structure before deployment
jq . "The Daily Energizer Article and Image Generator V3.json" > /dev/null && echo "Valid JSON"

# Generate documentation (if needed)
make create T=implementation-guide.md N=new-implementation.md

# Create backup before major changes
cp "The Daily Energizer Article and Image Generator V3.json" "backup-$(date +%Y%m%d).json"
```

### File Structure
```
workflows/daily-energizer/
├── The Daily Energizer Article and Image Generator V3.json  # Main workflow (2,513 lines, 86KB)
├── features/                                               # Feature documentation
│   ├── PRDs/                                              # Product Requirements
│   ├── ADRs/                                              # Architecture Decision Records
│   ├── requirements/                                      # Implementation guides
│   └── tasks/                                             # Task breakdowns
├── docs/                                                  # Additional documentation
└── ai-dev/                                               # AI development templates
```

### Critical Files
- **Main Workflow V4**: `The Daily Energizer Article and Image Generator V4.json` (Current production with enhanced features)
- **Legacy Workflow V3**: `The Daily Energizer Article and Image Generator V3.json` (86KB, 2,513 lines)
- **Legacy Workflow V2**: `The Daily Energizer Article and Image Generator V2-Jeremy.json` (83KB)
- **Implementation History**: `features/requirements/IMPLEMENTATION-GUIDE.md`
- **Client Requirements**: `features/requirements/BRENT-ACTION-PLAN.md`
- **Feature Summary**: `FEATURE-UPDATES-SUMMARY.md`
- **Manual Updates**: `MANUAL-UPDATE-GUIDE.md`

## Version Control & Backup Strategy

### Before Making Changes
1. **Always backup the main workflow file first**
2. **Test changes in N8N development environment**
3. **Validate JSON structure with jq**
4. **Document changes in appropriate feature files**

### Workflow Versioning
- **Current**: `The Daily Energizer Article and Image Generator V4.json` (Production)
- **Previous**: `The Daily Energizer Article and Image Generator V3.json` (Stable fallback - 86KB, 2,513 lines)
- **Legacy**: `The Daily Energizer Article and Image Generator V2-Jeremy.json` (83KB)
- **Backup naming**: `backup-YYYYMMDD.json`
- **Development versions** should include descriptive suffixes

## V4 New Features & Enhancements

### Enhanced Article Processing
- **Story-Centered Summary**: Generates focused 200-word summaries
- **Content Validation**: Ensures final signature line inclusion
- **Duplicate Prevention**: Remove Duplicates node prevents repeated stories

### Automated Image Generation
- **Image Processing Pipeline**: Converts shareable URLs to direct URLs
- **Google Drive Integration**: Transforms shareable links to viewable format
- **Image Preview**: Formula-based image preview in Google Sheets

### Advanced Google Sheets Integration
- **Review Status Tracking**: "Pending Approval" status for workflow control
- **Image URL Management**: Direct image URLs and preview formulas
- **Enhanced Data Structure**: Better organization of article data

### Key V4 Node Additions
- `Remove Duplicates` - Prevents story repetition
- `Write Story-Centered Summary` - Creates focused summaries
- `Ensure Final Line is Included` - Content validation
- `Transform Shareable URL to Direct URL` - Image processing
- `Update Status, Image URL and Image Preview Formula` - Enhanced sheets integration

## Documentation References

- **Technical Details**: See `features/requirements/IMPLEMENTATION-GUIDE.md`
- **Client Requirements**: See `features/requirements/BRENT-ACTION-PLAN.md`
- **Manual Updates**: See `MANUAL-UPDATE-GUIDE.md`
- **Feature Summary**: See `FEATURE-UPDATES-SUMMARY.md`