Generate and publish a technical blog post to startaitools.com AND create a Twitter/X thread in one command.

## Your Task

This command creates a blog post for startaitools.com (technical audience) AND generates a Twitter/X thread to promote it.

### Phase 1: Analyze Working Session (Once)

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent post date in `/home/jeremy/projects/blog/startaitools/content/posts/` (fallback: last 14 days)
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
   - Search existing posts in `/home/jeremy/projects/blog/startaitools/content/posts/`
   - Identify 2-3 related posts by keyword/topic matching
   - Note their titles and URLs for linking

### Phase 2: Write Technical Blog Post

3. **Write Technical Blog Post**
   - **Tone:** Technical, honest, factual - showcase abilities through real work
   - **Style:** Mix of case study + tutorial elements + technical depth with full problem-solving journey
   - **Structure:**
     - Title (clear, specific to what was built/solved)
     - Introduction (what problem we tackled, why it matters)
     - The Journey (what we tried, what failed, how we troubleshot - be honest!)
     - Technical Details (what was built, architecture, key decisions)
     - Implementation Notes (challenges, solutions, code examples, iterative refinements)
     - What We Learned (insights from the full session, not just the final solution)
     - Results/Outcomes (what works now, metrics if available, next steps)
     - Related Posts (cross-links to 2-3 relevant existing posts)
   - **Focus:** Deep technical implementation details for developers
   - **Educational aspect:** Show the thinking, not just the code. Include false starts and pivots.
   - Use Hugo front matter (YAML format):
     ```yaml
     ---
     title: "Clear Descriptive Title"
     date: 2025-MM-DDTHH:MM:SS-06:00
     draft: false
     tags: ["relevant", "tags"]
     author: "Jeremy Longshore"
     description: "SEO-friendly description"
     ---
     ```

### Phase 3: Ask for Thread Size

4. **Prompt for Thread Size**
   - Ask: "Thread size? (1-7)"
   - User responds with just the number: 1, 2, 3, 4, 5, 6, or 7
   - Default to 3 if no response

### Phase 4: Generate X Thread

5. **Create X Thread Based on Size**

   **Size 1 (Single Tweet):**
   - Hook + Key insight + Link + Hashtags
   - Max 280 characters

   **Size 2 (Mini Thread):**
   - Tweet 1: Hook → Key insight
   - Tweet 2: Link + CTA + Hashtags

   **Size 3 (Quick Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Key technical insight or result
   - Tweet 3: Link + CTA + Hashtags

   **Size 4 (Short Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem you solved
   - Tweet 3: Technical solution approach
   - Tweet 4: Link + CTA + Hashtags

   **Size 5 (Standard Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem context
   - Tweet 3: Technical approach
   - Tweet 4: Key result or insight
   - Tweet 5: Link + CTA + Hashtags

   **Size 6 (Medium Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem context
   - Tweet 3: Technical approach
   - Tweet 4: Key insight #1
   - Tweet 5: Key insight #2
   - Tweet 6: Link + CTA + Hashtags

   **Size 7 (Extended Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem context
   - Tweet 3: Technical approach
   - Tweet 4: Key insight #1
   - Tweet 5: Key insight #2
   - Tweet 6: Results and impact
   - Tweet 7: Link + CTA + Hashtags

### Phase 5: Show Both for Review

6. **Present Blog Post and Thread**
   - Show complete blog post first
   - Show X thread with numbering
   - Show character counts for each tweet
   - Ask: "Ready to publish? (yes/edit/cancel)"
   - Wait for approval

### Phase 6: Publish Both (After Approval)

7. **Publish Blog Post**
   - Create file: `/home/jeremy/projects/blog/startaitools/content/posts/[slug].md`
   - Run: `cd /home/jeremy/projects/blog/startaitools && hugo --gc --minify --cleanDestinationDir`
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
   - **Post thread directly to X/Twitter**
   - **Chain replies for multi-tweet threads**
   - **Save thread with metadata:** `/home/jeremy/projects/blog/x-threads/YYYY-MM-DD-slug-startai-x[size].md`

9. **Track Analytics (NEW)**
   - Import analytics helpers: `sys.path.append('/home/jeremy/analytics')`
   - Auto-add blog post: `auto_add_blog_post(blog_file_path, 'startaitools')`
   - Auto-add X thread: `auto_add_x_thread(thread_file_path, blog_post_slug)`
   - Update monthly analytics: `update_monthly_analytics('startaitools')`
   - Report analytics summary: word count, character count, thread details

10. **Confirm Deployment**
    - Verify blog build succeeded
    - Confirm blog deployment initiated
    - Report live blog URL
    - Provide X thread file location
    - Show analytics tracking confirmation

## Key Principles

- **Single analysis, dual output** - Same work session becomes blog post + X promotion
- Be honest and factual (no fluff)
- **Show the entire journey** - problems, false starts, troubleshooting, solutions
- Showcase Jeremy's technical abilities through real problem-solving process
- Educational value comes from seeing HOW decisions were made, not just WHAT was decided
- Document what didn't work as much as what did - readers learn from both
- Cross-link to related content when relevant
- Technical depth for developers
- SEO-optimized with proper tags and descriptions

## Thread Best Practices

- **TL;DR at START** - put key insight first (not at bottom) for fast scrollers
- **Hook in first tweet** - grab attention immediately after TL;DR
- **Technical but accessible** - explain jargon briefly
- **One idea per tweet** - keep it scannable
- **Strong CTA** - drive traffic back to full post
- **Minimal hashtags** - 1-2 max, highly relevant
- **Line breaks** for readability

## Critical Reminders

- **Review the FULL conversation history** - not just git commits
- What you're writing about just happened in this session - use that context!
- The troubleshooting steps and iterative refinements are the most valuable parts
- Don't present a polished "final solution" - show the messy real process
- If we tried 3 things before one worked, document all 3 attempts
- Thread should tease the blog post, not replace it

## Response Options

After showing drafts:
- **"yes"** - Publish blog post and save X thread
- **"edit"** - Make changes before publishing
- **"cancel"** - Don't publish either

## Example Invocation

User runs `/blog-startai-x` from any project directory after completing work:
1. Analyzes the complete session
2. Asks "Thread size? (1-7)"
3. User responds "3"
4. Generates technical blog post + 3-tweet thread
5. Shows both for review
6. Publishes blog + saves thread after approval

**Result:** Technical blog post live on startaitools.com + X thread ready to copy-paste within 5 minutes.