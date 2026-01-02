# 🤖 Maestro Agents

Specialized AI agents for different development domains. Each agent has specific expertise, tools, and skill references.

## Agent List

| Agent | Lines | Expertise |
|-------|-------|-----------|
| [penetration-tester](penetration-tester.md) | 280 | 🆕 Offensive security, PTES, exploitation, red team |
| [debugger](debugger.md) | 250 | Root cause analysis, systematic debugging |
| [api-designer](api-designer.md) | 521 | REST/GraphQL, OpenAPI, API security |
| [mobile-developer](mobile-developer.md) | 354 | React Native, Flutter, Expo, App Store |
| [devops-engineer](devops-engineer.md) | 275 | PM2, deployment, CI/CD, rollback |
| [test-engineer](test-engineer.md) | 268 | Testing strategies, TDD, coverage |
| [security-auditor](security-auditor.md) | 230 | OWASP Top 10:2025, vulnerability scanning |
| [explorer-agent](explorer-agent.md) | 210 | Codebase exploration, dependency research |
| [orchestrator](orchestrator.md) | 209 | Multi-agent coordination |
| [database-architect](database-architect.md) | 189 | Schema design, Prisma, migrations |
| [backend-specialist](backend-specialist.md) | 187 | Node.js, Express, FastAPI |
| [frontend-specialist](frontend-specialist.md) | 149 | React, Next.js, Tailwind |
| [project-planner](project-planner.md) | 140 | Task breakdown, planning |
| [performance-optimizer](performance-optimizer.md) | 132 | Performance profiling |
| [documentation-writer](documentation-writer.md) | 98 | Documentation, API docs |
| [seo-specialist](seo-specialist.md) | 110 | 🆕 SEO, GEO, Core Web Vitals, AI citations |


## Agent Format

Each agent follows this structure:

```yaml
---
name: agent-name
description: Brief description with trigger keywords
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: skill1, skill2
---

# Agent Name

## Your Expertise
## Code Patterns  
## Review Checklist
## When You Should Be Used
```

## Usage

Agents are invoked by Claude based on context. Keywords in user requests trigger appropriate agents.

**Triggers:**
- "deploy", "production" → devops-engineer
- "mobile", "react native" → mobile-developer
- "api", "endpoint" → api-designer
- "test", "coverage" → test-engineer
- "lint", "check quality", "validate" → lint-and-validate (skill)
