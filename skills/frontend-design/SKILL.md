---
name: frontend-design
description: Design and implement modern frontend interfaces. Use when creating web applications, dashboards, landing pages, or component libraries. Includes CSS frameworks, responsive design, accessibility, and UI/UX patterns.
---

# Frontend Design Skill

This skill provides patterns and best practices for designing and implementing modern frontend interfaces.

## When to Use

- Creating web applications
- Building dashboards
- Designing landing pages
- Developing component libraries
- Implementing responsive designs
- Ensuring accessibility compliance

## Design Principles

### 1. Mobile-First Responsive Design

```css
/* Base styles for mobile */
.container {
  padding: 1rem;
  width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }
}
```

### 2. CSS Custom Properties

```css
:root {
  --color-primary: #6366f1;
  --color-success: #10b981;
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f8fafc;
  --text-muted: #94a3b8;
  --border-color: rgba(148, 163, 184, 0.1);
}
```

### 3. Component Patterns

```css
.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  padding: 1.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  background: var(--color-primary);
  color: white;
}
```

## Common Patterns

### Dashboard Layout
- Header with navigation
- Stats grid (auto-fit)
- Card-based content areas
- Responsive sidebar

### Login Screen
- Centered box
- Brand icon/logo
- Password input
- Full-width button

### Data Tables
- Sortable headers
- Pagination
- Search/filter
- Row actions

## Tools

- **Tailwind CSS** - Utility-first framework
- **CSS Grid/Flexbox** - Modern layouts
- **Inter** - Recommended font
- **Font Awesome** - Icons

## Related Skills

- `api-gateway` - Backend integration
- `code` - JavaScript patterns
