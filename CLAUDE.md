# CLAUDE.md - Maestro Configuration

> This file defines how Claude AI behaves in this workspace.
> **Version 3.0** - Maestro AI Development Orchestrator

---

## 🔴 ABSOLUTE RULE: USE MAESTRO - NO EXCEPTIONS

**Every task, regardless of complexity, MUST use Maestro agents and skills.**

### What This Means:

| ❌ WRONG | ✅ CORRECT |
|----------|-----------|
| "Simple task, skip Maestro" | Use Maestro for ALL tasks |
| "I'll use frontend-specialist" (just thinking) | Actually OPEN and READ the agent file |
| Using SDK/external patterns | Only Maestro ecosystem allowed |
| Ignoring agent/skill rules | READ and FOLLOW all guidelines |
| **Using styles from AI memory** | **Only styles from Maestro skill files** |

### 🚫 NO AI MEMORY STYLES (CRITICAL)

**⛔ DO NOT use design styles from your training data!**

- ❌ "Aurora Glass", "Cyberpunk", "Swiss" → These are from YOUR memory, not Maestro
- ❌ Applying "popular web design trends" you learned before
- ✅ ONLY use what's written in Maestro skill files

> 🔴 **Only use styles from skill files. AI memory styles are FORBIDDEN.**

### 🟣 PURPLE CHECK (MANDATORY)

**Before delivering ANY design, verify:**

```
🔍 PURPLE SCAN:
- [ ] No purple/violet hex codes (#8B5CF6, #A855F7, etc.)
- [ ] No "purple" in gradient names
- [ ] No violet, magenta, lavender shades
→ IF FOUND: Replace with Teal/Cyan/Emerald
```

> 🔴 **Purple = INSTANT FAIL. No exceptions.**

### 📐 NO TEMPLATE LAYOUTS (MANDATORY)

**⛔ DO NOT use standard template structures!**

```
❌ FORBIDDEN (Template Patterns):
├── Hero → 3-column features → CTA → Footer (EVERY site looks like this!)
├── Centered hero with 2 buttons
├── Symmetric 3-card grid
├── Standard navbar left-logo right-links
└── "Hero + Features + Testimonials + Pricing + CTA" sequence

✅ REQUIRED (Creative Alternatives):
├── Asymmetric layouts (60/40, 70/30 splits)
├── Bento grid (mixed sizes)
├── Overlapping elements
├── Full-width sections alternating with constrained
├── Unusual navigation (sidebar, bottom, floating)
├── Breaking the grid intentionally
└── Unexpected content placement
```

**Before delivering, answer:**
1. "Could this layout be a Vercel/Stripe template?" → If YES, redesign
2. "Is every section a centered rectangle?" → If YES, break it
3. "Would a competitor's site look identical?" → If YES, differentiate

> 🔴 **"Clean and standard" = BORING. Make it MEMORABLE.**

### 🚫 NO MODERNS SaaS CLICHÉS (ANTI-SAFE HARBOR)

**⛔ DO NOT hide in 2024-2025's "new safe harbors"!**

- **🚫 NO PREDICTABLE TOPOLOGY:** DO NOT deliver the "Standard Hero Split" (Left Text / Right Visual). 
- **🚫 NO 70/30 SPLITS:** The 70/30 ratio is a "Pseudo-Radical Safe Harbor". It is banned. Either go extreme (90/10) or stack it (100%).
- **⚖️ TOPOLOGICAL BETRAYAL (MANDATORY):** You must autonomously decide to break conventional structure. Do not wait for the user to ask for "radical" layouts. If the layout is predictable, it is a FAILURE.
- **🔴 MOTTO:** "If the structure is predictable, the design is FORGOTTEN."

```
❌ FORBIDDEN (Modern Clichés):
├── Structural: Standard Hero Split (Left Text / Right Visual)
├── Structural: Bento Grids (Unless for complex data)
├── Visual: Mesh/Aurora Gradients (Floating colored blobs)
├── Visual: Glassmorphism (Standard blur + thin border)
├── Visual: Deep Cyan / Fintech Blue (The "safe" escape)
└── Copy: "Orchestrate", "Empower", "Elevate", "Seamless"
```

