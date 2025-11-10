Generate and publish blog posts to BOTH startaitools.com AND jeremylongshore.com PLUS create a Twitter/X thread in one command.

## Your Task

This command creates TWO blog posts (technical + portfolio) AND generates a Twitter/X thread to promote them.

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

2. **Find Cross-Links for Both Sites**
   - Search existing posts in `/home/jeremy/projects/blog/startaitools/content/posts/`
   - Search existing posts in `/home/jeremy/projects/blog/jeremylongshore/content/posts/`
   - Identify 2-3 related posts per site by keyword/topic matching
   - Note their titles and URLs for linking

### Phase 2: Write Both Blog Posts

3. **Write Technical Blog Post (StartAITools)**
   - **Tone:** Technical, honest, factual - showcase abilities through real work
   - **Style:** Mix of case study + tutorial elements + technical depth with full problem-solving journey
   - **Focus:** Deep technical implementation details for developers
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

4. **Write Portfolio Blog Post (JeremyLongshore)**
   - **Tone:** Professional, career-focused, demonstrates problem-solving
   - **Style:** Narrative showcasing capabilities for employers/clients
   - **Same content, different narrative:**
     - Focus on professional methodology and business impact
     - Highlight transferable skills and systematic approach
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

5. **Prompt for Thread Size**
   - Ask: "Thread size? (1-7)"
   - User responds with just the number: 1, 2, 3, 4, 5, 6, or 7
   - Default to 3 if no response

### Phase 4: Generate X Thread

