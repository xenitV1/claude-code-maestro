# Claude Code CLI Reference

> Complete reference for Claude Code command-line interface, including commands, flags, interactive mode, checkpointing, hooks, and plugins.

---

## Table of Contents

- [CLI Commands](#cli-commands)
- [CLI Flags](#cli-flags)
- [Agents Flag Format](#agents-flag-format)
- [System Prompt Flags](#system-prompt-flags)
- [Interactive Mode](#interactive-mode)
- [Checkpointing](#checkpointing)
- [Hooks Reference](#hooks-reference)
- [Plugins Reference](#plugins-reference)

---

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent conversation in current directory | `claude -c` |
| `claude -c -p "query"` | Continue via SDK | `claude -c -p "Check for type errors"` |
| `claude -r "<session>" "query"` | Resume session by ID or name | `claude -r "auth-refactor" "Finish this PR"` |
| `claude update` | Update to latest version | `claude update` |
| `claude mcp` | Configure Model Context Protocol (MCP) servers | See MCP documentation |

---

## CLI Flags

Customize Claude Code's behavior with these command-line flags:

| Flag | Description | Example |
|------|-------------|---------|
| `--add-dir` | Add additional working directories for Claude to access | `claude --add-dir ../apps ../lib` |
| `--agent` | Specify an agent for the current session | `claude --agent my-custom-agent` |
| `--agents` | Define custom subagents dynamically via JSON | See [Agents Flag Format](#agents-flag-format) |
| `--allowedTools` | Tools that execute without prompting for permission | `"Bash(git log:*)" "Read"` |
| `--append-system-prompt` | Append custom text to the end of the default system prompt | `claude --append-system-prompt "Always use TypeScript"` |
| `--betas` | Beta headers to include in API requests (API key users only) | `claude --betas interleaved-thinking` |
| `--chrome` | Enable Chrome browser integration for web automation and testing | `claude --chrome` |
| `--continue, -c` | Load the most recent conversation in the current directory | `claude --continue` |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution) | `claude --dangerously-skip-permissions` |
| `--debug` | Enable debug mode with optional category filtering | `claude --debug "api,mcp"` |
| `--disallowedTools` | Tools that are removed from the model's context | `"Bash(git log:*)" "Edit"` |
| `--enable-lsp-logging` | Enable verbose LSP logging for debugging | `claude --enable-lsp-logging` |
| `--fallback-model` | Enable automatic fallback to specified model when overloaded | `claude -p --fallback-model sonnet "query"` |
| `--fork-session` | When resuming, create a new session ID instead of reusing | `claude --resume abc123 --fork-session` |
| `--ide` | Automatically connect to IDE on startup | `claude --ide` |
| `--include-partial-messages` | Include partial streaming events in output | `claude -p --output-format stream-json --include-partial-messages "query"` |
| `--input-format` | Specify input format for print mode (`text`, `stream-json`) | `claude -p --input-format stream-json` |
| `--json-schema` | Get validated JSON output matching a JSON Schema | `claude -p --json-schema '{...}' "query"` |
| `--max-turns` | Limit the number of agentic turns in non-interactive mode | `claude -p --max-turns 3 "query"` |
| `--mcp-config` | Load MCP servers from JSON files or strings | `claude --mcp-config ./mcp.json` |
| `--model` | Sets the model for the current session | `claude --model claude-sonnet-4-5-20250929` |
| `--no-chrome` | Disable Chrome browser integration for this session | `claude --no-chrome` |
| `--output-format` | Specify output format for print mode (`text`, `json`, `stream-json`) | `claude -p "query" --output-format json` |
| `--permission-mode` | Begin in a specified permission mode | `claude --permission-mode plan` |
| `--permission-prompt-tool` | Specify an MCP tool to handle permission prompts | `claude -p --permission-prompt-tool mcp_auth_tool "query"` |
| `--plugin-dir` | Load plugins from directories for this session only | `claude --plugin-dir ./my-plugins` |
| `--print, -p` | Print response without interactive mode | `claude -p "query"` |
| `--resume, -r` | Resume a specific session by ID or name | `claude --resume auth-refactor` |
| `--session-id` | Use a specific session ID for the conversation (must be valid UUID) | `claude --session-id "550e8400-..."` |
| `--setting-sources` | Comma-separated list of setting sources to load | `claude --setting-sources user,project` |
| `--settings` | Path to a settings JSON file or a JSON string | `claude --settings ./settings.json` |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config` | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--system-prompt` | Replace the entire system prompt with custom text | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | Load system prompt from a file (print mode only) | `claude -p --system-prompt-file ./prompt.txt "query"` |
| `--tools` | Restrict which built-in tools Claude can use | `claude --tools "Bash,Edit,Read"` |
| `--verbose` | Enable verbose logging, shows full turn-by-turn output | `claude --verbose` |
| `--version, -v` | Output the version number | `claude -v` |

> **Tip:** The `--output-format json` flag is particularly useful for scripting and automation, allowing you to parse Claude's responses programmatically.

---

## Agents Flag Format

The `--agents` flag accepts a JSON object that defines one or more custom subagents:

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Natural language description of when the subagent should be invoked |
| `prompt` | Yes | The system prompt that guides the subagent's behavior |
| `tools` | No | Array of specific tools the subagent can use (e.g., `["Read", "Edit", "Bash"]`) |
| `model` | No | Model alias to use: `sonnet`, `opus`, or `haiku` |

### Example

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

---

## System Prompt Flags

Claude Code provides three flags for customizing the system prompt:

| Flag | Behavior | Modes | Use Case |
|------|----------|-------|----------|
| `--system-prompt` | Replaces entire default prompt | Interactive + Print | Complete control over Claude's behavior |
| `--system-prompt-file` | Replaces with file contents | Print only | Load prompts from files for reproducibility |
| `--append-system-prompt` | Appends to default prompt | Interactive + Print | Add specific instructions while keeping default behavior |

### When to Use Each

**`--system-prompt`**: Use when you need complete control over Claude's system prompt. This removes all default Claude Code instructions.

```bash
claude --system-prompt "You are a Python expert who only writes type-annotated code"
```

**`--system-prompt-file`**: Use when you want to load a custom prompt from a file.

```bash
claude -p --system-prompt-file ./prompts/code-review.txt "Review this PR"
```

**`--append-system-prompt`**: Use when you want to add specific instructions while keeping Claude Code's default capabilities intact. **This is the safest option for most use cases.**

```bash
claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
```

> **Note:** `--system-prompt` and `--system-prompt-file` are mutually exclusive. You cannot use both flags simultaneously.

---

## Interactive Mode

Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.

### General Controls

| Shortcut | Description | Context |
|----------|-------------|---------|
| `Ctrl+C` | Cancel current input or generation | Standard interrupt |
| `Ctrl+D` | Exit Claude Code session | EOF signal |
| `Ctrl+L` | Clear terminal screen | Keeps conversation history |
| `Ctrl+O` | Toggle verbose output | Shows detailed tool usage |
| `Ctrl+R` | Reverse search command history | Search previous commands |
| `Ctrl+V` (macOS/Linux) / `Alt+V` (Windows) | Paste image from clipboard | Pastes image or path |
| `Up/Down arrows` | Navigate command history | Recall previous inputs |
| `Esc + Esc` | Rewind the code/conversation | Restore to previous point |
| `Shift+Tab` or `Alt+M` | Toggle permission modes | Switch between modes |
| `Option+P` (macOS) / `Alt+P` (Windows/Linux) | Switch model | Without clearing prompt |

### Multiline Input

| Method | Shortcut | Context |
|--------|----------|---------|
| Quick escape | `\` + `Enter` | Works in all terminals |
| macOS default | `Option+Enter` | Default on macOS |
| Terminal setup | `Shift+Enter` | After `/terminal-setup` |
| Control sequence | `Ctrl+J` | Line feed character |
| Paste mode | Paste directly | For code blocks, logs |

### Quick Commands

| Shortcut | Description | Notes |
|----------|-------------|-------|
| `/` at start | Slash command | See slash commands |
| `!` at start | Bash mode | Run commands directly |
| `@` | File path mention | Trigger file path autocomplete |

### Vim Editor Mode

Enable vim-style editing with `/vim` command or configure permanently via `/config`.

#### Mode Switching

| Command | Action | From Mode |
|---------|--------|-----------|
| `Esc` | Enter NORMAL mode | INSERT |
| `i` | Insert before cursor | NORMAL |
| `I` | Insert at beginning of line | NORMAL |
| `a` | Insert after cursor | NORMAL |
| `A` | Insert at end of line | NORMAL |
| `o` | Open line below | NORMAL |
| `O` | Open line above | NORMAL |

#### Navigation (NORMAL mode)

| Command | Action |
|---------|--------|
| `h/j/k/l` | Move left/down/up/right |
| `w` | Next word |
| `e` | End of word |
| `b` | Previous word |
| `0` | Beginning of line |
| `$` | End of line |
| `^` | First non-blank character |
| `gg` | Beginning of input |
| `G` | End of input |

#### Editing (NORMAL mode)

| Command | Action |
|---------|--------|
| `x` | Delete character |
| `dd` | Delete line |
| `D` | Delete to end of line |
| `dw/de/db` | Delete word/to end/back |
| `cc` | Change line |
| `C` | Change to end of line |
| `cw/ce/cb` | Change word/to end/back |
| `.` | Repeat last change |

### Reverse Search with Ctrl+R

Press `Ctrl+R` to interactively search through your command history:

1. **Start search**: Press `Ctrl+R` to activate reverse history search
2. **Type query**: Enter text to search for in previous commands
3. **Navigate matches**: Press `Ctrl+R` again to cycle through older matches
4. **Accept match**:
   - Press `Tab` or `Esc` to accept and continue editing
   - Press `Enter` to accept and execute immediately
5. **Cancel search**:
   - Press `Ctrl+C` to cancel and restore original input
   - Press `Backspace` on empty search to cancel

### Background Bash Commands

Claude Code supports running bash commands in the background, allowing you to continue working while long-running processes execute.

#### How Backgrounding Works

- Prompt Claude Code to run a command in the background
- Press `Ctrl+B` to move a regular Bash tool invocation to the background
- Output is buffered and Claude can retrieve it using the `BashOutput` tool
- Background tasks have unique IDs for tracking

**Common backgrounded commands:**
- Build tools (webpack, vite, make)
- Package managers (npm, yarn, pnpm)
- Test runners (jest, pytest)
- Development servers
- Long-running processes (docker, terraform)

### Bash Mode with `!` Prefix

Run bash commands directly without going through Claude:

```bash
! npm test
! git status
! ls -la
```

Bash mode:
- Adds the command and its output to the conversation context
- Shows real-time progress and output
- Supports the same `Ctrl+B` backgrounding for long-running commands
- Does not require Claude to interpret or approve the command

---

## Checkpointing

Automatically track and rewind Claude's edits to quickly recover from unwanted changes.

### How Checkpoints Work

As you work with Claude, checkpointing automatically captures the state of your code before each edit. This safety net lets you pursue ambitious, wide-scale tasks knowing you can always return to a prior code state.

#### Automatic Tracking

- Every user prompt creates a new checkpoint
- Checkpoints persist across sessions
- Automatically cleaned up along with sessions after 30 days (configurable)

#### Rewinding Changes

Press `Esc` twice (`Esc + Esc`) or use the `/rewind` command to open the rewind menu. You can choose to restore:

- **Conversation only**: Rewind to a user message while keeping code changes
- **Code only**: Revert file changes while keeping the conversation
- **Both code and conversation**: Restore both to a prior point in the session

### Common Use Cases

Checkpoints are particularly useful when:

- **Exploring alternatives**: Try different implementation approaches without losing your starting point
- **Recovering from mistakes**: Quickly undo changes that introduced bugs
- **Iterating on features**: Experiment with variations knowing you can revert to working states

### Limitations

#### Bash Command Changes Not Tracked

Checkpointing does **not** track files modified by bash commands:

```bash
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

These file modifications cannot be undone through rewind. Only direct file edits made through Claude's file editing tools are tracked.

#### External Changes Not Tracked

Checkpointing only tracks files that have been edited within the current session. Manual changes you make outside of Claude Code are normally not captured.

#### Not a Replacement for Version Control

Checkpoints are designed for quick, session-level recovery:

- Continue using version control (e.g., Git) for commits, branches, and long-term history
- Checkpoints complement but don't replace proper version control
- Think of checkpoints as "local undo" and Git as "permanent history"

---

## Hooks Reference

Hooks allow you to execute custom scripts in response to Claude Code events.

### Configuration

Claude Code hooks are configured in your settings files:

- `~/.claude/settings.json` - User settings
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local project settings (not committed)

### Structure

Hooks are organized by matchers, where each matcher can have multiple hooks:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

**Fields:**
- `matcher`: Pattern to match tool names (case-sensitive). Supports regex: `Edit|Write` or `Notebook.*`. Use `*` to match all tools.
- `hooks`: Array of hooks to execute when the pattern matches
- `type`: Hook execution type - `"command"` for bash commands or `"prompt"` for LLM-based evaluation
- `command`: (For `type: "command"`) The bash command to execute
- `prompt`: (For `type: "prompt"`) The prompt to send to the LLM for evaluation
- `timeout`: (Optional) How long a hook should run before canceling

### Hook Events

| Event | Description |
|-------|-------------|
| `PreToolUse` | Runs after Claude creates tool parameters and before processing |
| `PermissionRequest` | Runs when the user is shown a permission dialog |
| `PostToolUse` | Runs immediately after a tool completes successfully |
| `Notification` | Runs when Claude Code sends notifications |
| `UserPromptSubmit` | Runs when the user submits a prompt, before Claude processes it |
| `Stop` | Runs when the main Claude Code agent has finished responding |
| `SubagentStop` | Runs when a Claude Code subagent has finished responding |
| `PreCompact` | Runs before Claude Code runs a compact operation |
| `SessionStart` | Runs when Claude Code starts or resumes a session |
| `SessionEnd` | Runs when a Claude Code session ends |

### Common Tool Matchers

- `Task` - Subagent tasks
- `Bash` - Shell commands
- `Glob` - File pattern matching
- `Grep` - Content search
- `Read` - File reading
- `Edit` - File editing
- `Write` - File writing
- `WebFetch`, `WebSearch` - Web operations

### Hook Output

#### Exit Codes

- **Exit code 0**: Success. stdout is shown to the user in verbose mode
- **Exit code 2**: Blocking error. stderr is used as the error message and fed back to Claude
- **Other exit codes**: Non-blocking error. stderr is shown to the user in verbose mode

#### JSON Output

Hooks can return structured JSON in stdout for more sophisticated control:

```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true,
  "systemMessage": "string"
}
```

### Security Considerations

> **⚠️ USE AT YOUR OWN RISK**: Claude Code hooks execute arbitrary shell commands on your system automatically.

**Security Best Practices:**
- Validate and sanitize inputs - Never trust input data blindly
- Always quote shell variables - Use `"$VAR"` not `$VAR`
- Block path traversal - Check for `..` in file paths
- Use absolute paths - Specify full paths for scripts
- Skip sensitive files - Avoid `.env`, `.git/`, keys, etc.

---

## Plugins Reference

Complete technical reference for Claude Code plugin system.

### Plugin Components

Plugins can provide five types of components:

| Component | Location | Description |
|-----------|----------|-------------|
| Commands | `commands/` directory | Custom slash commands |
| Agents | `agents/` directory | Specialized subagents for specific tasks |
| Skills | `skills/` directory | Agent Skills that extend Claude's capabilities |
| Hooks | `hooks/hooks.json` | Event handlers for Claude Code events |
| MCP Servers | `.mcp.json` | Model Context Protocol server definitions |
| LSP Servers | `.lsp.json` | Language Server Protocol configurations |

### Plugin Installation Scopes

| Scope | Settings File | Use Case |
|-------|---------------|----------|
| `user` | `~/.claude/settings.json` | Personal plugins available across all projects (default) |
| `project` | `.claude/settings.json` | Team plugins shared via version control |
| `local` | `.claude/settings.local.json` | Project-specific plugins, gitignored |
| `managed` | `managed-settings.json` | Managed plugins (read-only, update only) |

### Plugin Manifest Schema

The `plugin.json` file defines your plugin's metadata:

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "lspServers": "./.lsp.json"
}
```

#### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | string | Unique identifier (kebab-case, no spaces) | `"deployment-tools"` |

#### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Semantic version |
| `description` | string | Brief explanation of plugin purpose |
| `author` | object | Author information |
| `homepage` | string | Documentation URL |
| `repository` | string | Source code URL |
| `license` | string | License identifier |
| `keywords` | array | Discovery tags |

### Plugin Directory Structure

```
enterprise-plugin/
├── .claude-plugin/           # Metadata directory
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Default command location
│   ├── status.md
│   └── logs.md
├── agents/                   # Default agent location
│   ├── security-reviewer.md
│   └── performance-tester.md
├── skills/                   # Agent Skills
│   └── code-reviewer/
│       └── SKILL.md
├── hooks/                    # Hook configurations
│   └── hooks.json
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   └── security-scan.sh
├── LICENSE
└── CHANGELOG.md
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `claude plugin install <plugin>` | Install a plugin from available marketplaces |
| `claude plugin uninstall <plugin>` | Remove an installed plugin |
| `claude plugin enable <plugin>` | Enable a disabled plugin |
| `claude plugin disable <plugin>` | Disable a plugin without uninstalling |
| `claude plugin update <plugin>` | Update a plugin to the latest version |

**Options:**
- `-s, --scope <scope>`: Installation scope (`user`, `project`, or `local`)
- `-h, --help`: Display help for command

### Environment Variables

- `${CLAUDE_PLUGIN_ROOT}`: Absolute path to your plugin directory
- `${CLAUDE_PROJECT_DIR}`: Project root directory

---

## See Also

- [Chrome Extension](https://docs.anthropic.com/claude-code/chrome) - Browser automation and web testing
- [Slash Commands](https://docs.anthropic.com/claude-code/slash-commands) - Interactive session commands
- [Quickstart Guide](https://docs.anthropic.com/claude-code/quickstart) - Getting started with Claude Code
- [Common Workflows](https://docs.anthropic.com/claude-code/workflows) - Advanced workflows and patterns
- [Settings](https://docs.anthropic.com/claude-code/settings) - Configuration options
- [SDK Documentation](https://docs.anthropic.com/claude-code/sdk) - Programmatic usage and integrations