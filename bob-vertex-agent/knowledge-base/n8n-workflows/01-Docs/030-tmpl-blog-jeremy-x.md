Generate and publish a portfolio blog post to jeremylongshore.com AND create a Twitter/X thread in one command.

## Your Task

This command creates a blog post for jeremylongshore.com (professional/career audience) AND generates a Twitter/X thread to promote it.

### Phase 1: Analyze Working Session (Once)

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent post date in `/home/jeremy/projects/blog/jeremylongshore/content/posts/` (fallback: last 14 days)
   - **Current Conversation**: Review the COMPLETE conversation history from this session
     - What problem were we solving?
     - What questions did Jeremy ask?
     - What solutions did we try that failed?
     - What troubleshooting steps did we take?
     - What was the iterative problem-solving process?
     - What did we learn along the way?
   - **Project Context**: Examine file changes, TODO lists, CLAUDE.md files in CURRENT directory
   - **Missed Opportunities**: Identify anything valuable we worked on that might not be in git yet
   - **The Journey**: Capture the full story - false starts, pivots, discoveries, not just the final solution

2. **Find Cross-Links**
   - Search existing posts in `/home/jeremy/projects/blog/jeremylongshore/content/posts/`
   - Identify 2-3 related posts by keyword/topic matching
   - Note their titles and URLs for linking

### Phase 2: Write Portfolio Blog Post

3. **Write Portfolio Blog Post**
   - **Tone:** Professional, career-focused, demonstrates problem-solving
   - **Style:** Narrative showcasing capabilities for employers/clients
   - **Same content, different narrative:**
     - Title (career-impact focused)
     - Challenge (business/professional context)
     - Approach (problem-solving methodology)
     - Solution (what was delivered)
     - Skills Demonstrated (highlight technical and soft skills)
     - Impact (professional growth, portfolio value)
     - Related Work (cross-links to 2-3 portfolio posts)
   - **Focus:** Problem-solving capabilities and professional growth
   - **Audience:** Employers, clients, recruiters
   - Use Hugo front matter (TOML format):
     ```toml
     +++
     title = 'Professional Title'
     date = 2025-MM-DDTHH:MM:SS-05:00
     draft = false
     tags = ["career", "skills"]
     +++
     ```

### Phase 3: Ask for Thread Size

4. **Prompt for Thread Size**
   - Ask: "Thread size? (1-7)"
   - User responds with just the number: 1, 2, 3, 4, 5, 6, or 7
   - Default to 3 if no response

### Phase 4: Generate X Thread

5. **Create X Thread Based on Size (Professional Tone)**

   **Size 1 (Single Tweet):**
   - Professional hook + Key achievement + Link + Hashtags
   - Max 280 characters

   **Size 2 (Mini Thread):**
   - Tweet 1: Professional hook → Key capability demonstrated
   - Tweet 2: Link + CTA + Professional hashtags

   **Size 3 (Quick Thread):**
   - Tweet 1: Hook + what you delivered/built
   - Tweet 2: Key skill or methodology demonstrated
   - Tweet 3: Link + CTA + Professional hashtags

   **Size 4 (Short Thread):**
   - Tweet 1: Hook + what you delivered
   - Tweet 2: Challenge you solved
   - Tweet 3: Professional approach/methodology
   - Tweet 4: Link + CTA + Professional hashtags

   **Size 5 (Standard Thread):**
   - Tweet 1: Hook + what you delivered
   - Tweet 2: Business/professional challenge
   - Tweet 3: Your approach and methodology
   - Tweet 4: Key result or capability demonstrated
   - Tweet 5: Link + CTA + Professional hashtags

   **Size 6 (Medium Thread):**
   - Tweet 1: Hook + what you delivered
   - Tweet 2: Business context and challenge
   - Tweet 3: Your problem-solving approach
   - Tweet 4: Key skill demonstrated #1
   - Tweet 5: Key skill demonstrated #2
   - Tweet 6: Link + CTA + Professional hashtags

   **Size 7 (Extended Thread):**
   - Tweet 1: Hook + what you delivered
   - Tweet 2: Business context and challenge
   - Tweet 3: Your systematic approach
   - Tweet 4: Key skill demonstrated #1
   - Tweet 5: Key skill demonstrated #2
   - Tweet 6: Professional impact and results
   - Tweet 7: Link + CTA + Professional hashtags

