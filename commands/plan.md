---
description: Create project plan using project-planner agent. No code writing - only PLAN.md generation.
---

# /plan - Project Planning Mode

$ARGUMENTS

---

## 🔴 CRITICAL RULES

1. **NO CODE WRITING** - This command creates PLAN.md only
2. **Use project-planner agent** - NOT Claude Code's native Plan subagent
3. **Socratic Gate** - Ask clarifying questions before planning

---

## Task

Use the `project-planner` agent with this context:

```
CONTEXT:
- User Request: $ARGUMENTS
- Mode: PLANNING ONLY (no code)
- Output: docs/PLAN.md

RULES:
1. Follow project-planner.md Phase -1 (Context Check)
2. Follow project-planner.md Phase 0 (Socratic Gate)
3. Create PLAN.md with task breakdown
4. DO NOT write any code files
```

---

## Expected Output

| Deliverable | Location |
|-------------|----------|
| Project Plan | `docs/PLAN.md` |
| Task Breakdown | Inside PLAN.md |
| Agent Assignments | Inside PLAN.md |
| Verification Checklist | Phase X in PLAN.md |

---

## After Planning

Tell user:
```
✅ Plan created: docs/PLAN.md

Next steps:
- Review the plan
- Run `/create` to start implementation
- Or modify plan manually
```

---

## Usage

```
/plan e-commerce site with cart
/plan mobile app for fitness tracking
/plan SaaS dashboard with analytics
```
