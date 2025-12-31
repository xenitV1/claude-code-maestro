#!/usr/bin/env python3
"""
Session Hooks - Session start and end management
Unified script for SessionStart and SessionEnd hooks.

Usage:
    python session_hooks.py start [project_path]
    python session_hooks.py end [project_path]
"""

import json
import sys
import os
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Debug logging
DEBUG_LOG = Path.home() / ".claude" / "data" / "hook_debug.log"


def clear_debug_log():
    """Clear debug log at the start of each session."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        DEBUG_LOG.write_text(f"[{datetime.now().isoformat()}] === NEW SESSION ===\n")
    except:
        pass


def debug_log(message: str):
    """Write debug log."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] session_hooks.py: {message}\n")
    except Exception as e:
        # If can't write log, write to stderr (fallback)
        sys.stderr.write(f"DEBUG_LOG_ERROR: {e}\n")

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
PROJECTS_DIR = DATA_DIR / "projects"
CURRENT_PROJECT_FILE = DATA_DIR / "current-project.json"
GLOBAL_STATS_FILE = DATA_DIR / "global-stats.json"


def get_os_info() -> Dict[str, str]:
    """Detect operating system information."""
    system = platform.system().lower()

    if system == "windows":
        return {
            "name": "Windows",
            "shell": "PowerShell / CMD",
            "terminal": "PowerShell",
            "package_manager": "winget / chocolatey",
            "path_separator": "\\"
        }
    elif system == "darwin":
        return {
            "name": "macOS",
            "shell": "zsh / bash",
            "terminal": "Terminal.app / iTerm2",
            "package_manager": "brew",
            "path_separator": "/"
        }
    elif system == "linux":
        # Try to detect specific distro
        try:
            with open("/etc/os-release", "r") as f:
                os_release = f.read()
                if "ubuntu" in os_release.lower():
                    distro = "Ubuntu"
                elif "fedora" in os_release.lower():
                    distro = "Fedora"
                elif "debian" in os_release.lower():
                    distro = "Debian"
                elif "arch" in os_release.lower():
                    distro = "Arch Linux"
                else:
                    distro = "Linux"
        except:
            distro = "Linux"

        return {
            "name": distro,
            "shell": "bash / zsh",
            "terminal": "Terminal",
            "package_manager": "apt / yum / dnf",
            "path_separator": "/"
        }
    else:
        return {
            "name": "Unknown",
            "shell": "Unknown",
            "terminal": "Unknown",
            "package_manager": "Unknown",
            "path_separator": "/"
        }


def get_project_dir(project_path: str) -> Path:
    """Return data directory for project."""
    project_name = Path(project_path).name
    # Convert project name to safe filename
    safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
    return PROJECTS_DIR / safe_name


