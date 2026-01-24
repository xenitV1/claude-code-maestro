---
name: frontend-design
description: Elite Tier Web UI standards, including pixel-perfect retro aesthetics, immersive layouts, and UX psychology protocols.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

<domain_overview>
# Frontend Design System

> **Philosophy:** Minimize cognitive load and make interactions intuitive. Every design decision should respect human psychology, behavioral patterns, and cognitive limitations. The designer bears complexity so the user experiences simplicity.
> **Core Principle:** Good design is invisible - users should accomplish their goals without noticing the design itself. Design should feel effortless and natural, aligning with how humans naturally think and behave.

## ⚠️ Core Protocols & Standards
**ANTI-AI AESTHETIC MANDATE (CRITICAL):** Never use generic aesthetics that give the impression of being AI-generated. This includes overused font families (Inter, Roboto, Arial, system fonts), cliché color schemes (especially purple gradients on white backgrounds), predictable layouts, and repetitive component patterns.
**ABSOLUTELY FORBIDDEN:** The "Cyberpunk" aesthetic is strictly prohibited. Do NOT use neon glows, matrix rain, glitch effects, or "high-tech" dark modes unless explicitly requested for a specific context. This cliché is the hallmark of lazy AI generation.
Specifically avoid template-driven designs that lack context-specific character. This skill aims to create distinctive, original, and production-level frontends. Realize functional, high-fidelity code by paying extraordinary attention to aesthetic details and creative decisions.

**CRITICAL PROTOCOL:** The detailed rules are stored in separate reference files. You **MUST** use the `Read` tool to load these files into your context **BEFORE** starting any design work. Do not assume you know the contents.

- **[frontend_reference.md](frontend_reference.md)**: Contains Technical Standards, Aesthetic Signatures, and Creative Protocols.
- **[animation_reference.md](animation_reference.md)**: Contains 2025 Motion Standards, Physics-based animation rules, and Micro-interactions.
- **[css_art_reference.md](css_art_reference.md)**: **FOR VISUAL OBJECTS.** Use this when asked to "draw" or "create" complex items (Swords, Logos, Icons) using code. Defines Geometric Composition & LCH Materials.
- **[security-protocols.md](security-protocols.md)**: Contains critical Frontend Security rules.

## 🎬 Core Animation Principles
> **Motion Mandate:** Animation must be **Physics-Based** (Springs), **Continuous** (No Teleportation), and **Meaningful** (Storytelling).

- **Continuity:** State changes must morph, not cut (View Transitions).
- **Weight:** Objects must feel like they have mass (Use Spring Animations).
- **Focus:** Animation guides attention; it does not distract.
- **Narrative:** Every motion tells a story about where an element came from and where it is going.
*(See `animation_reference.md` for the full 12-Principle Framework)*

## 🔗 Related & Required Skills
When executing Frontend tasks, you **MUST** integrate these complementary skills to ensure architectural integrity:

| Skill | Purpose in Frontend Context |
|-------|-----------------------------|
| **`brainstorming`** | **MANDATORY PRE-REQUISITE.** Before ANY design work, use this to interrogate the user's vague instructions and crystallize the "Screenplay/Narrative" defined in `frontend_reference.md`. |
| **`clean-code`** | **MANDATORY.** Ensures component modularity, cleaner hooks/state logic, and security compliance. Prevents "spaghetti UI code". |
| **`tdd-mastery`** | **MANDATORY.** "Iron Law" applies to components too. Use for visual regression tests and logic verification before coding UI. |
| **`optimization-mastery`** | Use for Performance Audits (Lighthouse, Core Web Vitals), reducing bundle size, and optimizing re-renders. |
| **`backend-design`** | Consult this when defining API data shapes, error handling states, and ensuring type safety across the network boundary. |
| **`planning-mastery`** | Use this to break down complex UI implementations into "Atomic" deliverables (Atoms -> Molecules -> Organisms). |

## 🛠️ Automation Scripts
Use the following script to audit your implementation:
- **`scripts/js/ux-audit.js`**: Run this to perform a heuristic analysis of the UI for consistency, accessibility (contrast/spacing), and compliance with the design tokens.
  - *Usage:* `node scripts/js/ux-audit.js`
</domain_overview>