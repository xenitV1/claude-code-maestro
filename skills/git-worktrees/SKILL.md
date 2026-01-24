---
name: git-worktrees
description: Create isolated git workspaces for feature development. Smart directory selection, safety verification, and cross-platform support (Windows/Unix).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
<domain_overview>
# 🌳 GIT WORKTREES: ISOLATED WORKSPACES
> **Philosophy:** Isolation prevents contamination. Work on features without affecting the main workspace. Systematic directory selection + safety verification = reliable isolation.
**ISOLATION INTEGRITY MANDATE (CRITICAL):** Never create worktrees in directories that are not explicitly ignored by Git. AI-generated workflows often fail by polluting the primary repository with tracked worktree data. You MUST verify that the destination directory is within `.gitignore` before execution. Furthermore, you MUST ensure a 'Clean Baseline' by running tests before starting any feature work in a new worktree to avoid cross-contamination of artifacts.
</domain_overview>
---
<directory_selection>
## 🎯 OVERVIEW
Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.
**Benefits:**
- Work on feature branch without stashing changes
- Test in isolation without affecting main workspace
- Run long processes without blocking other work
- Easy cleanup when feature is complete

---
## 📋 WHEN TO USE
**Use before:**
- Starting new feature development
- Implementing plans from `@planning-mastery`
- Making experimental changes
- Working on multiple features in parallel
**Skip for:**
- Quick bug fixes on current branch
- Documentation updates
- Configuration changes
---
## 📁 DIRECTORY SELECTION PROCESS
Follow this priority order:
### 1. Check Existing Directories
**Unix/macOS:**
```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```
**Windows (PowerShell):**
```powershell
if (Test-Path ".worktrees") { ".worktrees" }
elseif (Test-Path "worktrees") { "worktrees" }
```
**If found:** Use that directory. If both exist, `.worktrees` wins.
### 2. Check CLAUDE.md
```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```
**If preference specified:** Use it without asking.
### 3. Ask User
If no directory exists and no CLAUDE.md preference:
```
No worktree directory found. Where should I create worktrees?
1. .worktrees/ (project-local, hidden)
2. %USERPROFILE%\.config\maestro\worktrees\<project>\ (global location)
Which would you prefer?
```
</directory_selection>
<safety_verification>
## 🔒 SAFETY VERIFICATION
### For Project-Local Directories
**MUST verify directory is ignored before creating worktree:**
**Unix/macOS:**
```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```
**Windows (PowerShell):**
```powershell
git check-ignore -q .worktrees 2>$null
if ($LASTEXITCODE -ne 0) {
    git check-ignore -q worktrees 2>$null
}
```
**If NOT ignored:**
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation
**Why critical:** Prevents accidentally committing worktree contents to repository.
### For Global Directory
No .gitignore verification needed - outside project entirely.
</safety_verification>
<creation_and_setup>
## 🔨 CREATION STEPS
### 1. Detect Project Name
**Unix/macOS:**
```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```
**Windows (PowerShell):**
```powershell
$project = Split-Path -Leaf (git rev-parse --show-toplevel)
```
### 2. Create Worktree
**Unix/macOS:**
```bash
# Project-local
path=".worktrees/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
# Or global
path="$HOME/.config/maestro/worktrees/$project/$BRANCH_NAME"
mkdir -p "$(dirname "$path")"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```
**Windows (PowerShell):**
```powershell
# Project-local
$path = ".worktrees\$BRANCH_NAME"
git worktree add $path -b $BRANCH_NAME
Set-Location $path
# Or global
$path = "$env:USERPROFILE\.config\maestro\worktrees\$project\$BRANCH_NAME"
New-Item -ItemType Directory -Force -Path (Split-Path $path)
git worktree add $path -b $BRANCH_NAME
Set-Location $path
```
### 3. Run Project Setup
Auto-detect and run appropriate setup:
**Cross-platform:**
```bash
# Node.js
if [ -f package.json ]; then npm install; fi
# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi
# Rust
if [ -f Cargo.toml ]; then cargo build; fi
# Go
if [ -f go.mod ]; then go mod download; fi
```

**Windows (PowerShell):**
```powershell
# Node.js
if (Test-Path "package.json") { npm install }

# Python
if (Test-Path "requirements.txt") { pip install -r requirements.txt }
if (Test-Path "pyproject.toml") { poetry install }

# Rust
if (Test-Path "Cargo.toml") { cargo build }

# Go
if (Test-Path "go.mod") { go mod download }
```

### 4. Verify Clean Baseline
Run tests to ensure worktree starts clean:
```bash
# Use project-appropriate command
npm test
pytest
cargo test
go test ./...
```
**If tests fail:** Report failures, ask whether to proceed or investigate.
**If tests pass:** Report ready.
### 5. Report Location
```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```
</creation_and_setup>
<audit_and_reference>
## 📊 QUICK REFERENCE
| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |
---
## 🧹 CLEANUP
When feature work is complete:
**List worktrees:**
```bash
git worktree list
```
**Remove worktree:**
```bash
git worktree remove .worktrees/feature-name
# or force if uncommitted changes
git worktree remove --force .worktrees/feature-name
```
**Prune stale entries:**
```bash
git worktree prune
```
---
## 🚫 COMMON MISTAKES

### Skipping ignore verification
- **Problem:** Worktree contents get tracked, pollute git status
  - **Fix:** Always use `git check-ignore` before creating project-local worktree
### Assuming directory location
- **Problem:** Creates inconsistency, violates project conventions
  - **Fix:** Follow priority: existing > CLAUDE.md > ask
### Proceeding with failing tests
- **Problem:** Can't distinguish new bugs from pre-existing issues
  - **Fix:** Report failures, get explicit permission to proceed
### Hardcoding setup commands
- **Problem:** Breaks on projects using different tools
  - **Fix:** Auto-detect from project files (package.json, etc.)
### Forgetting to cleanup
- **Problem:** Disk space consumed, stale branches accumulate
  - **Fix:** Remove worktree when feature is merged
---

## 📝 EXAMPLE WORKFLOW
```
You: I'm using the git-worktrees skill to set up an isolated workspace.
[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]
Worktree ready at C:\Users\Dev\myproject\.worktrees\auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```
---
## 🚨 RED FLAGS
**Never:**
- Create worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip CLAUDE.md check
**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify directory is ignored for project-local
- Auto-detect and run project setup
- Verify clean test baseline
- Report full path when done
---
## 🔗 INTEGRATION
### Called by:
- `@brainstorming` - After design approved, before implementation
- `@planning-mastery` - When executing plan
### Pairs with:
- `@planning-mastery` - Work happens in this worktree
- `@tdd-mastery` - Implementation methodology
- `@verification-mastery` - Complete development after all tasks
---
## 🔗 RALPH WIGGUM INTEGRATION
When Ralph Wiggum is active:
1. **Before first iteration:** Create worktree for isolated work
2. **During iterations:** All work happens in worktree
3. **After completion:** Merge or create PR from worktree
4. **Cleanup:** Remove worktree after merge
---
## 🔗 RELATED SKILLS
- **@brainstorming** - Design before worktree creation
- **@planning-mastery** - Plan to execute in worktree
- **@verification-mastery** - Verify before finishing branch
</audit_and_reference>
