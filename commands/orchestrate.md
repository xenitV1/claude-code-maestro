---
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
---

# Multi-Agent Orchestration

You are now in **ORCHESTRATION MODE**. Your task: coordinate specialized agents to solve this complex problem.

## Task to Orchestrate
$ARGUMENTS

---

## Pre-Flight: Mode Check

**CRITICAL:** Before orchestrating, check current Claude Code mode:

| Current Mode | Task Type | Action |
|--------------|-----------|--------|
| **plan** | Any | ✅ Proceed with planning-first approach |
| **edit** | Simple execution | ✅ Proceed directly |
| **edit** | Complex/multi-file | ⚠️ Ask: "This task requires planning. Switch to plan mode?" |
| **ask** | Any | ⚠️ Ask: "Ready to orchestrate. Switch to edit or plan mode?" |

**If task requires planning but mode is not `plan`:**
> "Bu görev planlama gerektiriyor. Plan moduna geçmek ister misiniz? (`/plan` ile geçebilirsiniz)"

---

## Dynamic Priority by Mode

### Plan Mode Priority
```
1. project-planner     → Task breakdown
2. explorer-agent      → Discovery
3. [domain-agents]     → Analysis
4. documentation-writer → Document plan
```

### Edit Mode Priority
```
1. explorer-agent      → Quick discovery
2. [domain-agents]     → Implementation
3. test-engineer       → Verification
4. devops-engineer     → Deployment (if needed)
```

### Debug Mode Priority (triggered by /debug keywords)
```
1. debugger            → Root cause
2. explorer-agent      → Context
3. test-engineer       → Reproduce
4. [domain-agents]     → Fix
```

### Security Mode Priority (triggered by security keywords)
```
1. security-auditor    → Vulnerabilities
2. penetration-tester  → Active testing
3. backend-specialist  → Secure implementation
4. devops-engineer     → Hardening
```

---

## Orchestration Protocol

### Step 1: Analyze the Task
Identify which domains this task touches:
- Security? → security-auditor, penetration-tester
- Backend/API? → backend-specialist, api-designer
- Frontend/UI? → frontend-specialist
- Database? → database-architect
- Testing? → test-engineer
- DevOps? → devops-engineer
- Mobile? → mobile-developer
- Debugging? → debugger
- Discovery? → explorer-agent
- Documentation? → documentation-writer
- Performance? → performance-optimizer
- Planning? → project-planner
- SEO? → seo-specialist
- Game Development? → game-developer

### Step 2: Select Agents (17 available)
Choose agents based on current mode priority and task requirements.

### Step 3: Execute Sequentially
Invoke each agent using native Agent Tool:
```
Use the [agent-name] agent to [specific task]
```

### Step 4: Synthesize Results
Combine all agent outputs into a unified report.

---

## Invocation Syntax

**Single Agent:**
```
Use the security-auditor agent to analyze authentication vulnerabilities
```

**Chained Agents:**
```
First, use explorer-agent to map the codebase structure.
Then, use backend-specialist to review the API layer.
Finally, use test-engineer to identify missing tests.
```

---

## Output Format

```markdown
## 🎼 Orchestration Report

### Task
[Original task summary]

### Mode
[Current Claude Code mode: plan/edit/ask]

### Agents Invoked
| Agent | Focus Area | Status |
|-------|------------|--------|
| agent-name | What they analyzed | ✅ |

### Key Findings
1. **[Agent]**: Finding
2. **[Agent]**: Finding

### Recommendations
- [ ] Priority 1: ...
- [ ] Priority 2: ...

### Summary
[One paragraph synthesis]
```

---

**Begin orchestration now. Check mode, apply priority, invoke agents, synthesize results.**
