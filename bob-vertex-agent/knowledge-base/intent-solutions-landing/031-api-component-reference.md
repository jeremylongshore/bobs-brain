# Component API Reference

This document provides API documentation for custom components and usage guidelines for shadcn/ui components.

## UI Component Library (shadcn/ui)

The project uses [shadcn/ui](https://ui.shadcn.com) - a collection of 57 high-quality React components built with Radix UI and Tailwind CSS.

### Available Components

All components located in `src/components/ui/`:

#### Forms & Inputs
- `button.tsx` - Button component with variants
- `input.tsx` - Text input field
- `textarea.tsx` - Multi-line text input
- `checkbox.tsx` - Checkbox input
- `radio-group.tsx` - Radio button group
- `select.tsx` - Dropdown select
- `switch.tsx` - Toggle switch
- `slider.tsx` - Range slider
- `label.tsx` - Form label

#### Layout & Navigation
- `card.tsx` - Content container
- `tabs.tsx` - Tabbed interface
- `accordion.tsx` - Collapsible content
- `separator.tsx` - Visual divider
- `breadcrumb.tsx` - Navigation breadcrumbs
- `menubar.tsx` - Menu bar
- `navigation-menu.tsx` - Navigation menu
- `sidebar.tsx` - Sidebar layout

#### Feedback & Overlays
- `alert.tsx` - Alert messages
- `alert-dialog.tsx` - Modal alert dialog
- `dialog.tsx` - Modal dialog
- `sheet.tsx` - Slide-out panel
- `toast.tsx` - Toast notifications
- `popover.tsx` - Popover overlay
- `tooltip.tsx` - Tooltip overlay
- `hover-card.tsx` - Hover card
- `progress.tsx` - Progress indicator
- `skeleton.tsx` - Loading skeleton

#### Data Display
- `table.tsx` - Data table
- `chart.tsx` - Chart components
- `avatar.tsx` - User avatar
- `badge.tsx` - Status badge
- `calendar.tsx` - Calendar picker
- `carousel.tsx` - Image carousel

### Component Usage Pattern

All shadcn/ui components follow this pattern:

```typescript
import { Button } from "@/components/ui/button"

export function Example() {
  return (
    <Button variant="default" size="lg">
      Click me
    </Button>
  )
}
```

### Common Props

Most components accept these props:

| Prop | Type | Description |
|------|------|-------------|
| `className` | string | Additional CSS classes |
| `variant` | string | Visual variant (default, outline, ghost, etc.) |
| `size` | string | Size variant (sm, md, lg, etc.) |
| `disabled` | boolean | Disabled state |
| `asChild` | boolean | Render as child component |

## Custom Hooks

### use-mobile

Detects mobile screen size.

```typescript
import { useMobile } from "@/hooks/use-mobile"

export function Component() {
  const isMobile = useMobile()

  return (
    <div>
      {isMobile ? "Mobile View" : "Desktop View"}
    </div>
  )
}
```

**Returns**: `boolean` - true if viewport width < 768px

### use-toast

Manages toast notifications.

```typescript
import { useToast } from "@/hooks/use-toast"

export function Component() {
  const { toast } = useToast()

  const showToast = () => {
    toast({
      title: "Success!",
      description: "Your action was completed.",
      variant: "default" // or "destructive"
    })
  }

  return <button onClick={showToast}>Show Toast</button>
}
```

**API**:
- `toast(options)` - Display toast notification
- `options.title` - Toast title (string)
- `options.description` - Toast message (string)
- `options.variant` - Visual style ("default" | "destructive")
- `options.duration` - Auto-dismiss duration (ms, default: 5000)

## Utility Functions

### cn (Class Name Helper)

Merges Tailwind classes with conditional logic.

```typescript
import { cn } from "@/lib/utils"

export function Component({ isActive, className }) {
  return (
    <div className={cn(
      "base-class",
      isActive && "active-class",
      className
    )}>
      Content
    </div>
  )
}
```

**Usage**:
```typescript
cn("px-4 py-2", conditional && "bg-blue-500", props.className)
```

## Page Components

### Index.tsx

Landing page component (main route).

**Location**: `src/pages/Index.tsx`

**Structure**:
```typescript
export default function Index() {
  return (
    <>
      <Header />
      <Hero />
      <Services />
      <Testimonials />
      <Contact />
      <Footer />
    </>
  )
}
```

### NotFound.tsx

404 error page.

**Location**: `src/pages/NotFound.tsx`

**Structure**:
```typescript
export default function NotFound() {
  return (
    <div className="error-container">
      <h1>404 - Page Not Found</h1>
      <Link to="/">Return Home</Link>
    </div>
  )
}
```

## Component Guidelines

### Creating New Components

1. **Use TypeScript** with explicit prop types:
```typescript
interface ButtonProps {
  children: React.ReactNode
  variant?: "default" | "outline"
  onClick?: () => void
}

export function Button({ children, variant = "default", onClick }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>
}
```

2. **Export from index** (when creating component folders):
```typescript
// components/Card/index.ts
export { Card } from './Card'
export type { CardProps } from './Card'
```

3. **Use cn() for conditional classes**:
```typescript
<div className={cn("base", isActive && "active", className)} />
```

### Styling Conventions

- **Mobile-first**: Start with mobile styles, add breakpoints upward
- **Utility classes**: Prefer Tailwind utilities over custom CSS
- **Consistency**: Follow existing component patterns
- **Accessibility**: Include ARIA labels, keyboard support

### Performance Best Practices

- **Lazy load** heavy components:
```typescript
const HeavyComponent = React.lazy(() => import('./HeavyComponent'))
```

- **Memoize** expensive calculations:
```typescript
const expensiveValue = useMemo(() => calculateValue(data), [data])
```

- **Avoid inline functions** in render:
```typescript
// Bad
<button onClick={() => handleClick(id)} />

// Good
const handleClickWithId = useCallback(() => handleClick(id), [id])
<button onClick={handleClickWithId} />
```

## Testing Components (Future)

When tests are implemented:

```typescript
import { render, screen } from '@testing-library/react'
import { Button } from './Button'

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
})
```

## Further Reading

- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Radix UI Primitives](https://www.radix-ui.com)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Documentation](https://react.dev)

---
**Last Updated**: October 4, 2025
**Component Library Version**: shadcn/ui latest
