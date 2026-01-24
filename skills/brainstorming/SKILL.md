---
name: brainstorming
description: Design-first methodology. Explore user intent, requirements and design before implementation. Turn ideas into fully formed specs through collaborative dialogue.
---
<domain_overview>
# 💡 BRAINSTORMING: DESIGN BEFORE CODE
> **Philosophy:** Understanding comes before implementation. A well-designed solution is half-implemented. Never code without a clear design.

**HALLUCINATION FIREWALL MANDATE (CRITICAL):** Never propose software components or libraries without verification. AI-generated designs frequently fail by hallucinating non-existent packages or misinterpreting their capabilities. Every recommended 3rd-party library MUST be validated using `npm info` or equivalent before the plan is finalized. Furthermore, you MUST provide at least one 'Counter-Architecture' (Steel-man argument) that challenges your primary recommendation to prevent homogenized or biased designs.
Help turn ideas into fully formed designs and specs through natural collaborative dialogue.
**Process:**
1. Understand the current project context
2. Ask questions one at a time to refine the idea
3. Present the design in small sections (200-300 words)
4. Check after each section whether it looks right
---
## 📋 WHEN TO USE
**MUST use before:**
- Creating new features
- Building new components
- Adding significant functionality
- Modifying core behavior
- Any task that takes more than 30 minutes
**Skip only for:**
- Simple bug fixes with obvious solutions
- Documentation updates
- Trivial configuration changes
</domain_overview>
<process_workflow>
## 🔄 THE PROCESS
### Phase 1: Understanding the Idea
**First, check current project state:**
- Review relevant files and docs
- Check recent commits
- Understand existing patterns
**Then ask questions one at a time:**
- **MANDATORY:** Use the `AskUserQuestion` tool for ALL questions.
- Prefer multiple choice options within the tool whenever possible.
- Open-ended questions should also use `AskUserQuestion` (users can use the 'Other' option).
- **Only one question per tool call.**
- If topic needs more exploration, break into multiple sequential tool calls.
**Focus on understanding:**
- Purpose: What problem does this solve?
- Constraints: What limitations exist?
- Success criteria: How do we know it works?
- Edge cases: What could go wrong?
### Phase 2: Exploring Approaches
**Always propose 2-3 different approaches with trade-offs:**
```
I see three possible approaches:
**Option A: [Name]**
- Pros: Simple, fast to implement
- Cons: May not scale, harder to test
- Best for: Quick prototypes
**Option B: [Name]**
- Pros: Scalable, well-tested pattern
- Cons: More complex, longer implementation
- Best for: Production systems
**Option C: [Name]**
- Pros: Flexible, future-proof
- Cons: Over-engineered for current needs
- Best for: When requirements are uncertain
**My recommendation:** Option B because [reasoning]
Which approach resonates with your goals?
```
**Lead with your recommended option and explain why.**
### Phase 3: Presenting the Design
**Once you understand what you're building, present the design:**
1. **Break it into sections of 200-300 words**
2. **Ask after each section:** "Does this look right so far?"
3. **Be ready to go back and clarify** if something doesn't make sense
**Cover these areas:**
- Architecture: How components fit together
- Components: What pieces we need to build
- Data flow: How information moves through the system
- Error handling: What happens when things fail
- Testing: How we verify it works
### Phase 4: Documentation
**After design is validated:**
1. Write the design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
2. Commit the design document to git
3. Ask: "Ready to set up for implementation?"
</process_workflow>
<methodology_protocols>
## 🎤 QUESTION TECHNIQUES
### Multiple Choice (MANDATORY TOOL USE)
Always use the `AskUserQuestion` tool for structured feedback:
```json
{
  "questions": [
    {
      "header": "Auth Method",
      "question": "How should users authenticate?",
      "options": [
        {"label": "JWT Tokens", "description": "Stateless, scalable"},
        {"label": "Server Sessions", "description": "Simple, secure"},
        {"label": "OAuth Only", "description": "Delegate to providers"}
      ],
      "multiSelect": false
    }
  ]
}
```
### Open-Ended (Using Tool)
Even for open-ended questions, use the tool. The CLI will provide an "Other" option for custom text input.
"What's the most important user story for this feature?"
### Clarifying
"You mentioned 'fast' - what response time would feel fast enough?"
---
## 🚫 ANTI-PATTERNS TO AVOID
| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Multiple questions at once | One question per message |
| Jumping to implementation | Complete design first |
| Assuming requirements | Ask to confirm |
| Presenting 1000-word designs | 200-300 word sections |
| Ignoring trade-offs | Always present alternatives |
| Skipping edge cases | Explore failure modes |
</methodology_protocols>
<design_artifacts>
## 📝 DESIGN DOCUMENT TEMPLATE
```markdown
# [Feature Name] Design
**Date:** YYYY-MM-DD
**Author:** Grandmaster (with user collaboration)
**Status:** Draft | Approved | Implemented
## Problem Statement
What problem are we solving? Why does it matter?
## Goals
- Primary goal
- Secondary goals
- Non-goals (explicitly out of scope)
## Approach
### Architecture
How components fit together.
### Components
1. **Component A**
   - Purpose
   - Interface
   - Dependencies
2. **Component B**
   - Purpose
   - Interface
   - Dependencies
### Data Flow
1. User action triggers X
2. X calls Y with Z
3. Y returns result
4. Result displayed to user
### Error Handling
| Error | Handling | User Message |
|-------|----------|--------------|
| Network failure | Retry 3x | "Connection lost, retrying..." |
| Invalid input | Reject | "Please check your input" |
## Testing Strategy
- Unit tests for each component
- Integration test for happy path
- Edge case tests for error handling
## Open Questions
- [ ] Question 1
- [ ] Question 2
## Decision Log
| Date | Decision | Rationale |
|------|----------|-----------|
| YYYY-MM-DD | Chose Option B | Better scalability |
```
</design_artifacts>
<integration_protocols>
## 🔗 INTEGRATION WITH MAESTRO
### Triggering Brainstorming
User can invoke explicitly:
```
/maestro design [feature description]
```
Or system detects complex task and suggests:
```
This looks like a significant feature. Would you like to 
brainstorm the design first, or proceed directly?
```
### After Brainstorming
1. **If continuing to implementation:**
   - Use `@planning-mastery` to create detailed plan
   - Use `@git-worktrees` to create isolated workspace
2. **If pausing:**
   - Design document is saved
   - Can resume later with `/maestro plan [design-doc]`
---
## 🔗 RALPH WIGGUM INTEGRATION
When Ralph Wiggum is active with "Feature Mode":
1. **Before first iteration:** Run brainstorming phase
2. **Design document:** Required before implementation begins
3. **Scope lock:** Don't add features not in design
4. **Design changes:** Require explicit approval
</integration_protocols>
<audit_and_reference>
## 📋 KEY PRINCIPLES
| Principle | Description |
|-----------|-------------|
| **One question at a time** | Don't overwhelm with multiple questions |
| **Multiple choice preferred** | Easier to answer than open-ended |
| **YAGNI ruthlessly** | Remove unnecessary features from designs |
| **Explore alternatives** | Always propose 2-3 approaches |
| **Incremental validation** | Present design in sections, validate each |
| **Be flexible** | Go back and clarify when needed |
---
## 🔗 RELATED SKILLS
- **@planning-mastery** - Create implementation plan from design
- **@git-worktrees** - Set up isolated workspace
- **@tdd-mastery** - Implement with tests first
- **@clean-code** - Quality standards for implementation
</audit_and_reference>
