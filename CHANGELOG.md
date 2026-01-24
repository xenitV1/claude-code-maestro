# Changelog


**Author:** [xenitV1](https://github.com/xenitV1) | [X/Twitter](https://x.com/xenit_v0)

---

## [0.6.0] - 2026-01-24

### 🏗️ Major Project Evolution & Native Plugin Support

This version marks a turning point where the project has completely transformed and is fully integrated into the Claude Code Plugin ecosystem. The architecture has evolved from a multi-agent system to a centralized "Grandmaster" model.

### 🚀 Key Changes
- **Single Agent Model:** The multi-agent structure has been retired; there is now a single **Grandmaster Agent** (`agents/grandmaster.md`) that manages all operations and dynamically selects skills based on demand.
- **Long-Term Memory (LTM) System:** Introduced a persistent memory mechanism that tracks project context, architectural decisions, and recurring errors across sessions.
- **Claude Code Compaction Sync:** Integrated with Claude Code's `compact` feature; session summaries and key takeaways are now automatically saved to the LTM `brain` during context compaction.
- **XML Tag Transition:** All skill and agent content has been restructured with granular **XML tags** (`<domain_overview>`, `<core_workflow>`, etc.) to provide better context parsing for LLMs.
- **Claude Code Plugin Support:** The project is now a directly installable plugin supporting the official `.claude-plugin/plugin.json` standards.
- **Python to JS Migration:** All automation scripts have been converted from Python to **Node.js (JavaScript)** for full **cross-platform support** (Windows, macOS, Linux) and improved speed.

### ➕ Added
- **Persistent Error Collection:** Automatically identifies and stores repeating errors to provide smarter debugging strategies.
- **Ralph Wiggum Mode:** Added an autonomous debugging and iterative code development loop.
- **Context7 Integration:** Permanent memory and external documentation support via Upstash-based MCP server.
- **Mandates:** Added "Cyberpunk/Neon" ban in frontend and enforced Test-First/Evidence-based requirements.
- **Chat History Archiving:** Support for permanently saving session data and specific chat history upon request for long-term project continuity.

### 🧹 Cleanup
- Refined focus by removing over 20 legacy and bloated skill directories.
- Cleaned up unnecessary configuration files (Makefile, ARCHITECTURE.md, etc.).

### 🤝 Acknowledgments
- Several core skills were adapted and heavily optimized for the Maestro environment from [obra/superpowers](https://github.com/obra/superpowers), including: `debug-mastery`, `verification-mastery`, `tdd-mastery`, `planning-mastery`, and `brainstorming`, 'git-worktrees' .

### 🔧 Fixed
- Resolved version confusion (synced package.json, plugin.json, and documentation to 0.6.0).

---

## Pre-1.0 History (Python Version)

The following versions document the original Python-based implementation at [claude-code-maestro](https://github.com/xenitV1/claude-code-maestro).

---

## [0.3.3] - 2026-01-11

### 🧠 Intelligent Planning & Dynamic Naming

### Added

#### Analytical Mode (Survey)
- **`project-planner.md`** → Introduced **Analytical vs. Planning Mode**
  - **SURVEY Mode:** Triggers on "analyze", "find", "explain". Research only, no plan file created.
  - **PLANNING Mode:** Triggers on "build", "refactor", "create". Mandatory plan file required.
- **`CLAUDE.md`** → New **SURVEY/INTEL** request classification to prevent over-triggering the planning agent.

#### Dynamic Naming Enforcement
- **`project-planner.md`** → Strict ban on generic names like `plan.md`, `PLAN.md`, or `plan.dm`.
- Forced task-based naming (e.g., `auth-feature.md` instead of `plan.md`) for better project organization.

### Changed
- **`CLAUDE.md`** → **Edit Mode** logic softened: Only suggests a plan for multi-file/structural changes.

---

## [0.3.2] - 2026-01-09

### 🔧 Documentation Reduction & Workflow Improvements

### Changed

#### Documentation Generation
- Documentation agent marked as "explicit request only" (not auto-invoked)

#### Plan File System
- **Location:** `docs/PLAN-*.md` → `./[task-slug].md` (project root)
- **Naming:** Dynamic based on task, no `PLAN-` prefix required
- Complete rewrite of planning skill: Principles over templates

#### Approval Flow
- Plans now created and work proceeds without piece-by-piece approval

### Added

#### Agent Self-Check
- Goal met? Files edited? Code works? No errors? Nothing forgotten?

#### Dependency Awareness
- Before editing ANY file: What imports this? What does this import? What tests cover this?

#### OS Detection for Commands
- Windows → Use Claude Write tool for files, PowerShell for commands
- macOS/Linux → Can use `touch`, `mkdir -p`, bash commands

---

## [0.3.1] - 2026-01-09

### Fixed

#### Windows Console Encoding
- **13 Python scripts** updated to remove emoji characters causing `UnicodeEncodeError` on Windows cp1254 consoles
- Added UTF-8 safety encoding

#### SEO/GEO Script Bugs
- Complete rewrite of geo_checker.py and seo_checker.py

#### SessionEnd Hook Deprecated
- **`SessionEnd`** hook replaced with **`Stop`** per Claude Code CLI 2.1.2+ requirements

### Added

#### Game Development Enhancement
- `game-art/SKILL.md` and `game-audio/SKILL.md`

#### GEO Checker 2025 Updates
- Entity Recognition, Original Statistics/Data detection, Direct Answer Patterns

---

## [0.3.0] - 2026-01-09

### 🏗️ Modular Architecture Overhaul

### Added

#### 🔧 allowed-tools System
- When a skill is active, Claude can ONLY use specified tools (read-only security)

#### 📁 New Files
- **`/plan` command** → Planning-only mode
- **`ARCHITECTURE.md`** → Complete system architecture document
- **22+ new modular files** → SKILL.md files streamlined

#### 🐍 Python Scripts (Zero-Context Execution)
- Scripts execute without consuming context tokens
- playwright_runner.py, accessibility_checker.py, ux_audit.py, mobile_audit.py, lighthouse_audit.py, security_scan.py

### Changed
- **`orchestrator.md`** → Mandatory PLAN.md check, Socratic Gate
- **42 SKILL.md files** → Progressive Disclosure applied

### Removed
- `scripts/lint_check.py` (native npm commands faster)
- `skills/api-security-testing/` (consolidated)
- `skills/artifacts-builder/` (redundant)
- `skills/git-worktrees/` (rarely used)

---

## [0.2.4] - 2026-01-06

### 📱 Comprehensive Mobile Development Expansion

### Added
- **13 New Specialized Mobile Skills**
- Touch Psychology & Ergonomics (Fitts' Law, Thumb Zone)
- Mandatory Build Verification Loop
- Flutter and Ionic/Capacitor detection

### Fixed
- `node_modules` exclusion in explorer helper
- Setup script counters

---

## [0.2.0] - 2026-01-05

### 🎨 Major Design Philosophy Overhaul

### Added
- **NO AI MEMORY STYLES** rule
- **PURPLE BAN** - No purple/violet hex codes allowed
- **NO TEMPLATE LAYOUTS** - Asymmetric layouts required
- **Full Skill Chain Loading** procedure
- **7 new frontend design reference files**

### Changed
- 76 files changed, net -6,264 lines (more concise)
- All agents updated with "CLARIFY BEFORE CODING" sections
- All skills restructured with decision trees

---

## [0.0.7] - 2026-01-02

### Added
- **Native Multi-Agent Orchestration** using Claude's Agent tool
- **Game Developer Agent** with comprehensive game development skills
- **Parallel Agents Skill** for subagent coordination

### Removed
- `scripts/parallel_orchestrator.py` (replaced by native orchestration)

---

## [0.0.6] - 2026-01-01

### Added
- **Dependency Scanner** for file relationship tracking
- **SEO Specialist Agent**
- File tree annotations showing dependencies

---

## [0.0.5] - 2026-01-01

### Added
- **Cross-Platform Support** (Windows, macOS, Linux)
- `Makefile` with platform detection
- `scripts/setup.py` for automated installation
- **Architecture Skill** with decision frameworks

---

## [0.0.4] - 2025-12-31

### Added
- **CODEBASE.md** relocated to root for better visibility
- **mobile-typography skill**

---

## [0.0.3] - 2025-12-31

### Added
- **OS Detection & Context Injection**
- **Project Structure Discovery**

### Fixed
- `AttributeError` in session_hooks.py

### Removed
- Terminal Error Learning System (hooks compatibility issues)

---

## [0.0.2] - 2025-12-31

### Added
- **Security Testing** (penetration-tester agent, vulnerability-scanner skill)
- **Debug Logging** to all scripts

### Removed
- `scripts/progress_reporter.py`

---

## [0.0.1] - 2025-12-30

### Initial Release
- 14 specialized agents
- 37 skills (patterns, templates)
- 9 Python hook scripts
- 8 slash commands
- Session management
- Auto preview server

---

[0.6.0]: https://github.com/xenitV1/claude-code-maestro/compare/v0.3.3...v0.6.0
[0.3.3]: https://github.com/xenitV1/claude-code-maestro/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/xenitV1/claude-code-maestro/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/xenitV1/claude-code-maestro/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/xenitV1/claude-code-maestro/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/xenitV1/claude-code-maestro/compare/v0.2.0...v0.2.4
[0.2.0]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.7...v0.2.0
[0.0.7]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/xenitV1/claude-code-maestro/releases/tag/v0.0.1
