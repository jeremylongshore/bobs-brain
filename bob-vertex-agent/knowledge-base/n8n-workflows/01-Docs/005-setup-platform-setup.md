# Platform Setup Guide

Complete setup instructions for each supported blog platform.

## Table of Contents

- [Hugo Setup](#hugo-setup)
- [Jekyll Setup](#jekyll-setup)
- [Gatsby Setup](#gatsby-setup)
- [Next.js Setup](#nextjs-setup)
- [WordPress Setup](#wordpress-setup)
- [Common Configuration](#common-configuration)

---

## Hugo Setup

### Prerequisites
```bash
# Install Hugo (macOS)
brew install hugo

# Install Hugo (Linux)
sudo snap install hugo

# Verify installation
hugo version  # Should be v0.100+
```

### Blog Structure
```
your-hugo-blog/
├── config.toml or hugo.toml    # Site configuration
├── content/
│   └── posts/                  # Blog posts location
├── themes/                     # Theme directory
└── public/                     # Generated site (gitignored)
```

### Command Customization

1. **Copy command template:**
   ```bash
   cp ~/.claude/commands/blog-hugo-technical.md ~/.claude/commands/blog-myblog.md
   ```

2. **Edit paths (line 6):**
   ```markdown
   - **Git History**: Check commits since the most recent post date in `/path/to/your/hugo/content/posts/`
   ```

3. **Update build command (line 58):**
   ```bash
   cd /path/to/your/hugo/blog && hugo --gc --minify --cleanDestinationDir
   ```

4. **Adjust front matter format (lines 38-48):**
   - YAML (most common): Keep as-is
   - TOML: Change to `+++` delimiters and TOML syntax

### Deployment Options
- **Netlify:** Auto-deploys on git push, configure `netlify.toml`
- **GitHub Pages:** Use GitHub Actions workflow
- **Vercel:** Connect repo and auto-deploy
- **AWS S3 + CloudFront:** Manual sync or CI/CD pipeline

---

## Jekyll Setup

### Prerequisites
```bash
# Install Ruby and Bundler
# macOS (Ruby pre-installed)
gem install bundler jekyll

# Ubuntu/Debian
sudo apt-get install ruby-full build-essential
gem install bundler jekyll

# Verify installation
jekyll -v
```

### Blog Structure
```
your-jekyll-blog/
├── _config.yml              # Site configuration
├── _posts/                  # Blog posts (YYYY-MM-DD-title.md)
├── _layouts/                # Page layouts
└── _site/                   # Generated site (gitignored)
```

### Command Customization

1. **Copy command template:**
   ```bash
   cp ~/.claude/commands/blog-jekyll-technical.md ~/.claude/commands/blog-myblog.md
   ```

2. **Edit paths (line 6):**
   ```markdown
   - **Git History**: Check commits since the most recent post date in your Jekyll `_posts/` directory
   ```
   Update to your actual `_posts/` path.

3. **Update build command (line 56):**
   ```bash
   bundle exec jekyll build
   ```

4. **Front matter format (lines 38-46):**
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   date: 2025-MM-DD HH:MM:SS -0600
   categories: [category1, category2]
   tags: [tag1, tag2]
   ---
   ```

### Deployment Options
- **GitHub Pages:** Push to `gh-pages` branch or `docs/` folder
- **Netlify:** Configure `netlify.toml` with `bundle exec jekyll build`
- **Vercel:** Add build command in project settings
- **Self-hosted:** Copy `_site/` to web server

---

## Gatsby Setup

### Prerequisites
```bash
# Install Node.js (v18+ recommended)
# Install Gatsby CLI
npm install -g gatsby-cli

# Verify installation
gatsby --version
```

### Blog Structure
```
your-gatsby-blog/
├── gatsby-config.js         # Site configuration
├── content/
│   └── posts/               # Markdown/MDX posts
├── src/
│   └── pages/
│       └── blog/            # Blog pages
└── public/                  # Generated site (gitignored)
```

### Command Customization

1. **Copy command template:**
   ```bash
   cp ~/.claude/commands/blog-gatsby-technical.md ~/.claude/commands/blog-myblog.md
   ```

2. **Identify your content location:**
   - Using `gatsby-source-filesystem`: `content/posts/`
   - Using `gatsby-plugin-mdx`: Could be `src/pages/blog/` or custom
   - Check `gatsby-config.js` for `gatsby-source-filesystem` path

3. **Edit paths (line 6):**
   ```markdown
   - **Git History**: Check commits since the most recent post date in your Gatsby `content/posts/` directory
   ```

4. **Update build command (line 56):**
   ```bash
   npm run build
   # or
   gatsby build
   ```

5. **Front matter format (lines 38-47):**
   ```yaml
   ---
   title: "Your Post Title"
   date: "2025-MM-DD"
   description: "SEO-friendly description"
   tags: ["tag1", "tag2"]
   slug: "/blog/post-slug"
   ---
   ```

### Deployment Options
- **Netlify:** Auto-deploy with `gatsby build`
- **Vercel:** Native Gatsby support
- **Gatsby Cloud:** Optimized Gatsby hosting
- **GitHub Pages:** Use `gh-pages` package

---

## Next.js Setup

### Prerequisites
```bash
# Install Node.js (v18+ recommended)
# Next.js CLI comes with create-next-app

# For existing project, ensure dependencies installed
npm install
```

### Blog Structure

**App Router (Next.js 13+):**
```
your-nextjs-blog/
├── app/
│   └── blog/
│       └── [slug]/
│           └── page.mdx
├── content/posts/           # External content (optional)
└── .next/                   # Build output (gitignored)
```

**Pages Router (Next.js 12 and earlier):**
```
your-nextjs-blog/
├── pages/
│   └── blog/
│       └── [slug].mdx
├── content/posts/           # External content (optional)
└── .next/                   # Build output (gitignored)
```

### Command Customization

1. **Copy command template:**
   ```bash
   cp ~/.claude/commands/blog-nextjs-technical.md ~/.claude/commands/blog-myblog.md
   ```

2. **Identify your routing style:**
   - App Router: `app/blog/[slug]/page.mdx`
   - Pages Router: `pages/blog/[slug].mdx`
   - External content with next-mdx-remote: `content/posts/slug.md`
   - Contentlayer: `content/posts/slug.md` with generated types

3. **Edit paths (line 6):**
   ```markdown
   - **Git History**: Check commits since the most recent post date in your Next.js content directory
   ```

4. **Update build command (line 58):**
   ```bash
   npm run build
   # then test with
   npm run start
   ```

5. **Front matter format depends on setup:**
   ```yaml
   ---
   title: "Your Post Title"
   date: "2025-MM-DD"
   description: "SEO description"
   tags: ["tag1", "tag2"]
   ---
   ```

### Deployment Options
- **Vercel:** Optimal for Next.js (native support)
- **Netlify:** Full Next.js support
- **AWS Amplify:** Next.js SSR support
- **Self-hosted:** Docker or Node.js server

---

## WordPress Setup

### Prerequisites

**Option A: WP-CLI (Recommended for automation)**
```bash
# Install WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp

# Verify installation
wp --info
```

**Option B: REST API (No server access needed)**
- Requires WordPress 5.0+
- Application passwords feature (WordPress 5.6+)

### Command Customization

1. **Copy command template:**
   ```bash
   cp ~/.claude/commands/blog-wordpress-technical.md ~/.claude/commands/blog-myblog.md
   ```

2. **Choose publishing method (lines 56-78):**

   **WP-CLI Setup:**
   ```bash
   # Configure wp-cli.yml in project root
   @mysite:
     ssh: user@example.com
     path: /var/www/html

   # Test connection
   wp @mysite post list
   ```

   **REST API Setup:**
   ```bash
   # Generate application password:
   # WordPress Admin → Users → Profile → Application Passwords → Add New

   # Test connection
   curl -X GET "https://yoursite.com/wp-json/wp/v2/posts?per_page=1" \
     -u "username:your_app_password"
   ```

3. **Store credentials securely:**
   ```bash
   # Environment variables (recommended)
   export WP_SITE_URL="https://yoursite.com"
   export WP_USERNAME="admin"
   export WP_APP_PASSWORD="your_app_password"

   # Or use wp-cli.yml for WP-CLI
   ```

4. **Get category and tag IDs:**
   ```bash
   # WP-CLI method
   wp term list category --field=term_id,name
   wp term list post_tag --field=term_id,name

   # REST API method
   curl "https://yoursite.com/wp-json/wp/v2/categories"
   curl "https://yoursite.com/wp-json/wp/v2/tags"
   ```

5. **Update command with your site details (lines 56-78).**

### Deployment
WordPress posts publish immediately via WP-CLI or REST API - no separate build/deploy step required.

---

## Common Configuration

### 1. Claude Commands Directory
```bash
# Default location
~/.claude/commands/

# Verify commands are discovered
ls -la ~/.claude/commands/blog-*.md
```

### 2. Command Naming Convention
```bash
# Good naming examples:
blog-technical.md        # Generic technical blog
blog-portfolio.md        # Portfolio/career blog
blog-company.md          # Company/business blog
blog-personal.md         # Personal blog
blog-[yoursite].md       # Site-specific command
```

### 3. Git Configuration
```bash
# Ensure git is configured
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set up remote
git remote -v  # Verify remote is configured
```

### 4. Testing Your Command

1. **Navigate to any project:**
   ```bash
   cd ~/projects/test-project
   ```

2. **Make some commits:**
   ```bash
   echo "test" > test.txt
   git add .
   git commit -m "test: command testing"
   ```

3. **Invoke your command:**
   ```bash
   # In Claude Code CLI
   /blog-myblog
   ```

4. **Claude will:**
   - Analyze git history
   - Review conversation
   - Generate draft post
   - Show for review
   - Wait for approval
   - Publish after approval

### 5. Troubleshooting

**Command not found:**
- Verify file is in `~/.claude/commands/` with `.md` extension
- Command names must use hyphens: `blog-myblog` not `blogmyblog`
- Try invoking twice (commands register dynamically)

**Build fails:**
- Check build command paths are correct
- Verify blog directory exists
- Test build command manually first
- Check for syntax errors in generated content

**Git push fails:**
- Verify remote is configured: `git remote -v`
- Check authentication (SSH keys or HTTPS credentials)
- Ensure branch exists on remote

**WordPress publish fails:**
- Verify WP-CLI installed: `wp --info`
- Test REST API authentication manually
- Check site URL and credentials
- Verify category/tag IDs exist

---

## Next Steps

1. Choose your platform from the list above
2. Follow platform-specific setup instructions
3. Customize command template for your blog
4. Test with a small project
5. Start using in your daily development workflow

For more help, see the [main README](../README.md) or [open an issue](https://github.com/jeremylongshore/Claude-AutoBlog-SlashCommands/issues).