6. **Create X Thread Based on Size (Technical Focus)**

   **Size 1 (Single Tweet):**
   - Technical hook + Key insight + Links to BOTH posts + Hashtags
   - Max 280 characters

   **Size 2 (Mini Thread):**
   - Tweet 1: Hook → Key technical insight
   - Tweet 2: Links to both posts + CTA + Hashtags

   **Size 3 (Quick Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Key technical insight or result
   - Tweet 3: Links to both posts (technical + portfolio) + CTA + Hashtags

   **Size 4 (Short Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem you solved
   - Tweet 3: Technical solution approach
   - Tweet 4: Links to both posts + CTA + Hashtags

   **Size 5 (Standard Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem context
   - Tweet 3: Technical approach
   - Tweet 4: Key result or insight
   - Tweet 5: Links to both posts (technical + portfolio) + CTA + Hashtags

   **Size 6 (Medium Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem context
   - Tweet 3: Technical approach
   - Tweet 4: Key insight #1
   - Tweet 5: Key insight #2
   - Tweet 6: Links to both posts + CTA + Hashtags

   **Size 7 (Extended Thread):**
   - Tweet 1: Hook + what you built
   - Tweet 2: Problem context
   - Tweet 3: Technical approach
   - Tweet 4: Key insight #1
   - Tweet 5: Key insight #2
   - Tweet 6: Results and impact
   - Tweet 7: Links to both posts (technical + portfolio) + CTA + Hashtags

### Phase 5: Show All for Review

7. **Present Both Posts and Thread**
   - Show StartAITools post first (technical version)
   - Show JeremyLongshore post second (portfolio version)
   - Show X thread with numbering
   - Show character counts for each tweet
   - Ask: "Ready to publish all? (yes/edit/skip-one/cancel)"
   - Wait for approval

### Phase 6: Publish All (After Approval)

8. **Publish to StartAITools**
   - Create file: `/home/jeremy/projects/blog/startaitools/content/posts/[slug].md`
   - Run: `cd /home/jeremy/projects/blog/startaitools && hugo --gc --minify --cleanDestinationDir`
   - Verify build succeeds
   - Git commit: "feat: add blog post - [title]"
   - Git push to trigger Netlify deployment

9. **Publish to JeremyLongshore**
   - Create file: `/home/jeremy/projects/blog/jeremylongshore/content/posts/[slug].md`
   - Run: `cd /home/jeremy/projects/blog/jeremylongshore && hugo --gc --minify --cleanDestinationDir`
   - Verify build succeeds
   - Git commit: "feat: add blog post - [title]"
   - Git push to trigger Netlify deployment

10. **Post X Thread Directly**
    - **Load X API credentials from Waygate MCP:**
      ```bash
      export X_API_KEY="thpZd6tCyjgYJVTr0waBx2RolP"
      export X_API_SECRET="tAnB8BhULV3J4sfP2HC5qSot5ShVHKxoNP60UoJWBlqZpFOTnh9"
      export X_OAUTH2_ACCESS_TOKEN="YjJUUFJTN3g5Zl91eFJ2cjZGUEV6Q0k4OFdUYUpFOFF5X3Jmc3R6aXpzMkMzOjE3NTkwNDIwMTg0NzE6MTowOmF0OjE"
      ```
    - **Post first tweet:**
      ```bash
      curl -X POST "https://api.twitter.com/2/tweets" \
        -H "Authorization: Bearer $X_OAUTH2_ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"text": "Tweet 1 content here"}'
      ```
    - **For multi-tweet threads, chain replies:**
      ```bash
      # Get tweet ID from first response, then:
      curl -X POST "https://api.twitter.com/2/tweets" \
        -H "Authorization: Bearer $X_OAUTH2_ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"text": "Tweet 2 content", "reply": {"in_reply_to_tweet_id": "FIRST_TWEET_ID"}}'
      ```
    - **Save thread with metadata:**
      - File: `/home/jeremy/projects/blog/x-threads/YYYY-MM-DD-slug-both-x[size].md`
      - Include: Tweet IDs, timestamps, character counts, engagement tracking
      - Format for analytics and future reference

11. **Confirm All Deployments**
    - Verify both blog builds succeeded
    - Confirm both blog deployments initiated
    - Report both live blog URLs
    - Provide X thread file location

## Key Principles

- **Single analysis, triple output** - Same work session becomes 2 blog posts + X promotion
- **Different audiences require different framing:**
  - StartAITools: "Here's how to build this" (teaching developers)
  - JeremyLongshore: "Here's how I solved this" (showcasing to employers)
  - X Thread: "Here's what I accomplished" (broad professional network)
- Be honest and factual (no fluff)
- **Show the entire journey** - problems, false starts, troubleshooting, solutions
- Educational value comes from seeing HOW decisions were made, not just WHAT was decided
- Document what didn't work as much as what did - readers learn from both
- Cross-link to related content when relevant

## Thread Best Practices

- **Dual promotion** - mention both technical deep-dive AND portfolio view
- **Hook in first tweet** - grab attention immediately
- **Technical but accessible** - explain jargon briefly
- **Strong CTA** - drive traffic to BOTH posts
- **Professional hashtags** - mix technical and career-focused

## Critical Reminders

- **Review the FULL conversation history** - not just git commits
- What you're writing about just happened in this session - use that context!
- The troubleshooting steps and iterative refinements are the most valuable parts
- Don't present a polished "final solution" - show the messy real process
- Thread should promote BOTH posts with clear value proposition for each

## Response Options

After showing drafts:
- **"yes"** - Publish both blog posts and save X thread
- **"edit"** - Make changes before publishing
- **"skip-startaitools"** - Only publish jeremylongshore + thread
- **"skip-jeremylongshore"** - Only publish startaitools + thread
- **"cancel"** - Don't publish anything

## Example Invocation

User runs `/blog-both-x` from any project directory after completing work:
1. Analyzes the complete session
2. Asks "Thread size? (1-7)"
3. User responds "5"
4. Generates technical post + portfolio post + 5-tweet thread
5. Shows all three for review
6. Publishes both blogs + saves thread after approval

**Result:** Two blog posts live (startaitools.com + jeremylongshore.com) + X thread promoting both within 5 minutes.