def ensure_project_data_dir(project_path: str) -> Path:
    """Create and return data directory for project."""
    project_dir = get_project_dir(project_path)
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def detect_project_type(project_path: str, max_depth: int = 3) -> Dict[str, Any]:
    """Detect project type (with recursive search)."""
    path = Path(project_path)
    analysis = {
        "projectType": None,
        "framework": None,
        "platform": None,
        "detectedAt": None  # Which directory was it detected in
    }

    def find_project_files(current_path: Path, depth: int = 0) -> Optional[Dict[str, Any]]:
        """Recursively search for project files."""
        if depth > max_depth:
            return None

        # Node.js project
        package_json = current_path / "package.json"
        if package_json.exists():
            try:
                pkg = json.loads(package_json.read_text())
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

                result = {
                    "projectType": "node",
                    "framework": None,
                    "platform": None,
                    "detectedAt": str(current_path)
                }

                if "react-native" in deps or "expo" in deps:
                    result["framework"] = "react-native"
                    result["platform"] = "mobile"
                elif "next" in deps:
                    result["framework"] = "nextjs"
                    result["platform"] = "web"
                elif "react" in deps:
                    result["framework"] = "react"
                    result["platform"] = "web"
                elif "express" in deps:
                    result["framework"] = "express"
                    result["platform"] = "api"
                elif "fastify" in deps:
                    result["framework"] = "fastify"
                    result["platform"] = "api"
                elif "vue" in deps:
                    result["framework"] = "vue"
                    result["platform"] = "web"
                else:
                    result["framework"] = "node"
                    result["platform"] = "general"

                return result
            except:
                pass

        # Python project
        if (current_path / "requirements.txt").exists() or (current_path / "pyproject.toml").exists():
            result = {
                "projectType": "python",
                "framework": "python",
                "platform": "general",
                "detectedAt": str(current_path)
            }
            if (current_path / "manage.py").exists():
                result["framework"] = "django"
                result["platform"] = "web"
            elif (current_path / "app.py").exists() or (current_path / "main.py").exists():
                result["framework"] = "flask-or-fastapi"
                result["platform"] = "api"
            return result

        # Rust project
        if (current_path / "Cargo.toml").exists():
            return {
                "projectType": "rust",
                "framework": "rust",
                "platform": "general",
                "detectedAt": str(current_path)
            }

        # Go project
        if (current_path / "go.mod").exists():
            return {
                "projectType": "go",
                "framework": "go",
                "platform": "general",
                "detectedAt": str(current_path)
            }

        # Search in subdirectories
        try:
            for item in current_path.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name not in ['node_modules', 'venv', '__pycache__', 'dist', 'build']:
                    result = find_project_files(item, depth + 1)
                    if result:
                        return result
        except PermissionError:
            pass

        return None

    # Start recursive search
    result = find_project_files(path)
    if result:
        analysis.update(result)

    return analysis


def get_os_commands(os_info: Dict[str, str]) -> str:
    """Get OS-specific terminal commands."""
    os_name = os_info.get("name", "Unknown")
    shell = os_info.get("shell", "Unknown")

    if os_name == "Windows":
        return """#### 🪟 Windows Terminal Commands

##### PowerShell
```powershell
ls                    # List files
cd <path>             # Change directory
pwd                   # Current directory
mkdir <dir>            # Create directory
rm <file>             # Remove file
rm -r <dir>           # Remove directory
cat <file>            # View file
echo $env:PATH        # Show environment variables
```

##### Common Tasks
- **File Explorer**: `start .`
- **Open with default app**: `start <file>`
- **Process manager**: `taskmgr` or `Get-Process`
- **Network info**: `ipconfig` or `Get-NetIPAddress`
- **System info**: `systeminfo`

##### Package Managers
```powershell
winget install <app>     # Install application
winget search <app>      # Search for application
winget upgrade <app>     # Upgrade application
winget list              # List installed apps
```

---

"""

    elif os_name == "macOS":
        return """#### 🍎 macOS Terminal Commands

##### Shell (zsh/bash)
```bash
ls                    # List files
cd <path>             # Change directory
pwd                   # Current directory
mkdir <dir>            # Create directory
rm <file>             # Remove file
rm -rf <dir>          # Remove directory
cat <file>            # View file
echo $PATH            # Show environment variables
```

##### Common Tasks
- **Finder**: `open .` (current folder in Finder)
- **Text edit**: `open -a TextEdit <file>`
- **System monitor**: `Activity Monitor` app
- **Network info**: `ifconfig` or `networksetup -listallhardwareports`
- **System info**: `sw_vers`

##### Homebrew Package Manager
```bash
brew install <formula>    # Install package
brew search <formula>     # Search for package
brew upgrade <formula>    # Upgrade package
brew list                 # List installed packages
brew update               # Update Homebrew
```

---

"""

    else:  # Linux
        return """#### 🐧 Linux Terminal Commands

##### Shell (bash/zsh)
```bash
ls                    # List files
cd <path>             # Change directory
pwd                   # Current directory
mkdir <dir>            # Create directory
rm <file>             # Remove file
rm -rf <dir>          # Remove directory
cat <file>            # View file
echo $PATH            # Show environment variables
```

##### Common Tasks
- **File manager**: `xdg-open .` or `nautilus .`
- **Text editor**: `nano <file>`, `vim <file>`, or `code <file>`
- **Process monitor**: `htop` or `top`
- **Network info**: `ip addr` or `ifconfig`
- **Disk usage**: `df -h` (disk free), `du -sh <dir>` (directory size)

##### Package Managers
```bash
# Debian/Ubuntu (apt)
sudo apt install <package>      # Install
sudo apt update                 # Update lists
sudo apt upgrade                # Upgrade packages
apt search <package>            # Search

# Fedora/RHEL (dnf/yum)
sudo dnf install <package>      # Install
sudo dnf update                 # Update
sudo dnf upgrade                # Upgrade

# Arch (pacman)
sudo pacman -S <package>        # Install
sudo pacman -Syu                # Update & upgrade
```

---

"""


    return "*No specific commands for this OS*"


