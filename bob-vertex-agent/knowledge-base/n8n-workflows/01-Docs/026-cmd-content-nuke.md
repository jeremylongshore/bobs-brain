Generate and publish content across ALL platforms in one content nuke: StartAITools blog, JeremyLongshore blog, X thread, and LinkedIn post.

## Your Task

This command takes ONE working session and creates FOUR optimized content pieces for maximum reach across your entire content ecosystem.

### Phase 1: Analyze Working Session (Once)

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent post date in both blog directories
   - **Current Conversation**: Review the COMPLETE conversation history from this session
     - What problem were we solving?
     - What technical challenges did we overcome?
     - What business value was created?
     - What personal insights were gained?
     - What tools/processes were built or improved?
   - **Project Context**: Examine file changes, TODO lists, CLAUDE.md files in CURRENT directory
   - **Content Angles**: Identify both technical AND personal story elements

2. **Find Cross-Links**
   - Search existing posts in both blog directories
   - Identify related posts for cross-linking
   - Note complementary content opportunities

### Phase 2: Content Adaptation Engine

3. **Generate Multi-Angle Content Strategy**

   **Business Lead Generation Angle** (StartAITools + LinkedIn):
   - Focus: Technical capabilities that drive business value, architectural solutions
   - Audience: Potential clients, CTOs, technical decision makers
   - Purpose: Generate leads for IntentSolutions.io business
   - Tone: Professional authority, proven expertise, scalable solutions
   - CTA: Subtle drive toward IntentSolutions.io for business inquiries

   **Hiring Evaluation Angle** (JeremyLongshore + X):
   - Focus: Problem-solving approach, professional competence, delivery capability
   - Audience: Hiring managers, potential employers, recruitment contacts
   - Purpose: Showcase hire-worthy qualities and professional growth
   - Tone: Authentic but competent, relatable but results-oriented
   - CTA: "This is how I work and deliver results"

### Phase 3: Ask for Thread Size & Intelligent Link Selection

4. **Prompt for Thread Size**
   - Ask: "Thread size? (1-7)"
   - User responds with just the number: 1, 2, 3, 4, 5, 6, or 7
   - Default to 3 if no response

5. **Intelligent Link Selection for X Thread**
   - Analyze last 30-45 minutes of session context
   - Determine most relevant link based on:
     - Primary project/repository being worked on
     - Tools or systems built/modified
     - If blog content focuses on specific project → link to that repo
     - If demonstrating general concept → link to StartAITools blog post
     - If personal journey story → link to JeremyLongshore blog post
     - If technical implementation → link to GitHub repository
   - Auto-select the most contextually relevant link
   - No manual picker needed - Claude decides intelligently

### Phase 4: Generate All Content

6. **StartAITools Blog Post** (Technical Deep-Dive)
   - Structure: Technical architecture, implementation details, business impact
   - Focus: What was built, how it works, why it matters professionally
   - Include: Code examples, architecture diagrams, performance metrics
   - Cross-link to related technical posts
   - Tags: Technical, business-focused

7. **JeremyLongshore Blog Post** (Personal Journey)
   - Structure: Challenge faced, learning process, personal growth, lessons learned
   - Focus: Human side of technical work, growth mindset, authentic experiences
   - Include: Behind-the-scenes insights, problem-solving approach, reflection
   - Cross-link to related personal posts
   - Tags: Personal development, learning-focused

8. **X Thread** (Personal Tone with TL;DR)
   - Format: TL;DR at START + personal insights + selected custom link
   - Tone: Match JeremyLongshore blog (conversational, authentic)
   - Focus: Quick insights, relatable experiences, growth moments
   - Thread sizes 1-7 as defined in blog-startai-x command

9. **LinkedIn Post** (Company/Professional)
   - Format: Professional achievement post for Intent Solutions company page
   - Focus: Business results, technical innovation, team capabilities
   - Include: Metrics, client value, industry leadership
   - Tone: Professional, results-driven, company brand building
   - Length: 1200-1500 characters optimal for LinkedIn

### Phase 5: Show All Content for Review

10. **Present Complete Content Package**
    - Show StartAITools blog post
    - Show JeremyLongshore blog post
    - Show X thread with numbering and character counts
    - Show LinkedIn post with character count
    - Ask: "Ready to publish content nuke? (yes/edit/cancel)"
    - Wait for approval

### Phase 6: Content Nuke Deployment

11. **Publish StartAITools Blog**
    - Create file: `/home/jeremy/projects/blog/startaitools/content/posts/[slug].md`
    - Run Hugo build and deploy
    - Git commit and push

