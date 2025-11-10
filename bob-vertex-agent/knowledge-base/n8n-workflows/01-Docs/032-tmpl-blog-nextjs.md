Generate and publish a technical blog post to your Next.js blog that showcases your work and teaches others how to build similar solutions.

## Your Task

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent post date in your Next.js content directory (fallback: last 14 days)
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
   - Search existing posts in your Next.js content directory (e.g., `content/`, `posts/`, or `app/blog/`)
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
   - Use proper Next.js MDX front matter (YAML format):
     ```yaml
     ---
     title: "Clear Descriptive Title"
     date: "2025-MM-DD"
     description: "SEO-friendly description"
     tags: ["relevant", "tags"]
     author: "Your Name"
     image: "/images/post-image.jpg"
     ---
     ```

4. **Show Draft for Review**
   - Display the complete blog post
   - Show suggested cross-links
   - Ask: "Ready to publish? (yes/edit)"
   - Wait for approval or edits

5. **Publish (After Approval)**
   - Create file in appropriate Next.js directory:
     - App Router: `app/blog/[slug]/page.mdx` or `content/posts/slug.mdx`
     - Pages Router: `pages/blog/[slug].mdx` or `content/posts/slug.md`
   - Run: `npm run build` to verify build succeeds
   - Test locally: `npm run start` or `npm run dev`
   - Git commit with message: "feat: add blog post - [title]"
   - Git push to trigger deployment (Vercel/Netlify/etc.)
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

**IMPORTANT**: Before using this command, customize these settings for your Next.js blog:

1. **Content Directory**: Update path based on your Next.js blog structure:
   - `app/blog/` (App Router with MDX)
   - `content/posts/` (External content with contentlayer/next-mdx-remote)
   - `posts/` (Custom content directory)

2. **Routing Style**: Specify your routing approach:
   - App Router: `app/blog/[slug]/page.mdx`
   - Pages Router: `pages/blog/[slug].mdx`
   - Content layer: `content/posts/slug.md` with separate routing

3. **MDX Configuration**: Confirm your MDX setup (next-mdx-remote, contentlayer, @next/mdx)

4. **Build Commands**: Update if using custom scripts:
   - `npm run build` (standard)
   - `next build` (direct)
   - Custom build pipeline commands

5. **Deployment Platform**: Adjust for your hosting:
   - Vercel (auto-deploy on push)
   - Netlify (configure netlify.toml)
   - Self-hosted (custom deployment)

## Example Invocation
User runs `/blog-nextjs-technical` from any project directory after completing work. You analyze:
1. The complete conversation we just had
2. Git commits since last post
3. The problems we solved and how we solved them
4. Everything we learned in this session - even stuff not in git yet