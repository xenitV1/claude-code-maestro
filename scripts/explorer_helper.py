#!/usr/bin/env python3
"""
Explorer Helper - Smart Project Discovery with Intelligent Filtering

Deep project discovery for Claude Code CLI with optimizations for large projects.
Implements smart filtering to reduce CODEBASE.md size while preserving important context.

Usage:
    python explorer_helper.py [path] [depth] [--silent]
"""

import os
import io
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Optional, Tuple

# Debug logging
DEBUG_LOG = Path.home() / ".claude" / "data" / "hook_debug.log"


def debug_log(message: str):
    """Write debug log."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] explorer_helper.py: {message}\n")
    except Exception as e:
        sys.stderr.write(f"DEBUG_LOG_ERROR: {e}\n")


# =============================================================================
# SMART FILTERING CONFIGURATION
# =============================================================================

# Maximum limits for large projects (None = no limit)
MAX_FILES_IN_TREE = None      # No limit - smart filtering handles size
MAX_TREE_DEPTH = None         # No limit - smart filtering handles depth
SUMMARY_THRESHOLD = 10        # Summary if more than this many files in a dir
MAX_ITEMS_BEFORE_SUMMARY = 15 # In a single directory

# Directories to ALWAYS exclude (never show)
EXCLUDE_DIRS: Set[str] = {
    # Package managers & virtual environments
    'node_modules', '.npm', '.yarn', '.pnpm-store',
    'venv', '.venv', 'env', '.env', 'virtualenv',
    '__pycache__', '.pytest_cache', '.mypy_cache',
    
    # Build outputs
    'dist', 'build', 'out', '.next', '.nuxt', '.output',
    'target', 'bin', 'obj',
    
    # Version control & IDE
    '.git', '.svn', '.hg',
    '.idea', '.vscode', '.vs',
    
    # Cache & temp
    '.cache', '.turbo', 'coverage', '.nyc_output',
    'tmp', 'temp', '.temp', '.tmp',
    
    # Test artifacts
    'playwright-report', 'test-results', '__snapshots__',
    'jest-cache', '.jest',
    
    # Misc
    'logs', '.logs',
}

# Directories to collapse (show as summary, not individual files)
COLLAPSE_DIRS: Set[str] = {
    # i18n / localization - often has 50+ locale folders
    'locales', 'locale', 'messages', 'translations', 'i18n', 'lang',
    
    # Assets that don't need individual listing
    'fonts', 'images', 'img', 'icons', 'assets',
    'public/sounds', 'public/images', 'public/fonts',
    'sounds', 'audio', 'videos', 'media', 'public',
    
    # Third-party copies
    'vendor', 'third_party', 'external', 'libs',
    
    # Generated docs
    'docs/api', 'api-docs', 'typedoc', 'docs', 'doc',
    
    # Examples (usually not core code)
    'examples', 'samples', 'demo', 'demos',
    
    # Migration files (can be many)
    'migrations', 'seeds', 'fixtures',
    
    # Test directories (keep tests but summarize)
    'tests', 'test', '__tests__', 'spec',
    
    # Release/changelog dirs
    '.release', '.github', '.husky', '.zap',
    
    # Static/generated content
    'static', 'generated', 'out',
}

# File extensions to ALWAYS exclude
EXCLUDE_EXTENSIONS: Set[str] = {
    # Fonts
    '.woff', '.woff2', '.ttf', '.otf', '.eot',
    
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.bmp', '.tiff',
    
    # Audio/Video
    '.mp3', '.wav', '.ogg', '.mp4', '.webm', '.avi', '.mov',
    
    # Archives
    '.zip', '.tar', '.gz', '.rar', '.7z',
    
    # Binary/Data
    '.wasm', '.bin', '.dat', '.db', '.sqlite',
    
    # Lock files
    '.lock',
    
    # Source maps
    '.map',
    
    # Test snapshots
    '.snap',
}

# File patterns to exclude (partial matches)
EXCLUDE_PATTERNS: Set[str] = {
    '.test.', '.spec.', '.e2e.', '_test.', '_spec.',
    '.min.js', '.min.css',
    '.d.ts',  # TypeScript declaration files (often auto-generated)
}

# Priority files - ALWAYS include these
PRIORITY_FILES: Set[str] = {
    # Config files
    'package.json', 'tsconfig.json', 'next.config.ts', 'next.config.js',
    'next.config.mjs', 'tailwind.config.ts', 'tailwind.config.js',
    'vite.config.ts', 'vite.config.js', 'webpack.config.js',
    'eslint.config.mjs', 'eslint.config.js', '.eslintrc.js',
    'prisma/schema.prisma', 'docker-compose.yml', 'Dockerfile',
    
    # Project documentation
    'README.md', 'CLAUDE.md', 'CODEBASE.md', 'CHANGELOG.md',
    
    # Entry points
    'index.ts', 'index.tsx', 'index.js', 'page.tsx', 'layout.tsx',
    'route.ts', 'route.tsx', 'app.ts', 'app.tsx', 'main.ts', 'main.tsx',
    
    # Type definitions
    'types.ts', 'types.tsx', 'types/index.ts',
}

# Priority directories - show MORE detail in these (deeper depth)
PRIORITY_DIRS: Set[str] = {
    'src', 'app', 'pages', 'components', 'lib', 'utils',
    'hooks', 'contexts', 'store', 'services', 'api',
    'server', 'scripts', 'config', 'types', 'actions',
    'prisma', 'supabase', 'database',
}

# Directories to always summarize (not priority, show only summary)
SUMMARIZE_ALWAYS_DIRS: Set[str] = {
    'excalidraw', 'excalidraw-master', 'excalidraw-app',
    'packages', 'node_modules', 'dev-docs',
    'security-reports', '.vercel',
}


# =============================================================================
# SMART FILTERING FUNCTIONS
# =============================================================================

def should_exclude_dir(dir_name: str, full_path: Path) -> bool:
    """Check if directory should be completely excluded."""
    # Direct name match
    if dir_name in EXCLUDE_DIRS:
        return True
    
    # Check if any parent is excluded
    for part in full_path.parts:
        if part in EXCLUDE_DIRS:
            return True
    
    return False


def should_collapse_dir(dir_name: str, full_path: Path) -> bool:
    """Check if directory should be collapsed to summary."""
    # Direct match
    if dir_name in COLLAPSE_DIRS:
        return True
    
    # Path pattern match (e.g., 'public/sounds')
    path_str = str(full_path).replace('\\', '/')
    for pattern in COLLAPSE_DIRS:
        if '/' in pattern and pattern in path_str:
            return True
    
    return False


def should_exclude_file(file_path: Path) -> bool:
    """Check if file should be excluded based on extension or pattern."""
    name = file_path.name.lower()
    suffix = file_path.suffix.lower()
    
    # Check extension
    if suffix in EXCLUDE_EXTENSIONS:
        return True
    
    # Check patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in name:
            return True
    
    return False


def is_priority_file(file_name: str) -> bool:
    """Check if file is a priority file that should always be included."""
    return file_name in PRIORITY_FILES


def is_priority_dir(dir_name: str) -> bool:
    """Check if directory is a priority directory."""
    return dir_name in PRIORITY_DIRS


def count_files_in_dir(path: Path) -> Tuple[int, Dict[str, int]]:
    """Count files in directory and return breakdown by extension."""
    count = 0
    by_extension: Dict[str, int] = {}
    
    try:
        for item in path.rglob('*'):
            if item.is_file():
                # Skip files in excluded directories
                if any(excluded in item.parts for excluded in EXCLUDE_DIRS):
                    continue
                count += 1
                ext = item.suffix.lower() or 'no-ext'
                by_extension[ext] = by_extension.get(ext, 0) + 1
    except (PermissionError, OSError):
        pass
    
    return count, by_extension


def format_dir_summary(path: Path) -> str:
    """Generate a summary string for a collapsed directory."""
    count, by_ext = count_files_in_dir(path)
    
    if count == 0:
        return "[empty]"
    
    # Get top 3 extensions
    sorted_exts = sorted(by_ext.items(), key=lambda x: -x[1])[:3]
    ext_summary = ", ".join(f"{c} {e}" for e, c in sorted_exts)
    
    return f"[{count} files: {ext_summary}]"


# =============================================================================
# SMART TREE GENERATOR
# =============================================================================

class SmartTreeGenerator:
    """Generates optimized project tree with smart filtering."""
    
    def __init__(self, root_path: Path, max_depth: int = MAX_TREE_DEPTH):
        self.root = root_path
        self.max_depth = max_depth
        self.file_count = 0
        self.skipped_dirs: Dict[str, str] = {}  # path -> reason
        self.collapsed_dirs: Dict[str, str] = {}  # path -> summary
    
    def generate(self) -> Dict:
        """Generate the filtered project tree."""
        return self._scan_dir(self.root, 0)
    
    def _scan_dir(self, path: Path, depth: int) -> Dict:
        """Recursively scan directory with smart filtering."""
        # Check depth limit (skip if None)
        if self.max_depth is not None and depth > self.max_depth:
            return {"...": f"[depth limit: {self.max_depth}]"}
        
        # Check file limit (skip if None)
        if MAX_FILES_IN_TREE is not None and self.file_count >= MAX_FILES_IN_TREE:
            return {"...": f"[file limit: {MAX_FILES_IN_TREE}]"}
        
        tree = {}
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            
            # Count items for potential summarization
            dir_items = [i for i in items if i.is_dir() and not should_exclude_dir(i.name, i)]
            file_items = [i for i in items if i.is_file()]
            
            for item in items:
                if item.is_dir():
                    rel_path = str(item.relative_to(self.root))
                    
                    # Check if should exclude
                    if should_exclude_dir(item.name, item):
                        self.skipped_dirs[rel_path] = "excluded"
                        continue
                    
                    # Check if in SUMMARIZE_ALWAYS_DIRS
                    if item.name in SUMMARIZE_ALWAYS_DIRS:
                        summary = format_dir_summary(item)
                        tree[item.name + "/"] = summary
                        self.collapsed_dirs[rel_path] = summary
                        continue
                    
                    # Check if should collapse
                    if should_collapse_dir(item.name, item):
                        summary = format_dir_summary(item)
                        tree[item.name + "/"] = summary
                        self.collapsed_dirs[rel_path] = summary
                        continue
                    
                    # Check if too many items in this dir (non-priority)
                    # BUT never collapse first-level dirs (depth 1) - these are main project folders
                    if not is_priority_dir(item.name) and depth > 1:
                        subitem_count = sum(1 for _ in item.iterdir()) if item.exists() else 0
                        if subitem_count > MAX_ITEMS_BEFORE_SUMMARY:
                            summary = format_dir_summary(item)
                            tree[item.name + "/"] = summary
                            self.collapsed_dirs[rel_path] = summary
                            continue
                    
                    # Recurse into directory
                    subtree = self._scan_dir(item, depth + 1)
                    if subtree:  # Only add if has content
                        tree[item.name] = subtree
                
                else:  # File
                    # Skip files at root level - we only want directory structure
                    if depth == 0:
                        continue
                    
                    # Check if should exclude
                    if should_exclude_file(item):
                        continue
                    
                    # Priority files always included (but not at root)
                    if is_priority_file(item.name):
                        tree[item.name] = "file"
                        self.file_count += 1
                        continue
                    
                    # Check file limit (skip if None)
                    if MAX_FILES_IN_TREE is not None and self.file_count >= MAX_FILES_IN_TREE:
                        if "..." not in tree:
                            tree["..."] = f"[+{len(file_items) - self.file_count} more files]"
                        break
                    
                    tree[item.name] = "file"
                    self.file_count += 1
        
        except PermissionError:
            return {"[LOCKED]": "Access Denied"}
        except OSError as e:
            return {"[ERROR]": str(e)}
        
        return tree
    
    def get_stats(self) -> Dict:
        """Get scanning statistics."""
        return {
            "files_included": self.file_count,
            "dirs_skipped": len(self.skipped_dirs),
            "dirs_collapsed": len(self.collapsed_dirs),
        }


# =============================================================================
# PROJECT SURVEY
# =============================================================================

def get_project_survey(root_path: str = ".", max_depth: int = MAX_TREE_DEPTH) -> Dict:
    """Get comprehensive project survey with smart filtering."""
    root = Path(root_path).resolve()
    
    # Generate smart tree
    generator = SmartTreeGenerator(root, max_depth)
    structure = generator.generate()
    stats = generator.get_stats()
    
    survey = {
        "root": str(root),
        "tech_stack": [],
        "entry_points": [],
        "dependencies": {},
        "structure": structure,
        "scan_stats": stats,
    }

    # Tech Stack Detection
    tech_identifiers = {
        "package.json": "Node.js/NPM",
        "tsconfig.json": "TypeScript",
        "requirements.txt": "Python (pip)",
        "pyproject.toml": "Python (Poetry/Flit)",
        "next.config.js": "Next.js",
        "next.config.ts": "Next.js",
        "next.config.mjs": "Next.js",
        "tailwind.config.js": "Tailwind CSS",
        "tailwind.config.ts": "Tailwind CSS",
        "prisma/schema.prisma": "Prisma ORM",
        "expo.json": "Expo/React Native",
        "app.json": "React Native/Expo",
        "docker-compose.yml": "Docker Compose",
        "Dockerfile": "Docker",
        "settings.json": "Maestro (Settings)",
        "CLAUDE.md": "Maestro (Context)",
        ".env": "Environment Config",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "Makefile": "Make",
    }

    def detect_tech(path: Path, depth: int = 0):
        if depth > 3:
            return
        try:
            for item in path.iterdir():
                if item.name in tech_identifiers:
                    tech = tech_identifiers[item.name]
                    if tech not in survey["tech_stack"]:
                        survey["tech_stack"].append(tech)
                    
                    if item.name == "package.json":
                        try:
                            pkg = json.loads(item.read_text(encoding='utf-8'))
                            deps = list(pkg.get("dependencies", {}).keys())[:20]  # Limit
                            survey["dependencies"]["npm"] = deps
                        except:
                            pass
                
                elif item.is_dir() and item.name not in EXCLUDE_DIRS:
                    detect_tech(item, depth + 1)
        except:
            pass

    detect_tech(root)

    # Entry Point Identification
    possible_entries = [
        "src/index.ts", "src/main.ts", "src/index.js", "src/app.ts",
        "src/app/page.tsx", "src/app/layout.tsx",
        "index.js", "index.ts", "app.py", "main.py", "app.js", "server.ts"
    ]
    for entry in possible_entries:
        if (root / entry).exists():
            survey["entry_points"].append(entry)

    return survey


# =============================================================================
# MAIN
# =============================================================================

def main():
    debug_log(f"MAIN called: argv={sys.argv}")

    parser = argparse.ArgumentParser(
        description="Smart project discovery for Claude Code CLI with intelligent filtering."
    )
    parser.add_argument("path", nargs="?", default=".", help="Root path to scan")
    parser.add_argument("depth", type=int, nargs="?", default=MAX_TREE_DEPTH, 
                        help=f"Scan depth (default: {MAX_TREE_DEPTH})")
    parser.add_argument("--silent", action="store_true", help="Suppress terminal output")

    args = parser.parse_args()

    debug_log(f"Parsed: path={args.path}, depth={args.depth}, silent={args.silent}")

    try:
        # Windows terminal unicode support
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

    try:
        report = get_project_survey(args.path, max_depth=args.depth)
        stats = report.get("scan_stats", {})
        
        debug_log(f"Survey completed: {stats.get('files_included', 0)} files, "
                  f"{stats.get('dirs_skipped', 0)} dirs skipped, "
                  f"{stats.get('dirs_collapsed', 0)} dirs collapsed")

        # Save to project data directory
        CLAUDE_DIR = Path.home() / ".claude"
        DATA_DIR = CLAUDE_DIR / "data"
        PROJECTS_DIR = DATA_DIR / "projects"
        
        project_name = Path(report["root"]).name
        safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
        project_dir = PROJECTS_DIR / safe_name
        project_dir.mkdir(parents=True, exist_ok=True)

        output_file = project_dir / "discovery-report.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        debug_log(f"Report saved to {output_file}")

        if not args.silent:
            print(f"[OK] Smart project discovery completed (Depth: {args.depth})")
            print(f"[STATS] {stats.get('files_included', 0)} files included, "
                  f"{stats.get('dirs_collapsed', 0)} dirs summarized")
            print(f"[REPORT] {output_file}")
            if report['tech_stack']:
                print(f"[TECH] {', '.join(report['tech_stack'])}")
        debug_log("EXPLORER completed successfully")
        
    except Exception as e:
        debug_log(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        debug_log(f"TRACEBACK: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
