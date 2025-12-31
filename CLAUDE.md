# CLAUDE.md - Maestro Configuration

> This file defines how Claude AI behaves in this workspace.
> **Version 3.0** - Maestro AI Development Orchestrator

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
2. **`.claude/rules.md`** - Auto-generated project context (created by session hooks)

> **Note:** `.claude/rules.md` is auto-generated on each session start and contains:
> - Project type detection (Node.js, Python, etc.)
> - Framework identification (Next.js, React Native, etc.)
> - OS-specific terminal commands
> - Complete project structure tree
> - Clean code standards

---

## 🤖 Available Agents (15)

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

---

## 📚 Skills (40)

### Core Skills

| Skill | Purpose |
|-------|---------|
| `app-builder` | Main orchestrator - project building |
| `clean-code` | **CRITICAL** - Concise, direct coding - no over-engineering |
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
└── ... (40 total)
```

---

## 🐍 Python Scripts

| Script | Hook | Purpose |
|--------|------|---------|
| `session_hooks.py` | SessionStart/End | Project detection, session tracking |
| `explorer_helper.py` | SessionStart | Deep project discovery |
| `parallel_orchestrator.py` | - | Parallel agent orchestrator |
| `session_manager.py` | - | Project state management |
| `auto_preview.py` | - | Preview server control |

### Dependencies

```bash
pip install rich pydantic
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

## � Claude Code Mode Mapping

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
├── agents/          # 14 specialized agents
├── skills/          # 37 knowledge resources
├── commands/        # 8 slash commands
├── scripts/         # 5 Python automation scripts
├── data/            # Runtime state
├── settings.json    # Hook configuration
├── README.md        # Project documentation
└── CLAUDE.md        # This file
```

---

## ⚙️ Hook Configuration

Hooks are configured in `settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [{
          "type": "command",
          "command": "python scripts/session_hooks.py start --silent"
        }]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "python scripts/session_hooks.py end --silent"
        }]
      }
    ]
  }
}
```

---

## 📊 Statistics

| Category | Count |
|----------|-------|
| Agents | 14 |
| Skills | 37 |
| Commands | 8 |
| Scripts | 5 |
| Templates | 12 |

---

**Version:** 3.0 - Maestro AI Development Orchestrator  
**Last Updated:** 2025-12-31
