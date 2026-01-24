# Maestro: AI Development Orchestrator

Elite-tier orchestration framework for Claude Code CLI. Supercharges AI development through specialized agents, modular skills, intelligent hooks, and persistent memory systems.

> **Version:** 0.6.0  
> **Author:** [xenitV1](https://github.com/xenitV1) • [X/Twitter](https://x.com/xenit_v0)  
> **Philosophy:** "Why over How. Architecture precedes implementation."

## Quick Start

### Installation

Maestro is distributed as a Claude Code Plugin. To install it, you first need to add the repository as a marketplace:

```bash
# 1. Add Maestro as a marketplace
/plugin marketplace add xenitV1/claude-code-maestro

# 2. Install the Maestro plugin
/plugin install maestro@xenitV1-claude-code-maestro
```

### Prerequisites

- **Node.js 18+** (required for hooks)
- Claude Code CLI

### Usage

Since Maestro is a plugin, its commands are namespaced. Use the format `/maestro:command`.

```bash
# Basic orchestration
/maestro your task description

# With Ralph Wiggum (autonomous iterations)
/maestro fix bugs and improve code. ralph 5 iterations

# Design mode
/maestro design new authentication system

# Plan mode
/maestro plan implement user dashboard

# Use the Grandmaster agent directly
/agent:grandmaster
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MAESTRO SYSTEM                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────────────┐   │
│  │ /maestro │───▶│ grandmaster  │───▶│       SKILLS            │   │
│  │ command  │    │    agent     │    │ (frontend, backend,     │   │
│  └──────────┘    └──────────────┘    │  tdd, debug, etc.)      │   │
│                         │            └─────────────────────────┘   │
│                         ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HOOK SYSTEM                               │   │
│  │  SessionStart │ PostToolUse │ Stop │ PreCompact │ etc.      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                         │                                           │
│                         ▼                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    LONG-TERM MEMORY (LTM)                      │   │
│  │                      (brain.jsonl)                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
maestro/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/
│   └── grandmaster.md       # Central orchestrator agent
├── commands/
│   └── maestro.md           # /maestro slash command
├── hooks/
│   ├── hooks.json           # Hook configuration
│   ├── lib/                 # Shared JS utilities
│   │   ├── utils.js         # Cross-platform utilities
│   │   ├── brain.js         # LTM operations
│   │   └── ralph.js         # Ralph state management
│   ├── session-start.js     # Tech stack detection + LTM injection
│   ├── brain-sync.js        # LTM sync (PostToolUse)
│   ├── stop.js              # Ralph Wiggum iteration
│   ├── ralph.js             # QA enforcement
│   ├── sentinel.js          # Change detection
│   └── pre-maestro.js       # Skill recommendation
├── skills/
│   ├── clean-code/          # Code quality standards
│   ├── frontend-design/     # Elite UI/UX
│   ├── backend-design/      # API & Database patterns
│   ├── tdd-mastery/         # Test-Driven Development
│   ├── debug-mastery/       # Systematic debugging
│   ├── verification-mastery/# Evidence-based completion
│   ├── brainstorming/       # Design-first methodology
│   ├── planning-mastery/    # Implementation planning
│   ├── git-worktrees/       # Isolated workspaces
│   ├── ralph-wiggum/        # Autonomous QA system
│   ├── browser-extension/   # Extension development
│   └── optimization-mastery/# Performance optimization
├── package.json             # Node.js metadata
├── LICENSE                  # MIT License
└── README.md
```

## Memory Systems

### Long-Term Memory (brain.jsonl)
Persistent project context across sessions:
- **Tech Stack:** Frameworks, dependencies, architecture patterns
- **Decisions:** Key architectural decisions made
- **Goals:** Project objectives
- **Errors:** Known issues and blockers
- **Compact History:** Session summaries after context compaction
- **File Changes:** Changelog of edits and creates

## Ralph Wiggum: Autonomous QA

Elite QA system with Four Pillars:

| Pillar | Purpose |
|--------|---------|
| **Proactive Gate** | Edge case identification BEFORE coding |
| **Reflection Loop** | Self-critique and refinement |
| **Verification Matrix** | Test coverage tracking (80% minimum) |
| **Circuit Breaker** | Stagnation detection and pivot strategies |

Activate with: `ralph N iterations` or "Ralph Wiggum mode"

## Skills Overview

| Skill | Description |
|-------|-------------|
| `clean-code` | 2025 standards, SOLID, security-first |
| `frontend-design` | Atomic Design 2.0, Lovable/v0 standard |
| `backend-design` | Zero-trust, API contracts |
| `tdd-mastery` | Iron Law: Test before code |
| `debug-mastery` | 4-phase systematic debugging |
| `verification-mastery` | Evidence before completion |
| `brainstorming` | Design-first methodology |
| `planning-mastery` | Bite-sized task breakdown |
| `git-worktrees` | Isolated feature development |
| `ralph-wiggum` | Autonomous QA orchestration |
| `optimization-mastery` | Performance, INP, partial hydration |
| `context7` | Auto library documentation from Upstash |
| `browser-extension` | Manifest v3, service workers |

## Platform Compatibility

| Platform | Rating | Notes |
|----------|--------|-------|
| **Claude Code CLI** | ⭐⭐⭐⭐⭐ | Native environment, full functionality |
| **Windows** | ⭐⭐⭐⭐⭐ | Full cross-platform support |
| **macOS** | ⭐⭐⭐⭐⭐ | Full cross-platform support |
| **Linux** | ⭐⭐⭐⭐⭐ | Full cross-platform support |

## Core Protocols

1. **Socratic Gate:** Ask clarifying questions before assuming
2. **Think First:** `<think>` before complex actions
3. **TDD Iron Law:** No production code without failing test
4. **Verification:** Evidence before completion claims
5. **Clean Code:** No TODO/FIXME, no lazy placeholders

## Acknowledgments

Several skills were inspired by and adapted from [obra/superpowers](https://github.com/obra/superpowers) and have been heavily optimized for the Maestro orchestration environment:

| Feature | Source | Maestro Skill |
|---------|--------|---------------|
| TDD Iron Law | superpowers/tdd | `tdd-mastery` |
| Systematic Debugging | superpowers/debugging | `debug-mastery` |
| Verification Protocol | superpowers/verification | `verification-mastery` |
| Brainstorming Method | superpowers/brainstorming | `brainstorming` |
| Implementation Planning | superpowers/planning | `planning-mastery` |
| Git Worktrees | superpowers/worktrees | `git-worktrees` |

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=xenitV1/claude-code-maestro&type=Date)](https://star-history.com/#xenitV1/claude-code-maestro&Date)

## Author

Created and maintained by **[xenitV1](https://github.com/xenitV1)**

- GitHub: [github.com/xenitV1](https://github.com/xenitV1)
- X/Twitter: [x.com/xenit_v0](https://x.com/xenit_v0)

## License

MIT License - See [LICENSE](LICENSE) for details.

---

*Orchestrating the future of autonomous development.*