def load_clean_code_skill() -> str:
    """Load clean-code skill content."""
    skill_path = Path(__file__).parent.parent / "skills" / "clean-code" / "SKILL.md"
    try:
        if skill_path.exists():
            content = skill_path.read_text(encoding="utf-8")
            # Extract the content after the frontmatter (between --- markers)
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
            return content
    except Exception as e:
        debug_log(f"Could not load clean-code skill: {e}")
    return ""


def load_discovery_structure(project_path: str) -> str:
    """Load and format project structure from discovery report."""
    project_name = Path(project_path).name
    safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
    discovery_file = PROJECTS_DIR / safe_name / "discovery-report.json"

    if not discovery_file.exists():
        return ""

    try:
        report = json.loads(discovery_file.read_text(encoding="utf-8"))
        structure = report.get("structure", {})

        if not structure:
            return ""

        # Format structure as tree
        def format_tree(data: dict, indent: int = 0) -> list:
            lines = []
            prefix = "  " * indent
            for key, value in sorted(data.items()):
                if value == "file":
                    lines.append(f"{prefix}{key}")
                elif isinstance(value, dict):
                    lines.append(f"{prefix}{key}/")
                    lines.extend(format_tree(value, indent + 1))
            return lines

        tree_lines = format_tree(structure)

        return f"""## 📂 Project Structure

```
{chr(10).join(tree_lines)}
```

"""
    except Exception as e:
        debug_log(f"Could not load discovery structure: {e}")
        return ""


def generate_context_markdown(session_info: Dict, analysis: Dict, os_info: Dict[str, str]) -> str:
    """Generate markdown context for AI to read."""
    project_name = session_info.get("projectName", "Unknown")
    framework = analysis.get("framework", "Unknown")
    platform = analysis.get("platform", "Unknown")
    project_type = analysis.get("projectType", "Unknown")
    project_path = session_info.get("projectPath", "")

    os_name = os_info.get("name", "Unknown")
    os_shell = os_info.get("shell", "Unknown")

    # Load clean code skill
    clean_code_content = load_clean_code_skill()

    # Load discovery structure
    structure_content = load_discovery_structure(project_path)

    # Safe string conversion - handle None values
    def safe_upper(val: str) -> str:
        if val is None or val == 'Unknown':
            return 'Unknown'
        return str(val).upper()

    md = f"""# 📁 Project Context

**Project:** `{project_name}`
**Framework:** `{framework or 'Unknown'}`
**Type:** `{project_type or 'Unknown'}`
**Path:** `{project_path}`
**Detected:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🖥️ Operating System

| Property | Value |
|----------|-------|
| **OS** | {os_name} |
| **Shell** | {os_shell} |

---

## ⚡ Terminal Commands (Current OS)

{get_os_commands(os_info)}
## 🎯 Project Environment

| Property | Value |
|----------|-------|
| **Project Type** | {safe_upper(project_type)} |
| **Framework** | {safe_upper(framework)} |
| **Platform** | {safe_upper(platform)} |

---

## 📋 Quick Project Commands

{get_project_commands(project_type, framework)}

---

{structure_content}
{clean_code_content}

---

*This file is auto-generated by Maestro session hooks. Do not edit manually.*
"""
    return md


