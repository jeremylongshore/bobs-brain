# 🔧 Step-by-Step Implementation Plan

**Date:** September 19, 2025
**Project:** Daily Energizer Workflow V4 Enhancements
**Client:** Brent Hunter

---

## **Phase 1: Source URL Capture (Tasks 1-2)**

### Step 1: Update RSS "Set Fields" Nodes
**For each of the 10 RSS feeds:**
```javascript
// Current fields + new source_url field
{
  "title": "={{ $json.title }}",
  "summary": "={{ $json.content }}",
  "pubDate": "={{ $json.pubDate }}",
  "source": "Good News Network",
  "source_url": "={{ $json.link || $json.url || $json.guid || '' }}" // NEW FIELD
}
```

### Step 2: Update Main Google Sheets Node
**Add to "Add Article and Article Info to Sheet" node:**
```javascript
columns: {
  // Existing fields...
  "Source URL": "={{ $('Select Story').item.json.output.selected_story.source_url }}", // NEW MAPPING
}
```

---

## **Phase 2: Fix All Stories Data (Tasks 3-4)**

### Step 3: Add Missing Count Mapping
**In "Add Article and Article Info to Sheet" node:**
```javascript
"All Stories Count": "={{ $('Format Output').item.json.all_stories_scoring.length }}"
```

### Step 4: Add Missing Scoring Mapping
**In "Add Article and Article Info to Sheet" node:**
```javascript
"All Stories Scoring": "={{ JSON.stringify($('Format Output').item.json.all_stories_scoring) }}"
```

---

## **Phase 3: Story Evaluations Tab (Tasks 5-7)**

### Step 5: Create Preparation Function Node
**New Function Node: "Prepare Story Evaluations Data"**
```javascript
// Takes Format Output data and creates sorted array
const allStories = $input.first().json.all_stories_scoring;
const selectedStory = $input.first().json.selected_story;

// Sort by Total Score (highest first)
const sortedStories = allStories.sort((a, b) => b.total_score - a.total_score);

// Format for Google Sheets (11 columns exact order)
const sheetData = sortedStories.map(story => ({
  "Source": story.source,
  "Article Name": story.title,
  "Article URL": story.source_url || "",
  "Article Date": story.pubDate || "",
  "Emotional Impact Score": story.emotional_impact,
  "Global Relevance Score": story.global_relevance,
  "Specificity Score": story.specificity,
  "Total Score": story.total_score,
  "Selection Reason": story.story_number === selectedStory.story_number ? $input.first().json.selection_reason : "",
  "All Stories Count": allStories.length,
  "All Stories Scoring": JSON.stringify(allStories)
}));

return sheetData;
```

### Step 6: Create Story Evaluations Google Sheets Node
**New Google Sheets Node: "Update Story Evaluations Tab"**
```javascript
// Operation: Update
// Range: A2:K1000 (overwrites, preserves headers in row 1)
// Maps all 11 columns in exact order specified
```

### Step 7: Connect New Nodes
**Workflow Connection:**
```
Format Output → Prepare Story Evaluations Data → Update Story Evaluations Tab
```

---

## **Phase 4: RSS Source Analysis Tab (Tasks 8-12)**

### Step 8: Create RSS Statistics Collection Function
**New Function Node: "Collect RSS Statistics"**
```javascript
// Position: After all RSS feeds, before Remove Duplicates
// Collects stats from all 10 RSS feed branches

const stats = [];
const rssFeeds = [
  "Good News Network", "Positive News UK", "Sunny Skyz",
  "The Optimist Daily", "Good Good Good", "Nice News",
  "Epoch Times Bright", "Reasons to Be Cheerful",
  "YES! Magazine", "Not All News is Bad!"
];

// For each RSS source, count total and 48hr stories
rssFeeds.forEach(source => {
  const sourceItems = $input.all().filter(item => item.json.source === source);
  const totalStories = sourceItems.length;

  // Count stories within 48 hours
  const fortyEightHoursAgo = new Date();
  fortyEightHoursAgo.setHours(fortyEightHoursAgo.getHours() - 48);

  const recentStories = sourceItems.filter(item => {
    const storyDate = new Date(item.json.pubDate);
    return storyDate >= fortyEightHoursAgo;
  }).length;

  stats.push({
    "Source": source,
    "# of Stories": totalStories,
    "# Stories in Time Period": recentStories
  });
});

return stats;
```

### Step 9: Create RSS Analysis Google Sheets Node
**New Google Sheets Node: "Update RSS Source Analysis Tab"**
```javascript
// Operation: Update
// Sheet: RSS Source Analysis
// Range: A2:C20 (overwrites data, preserves headers)
// Columns: Source | # of Stories | # Stories in Time Period
```

### Step 10: Position RSS Analysis in Workflow
**Connection Point:**
```
Merge Stories → Collect RSS Statistics → Update RSS Source Analysis Tab
Remove Duplicates (continues main flow)
```

---

## **Phase 5: Testing & Validation (Implicit)**

### Step 11: Data Flow Verification
1. **Source URLs**: Verify clickable links in main sheet
2. **All Stories Data**: Confirm data appears in both locations
3. **Story Evaluations**: Check sorting and all 11 columns
4. **RSS Analysis**: Verify productivity calculations

### Step 12: Sheet Configuration
1. **Create new tabs** in Google Sheets
2. **Set headers** for each new tab
3. **Test overwrite behavior** (no appending)

---

## 📊 **Final Workflow Architecture**

```
10 RSS Feeds (with source_url)
↓
48 Hour Filters
↓
Merge Stories → [RSS Statistics] → RSS Analysis Tab
↓
Remove Duplicates
↓
Story Selection & Processing
↓
Main Sheet (with Source URL + All Stories data)
↓
[Story Evaluations] → Story Evaluations Tab
```

## 🎯 **Expected Results**

**3 Enhanced Google Sheets Tabs:**
1. **Articles** - Now includes Source URL, All Stories Count/Scoring
2. **Story Evaluations** - All stories sorted by score (11 columns)
3. **RSS Source Analysis** - Feed productivity metrics (3 columns)

**Business Intelligence Gained:**
- Clickable source verification
- Complete transparency in story selection
- RSS feed performance optimization data

## 📋 **Implementation Checklist**

### Phase 1: Source URL Capture
- [ ] Add source_url field to all 10 RSS 'Set Fields' nodes
- [ ] Update main Google Sheets node to populate 'Source URL' column

### Phase 2: Fix All Stories Data
- [ ] Add missing 'All Stories Count' mapping to main sheet
- [ ] Add missing 'All Stories Scoring' mapping to main sheet

### Phase 3: Story Evaluations Tab
- [ ] Create Story Evaluations tab with single Update node (not Clear + Append)
- [ ] Implement pre-sorted data by Total Score (highest to lowest)
- [ ] Set exact column order for Story Evaluations tab (11 columns)

### Phase 4: RSS Source Analysis Tab
- [ ] Create RSS Source Analysis tab for feed productivity analysis
- [ ] Implement story counting logic for total retrieved stories per source
- [ ] Implement story counting logic for 48-hour filtered stories per source
- [ ] Create RSS Source Analysis sheet with columns: Source, # of Stories, # Stories in Time Period
- [ ] Configure RSS Source Analysis tab to overwrite data each workflow run

### Phase 5: Testing & Validation
- [ ] Test all new functionality end-to-end
- [ ] Verify data accuracy and sheet formatting
- [ ] Confirm overwrite behavior works correctly

---

**Ready to implement? 🚀**

---

*Generated: September 19, 2025*
*Document Version: 1.0*