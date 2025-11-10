## Layout Blueprint — DIAGPRO Vertex→PDF

### 1. Cover & Header
- **REPORT_ID** fixed in top-right tag.
- **SUMMARY** hero paragraph below header banner.
- **CONFIDENCE** percentage badge next to summary.

### 2. Safety Strip
- Render **SAFETY_FLAGS** immediately after summary.
- Each flag shown as colored callout (CRITICAL = red, WARNING = amber, NOTICE = blue) with `DESCRIPTION` and bold `ACTION`.
- Omit section when list empty.

### 3. Findings Stack
- Title: “Primary Findings”.
- For each **FINDINGS** entry, show `TITLE`, supporting `DETAIL`, and confidence meter tied to field `CONFIDENCE`.
- If more than 4 findings, show first 4 and append “+N more” bullet.

### 4. Recommendation Matrix
- Title: “Recommended Next Steps”.
- Group **RECOMMENDATIONS** by `READINESS` buckets:
  - CUSTOMER — tasks owner can do now.
  - PROFESSIONAL — items requiring certified technician.
  - SCHEDULE — items to calendar for later.
- Within each group, display ordered `STEPS` as numbered list. Collapse after 5 steps with “+N more”.

### 5. Confidence Block
- Present block titled “Confidence Assessment”.
- Show **CONFIDENCE** value with gauge.
- If CONFIDENCE < threshold, include shaded box “To raise confidence” populated from **UPLIFT** items. Each entry single-line bullet. If no items, display “No additional actions required.”

### 6. Readiness Footer
- Footer ribbon across bottom of final page.
- Display **CUSTOMER_READINESS_CHECK.VERDICT** in uppercase badge.
- Adjacent text: **CUSTOMER_READINESS_CHECK.SHORT_REASON** (truncate beyond 220 characters).

### 7. Pagination & Length Controls
- Target total report length of 2–4 pages at 11pt.
- Use condensed typography to remain within limit.
- Whenever any repeatable list (FINDINGS, RECOMMENDATIONS, UPLIFT) exceeds visual space, truncate with “+N more”.
- Reserve page 1 for Summary, Safety, first Findings. Page 2 for remaining Findings and Recommendations. Keep Confidence block on page 3 if needed. Do not exceed 4 pages without stress override.