def get_project_commands(project_type: str, framework: str) -> str:
    """Get project-specific terminal commands."""
    if project_type == "node":
        base = """#### Package Management
```bash
npm install              # Install dependencies
npm install <package>    # Add package
```

#### Development
```bash
npm run dev              # Start dev server
npm run build            # Build for production
```
"""
        if framework == "nextjs":
            return base + """#### Next.js
```bash
npx next dev             # Development
npx next build           # Production build
```
"""
        return base
    elif project_type == "python":
        return """#### Python
```bash
pip install -r requirements.txt    # Install dependencies
python manage.py runserver         # Django dev server
python -m pytest                   # Run tests
```
"""
    return ""


def session_start(project_path: str, silent: bool = False):
    """Session start."""
    debug_log(f"SESSION_START called: project_path={project_path}, silent={silent}")

    # Detect OS
    os_info = get_os_info()
    debug_log(f"OS detected: {os_info['name']}")

    # Create project-based data directory
    project_dir = ensure_project_data_dir(project_path)

    # Detect project
    analysis = detect_project_type(project_path)

    # Create session info
    session_info = {
        "projectPath": project_path,
        "projectName": Path(project_path).name,
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis,
        "os": os_info
    }

    # Save session stats to project directory
    session_stats_file = project_dir / "session-stats.json"
    session_stats_file.write_text(json.dumps(session_info, indent=2, ensure_ascii=False))

    # Also save current project reference globally
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CURRENT_PROJECT_FILE.write_text(json.dumps({
        "projectPath": project_path,
        "projectName": Path(project_path).name,
        "dataDir": str(project_dir),
        "lastAccess": datetime.now().isoformat()
    }, indent=2, ensure_ascii=False))

    # Create context file in .claude directory for AI to read
    claude_dir = Path(project_path) / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    context_file = claude_dir / "rules.md"
    context_md = generate_context_markdown(session_info, analysis, os_info)
    context_file.write_text(context_md, encoding="utf-8")

    # Output for Claude (markdown format for AI to parse)
    if not silent:
        print("\n" + context_md)

    debug_log("SESSION_START completed successfully")


def session_end(project_path: str, silent: bool = False):
    """Session end."""
    # Project-based data directory
    project_dir = get_project_dir(project_path)
    session_stats_file = project_dir / "session-stats.json"

    # Load current session
    session_stats = {}
    if session_stats_file.exists():
        try:
            session_stats = json.loads(session_stats_file.read_text())
        except:
            pass

    # Calculate session duration
    started_at = session_stats.get("timestamp")
    duration = None
    if started_at:
        try:
            start_time = datetime.fromisoformat(started_at)
            duration = str(datetime.now() - start_time)
        except:
            pass

    # Output
    output = {
        "timestamp": datetime.now().isoformat(),
        "projectPath": project_path,
        "status": "completed"
    }

    if duration:
        output["duration"] = duration

    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")

    if not silent:
        print(f"\n✅ Session completed")
        if duration:
            print(f"⏱️ Duration: {duration}")


def main():
    """Main function."""
    # Clear debug log at the very start of each hook invocation
    clear_debug_log()

    debug_log(f"MAIN called: argv={sys.argv}")

    if len(sys.argv) < 2:
        print("Usage: python session_hooks.py [start|end] [--silent] [project_path]")
        sys.exit(1)

    # Check for --silent flag
    silent = "--silent" in sys.argv
    # Remove --silent from args for processing
    args = [a for a in sys.argv if a != "--silent"]

    # args[0] is script name, args[1] is command, args[2] is project path
    command = args[1].lower() if len(args) > 1 else "start"
    project_path = args[2] if len(args) > 2 else os.getcwd()

    debug_log(f"Parsed: command={command}, project_path={project_path}, silent={silent}")

    try:
        if command == "start":
            session_start(project_path, silent=silent)
            debug_log("SESSION_START completed successfully")
        elif command == "end":
            session_end(project_path, silent=silent)
            debug_log("SESSION_END completed successfully")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python session_hooks.py [start|end] [--silent] [project_path]")
            sys.exit(1)
    except Exception as e:
        debug_log(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        debug_log(f"TRACEBACK: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    try:
        # Windows terminal unicode support
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass
    main()
