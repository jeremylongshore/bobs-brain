# HUSTLE Survey - Response Persistence Investigation
**Date**: 2025-10-11
**Issue**: Survey not remembering user responses when navigating between sections
**Status**: ROOT CAUSE IDENTIFIED

---

## Problem Summary

Users report that the HUSTLE Survey (15-section, 76-question survey) is not remembering their responses when they navigate between sections. This creates a poor user experience as users have to re-enter data.

---

## Architecture Analysis

### Current Implementation

The survey uses a **multi-page architecture** with 15 separate Astro pages:
- `/survey/1.astro` through `/survey/15.astro`
- Each section is a standalone page
- Navigation is handled client-side with JavaScript
- Data persistence uses **sessionStorage**

### State Management Flow

```
User Input → Validation → sessionStorage → Next Page → Load sessionStorage → Repopulate Fields
```

**Storing data** (on "next" click):
```javascript
sessionStorage.setItem('survey_section_2', JSON.stringify(sectionData));
```

**Loading data** (on page load):
```javascript
const sectionData = sessionStorage.getItem('survey_section_2');
// Parse and restore form field values
```

---

## ROOT CAUSE IDENTIFIED

### ❌ **The Problem: NO DATA RESTORATION ON PAGE LOAD**

I examined multiple survey pages (sections 1, 2, 5, 15) and found:

1. **✅ Data IS being saved** to sessionStorage when "next" button is clicked
2. **❌ Data IS NOT being restored** when returning to a previous section

### Evidence from Code Analysis

**Section 2 (lines 350-424):**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  // Check consent
  const consent = sessionStorage.getItem('survey_consent');

  // Handle next button - SAVES data
  nextBtn?.addEventListener('click', () => {
    // ... validation ...
    sessionStorage.setItem('survey_section_2', JSON.stringify(sectionData));
    window.location.href = '/survey/3';
  });

  // Back button - ONLY navigates, doesn't restore data
  backBtn?.addEventListener('click', () => {
    window.location.href = '/survey/1';
  });
});
```

**Missing**: Code to restore form field values from sessionStorage on page load

---

## What's Working

1. ✅ **Consent check**: All pages verify consent before allowing access
2. ✅ **Data saving**: Each section saves responses to sessionStorage
3. ✅ **Final submission**: Section 15 collects ALL sessionStorage data and submits to Netlify
4. ✅ **Validation**: Required fields are validated before advancing
5. ✅ **Navigation**: Forward/backward navigation functions correctly

---

## What's Broken

1. ❌ **No data restoration**: When user clicks "back" or manually navigates to a previous section, form fields are empty
2. ❌ **No visual feedback**: Users don't know their data was saved
3. ❌ **Poor UX**: Users must re-enter data if they navigate backwards
4. ❌ **Inconsistent state**: sessionStorage has data, but UI doesn't reflect it

---

## Example User Journey (Current Broken Behavior)

```
1. User completes Section 2 (8 questions)
   → Data saved to sessionStorage: ✅
   → Navigates to Section 3: ✅

2. User realizes they made a mistake in Section 2
   → Clicks "back" button: ✅
   → Returns to Section 2: ✅
   → Form fields are EMPTY: ❌ BUG!
   → Data still exists in sessionStorage: ✅
   → User must re-enter all 8 answers: ❌ TERRIBLE UX!
```

---

## Technical Details

### SessionStorage Structure

Each section stores data as JSON:
```javascript
{
  "survey_section_1": {"consent": "yes"},
  "survey_section_2": {
    "numAthletes": "2",
    "grades": ["7th", "9th"],
    "hoursPerWeek": "11-15",
    "collegeRecruitment": "maybe-future",
    "sports": ["soccer", "basketball"],
    "sportsOther": "",
    "competitionLevel": ["hs-varsity", "travel-club"],
    "competitionLevelOther": "",
    "clubsTeams": "Gulf Shores FC",
    "location": "Gulf Shores, AL"
  },
  // ... sections 3-15
}
```

### Form Field Types

- **Radio buttons**: `<input type="radio" name="fieldName" value="option">`
- **Checkboxes**: `<input type="checkbox" name="fieldName" value="option">`
- **Text inputs**: `<input type="text" name="fieldName">`
- **Email**: `<input type="email" name="email">`
- **Phone**: `<input type="tel" name="phone">`

---

## Solution Required

### Add Data Restoration on Page Load

Each survey page needs this logic added to `DOMContentLoaded`:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  // 1. Check consent (existing)
  const consent = sessionStorage.getItem('survey_consent');
  if (!consent || consent !== 'yes') {
    window.location.href = '/survey/1';
    return;
  }

  // 2. RESTORE FORM DATA (MISSING - NEEDS TO BE ADDED!)
  restoreFormData();

  // 3. Handle navigation (existing)
  nextBtn?.addEventListener('click', () => { /* ... */ });
  backBtn?.addEventListener('click', () => { /* ... */ });
});

// NEW FUNCTION NEEDED
function restoreFormData() {
  const sectionData = sessionStorage.getItem('survey_section_X');
  if (!sectionData) return;

  try {
    const data = JSON.parse(sectionData);

    // Restore radio buttons
    if (data.fieldName) {
      const radio = document.querySelector(
        `input[name="fieldName"][value="${data.fieldName}"]`
      );
      if (radio) radio.checked = true;
    }

    // Restore checkboxes (arrays)
    if (Array.isArray(data.arrayField)) {
      data.arrayField.forEach(value => {
        const checkbox = document.querySelector(
          `input[name="arrayField"][value="${value}"]`
        );
        if (checkbox) checkbox.checked = true;
      });
    }

    // Restore text inputs
    if (data.textField) {
      const input = document.querySelector('input[name="textField"]');
      if (input) input.value = data.textField;
    }
  } catch (e) {
    console.error('Error restoring form data:', e);
  }
}
```

