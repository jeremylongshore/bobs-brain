Generate and publish a technical blog post to your Gatsby blog that showcases your work and teaches others how to build similar solutions.

## Your Task

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent post date in your Gatsby `content/posts/` or `src/pages/blog/` directory (fallback: last 14 days)
   - **Current Conversation**: Review the COMPLETE conversation history from this session
     - What problem were we solving?
     - What questions did the user ask?
     - What solutions did we try that failed?
     - What troubleshooting steps did we take?
     - What was the iterative problem-solving process?
     - What did we learn along the way?
   - **Project Context**: Examine file changes, TODO lists, documentation files in CURRENT directory
   - **Missed Opportunities**: Identify anything valuable we worked on that might not be in git yet
   - **The Journey**: Capture the full story - false starts, pivots, discoveries, not just the final solution

2. **Find Cross-Links**
   - Search existing posts in your Gatsby content directory
   - Identify 2-3 related posts by keyword/topic matching
   - Note their titles and URLs for linking

3. **Write the Blog Post**
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
   - **Focus:** Showcase what was built AND how it was built - the real process
   - **Educational aspect:** Show the thinking, not just the code. Include false starts and pivots.
   - **Critical:** Don't sanitize the process - readers learn more from seeing the troubleshooting
   - Use proper Gatsby front matter (YAML format):
     ```yaml
     ---
     title: "Clear Descriptive Title"
     date: "2025-MM-DD"
     description: "SEO-friendly description"
     tags: ["relevant", "tags"]
     category: "category-name"
     slug: "/blog/post-slug"
     ---
     ```

4. **Show Draft for Review**
   - Display the complete blog post
   - Show suggested cross-links
   - Ask: "Ready to publish? (yes/edit)"
   - Wait for approval or edits

5. **Publish (After Approval)**
   - Create file in appropriate Gatsby content directory (e.g., `content/posts/slug.md` or `src/pages/blog/slug.mdx`)
   - Run: `npm run build` or `gatsby build` to verify build succeeds
   - Git commit with message: "feat: add blog post - [title]"
   - Git push to trigger deployment (Netlify/Vercel/GitHub Pages)
   - Confirm deployment initiated

## Key Principles
- Be honest and factual (no fluff, no marketing speak)
- **Show the entire journey** - problems, false starts, troubleshooting, solutions
- Showcase technical abilities through real problem-solving process
- Educational value comes from seeing HOW decisions were made, not just WHAT was decided
- Include conversation context - the questions asked reveal the thinking process
- Document what didn't work as much as what did - readers learn from both
- Cross-link to related content when relevant
- Technical depth appropriate for developer audience
- SEO-optimized with proper tags and descriptions

## Critical Reminders
- **Review the FULL conversation history** - not just git commits
- What you're writing about just happened in this session - use that context!
- The troubleshooting steps and iterative refinements are the most valuable parts
- Don't present a polished "final solution" - show the messy real process
- If we tried 3 things before one worked, document all 3 attempts

## Customization Required

**IMPORTANT**: Before using this command, customize these paths for your Gatsby blog:

1. **Content Directory**: Update path to your Gatsby content location (commonly `content/posts/` or `src/pages/blog/`)
2. **Front Matter Format**: Adjust fields to match your Gatsby setup (some use MDX, some Markdown)
3. **Build Command**: Update `npm run build` if using custom build script
4. **File Extension**: Change to `.mdx` if using MDX instead of Markdown
5. **Slug Format**: Adjust slug pattern to match your Gatsby routing configuration
6. **Deployment**: Confirm git push triggers your hosting provider rebuild

## Example Invocation
User runs `/blog-gatsby-technical` from any project directory after completing work. You analyze:
1. The complete conversation we just had
2. Git commits since last post
3. The problems we solved and how we solved them
4. Everything we learned in this session - even stuff not in git yet