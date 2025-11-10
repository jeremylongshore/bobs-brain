Generate and publish a portfolio/CV-style blog post to jeremylongshore.com (Jeremy's personal professional site) that highlights career growth, professional achievements, and technical capabilities.

## Your Task

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent post date in `/home/jeremy/projects/blog/jeremylongshore/content/posts/` (fallback: last 14 days)
   - **Current Conversation**: Review the COMPLETE conversation history from this session
     - What challenges did Jeremy tackle?
     - What problem-solving approaches did he use?
     - What skills did he demonstrate?
     - What was the thinking process?
     - What did he learn?
   - **Project Context**: Examine file changes, TODO lists, CLAUDE.md files in CURRENT directory
   - **Professional Growth**: Understand what was accomplished from a career development perspective
   - **The Journey**: Capture the professional narrative - how he approached problems, not just what he built

2. **Write the Blog Post**
   - **Tone:** Professional, reflective, achievement-oriented (but still honest)
   - **Style:** Portfolio piece that demonstrates capabilities and growth through real work
   - **Structure:**
     - Title (professional, achievement-focused)
     - Introduction (what you've been working on professionally)
     - The Challenge (what problem needed solving)
     - The Approach (how you tackled it - show problem-solving abilities)
     - The Work (what was built/accomplished, technologies used)
     - Professional Growth (skills developed, challenges overcome, lessons learned)
     - Impact/Results (what this demonstrates about capabilities)
     - Looking Forward (next challenges, areas of growth)
   - **Focus:** Resume-building narrative through demonstrated problem-solving
   - **Depth:** Less technical detail than startaitools, more career progression focus
   - **Authenticity:** Show real work and real learning - portfolio readers value honesty
   - Use proper Hugo front matter (TOML format for jeremylongshore):
     ```toml
     +++
     title = 'Professional Achievement Title'
     date = 2025-MM-DDTHH:MM:SS-05:00
     draft = false
     tags = ["career", "development", "relevant-tech"]
     +++
     ```

3. **Show Draft for Review**
   - Display the complete blog post
   - Ask: "Ready to publish? (yes/edit)"
   - Wait for approval or edits

4. **Publish (After Approval)**
   - Create file: `/home/jeremy/projects/blog/jeremylongshore/content/posts/[slug].md`
   - Run: `cd /home/jeremy/projects/blog/jeremylongshore && hugo --gc --minify --cleanDestinationDir`
   - Verify build succeeds
   - Git commit with message: "feat: add blog post - [title]"
   - Git push to trigger Netlify deployment
   - Confirm deployment initiated

## Key Principles
- Professional and polished tone (CV/resume audience)
- Focus on career growth and capability demonstration through real problem-solving
- Honest reflection on accomplishments and learning (including challenges faced)
- Less code, more narrative about professional development and thinking process
- Showcase technical capabilities through how problems were approached and solved
- Appropriate for potential employers/clients/collaborators
- **Show the journey** - employers want to see how you think and work, not just results

## Critical Reminders
- **Review the FULL conversation history** - the problem-solving process is what employers want to see
- What you're writing about just happened in this session - use that context!
- Career growth comes from overcoming challenges - document the challenges honestly
- The iterative process shows adaptability and learning - valuable professional traits

## Example Invocation
User runs `/blogjeremylongshore` from any project directory after completing work. You analyze:
1. The complete conversation and problem-solving approach
2. Git commits since last post
3. Skills demonstrated through real work
4. Professional growth and learning from this session