---

## Implementation Plan

### Phase 1: Create Restoration Utility Function
Create `/astro-site/src/utils/surveyRestore.ts`:
```typescript
export function restoreSurveySection(sectionNumber: number) {
  const sectionData = sessionStorage.getItem(`survey_section_${sectionNumber}`);
  if (!sectionData) return;

  try {
    const data = JSON.parse(sectionData);

    // Generic restoration logic for all field types
    Object.entries(data).forEach(([fieldName, fieldValue]) => {
      if (Array.isArray(fieldValue)) {
        // Restore checkboxes
        fieldValue.forEach(value => {
          const checkbox = document.querySelector(
            `input[name="${fieldName}"][value="${value}"]`
          ) as HTMLInputElement;
          if (checkbox) checkbox.checked = true;
        });
      } else if (typeof fieldValue === 'string') {
        // Try radio first
        const radio = document.querySelector(
          `input[type="radio"][name="${fieldName}"][value="${fieldValue}"]`
        ) as HTMLInputElement;

        if (radio) {
          radio.checked = true;
        } else {
          // Try text/email/tel input
          const input = document.querySelector(
            `input[name="${fieldName}"], textarea[name="${fieldName}"]`
          ) as HTMLInputElement | HTMLTextAreaElement;

          if (input) input.value = fieldValue;
        }
      }
    });
  } catch (e) {
    console.error(`Error restoring section ${sectionNumber}:`, e);
  }
}
```

### Phase 2: Update All 15 Survey Pages
Add to each section's `<script>` tag:
```javascript
import { restoreSurveySection } from '../../utils/surveyRestore';

document.addEventListener('DOMContentLoaded', () => {
  // ... existing consent check ...

  // ADD THIS LINE:
  restoreSurveySection(X); // Replace X with section number

  // ... rest of existing code ...
});
```

### Phase 3: Add Visual Feedback
Optional enhancement - show users their data was restored:
```javascript
// After restoration
const restoredCount = Object.keys(data).length;
if (restoredCount > 0) {
  showToast(`✅ Restored ${restoredCount} previous answers`);
}
```

---

## Testing Checklist

After implementing fix:

- [ ] Complete Section 1 → Navigate to Section 2 → Back to Section 1 → Verify fields populated
- [ ] Complete Sections 1-5 → Navigate to Section 15 → Back to Section 3 → Verify fields populated
- [ ] Complete entire survey → Submit → Verify all data received by Netlify
- [ ] Test with checkboxes (multiple selections)
- [ ] Test with radio buttons (single selection)
- [ ] Test with text fields
- [ ] Test with email/phone fields
- [ ] Test browser refresh on any section (should redirect to Section 1 if no consent)
- [ ] Test sessionStorage persistence across page navigations
- [ ] Test clearing sessionStorage after submission

---

## Files Requiring Changes

1. `/astro-site/src/utils/surveyRestore.ts` - NEW FILE
2. `/astro-site/src/pages/survey/1.astro` - Add restoration call
3. `/astro-site/src/pages/survey/2.astro` - Add restoration call
4. `/astro-site/src/pages/survey/3.astro` - Add restoration call
5. `/astro-site/src/pages/survey/4.astro` - Add restoration call
6. `/astro-site/src/pages/survey/5.astro` - Add restoration call
7. `/astro-site/src/pages/survey/6.astro` - Add restoration call
8. `/astro-site/src/pages/survey/7.astro` - Add restoration call
9. `/astro-site/src/pages/survey/8.astro` - Add restoration call
10. `/astro-site/src/pages/survey/9.astro` - Add restoration call
11. `/astro-site/src/pages/survey/10.astro` - Add restoration call
12. `/astro-site/src/pages/survey/11.astro` - Add restoration call
13. `/astro-site/src/pages/survey/12.astro` - Add restoration call
14. `/astro-site/src/pages/survey/13.astro` - Add restoration call
15. `/astro-site/src/pages/survey/14.astro` - Add restoration call
16. `/astro-site/src/pages/survey/15.astro` - Add restoration call (already has similar logic for final submission)

---

## Risk Assessment

**Risk**: Low
**Complexity**: Medium
**Impact**: High (Critical UX fix)

### Risks
- Potential TypeScript/import issues in Astro
- Field name mismatches between saved data and form fields
- Browser compatibility with sessionStorage

### Mitigation
- Test thoroughly in multiple browsers
- Add error handling for missing fields
- Log restoration attempts for debugging

---

## Additional Findings

1. **Section 15 already has restoration logic** for hidden fields (lines 284-325)
   - This proves the architecture CAN support restoration
   - Just need to apply same pattern to visible form fields

2. **Console logging would help debugging**
   - Add `console.log('Restored section X data:', data);`
   - Helps users/devs verify data persistence

3. **Consider progress indicator enhancement**
   - Show checkmarks on completed sections
   - Visual feedback that sections are "saved"

---

## Estimated Implementation Time

- **Phase 1** (Utility function): 30 minutes
- **Phase 2** (Update 15 pages): 1-2 hours
- **Phase 3** (Testing): 1-2 hours
- **Total**: 3-4 hours

---

## Conclusion

**The bug is confirmed**: Survey pages save data correctly but do NOT restore it on page load.

**Fix required**: Add form field restoration logic to all 15 survey pages using sessionStorage data.

**User impact**: Critical UX issue - users cannot review/change previous answers without re-entering everything.

**Next steps**: Implement restoration utility function and update all survey pages.

---

**Investigation completed**: 2025-10-11
**Investigator**: Claude Code
