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
        "detectedAt": None
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
                elif "@ionic/react" in deps or "@ionic/vue" in deps or "@capacitor/core" in deps:
                    result["framework"] = "ionic-capacitor"
                    result["platform"] = "mobile"
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

        # Flutter project
        if (current_path / "pubspec.yaml").exists():
            return {
                "projectType": "flutter",
                "framework": "flutter",
                "platform": "mobile",
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
        return """#### [WINDOWS] Terminal Commands

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
        return """#### [MACOS] Terminal Commands

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
        return """#### [LINUX] Terminal Commands

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


def load_discovery_structure(project_path: str, import_counts: dict = None) -> str:
    """Load and format project structure from discovery report.
    
    Args:
        project_path: Path to the project
        import_counts: Dict mapping file paths to list of files that import them
    
    Handles both regular files and collapsed directories (shown as summary strings).
    """
    project_name = Path(project_path).name
    safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
    discovery_file = PROJECTS_DIR / safe_name / "discovery-report.json"

    if not discovery_file.exists():
        return ""

    try:
        report = json.loads(discovery_file.read_text(encoding="utf-8"))
        structure = report.get("structure", {})
        scan_stats = report.get("scan_stats", {})

        if not structure:
            return ""

        # Format structure as tree with import info
        def format_tree(data: dict, current_path: str = "", indent: int = 0) -> list:
            lines = []
            prefix = "  " * indent
            for key, value in sorted(data.items()):
                # Remove trailing slash from directory names for path building
                clean_key = key.rstrip('/')
                full_path = f"{current_path}/{clean_key}" if current_path else clean_key
                # Normalize path separators for matching
                normalized_path = full_path.replace("\\", "/")
                
                if value == "file":
                    # Regular file
                    line = f"{prefix}{key}"
                    # Check if this file has dependents
                    if import_counts:
                        dependents = None
                        paths_to_check = [
                            normalized_path,
                            normalized_path.replace('.tsx', '').replace('.ts', ''),
                        ]
                        if key in ('index.ts', 'index.tsx'):
                            parent_path = '/'.join(normalized_path.split('/')[:-1])
                            paths_to_check.append(parent_path)
                        
                        for path_key, deps in import_counts.items():
                            path_key_normalized = path_key.replace("\\\\", "/")
                            for check_path in paths_to_check:
                                if (path_key_normalized == check_path or 
                                    path_key_normalized.endswith('/' + check_path) or
                                    check_path.endswith('/' + path_key_normalized) or
                                    path_key_normalized.endswith(key)):
                                    dependents = deps
                                    break
                            if dependents:
                                break
                        
                        if dependents and len(dependents) > 0:
                            dep_names = [Path(d).name for d in dependents[:3]]
                            suffix = f" ← {', '.join(dep_names)}"
                            if len(dependents) > 3:
                                suffix += f" +{len(dependents) - 3} more"
                            line += suffix
                    
                    lines.append(line)
                
                elif isinstance(value, str):
                    # Collapsed directory with summary (e.g., "[52 files: .tsx, .ts]")
                    # Key ends with "/" to indicate it's a directory
                    dir_name = key if key.endswith('/') else key + '/'
                    lines.append(f"{prefix}{dir_name} {value}")
                
                elif isinstance(value, dict):
                    # Regular directory - recurse
                    lines.append(f"{prefix}{key}/")
                    lines.extend(format_tree(value, full_path, indent + 1))
            
            return lines

        tree_lines = format_tree(structure)
        
        # Add stats note if available
        stats_note = ""
        if scan_stats:
            files = scan_stats.get('files_included', 0)
            collapsed = scan_stats.get('dirs_collapsed', 0)
            skipped = scan_stats.get('dirs_skipped', 0)
            if collapsed > 0 or skipped > 0:
                stats_note = f"\n> [STATS] Showing {files} files. {collapsed} dirs summarized, {skipped} dirs excluded (node_modules, etc.)\n"

        return f"""## Project Structure

> **Legend:** `file.ts <- A.tsx, B.tsx` = This file is **imported by** A.tsx and B.tsx.
> Directories with `[N files: ...]` are summarized to reduce size.{stats_note}

```
{chr(10).join(tree_lines)}
```

"""
    except Exception as e:
        debug_log(f"Could not load discovery structure: {e}")
        return ""


def scan_file_dependencies(project_path: str) -> tuple:
    """Scan ALL project files for dependencies (no limit).
    
    Returns:
        tuple: (markdown_summary, reverse_deps_dict)
               reverse_deps_dict maps import paths to list of files that import them
    """
    import re
    
    root = Path(project_path).resolve()
    
    SCANNABLE_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.py', '.vue', '.svelte'}
    SKIP_DIRS = {'node_modules', '.git', '.next', 'dist', 'build', '__pycache__', 'venv', '.venv', 
                 '.turbo', 'coverage', '.nyc_output', 'playwright-report', 'test-results'}
    
    summary = {
        "total_files": 0,
        "api_endpoints": set(),
        "db_models": set(),
        "high_impact_files": {}
    }
    
    file_imports = {}  # file -> list of imports
    
    try:
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in SCANNABLE_EXTENSIONS:
                continue
            if any(skip_dir in file_path.parts for skip_dir in SKIP_DIRS):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                rel_path = str(file_path.relative_to(root))
                ext = file_path.suffix.lower()
                
                local_imports = []
                
                # Extract imports based on file type
                if ext in {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.vue', '.svelte'}:
                    # JS/TS imports
                    imports = re.findall(r"from\s+['\"]([^'\"]+)['\"]", content)
                    imports += re.findall(r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content)
                    # Track local imports
                    local_imports = [imp for imp in imports if imp.startswith('.') or imp.startswith('@/')]
                    
                elif ext == '.py':
                    # Python relative imports: from .module import X, from ..package import Y
                    py_relative = re.findall(r"from\s+(\.+\w*(?:\.\w+)*)\s+import", content)
                    # Python absolute local imports: from mypackage.module import X
                    py_absolute = re.findall(r"from\s+(\w+(?:\.\w+)+)\s+import", content)
                    # Simple imports: import mymodule
                    py_simple = re.findall(r"^import\s+(\w+(?:\.\w+)*)", content, re.MULTILINE)
                    
                    # Filter to likely local imports (not standard library)
                    stdlib = {'os', 'sys', 'json', 're', 'typing', 'pathlib', 'datetime', 'collections', 
                              'functools', 'itertools', 'math', 'random', 'subprocess', 'threading',
                              'argparse', 'logging', 'unittest', 'io', 'time', 'copy', 'shutil', 'platform'}
                    
                    for imp in py_relative:
                        # Convert . and .. to relative path style
                        if imp.startswith('..'):
                            local_imports.append(imp)  # Keep as-is for resolution
                        elif imp.startswith('.'):
                            local_imports.append(imp)
                    
                    for imp in py_absolute + py_simple:
                        # Skip standard library
                        root_module = imp.split('.')[0]
                        if root_module not in stdlib and not root_module.startswith('_'):
                            local_imports.append(imp)
                
                if local_imports:
                    file_imports[rel_path] = local_imports
                
                # Extract API calls
                api_calls = re.findall(r"fetch\s*\(\s*['\"`]([^'\"`]+)['\"`]", content)
                api_calls += re.findall(r"axios\s*\.\s*(?:get|post|put|delete|patch)\s*\(\s*['\"`]([^'\"`]+)['\"`]", content)
                for call in api_calls:
                    if '/api/' in call or call.startswith('/'):
                        summary["api_endpoints"].add(call.split('?')[0])  # Remove query params
                
                # Extract DB models (Prisma)
                db_models = re.findall(r"(?:db|prisma)\s*\.\s*(\w+)\s*\.\s*(?:findMany|findUnique|create|update|delete)", content)
                summary["db_models"].update(db_models)
                
                summary["total_files"] += 1
                
            except Exception as e:
                debug_log(f"Error scanning {file_path}: {e}")
                continue
        
        # Build reverse dependencies (import path -> list of files that import it)
        reverse_deps = {}  # Maps resolved path to list of importing files
        import_counts = {}
        
        def resolve_import_path(imp: str, importing_file: str) -> str:
            """Resolve import path to actual file path.
            
            Args:
                imp: The import path (e.g., './types', '../shared/api', '@/utils', '.module')
                importing_file: The file doing the import (e.g., 'src/content/content.ts')
            """
            # Handle @/ alias (common in React/Next.js projects)
            if imp.startswith('@/'):
                resolved = 'src/' + imp[2:]  # @/constants -> src/constants
            elif imp.startswith('~/'):
                resolved = imp[2:]  # ~/utils -> utils
            elif imp.startswith('./') or imp.startswith('../'):
                # JS/TS relative path
                import_dir = str(Path(importing_file).parent)
                combined = os.path.join(import_dir, imp)
                normalized = os.path.normpath(combined)
                resolved = normalized.replace('\\', '/')
                if resolved.startswith('./'):
                    resolved = resolved[2:]
            elif imp.startswith('.'):
                # Python relative import: .module or ..package.module
                import_dir = str(Path(importing_file).parent)
                # Count leading dots
                dots = 0
                for c in imp:
                    if c == '.':
                        dots += 1
                    else:
                        break
                # Get the module part after dots
                module_part = imp[dots:]
                # Convert dots to parent directory traversal
                if dots == 1:
                    # Same directory: .module -> ./module
                    rel_path = './' + module_part.replace('.', '/')
                else:
                    # Parent directories: ..module -> ../module, ...module -> ../../module
                    parents = '../' * (dots - 1)
                    rel_path = parents + module_part.replace('.', '/')
                
                combined = os.path.join(import_dir, rel_path)
                normalized = os.path.normpath(combined)
                resolved = normalized.replace('\\', '/')
            else:
                # Python absolute import: convert dots to slashes
                resolved = imp.replace('.', '/')
            
            return resolved
        
        for importing_file, imports in file_imports.items():
            for imp in imports:
                # Resolve path using importing file's location
                resolved_path = resolve_import_path(imp, importing_file)
                
                # Store both original and resolved for matching
                if resolved_path not in reverse_deps:
                    reverse_deps[resolved_path] = []
                reverse_deps[resolved_path].append(importing_file)
                
                # Also store with /index.ts for directory imports
                if not resolved_path.endswith('.ts') and not resolved_path.endswith('.tsx'):
                    index_path = resolved_path + '/index.ts'
                    if index_path not in reverse_deps:
                        reverse_deps[index_path] = []
                    reverse_deps[index_path].append(importing_file)
                
                if resolved_path not in import_counts:
                    import_counts[resolved_path] = 0
                import_counts[resolved_path] += 1
        
        # Get top 5 most imported for summary
        sorted_imports = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        summary["high_impact_files"] = {k: v for k, v in sorted_imports if v > 1}
        
    except Exception as e:
        debug_log(f"Dependency scan error: {e}")
        return "", {}
    
    # Generate markdown
    if summary["total_files"] == 0:
        return "", {}
    
    md_lines = ["## File Dependencies\n"]
    md_lines.append(f"> Scanned {summary['total_files']} files\n")
    
    if summary["api_endpoints"]:
        md_lines.append("### API Endpoints Used\n")
        md_lines.append("```")
        for endpoint in sorted(summary["api_endpoints"]):
            md_lines.append(endpoint)
        md_lines.append("```\n")
    
    if summary["db_models"]:
        md_lines.append("### Database Models\n")
        md_lines.append("```")
        for model in sorted(summary["db_models"]):
            md_lines.append(model)
        md_lines.append("```\n")
    
    if summary["high_impact_files"]:
        md_lines.append("### High-Impact Files\n")
        md_lines.append("*Files imported by multiple other files:*\n")
        md_lines.append("| File | Imported by |")
        md_lines.append("|------|-------------|")
        for file_path, count in summary["high_impact_files"].items():
            md_lines.append(f"| `{file_path}` | {count} files |")
        md_lines.append("")
    
    return "\n".join(md_lines), reverse_deps


def generate_context_markdown(session_info: Dict, analysis: Dict, os_info: Dict[str, str]) -> str:
    """Generate streamlined markdown context for AI - focused on structure and dependencies."""
    project_name = session_info.get("projectName", "Unknown")
    framework = analysis.get("framework", "Unknown")
    project_type = analysis.get("projectType", "Unknown")
    project_path = session_info.get("projectPath", "")
    os_name = os_info.get("name", "Unknown")

    # Scan file dependencies first to get reverse deps
    dependency_content, reverse_deps = scan_file_dependencies(project_path)

    # Load discovery structure with dependency annotations
    structure_content = load_discovery_structure(project_path, reverse_deps)

    md = f"""# CODEBASE.md

> **Auto-generated project context.** Refreshed on every session start.

---

## Project Info

| Property | Value |
|----------|-------|
| **Project** | `{project_name}` |
| **Framework** | `{framework or 'Unknown'}` |
| **Type** | `{project_type or 'Unknown'}` |
| **OS** | {os_name} |
| **Path** | `{project_path}` |

---

{structure_content}
{dependency_content}

---

*Auto-generated by Maestro session hooks.*
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

    # Create CODEBASE.md in project root
    context_md = generate_context_markdown(session_info, analysis, os_info)
    codebase_file = Path(project_path) / "CODEBASE.md"
    codebase_file.write_text(context_md, encoding="utf-8")

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
        print(f"\n[OK] Session completed")
        if duration:
            print(f"[TIME] Duration: {duration}")


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
