Generate and publish a technical blog post to your WordPress blog that showcases your work and teaches others how to build similar solutions.

## Your Task

1. **Analyze ENTIRE Working Session**
   - **Git History**: Check commits since the most recent work session (fallback: last 14 days)
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
   - Search existing posts via WordPress API or database
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
   - Format as WordPress-ready HTML or Markdown (depending on your editor)

4. **Show Draft for Review**
   - Display the complete blog post
   - Show suggested cross-links
   - Show suggested categories and tags
   - Ask: "Ready to publish? (yes/edit)"
   - Wait for approval or edits

5. **Publish (After Approval)**

   **Option A: WordPress CLI (WP-CLI)**
   ```bash
   wp post create \
     --post_title="Post Title" \
     --post_content="$(cat post-content.md)" \
     --post_status=publish \
     --post_category="category-id" \
     --tags_input="tag1,tag2,tag3"
   ```

   **Option B: WordPress REST API**
   ```bash
   curl -X POST "https://yoursite.com/wp-json/wp/v2/posts" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Post Title",
       "content": "Post content",
       "status": "publish",
       "categories": [1, 2],
       "tags": [3, 4, 5]
     }'
   ```

   **Option C: Manual with Draft File**
   - Save post content to file for manual upload
   - Provide WordPress admin URL for posting
   - Include categories, tags, and featured image suggestions

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

**IMPORTANT**: Before using this command, set up WordPress publishing:

1. **Publishing Method**: Choose your approach:
   - **WP-CLI**: Install WP-CLI and configure access
   - **REST API**: Generate application password or OAuth token
   - **Manual**: Generate draft file for manual upload

2. **WordPress Site URL**: Update `https://yoursite.com` to your actual site

3. **Authentication**: Set up credentials:
   - WP-CLI: Configure `wp-cli.yml` with site alias
   - REST API: Generate application password in WordPress admin
   - Store credentials securely (environment variables or keychain)

4. **Categories/Tags**: Map your WordPress taxonomy:
   - Get category IDs: `wp term list category --field=term_id,name`
   - Get tag IDs: `wp term list post_tag --field=term_id,name`
   - Update default category/tag IDs in command

5. **Content Format**: Specify preferred format:
   - HTML (WordPress default)
   - Markdown (requires plugin like Jetpack or WP Markdown)
   - Gutenberg blocks (requires block editor JSON)

## Example WP-CLI Setup

```bash
# Install WP-CLI (if not installed)
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp

# Configure site alias in wp-cli.yml
@production:
  ssh: user@example.com/var/www/html
  path: /var/www/html

# Test connection
wp @production post list
```

## Example REST API Setup

```bash
# Generate application password in WordPress admin:
# Users → Profile → Application Passwords → Add New

# Store in environment variable
export WP_AUTH_TOKEN="your_app_password_here"
export WP_SITE_URL="https://yoursite.com"

# Test connection
curl -X GET "$WP_SITE_URL/wp-json/wp/v2/posts?per_page=1" \
  -u "username:$WP_AUTH_TOKEN"
```

## Example Invocation
User runs `/blog-wordpress-technical` from any project directory after completing work. You analyze:
1. The complete conversation we just had
2. Git commits since last post
3. The problems we solved and how we solved them
4. Everything we learned in this session - even stuff not in git yet

Then generate and publish to WordPress via your configured method.