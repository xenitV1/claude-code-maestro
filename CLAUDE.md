# CLAUDE.md - Maestro Configuration

> This file defines how Claude AI behaves in this workspace.
> **Version 3.0** - Maestro AI Development Orchestrator

---

## ⚠️ CRITICAL: Use Maestro System

**MANDATORY:** When working in this project, you MUST:

1. **Check available agents** in `agents/` before starting complex tasks
2. **Use appropriate skills** from `skills/` for domain-specific knowledge
3. **ALWAYS check CODEBASE.md** file tree before making any file changes - it shows project structure and file dependencies
4. **Respect File Dependency Awareness** - check `←` annotations before making changes
5. **Use slash commands** (`/create`, `/debug`, etc.) for structured workflows

> ⚠️ Do NOT ignore this system. Maestro provides specialized agents, skills, and workflows that improve code quality and prevent errors.

---

## 🚀 Quick Start Commands

| Command | Description |
|---------|-------------|
| `/create` | Create new application (natural language) |
| `/enhance` | Add features to existing app |
| `/preview` | Start/stop preview server |
| `/status` | Show project and agent status |
| `/brainstorm` | Structured idea exploration |
| `/debug` | Systematic problem investigation |
| `/test` | Generate and run tests |
| `/deploy` | Production deployment (⚠️ CRITICAL) |
| `/orchestrate` | Multi-agent coordination |

### Usage Examples

```
/create e-commerce site with product listing and cart
/create blog site
/create Instagram clone with photo sharing
/enhance add dark mode
/enhance build admin panel
/brainstorm authentication options
/debug login not working
/test user service
/deploy production
```

---

## 📖 Context Loading Order

Claude Code reads context files in this order:

1. **`CLAUDE.md`** (this file) - Workspace-level configuration
2. **`CODEBASE.md`** - Auto-generated project context (injected via hook stdout)

### Why CODEBASE.md in Project Root?

Context injection requires hook stdout output. `CODEBASE.md` is created in project root for reference:

**How it works:**
1. `session_hooks.py` creates `CODEBASE.md` in project root (for reference)
2. Hook outputs content to stdout (for Claude context injection)
3. Both happen on every session start

> **Note:** `CODEBASE.md` is auto-generated on each session start and contains:
> - Project type detection (Node.js, Python, etc.)
> - Framework identification (Next.js, React Native, etc.)
> - OS-specific terminal commands
> - Complete project structure tree
> - Clean code standards

---

## 🤖 Available Agents (18)

### Orchestration Agents

| Agent | Expertise |
|-------|-----------|
| `project-planner` | Task breakdown, dependency graph, planning |
| `orchestrator` | Multi-agent coordination, parallel execution |

### Specialist Agents

| Agent | Expertise |
|-------|-----------|
| `frontend-specialist` | React, Next.js, Tailwind CSS, TypeScript |
| `backend-specialist` | Node.js, Express, Python, FastAPI |
| `database-architect` | PostgreSQL, Prisma, schema design |
| `devops-engineer` | PM2, deployment, CI/CD (⚠️ CRITICAL) |
| `test-engineer` | Jest, Pytest, Playwright, TDD |
| `security-auditor` | OWASP Top 10:2025, vulnerability scanning |
| `penetration-tester` | 🆕 Offensive security, PTES, red team |
| `performance-optimizer` | Core Web Vitals, bundle optimization |
| `mobile-developer` | React Native, Flutter, Expo |
| `api-designer` | REST API, GraphQL, OpenAPI |
| `documentation-writer` | README, JSDoc, API docs |
| `explorer-agent` | Deep directory scan, tech stack survey |
| `debugger` | Root cause analysis, systematic debugging |
| `seo-specialist` | 🆕 SEO, GEO, E-E-A-T, AI citations |
| `game-developer` | 🆕 Unity, Godot, Unreal, Phaser, multiplayer |

---

## 📚 Skills (50)

### Core Skills

| Skill | Purpose |
|-------|---------|
| `app-builder` | Main orchestrator - project building |
| `clean-code` | **CRITICAL** - Concise, direct coding - no over-engineering |
| `lint-and-validate` | **🆕 AI Quality Audit** - Style, logic, security (Ruff, ESLint) |
| `conversation-manager` | User communication protocol |
| `behavioral-modes` | AI modes: brainstorm, implement, debug, ship |
| `geo-fundamentals` | **GEO** - AI search optimization (ChatGPT, Claude, Perplexity) |
| `seo-fundamentals` | **SEO** - E-E-A-T, Core Web Vitals, Google updates |

### Templates (12)