### Phase 5: Show Both for Review

6. **Present Blog Post and Thread**
   - Show complete blog post first
   - Show X thread with numbering
   - Show character counts for each tweet
   - Ask: "Ready to publish? (yes/edit/cancel)"
   - Wait for approval

### Phase 6: Publish Both (After Approval)

7. **Publish Blog Post**
   - Create file: `/home/jeremy/projects/blog/jeremylongshore/content/posts/[slug].md`
   - Run: `cd /home/jeremy/projects/blog/jeremylongshore && hugo --gc --minify --cleanDestinationDir`
   - Verify build succeeds
   - Git commit: "feat: add blog post - [title]"
   - Git push to trigger Netlify deployment

8. **Post X Thread Directly**
   - **Load X API credentials from Waygate MCP:**
     ```bash
     export X_API_KEY="thpZd6tCyjgYJVTr0waBx2RolP"
     export X_API_SECRET="tAnB8BhULV3J4sfP2HC5qSot5ShVHKxoNP60UoJWBlqZpFOTnh9"
     export X_OAUTH2_ACCESS_TOKEN="YjJUUFJTN3g5Zl91eFJ2cjZGUEV6Q0k4OFdUYUpFOFF5X3Jmc3R6aXpzMkMzOjE3NTkwNDIwMTg0NzE6MTowOmF0OjE"
     ```
   - **Post professional thread directly to X/Twitter**
   - **For multi-tweet threads, chain replies using in_reply_to_tweet_id**
   - **Save thread with metadata:** `/home/jeremy/projects/blog/x-threads/YYYY-MM-DD-slug-jeremy-x[size].md`

9. **Confirm Deployment**
   - Verify blog build succeeded
   - Confirm blog deployment initiated
   - Report live blog URL
   - Provide X thread file location

## Key Principles

- **Single analysis, dual output** - Same work session becomes portfolio post + professional X promotion
- Professional tone throughout
- **Showcase capabilities** - demonstrate skills and problem-solving abilities
- **Career-focused narrative** - frame work in terms of professional growth and value
- Educational value comes from seeing methodology and approach
- Cross-link to related portfolio work
- Professional depth appropriate for employers/clients/recruiters
- SEO-optimized with career-relevant tags

## Thread Best Practices (Professional Focus)

- **Professional hook** - showcase capabilities or achievements
- **Business context** - frame technical work in business terms
- **Methodology focus** - show your problem-solving approach
- **Career hashtags** - #SoftwareDeveloper #OpenSource #TechLeadership etc.
- **Network building** - invite professional discussion
- **Value proposition** - what you bring to organizations

## Critical Reminders

- **Review the FULL conversation history** - not just git commits
- Frame technical work in professional/business context
- Highlight transferable skills and methodologies
- Show systematic problem-solving approach
- Emphasize results and impact, not just technical details
- Professional tone suitable for employers and clients

## Response Options

After showing drafts:
- **"yes"** - Publish blog post and save X thread
- **"edit"** - Make changes before publishing
- **"cancel"** - Don't publish either

## Example Invocation

User runs `/blog-jeremy-x` from any project directory after completing work:
1. Analyzes the complete session
2. Asks "Thread size? (1-7)"
3. User responds "4"
4. Generates portfolio blog post + 4-tweet professional thread
5. Shows both for review
6. Publishes blog + saves thread after approval

**Result:** Portfolio blog post live on jeremylongshore.com + professional X thread ready to copy-paste within 5 minutes.