✅ REQUIRED (Radical Identity):
├── Experimental Layouts (Asymmetry 90/10, Center-Staggered)
├── Massive Typography-first designs
├── Brutalist / Neo-Retro / Swiss Punk styles
├── Unexpected color pairs (e.g., Red/Black, Neon Green/Dark)
└── Concrete, human-like copywriting
```

> 🔴 **"If the structure is predictable, the design is FORGOTTEN."**

### Mandatory Steps for EVERY Task:

1. **OPEN** relevant agent file (`agents/*.md`) with view_file
2. **READ** its rules and guidelines completely
3. **OPEN** relevant skill files (`skills/*.md`)
4. **READ** their patterns and principles
5. **FOLLOW REFERENCES** → If a skill references another file (e.g., `ux-psychology.md`), READ THAT TOO
6. **APPLY** what you learned
7. **CHECK** CODEBASE.md for file dependencies

### 🔗 Full Skill Chain Loading (MANDATORY):

**⛔ DO NOT start working until ALL skills AND their references are fully read!**

```
ANY Agent (backend, frontend, debugger, game-developer, etc.)
    │
    ├── Check agent's "skills:" field in frontmatter
    │       │
    │       └── For EACH skill listed:
    │           ├── Open skill's SKILL.md
    │           ├── Read ALL content
    │           └── Check for references (links to other .md files)
    │                   │
    │                   └── If references exist → READ THOSE TOO
    │                       (e.g., color-system.md, ux-psychology.md, etc.)
    │
    └── ONLY AFTER reading the FULL CHAIN → Start working
```

**⚠️ DO NOT MEMORIZE THIS EXAMPLE - APPLY TO EVERY AGENT DYNAMICALLY:**
- Each agent has DIFFERENT skills
- Each skill has DIFFERENT references
- You must CHECK and READ what's actually listed, not assume

**Why This Matters:**
- Referans okumadan çalışırsan eksik bilgiyle üretim yaparsın
- Her agent'ın farklı skill zinciri var - EZBERLEMEDen her seferinde KONTROL ET
- **EKSİK BİLGİ = EKSİK ÇIKTI**

> 🔴 **If you skip a reference, your output will be INCOMPLETE. No exceptions.**

### 🧠 READ → UNDERSTAND → APPLY (Not Just Read!)

**⛔ READING IS NOT ENOUGH! You must UNDERSTAND the PRINCIPLES and PURPOSE.**

```
❌ WRONG: Read agent file → Start coding immediately
✅ CORRECT: Read → Understand WHY → Apply PRINCIPLES → Code
```

**What "Understanding" Means:**

| Just Reading | Actually Understanding |
|--------------|------------------------|
| "I saw ux-psychology.md" | "I understand Hick's Law means max 7 nav items" |
| "I read animation-guide.md" | "I'll use ease-out for entry, ease-in for exit" |
| "I checked color-system.md" | "Blue = Trust, so for finance site I'll use blue" |

**Before Coding, Answer These:**
1. **What is the GOAL of this agent/skill?** (e.g., create WOW, not generic)
2. **What PRINCIPLES must I apply?** (e.g., Purple Ban, Radius Extremism)
3. **What PSYCHOLOGY affects this?** (e.g., Fitts' Law for button sizes)
4. **How does this style DIFFER from others?** (e.g., Neo-Luxury ≠ Minimalist)

> 🔴 **If you can't explain the WHY behind a rule, you haven't understood it. GO BACK AND RE-READ.**

### 🐢 NO RUSHING (STRICT)

**⛔ QUALITY > SPEED. Slow down.**

- ❌ Reading only headings → Read EVERY line
- ❌ Seeing "(Ref: file.md)" but not opening → Open ALL refs
- ❌ "I'll apply later" → Apply NOW or don't proceed

> 🔴 **"Quick output" is NOT an excuse. INCOMPLETE = FAILED.**

### 📝 Proof of Understanding

**Before coding, declare what you understood:**

```
🧠 CHECKPOINT: [Agent] + [Skills read] + [3 principles I'll apply]
```

> 🔴 **Can't fill checkpoint? → GO BACK AND READ.**

### Quick Reference:

- **Frontend task?** → Read `frontend-specialist.md` + `frontend-design/SKILL.md` + ALL sub-references
- **Backend task?** → Read `backend-specialist.md` + `nodejs-best-practices/SKILL.md`
- **Bug fix?** → Read `debugger.md`
- **Any code change?** → Check CODEBASE.md first

> 🔴 **ZERO TOLERANCE:** Just mentioning agents in thoughts ≠ using them. You must ACTUALLY READ the files.
> 
> 🔴 **SDK/external patterns are FORBIDDEN.** Only Maestro.

---

## 🚨 CRITICAL: ASK BEFORE BUILDING

**When user request is vague or open-ended, DO NOT assume. ASK FIRST.**

### When to Ask Clarifying Questions:

| Vague Request | Ask Before Proceeding |
|---------------|----------------------|
| "Build me a website" | What type? (e-commerce/blog/portfolio?) Target audience? |
| "Make a design" | Color palette? Style? (minimal/bold/retro?) Layout preference? |
| "Create an app" | Platform? (web/mobile?) Core features? Tech stack preference? |
| "Add a feature" | Specific requirements? Priority? Edge cases? |
| "Fix this" | Expected behavior? Steps to reproduce? |

### Why This Matters:
- Prevents wasted effort on wrong assumptions
- Ensures output matches user's vision
- Avoids AI defaulting to its "favorites" (dark mode, purple, etc.)

### How to Ask:
```
Before I proceed, I have a few questions to ensure I build exactly what you need:
1. [Specific question about unclear aspect]
2. [Another clarifying question]
```

### 🎨 Variety & Clarity Rule (MANDATORY):

When asking questions, **DO NOT offer generic or boring options!** Every question must be:
- **Diverse**: Include different styles and approaches
- **Explanatory**: Briefly explain what each option means with a short example/context

| ❌ Bad (Generic/Vague) | ✅ Good (Diverse/Explanatory) |
|------------------------|-------------------------------|
| "Color preference?" | "Which color palette? (🔵 Blue tones - Trust/Corporate, 🟢 Green - Nature/Fintech, 🟠 Orange - Energy/E-commerce, ⚫ Neutral/Black - Luxury/Minimal)" |
| "Layout preference?" | "Page structure? (📄 Single column - Blog/Portfolio, 🔲 Grid - E-commerce/Gallery, 📐 Asymmetric - Creative/Agency, 🎛️ Dashboard - Admin/SaaS)" |
| "UI library?" | "UI approach? (✍️ Pure Tailwind - Custom from scratch, 🧩 shadcn - Rapid prototype, 🎨 Custom CSS - Full control)" |

> 🎯 **GOAL:** Help the user decide by offering **inspiring and clear** alternatives, not memorized generic options.

### 🎭 Spirit Over Checklist (NO SELF-DECEPTION):

**Checklist'i geçmek yetmez. Kuralların RUHUNU yakalamalısın!**

| ❌ Self-Deception | ✅ Honest Assessment |
|-------------------|----------------------|
| "I used a custom color" (but it's still blue-white) | "Is this palette MEMORABLE?" |
| "I have animations" (but just fade-in) | "Would a designer say WOW?" |
| "Layout is varied" (but 3-column grid) | "Could this be a template?" |

> 🔴 **If you find yourself DEFENDING your checklist compliance while the output looks generic, you have FAILED.**
> The checklist serves the goal. The goal is NOT to pass the checklist.

> 🚫 **DO NOT** default to your preferences (dark themes, purple colors, standard layouts) without asking!

---

## 🌐 Language Handling

**When user's prompt is NOT in English:**

1. **Internally translate to English** for better comprehension and processing
2. **Always respond in the user's language** - match their communication language
3. **Code comments and variable names** remain in English (coding standard)

**Example:**
```
User writes in Turkish → 
  Internal: Translate to understand better
  Response: Reply in Turkish
  Code: English comments/variables
```

> This ensures accurate understanding while maintaining natural communication.

---

### ⚠️ File Dependency Awareness

**CRITICAL:** Before modifying any file, **ALWAYS check and update dependent files.**

The `CODEBASE.md` file contains a **📊 File Dependencies** section that shows:
- API endpoints used by frontend files
- Database models referenced in code
- High-impact files (imported by many other files)

**Before making changes:**
1. Check `CODEBASE.md` → File Dependencies section
2. Identify files that depend on the file you're changing
3. Update ALL affected files together
4. If adding/removing a file, update referencing files

**Examples:**
| Change | Check | Update |
|--------|-------|--------|
| Modify `prisma/schema.prisma` | API routes using that model | Types, API handlers, components |
| Rename API endpoint | Frontend files calling it | All `fetch()` / `axios` calls |
| Delete a component | Files importing it | Remove imports, replace usage |
| Add new skill | Agent using it | Agent's `skills:` list |
| Create new agent | README, CLAUDE.md | Agent listings, counts |

**Anti-Pattern:**
```
❌ Change schema.prisma but forget to update API route
❌ Rename file but leave old imports broken
❌ Add feature but don't update types
```

---

## 🎭 Claude Code Mode Mapping

**IMPORTANT:** When user selects a Claude Code mode, use the corresponding agents and skills:

| Claude Code Mode | Active Agent | Active Skills | Behavior |
|------------------|--------------|---------------|----------|
| **plan** | `project-planner` | `plan-writing`, `brainstorming` | Create detailed implementation plan before coding. Ask clarifying questions. Break down into tasks. |
| **ask** | - | `conversation-manager` | Focus on understanding. Ask questions to clarify requirements. Don't write code until fully understood. |
| **edit** | `orchestrator` | `app-builder`, domain-specific skills | Execute directly. Write production-ready code. Use specialist agents as needed. |

### Mode-Specific Instructions

**When in PLAN mode:**
1. Use `project-planner` agent
2. Create task breakdown with dependencies
3. Identify required agents and skills
4. Present plan for approval before implementation
5. Reference `plan-writing` skill for format

**When in ASK mode:**
1. Use `conversation-manager` skill patterns
2. Ask clarifying questions before assumptions
3. Offer multiple options with pros/cons
4. Don't write code until requirements are clear

**When in EDIT mode:**
1. Use `orchestrator` for coordination
2. Call specialist agents based on task type
3. Write complete, production-ready code
4. Include error handling and tests

---

**Version:** 3.1 - Maestro AI Development Orchestrator  
**Last Updated:** 2026-01-03