12. **Publish JeremyLongshore Blog**
    - Create file: `/home/jeremy/projects/blog/jeremylongshore/content/posts/[slug].md`
    - Run Hugo build and deploy
    - Git commit and push

13. **Save X Thread**
    - Save to `/home/jeremy/projects/blog/x-threads/YYYY-MM-DD-slug-nuclear-x[size].txt`
    - Format with TL;DR at START
    - Include selected custom link
    - Include posting instructions

14. **Save LinkedIn Post**
    - Save to `/home/jeremy/projects/blog/linkedin-posts/YYYY-MM-DD-slug-linkedin.txt`
    - Include character count
    - Include posting instructions for Intent Solutions company page
    - Include hashtag suggestions

15. **Track Nuclear Analytics**
    - Import analytics helpers: `sys.path.append('/home/jeremy/analytics')`
    - Auto-add StartAITools blog post
    - Auto-add JeremyLongshore blog post
    - Auto-add X thread
    - Create LinkedIn post entry in analytics
    - Update monthly analytics for both sites
    - Report comprehensive analytics summary

16. **Confirm Nuclear Deployment**
    - Verify both blog builds succeeded
    - Confirm both deployments initiated
    - Report both live blog URLs
    - Provide X thread file location
    - Provide LinkedIn post file location
    - Show complete analytics tracking confirmation

## Content Multiplication Strategy

**ONE Session Analysis → FOUR Platform-Optimized Outputs:**

```
Technical Implementation Session
           ↓
   Content Adaptation Engine
           ↓
┌─────────────────┬─────────────────┐
│ Technical Angle │ Personal Angle  │
├─────────────────┼─────────────────┤
│ StartAITools    │ JeremyLongshore │
│ Blog Post       │ Blog Post       │
│ (Architecture)  │ (Journey)       │
├─────────────────┼─────────────────┤
│ LinkedIn Post   │ X Thread        │
│ (Business)      │ (Insights)      │
└─────────────────┴─────────────────┘
```

## Nuclear Best Practices

### Content Adaptation Principles
- **Same session, different lenses** - Technical vs Personal perspective
- **Audience-specific value** - What each platform audience wants to hear
- **Cross-pollination** - Each piece drives traffic to others
- **Authentic voice** - Maintain your voice across different tones

### Platform Optimization
- **StartAITools**: Deep technical, professional authority, SEO optimized
- **JeremyLongshore**: Personal growth, authentic journey, relatable struggles
- **X Thread**: Quick insights, TL;DR format, conversational engagement
- **LinkedIn**: Business results, professional achievements, company brand

### Analytics Integration
- **Track everything** - All content pieces in unified analytics
- **Cross-platform metrics** - See which angles perform best where
- **Content ROI** - Measure time investment vs engagement across platforms
- **Iteration insights** - Learn what works for future nuclear blasts

## Response Options

After showing all content:
- **"yes"** - Deploy nuclear content blast across all platforms
- **"edit"** - Make changes before deployment
- **"cancel"** - Don't publish any content

## Example Content Nuke

User runs `/content-nuke` after completing a major technical implementation:

1. **Analyzes session**: API integration + MCP architecture work
2. **Asks thread size**: User responds "3"
3. **Asks link preference**: User chooses GitHub repo
4. **Generates four pieces**:
   - StartAITools: "Enterprise MCP Architecture: 6 Production Servers Integration"
   - JeremyLongshore: "From API Chaos to Unified Architecture: A Learning Journey"
   - X Thread: "TL;DR: Discovered existing MCP servers = 80% less work..." (3 tweets)
   - LinkedIn: "Intent Solutions successfully integrated 6 production MCP servers..."
5. **Shows for review**: Complete content package
6. **Deploys nuclear blast**: All platforms updated simultaneously
7. **Tracks analytics**: Complete cross-platform performance monitoring

**Result:** Maximum content leverage from single session - technical authority + personal brand + social engagement + professional presence.

## Nuclear Deployment Files

- **Blog Posts**: Auto-published to both sites with Hugo
- **X Thread**: `/home/jeremy/projects/blog/x-threads/YYYY-MM-DD-slug-nuclear-x[size].txt`
- **LinkedIn Post**: `/home/jeremy/projects/blog/linkedin-posts/YYYY-MM-DD-slug-linkedin.txt`
- **Analytics**: All content tracked in unified database

**Nuclear content multiplication achieved! 🚀**