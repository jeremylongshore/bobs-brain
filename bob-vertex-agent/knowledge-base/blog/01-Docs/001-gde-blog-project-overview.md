# 🌐 JeremyLongshore.com - Personal Blog & Portfolio

[![Hugo](https://img.shields.io/badge/Hugo-Extended-ff4088?logo=hugo)](https://gohugo.io/)
[![Netlify Status](https://api.netlify.com/api/v1/badges/47ad5c0b-2dd7-4579-b667-9fdc8b04e7a2/deploy-status)](https://app.netlify.com/sites/jeremylongshore/deploys)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> Personal blog and portfolio website showcasing AI engineering, software development, and entrepreneurial journey. Built with Hugo and optimized for performance.

🔗 **Live Site:** [jeremylongshore.com](https://jeremylongshore.com)

## ✨ Features

- 📝 **Tech Blog** - Insights on AI, software engineering, and startups
- 🚀 **Project Portfolio** - Showcasing DiagnosticPro, Start AI Tools, and more
- 📊 **AI Engineering Curriculum** - Comprehensive learning resources
- 🎨 **Clean Design** - Fast, responsive, accessible with Hermit v2 theme
- 🔍 **SEO Optimized** - Structured data, meta tags, sitemap
- ⚡ **Lightning Fast** - Static site with optimized assets
- 🌙 **Dark Mode** - Auto-switching based on system preference

## 🏗️ Tech Stack

- **Static Site Generator:** [Hugo](https://gohugo.io/) v0.149.1
- **Theme:** [Hermit v2](https://github.com/1bl4z3r/hermit-V2) (Customized)
- **Hosting:** [Netlify](https://netlify.com/)
- **Domain:** Porkbun
- **Analytics:** Google Analytics 4
- **Features:** Syntax highlighting, social sharing, related posts

## 📂 Content Structure

```
content/
├── en/                 # English content
│   ├── blogs/         # Blog posts
│   │   ├── tech/     # Technical articles
│   │   ├── startup/  # Entrepreneurship content
│   │   └── ai/       # AI & ML topics
│   ├── about.md      # About page
│   └── contact.md    # Contact page
data/
├── en/                # Data files
│   ├── author.toml   # Author information
│   ├── experience.toml # Work experience
│   └── projects.toml # Portfolio projects
```

## 🚀 Quick Start

### Prerequisites

- [Hugo](https://gohugo.io/installation/) v0.149.1+
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (optional, for advanced features)

### Local Development

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/jeremylongshore.com.git
cd jeremylongshore.com

# Start development server with drafts
hugo server -D

# View at http://localhost:1313
```

### Build for Production

```bash
# Build static site
hugo

# Output will be in ./public directory
```

## 📝 Writing Content

### Create New Post

```bash
# Create a new blog post
hugo new content/en/blogs/my-new-post.md

# Create a project page
hugo new content/en/projects/my-project.md
```

### Front Matter Template

```toml
+++
title = 'Your Post Title'
date = 2024-01-15T10:00:00-06:00
draft = false
tags = ["ai", "programming", "startup"]
categories = ["Technology"]
author = "Jeremy Longshore"
description = "Brief description for SEO"
images = ["/images/post-cover.jpg"]
toc = true
+++
```

## 🎨 Customization

### Site Configuration

Edit `hugo.toml` for site-wide settings:

```toml
baseURL = 'https://jeremylongshore.com/'
title = 'Jeremy Longshore - AI Engineer & Speed DevOps'
theme = 'hermit-v2'

[params]
  author = "Jeremy Longshore"
  description = "AI Engineer, Software Developer, Entrepreneur"
  themeColor = "#494f5c"
  accentColor = "#018472"
  ShowShareButtons = true
  ShowReadingTime = true
  ShowCodeCopyButtons = true
```

### Custom Styling

The Hermit v2 theme provides professional styling out of the box. To customize:

1. Override theme layouts in `layouts/` directory
2. Add custom CSS in `static/css/custom.css`
3. Modify theme colors in `hugo.toml`

## 🔗 Integrated Projects

### Featured Projects

1. **[DiagnosticPro](https://diagnosticpro.io)** - AI-powered diagnostic platform for repair professionals
2. **[Start AI Tools](https://startaitools.com)** - Curated directory of AI tools and resources
3. **[Intent Solutions](https://intentsolutions.io)** - AI deployment and consulting services
4. **[AI Engineering Curriculum](https://jeremylongshore.github.io/ai-engineering-curriculum/)** - Comprehensive learning path from zero to enterprise

### Start AI Tools Integration

This site can optionally sync content from Start AI Tools blog:

```bash
# Sync content from Start AI Tools (if script exists)
./scripts/sync-startaitools.sh
```

## 🚢 Deployment

### Netlify (Current Setup)

The site automatically deploys to Netlify on push to main branch:

- **Build command:** `hugo`
- **Publish directory:** `public/`
- **Hugo version:** 0.149.1 (defined in netlify.toml)
- **Domain:** jeremylongshore.com with HTTPS

### Manual Deployment

```bash
# Build the site
hugo

# Deploy public/ directory to any static host
rsync -avz public/ user@server:/var/www/html/
```

## 📊 Projects & Experience

Update portfolio content by editing data files:

- `data/en/author.toml` - Author bio and social links
- `data/en/experience.toml` - Work experience timeline
- `data/en/projects.toml` - Featured projects showcase

## 📈 Performance Metrics

- **Lighthouse Score:** 98+/100
- **Page Load:** < 1.5s
- **First Contentful Paint:** < 600ms
- **Time to Interactive:** < 1.2s
- **Total Page Size:** < 500KB

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugo](https://gohugo.io/) - Static site generator
- [Hermit v2 Theme](https://github.com/1bl4z3r/hermit-V2) - Clean, minimal theme
- [Netlify](https://netlify.com/) - Hosting platform
- Open source community

## 📧 Contact

- **Website:** [jeremylongshore.com](https://jeremylongshore.com)
- **Email:** jeremy@intentsolutions.io
- **GitHub:** [@jeremylongshore](https://github.com/jeremylongshore)
- **LinkedIn:** [Jeremy Longshore](https://linkedin.com/in/jeremylongshore)
- **X/Twitter:** [@asphaltcowb0y](https://x.com/asphaltcowb0y)

---

<p align="center">
  Made with ❤️ by Jeremy Longshore
</p>

<p align="center">
  <a href="https://github.com/jeremylongshore/jeremylongshore.com">⭐ Star this project</a> •
  <a href="https://jeremylongshore.com">🌐 Visit the site</a> •
  <a href="https://github.com/jeremylongshore/jeremylongshore.com/issues">🐛 Report an issue</a>
</p>