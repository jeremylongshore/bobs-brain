# Intent Solutions - Professional Services Landing Page

Modern, responsive landing page for Intent Solutions professional services and business offerings.

## 🚀 Features

- **Service Showcase**: Detailed service descriptions and offerings
- **Contact Forms**: Lead generation and inquiry forms
- **Portfolio Section**: Client work and case studies
- **Testimonials**: Client reviews and success stories  
- **SEO Optimized**: Meta tags, structured data, sitemap
- **Mobile First**: Fully responsive design
- **Performance**: Optimized for Core Web Vitals

## 📦 Installation

```bash
# Clone the repository
git clone [your-git-url]
cd intent-solutions-landing

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🏗️ Project Structure

```
intent-solutions-landing/
├── docs/
│   ├── PRDs/           # Product requirements & AI dev tasks
│   ├── ADRs/           # Architecture decision records
│   ├── specifications/ # Technical specifications
│   └── tasks/          # Task tracking
├── src/
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── assets/         # Images, fonts, etc.
│   └── styles/         # CSS/Tailwind styles
├── public/             # Static assets
└── .github/            # GitHub templates
```

## 🛠️ Technology Stack

- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form
- **Icons**: Lucide React
- **Analytics**: Google Analytics (configurable)

## 📋 Development Workflow

### AI-Driven Development Process

This project uses the AI dev task workflow:

1. **Create PRD**: Use `docs/PRDs/create-prd.md` to define features
2. **Generate Tasks**: Use `docs/PRDs/generate-tasks.md` to break down work
3. **Execute Tasks**: Use `docs/PRDs/process-task-list.md` to implement
4. **Document**: Record decisions in `docs/ADRs/`

### Common Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview build locally
npm run lint         # Run ESLint
npm run type-check   # TypeScript checking

# Testing
npm test            # Run tests
npm run test:watch  # Run tests in watch mode
```

## 🎨 Design System

### Colors
- Primary: Business blue tones
- Secondary: Professional grays
- Accent: Call-to-action colors

### Components
- Hero sections
- Feature cards
- Testimonial sliders
- Contact forms
- Navigation (sticky/responsive)
- Footer with links

## 📱 Responsive Design

- Mobile: 320px - 767px
- Tablet: 768px - 1023px  
- Desktop: 1024px+
- Wide: 1440px+

## 🚦 Performance Targets

- Lighthouse Score: 95+
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Cumulative Layout Shift: < 0.1

## 🔒 Security Best Practices

- Form validation and sanitization
- HTTPS enforced
- Content Security Policy headers
- Regular dependency updates
- Environment variables for sensitive data

## 📊 SEO Features

- Meta tags optimization
- Open Graph tags
- Twitter Card support
- XML sitemap
- Robots.txt
- Schema markup for business info

## 🌐 Deployment

### Lovable Platform

This project is configured for Lovable deployment:

1. Visit [Lovable Project](https://lovable.dev/projects/226460ae-0cff-4da1-ab04-be890486035c)
2. Click Share → Publish
3. Connect custom domain if needed

### Alternative Deployment

```bash
# Build the project
npm run build

# Deploy dist/ folder to:
# - Netlify
# - Vercel
# - AWS S3 + CloudFront
# - GitHub Pages
```

## 📝 Documentation

- **CLAUDE.md**: AI assistant context and guidelines
- **docs/PRDs/**: Feature requirements and planning
- **docs/ADRs/**: Architecture decisions
- **docs/specifications/**: Technical specs
- **docs/tasks/**: Task tracking

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Commit: `git commit -m "feat: add new feature"`
4. Push: `git push origin feature/your-feature`
5. Create Pull Request

## 📧 Support

For questions or support, please contact the Intent Solutions team.

## 📄 License

[License Type] - See LICENSE file for details