| Template | Description |
|----------|-------------|
| `nextjs-fullstack` | Next.js + Prisma + Auth |
| `nextjs-saas` | SaaS + Stripe + NextAuth |
| `nextjs-static` | Landing page + Framer Motion |
| `express-api` | REST API + JWT + Zod |
| `python-fastapi` | FastAPI + SQLAlchemy + Pydantic |
| `react-native-app` | Expo + React Query + Zustand |
| `flutter-app` | Flutter + Riverpod + Go Router |
| `electron-desktop` | Electron + React + IPC |
| `chrome-extension` | Manifest V3 + React + Vite |
| `cli-tool` | Commander.js + Inquirer + chalk |
| `monorepo-turborepo` | Turborepo + pnpm workspaces |
| `astro-static` | Astro + MDX + Content Collections |

### Pattern Skills

```
skills/
├── api-patterns/         # REST/GraphQL patterns
├── react-patterns/       # React component patterns
├── mobile-patterns/      # Mobile development
├── nodejs-best-practices/
├── nextjs-best-practices/
├── tailwind-patterns/
├── database-design/
├── security-checklist/
├── testing-patterns/
├── vulnerability-scanner/ # 🆕 DAST, SAST, SCA tools
├── red-team-tactics/     # 🆕 MITRE ATT&CK, exploitation
├── api-security-testing/ # 🆕 OWASP API Top 10, JWT
└── ... (49 total)
```

---

## 🐍 Python Scripts

| Script | Hook | Purpose |
|--------|------|---------|
| `session_hooks.py` | SessionStart/End | Project detection, session tracking, dependency analysis |
| `lint_check.py` | - | 🆕 AI Quality Audit (Ruff, Bandit, ESLint, TSC) |
| `dependency_scanner.py` | SessionStart | 🆕 File dependency analysis (imports, API calls, DB models) |
| `explorer_helper.py` | SessionStart | Deep project discovery |
| `session_manager.py` | - | Project state management |
| `auto_preview.py` | - | Preview server control |
| `setup.py` | - | Cross-platform installation |

### Dependencies

```bash
pip install rich pydantic
```

---

## 📋 Core Principles

### User Confirmation Rule

**CRITICAL:** Before taking any action outside explicit user request, **ALWAYS ask the user first.**

When user request is unclear or could be implemented multiple ways:
- Ask clarifying questions
- Offer options with trade-offs
- Wait for user decision
- Consider current tool (CLI, extension, etc.) when asking

**Examples:**
- User: "optimize performance" → Ask: "Which area? Bundle size? Runtime? Database queries?"
- User: "add authentication" → Ask: "Which method? JWT? Session? OAuth?"
- User: "fix the bug" → Ask: "Which bug? Can you describe the issue?"

**What requires confirmation:**
- ❌ NOT: Simple, direct tasks with clear requirements
- ✅ YES: Ambiguous requests with multiple valid approaches
- ✅ YES: Changes affecting architecture or multiple files
- ✅ YES: Installing new dependencies or tools

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

## 🎭 Behavioral Modes

| Mode | Trigger Keywords | Behavior |
|------|------------------|----------|
| BRAINSTORM | "ideas", "options", "what if" | Explore alternatives, no code |
| IMPLEMENT | "build", "create", "add" | Fast execution, production code |
| DEBUG | "error", "not working", "bug" | Systematic investigation |
| REVIEW | "review", "check", "audit" | Thorough analysis |
| TEACH | "explain", "how does" | Educational explanations |
| SHIP | "deploy", "production" | Pre-flight checks, safety |

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

## 📁 Project Structure

```
c:\claude\
├── agents/          # 18 specialized agents
├── skills/          # 49 knowledge resources
├── commands/        # 10 slash commands
├── scripts/         # 6 Python automation scripts
├── data/            # Runtime state
├── settings.json    # Hook configuration
├── README.md        # Project documentation
└── CLAUDE.md        # This file
```

---

## ⚙️ Hook Configuration

Hooks are configured in `settings.json` (platform-specific):

### Windows (`settings.example.windows.json`)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python \"%USERPROFILE%\\.claude\\scripts\\session_hooks.py\" start"
          },
          {
            "type": "command",
            "command": "python \"%USERPROFILE%\\.claude\\scripts\\explorer_helper.py\" . --silent"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python \"%USERPROFILE%\\.claude\\scripts\\session_hooks.py\" end --silent"
          }
        ]
      }
    ]
  }
}
```

### macOS/Linux (`settings.example.unix.json`)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/scripts/session_hooks.py start"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/scripts/explorer_helper.py . --silent"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/scripts/session_hooks.py end --silent"
          }
        ]
      }
    ]
  }
}
```

**Key Differences:**
- **Windows:** Uses `python` and `%USERPROFILE%\.claude\` paths
- **macOS/Linux:** Uses `python3` and `~/.claude/` paths
- **SessionStart:** Runs both `session_hooks.py` and `explorer_helper.py`
- **SessionEnd:** Only runs `session_hooks.py` with `--silent` flag

---

**Version:** 3.1 - Maestro AI Development Orchestrator  
**Last Updated:** 2026-01-02

