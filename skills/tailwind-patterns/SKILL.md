---
name: tailwind-patterns
description: Tailwind CSS principles. Responsive design, dark mode, utility patterns.
---

# Tailwind Patterns

> Utility-first CSS principles.

---

## 1. Core Philosophy

| Principle | Meaning |
|-----------|---------|
| Utility-first | Use utilities, not custom CSS |
| Composition | Combine utilities for components |
| Responsive | Mobile-first breakpoints |
| Consistency | Design system via config |

---

## 2. Responsive Design

### Breakpoint System

| Prefix | Min Width | Target |
|--------|-----------|--------|
| (none) | 0px | Mobile |
| `sm:` | 640px | Small tablet |
| `md:` | 768px | Tablet |
| `lg:` | 1024px | Laptop |
| `xl:` | 1280px | Desktop |
| `2xl:` | 1536px | Large desktop |

### Mobile-First Pattern

- Start with mobile styles
- Add breakpoints for larger screens
- Example: `w-full md:w-1/2 lg:w-1/3`

---

## 3. Dark Mode

### Approaches

| Method | Use |
|--------|-----|
| `class` | Manual toggle |
| `media` | System preference |

### Pattern

- Add `dark:` prefix for dark variants
- Example: `bg-white dark:bg-gray-900`

---

## 4. Common Patterns

### Layout

| Pattern | Classes |
|---------|---------|
| Center | `flex items-center justify-center` |
| Stack | `flex flex-col gap-4` |
| Row | `flex flex-row gap-4` |
| Grid | `grid grid-cols-1 md:grid-cols-3 gap-4` (Not: Asimetrik/Bento tercih edin!) |

### Spacing

| Pattern | Approach |
|---------|----------|
| Padding | `p-{size}` or `px-`, `py-` |
| Margin | `m-{size}` or `mx-`, `my-` |
| Gap | `gap-{size}` |

---

## 5. Component Patterns

### Button Principles

| State | Apply |
|-------|-------|
| Base | Padding, rounded, font |
| Hover | Background change |
| Focus | Ring for accessibility |
| Disabled | Opacity, cursor |

### Card Principles

| Element | Apply |
|---------|-------|
| Container | Background, rounded, shadow |
| Hover | Shadow increase, subtle scale |
| Padding | Consistent internal spacing |

---

## 6. Tailwind v4 Changes (2025)

### Key Differences

| v3 | v4 |
|----|----|
| tailwind.config.js | CSS-based `@theme` |
| Plugin system | Native CSS features |
| postcss | Oxide engine (faster) |

### New Features

- CSS-first configuration
- Native nesting support
- Modern CSS variables
- Faster build times

---

## 7. Best Practices

| Practice | Why |
|----------|-----|
| Consistent spacing scale | Visual rhythm |
| Extract components | Reusability |
| Use design tokens | Maintainability |
| Mobile-first | Better CSS cascade |

---

## 8. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Arbitrary values everywhere | Use design system |
| Inline styles | Use utilities |
| !important | Fix specificity |
| Duplicate class groups | Extract component |

---

> **Remember:** Tailwind is a design system in code. Respect the constraints.
