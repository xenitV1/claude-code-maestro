#!/usr/bin/env python3
"""
Dependency Scanner - Analyze file dependencies in user projects.

Detects:
- Import statements (ES6, CommonJS, Python)
- API endpoint calls (fetch, axios)
- Database model usage (Prisma, SQLAlchemy)
- Component dependencies

Usage:
    python dependency_scanner.py [project_path] [--output json|markdown]
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any

# Debug logging
DEBUG_LOG = Path.home() / ".claude" / "data" / "hook_debug.log"


def debug_log(message: str):
    """Write debug log."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] dependency_scanner.py: {message}\n")
    except:
        pass


# File extensions to scan
SCANNABLE_EXTENSIONS = {
    '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',  # JavaScript/TypeScript
    '.py',  # Python
    '.vue', '.svelte',  # Vue/Svelte
}

# Directories to skip
SKIP_DIRS = {
    'node_modules', '.git', '.next', 'dist', 'build', 
    '__pycache__', 'venv', '.venv', 'env', '.env',
    'coverage', '.nyc_output', '.turbo', '.cache'
}


def extract_js_imports(content: str) -> List[str]:
    """Extract import statements from JavaScript/TypeScript files."""
    imports = []
    
    # ES6 imports: import X from 'path' or import 'path'
    es6_pattern = r"import\s+(?:(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)\s+from\s+)?['\"]([^'\"]+)['\"]"
    imports.extend(re.findall(es6_pattern, content))
    
    # Dynamic imports: import('path')
    dynamic_pattern = r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
    imports.extend(re.findall(dynamic_pattern, content))
    
    # CommonJS: require('path')
    require_pattern = r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
    imports.extend(re.findall(require_pattern, content))
    
    return imports


def extract_python_imports(content: str) -> List[str]:
    """Extract import statements from Python files."""
    imports = []
    
    # import module
    import_pattern = r"^import\s+([\w.]+)"
    imports.extend(re.findall(import_pattern, content, re.MULTILINE))
    
    # from module import X
    from_pattern = r"^from\s+([\w.]+)\s+import"
    imports.extend(re.findall(from_pattern, content, re.MULTILINE))
    
    return imports


def extract_api_calls(content: str) -> List[str]:
    """Extract API endpoint calls from code."""
    api_calls = []
    
    # fetch('/api/...')
    fetch_pattern = r"fetch\s*\(\s*['\"`]([^'\"`]+)['\"`]"
    api_calls.extend(re.findall(fetch_pattern, content))
    
    # axios.get/post/put/delete('/api/...')
    axios_pattern = r"axios\s*\.\s*(?:get|post|put|delete|patch)\s*\(\s*['\"`]([^'\"`]+)['\"`]"
    api_calls.extend(re.findall(axios_pattern, content))
    
    # Template literal API calls: fetch(`/api/...`)
    template_pattern = r"fetch\s*\(\s*`([^`]+)`"
    for match in re.findall(template_pattern, content):
        # Extract static part before ${
        static_part = match.split('${')[0]
        if static_part:
            api_calls.append(static_part)
    
    # Filter to only API-like paths
    api_calls = [call for call in api_calls if '/api/' in call or call.startswith('/')]
    
    return api_calls


def extract_db_models(content: str) -> List[str]:
    """Extract database model references from code."""
    models = []
    
    # Prisma: db.modelName.findMany() etc.
    prisma_pattern = r"(?:db|prisma)\s*\.\s*(\w+)\s*\.\s*(?:findMany|findUnique|findFirst|create|update|delete|upsert|count|aggregate)"
    models.extend(re.findall(prisma_pattern, content))
    
    # SQLAlchemy: session.query(Model)
    sqlalchemy_pattern = r"session\s*\.\s*query\s*\(\s*(\w+)\s*\)"
    models.extend(re.findall(sqlalchemy_pattern, content))
    
    # Drizzle: db.select().from(table)
    drizzle_pattern = r"\.from\s*\(\s*(\w+)\s*\)"
    models.extend(re.findall(drizzle_pattern, content))
    
    return list(set(models))  # Dedupe


def extract_component_usage(content: str) -> List[str]:
    """Extract React/Vue component usage."""
    components = []
    
    # JSX components: <ComponentName or <ComponentName>
    jsx_pattern = r"<([A-Z][a-zA-Z0-9]*)"
    components.extend(re.findall(jsx_pattern, content))
    
    return list(set(components))  # Dedupe


def resolve_import_path(import_path: str, file_path: Path, project_root: Path) -> str:
    """Resolve import path to actual file path."""
    # Skip node_modules imports
    if not import_path.startswith('.') and not import_path.startswith('@/') and not import_path.startswith('~/'):
        return f"[npm] {import_path}"
    
    # Handle alias imports (@/, ~/)
    if import_path.startswith('@/'):
        import_path = import_path.replace('@/', 'src/')
    elif import_path.startswith('~/'):
        import_path = import_path.replace('~/', '')
    
    # Handle relative imports
    if import_path.startswith('.'):
        base_dir = file_path.parent
        resolved = (base_dir / import_path).resolve()
        try:
            return str(resolved.relative_to(project_root))
        except ValueError:
            return str(resolved)
    
    return import_path


def scan_file(file_path: Path, project_root: Path) -> Dict[str, Any]:
    """Scan a single file for dependencies."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        debug_log(f"Error reading {file_path}: {e}")
        return {}
    
    ext = file_path.suffix.lower()
    result = {
        "imports": [],
        "api_calls": [],
        "db_models": [],
        "components": [],
        "raw_imports": []
    }
    
    # Extract based on file type
    if ext in {'.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.vue', '.svelte'}:
        raw_imports = extract_js_imports(content)
        result["raw_imports"] = raw_imports
        result["imports"] = [resolve_import_path(imp, file_path, project_root) for imp in raw_imports]
        result["api_calls"] = extract_api_calls(content)
        result["db_models"] = extract_db_models(content)
        result["components"] = extract_component_usage(content)
        
    elif ext == '.py':
        result["raw_imports"] = extract_python_imports(content)
        result["imports"] = result["raw_imports"]
        result["db_models"] = extract_db_models(content)
    
    # Filter out empty results
    return {k: v for k, v in result.items() if v}


def build_reverse_dependencies(deps: Dict[str, Dict]) -> Dict[str, List[str]]:
    """Build reverse dependency map (what files depend on this file)."""
    reverse_deps = {}
    
    for file_path, file_deps in deps.items():
        for imp in file_deps.get("imports", []):
            # Skip npm packages
            if imp.startswith("[npm]"):
                continue
            
            # Normalize the import path
            if imp not in reverse_deps:
                reverse_deps[imp] = []
            reverse_deps[imp].append(file_path)
    
    return reverse_deps


def find_api_route_files(project_root: Path) -> Dict[str, str]:
    """Map API endpoints to their route files."""
    api_routes = {}
    
    # Next.js App Router: app/api/*/route.ts
    for route_file in project_root.rglob("**/api/**/route.{ts,js}"):
        try:
            rel_path = route_file.relative_to(project_root)
            # Convert path to API endpoint
            # app/api/users/route.ts -> /api/users
            parts = rel_path.parts
            if 'api' in parts:
                api_idx = parts.index('api')
                endpoint_parts = [p for p in parts[api_idx:-1] if p not in {'route.ts', 'route.js'}]
                endpoint = '/' + '/'.join(endpoint_parts)
                api_routes[endpoint] = str(rel_path)
        except:
            pass
    
    # Next.js Pages Router: pages/api/*.ts
    for route_file in project_root.rglob("pages/api/**/*.{ts,js}"):
        try:
            rel_path = route_file.relative_to(project_root)
            parts = rel_path.parts
            # pages/api/users.ts -> /api/users
            endpoint = '/' + '/'.join(parts[1:]).replace('.ts', '').replace('.js', '')
            api_routes[endpoint] = str(rel_path)
        except:
            pass
    
    return api_routes


def scan_project(project_path: str, max_files: int = 500) -> Dict[str, Any]:
    """Scan entire project for dependencies."""
    root = Path(project_path).resolve()
    
    result = {
        "project_root": str(root),
        "scanned_at": datetime.now().isoformat(),
        "files": {},
        "summary": {
            "total_files": 0,
            "files_with_imports": 0,
            "files_with_api_calls": 0,
            "files_with_db_models": 0,
            "unique_api_endpoints": set(),
            "unique_db_models": set(),
            "unique_npm_packages": set()
        },
        "api_routes": {},
        "reverse_dependencies": {}
    }
    
    file_count = 0
    
    for file_path in root.rglob("*"):
        # Skip directories
        if not file_path.is_file():
            continue
        
        # Check extension
        if file_path.suffix.lower() not in SCANNABLE_EXTENSIONS:
            continue
        
        # Skip excluded directories
        if any(skip_dir in file_path.parts for skip_dir in SKIP_DIRS):
            continue
        
        # Limit file count
        file_count += 1
        if file_count > max_files:
            debug_log(f"Reached max file limit ({max_files})")
            break
        
        try:
            rel_path = str(file_path.relative_to(root))
        except ValueError:
            continue
        
        file_deps = scan_file(file_path, root)
        
        if file_deps:
            result["files"][rel_path] = file_deps
            result["summary"]["total_files"] += 1
            
            if file_deps.get("imports"):
                result["summary"]["files_with_imports"] += 1
                # Track npm packages
                for imp in file_deps["imports"]:
                    if imp.startswith("[npm]"):
                        result["summary"]["unique_npm_packages"].add(imp.replace("[npm] ", ""))
            
            if file_deps.get("api_calls"):
                result["summary"]["files_with_api_calls"] += 1
                result["summary"]["unique_api_endpoints"].update(file_deps["api_calls"])
            
            if file_deps.get("db_models"):
                result["summary"]["files_with_db_models"] += 1
                result["summary"]["unique_db_models"].update(file_deps["db_models"])
    
    # Convert sets to lists for JSON serialization
    result["summary"]["unique_api_endpoints"] = list(result["summary"]["unique_api_endpoints"])
    result["summary"]["unique_db_models"] = list(result["summary"]["unique_db_models"])
    result["summary"]["unique_npm_packages"] = list(result["summary"]["unique_npm_packages"])
    
    # Find API route files
    result["api_routes"] = find_api_route_files(root)
    
    # Build reverse dependencies
    result["reverse_dependencies"] = build_reverse_dependencies(result["files"])
    
    return result


def format_markdown(result: Dict) -> str:
    """Format result as markdown for CODEBASE.md."""
    md = []
    md.append("## File Dependencies\n")
    md.append(f"> Scanned at: {result['scanned_at']}\n")
    
    summary = result["summary"]
    md.append("### Summary\n")
    md.append(f"| Metric | Count |")
    md.append(f"|--------|-------|")
    md.append(f"| Files scanned | {summary['total_files']} |")
    md.append(f"| Files with imports | {summary['files_with_imports']} |")
    md.append(f"| Files with API calls | {summary['files_with_api_calls']} |")
    md.append(f"| Files with DB models | {summary['files_with_db_models']} |")
    md.append(f"| Unique API endpoints | {len(summary['unique_api_endpoints'])} |")
    md.append(f"| Unique DB models | {len(summary['unique_db_models'])} |")
    md.append("")
    
    # API Endpoints
    if summary['unique_api_endpoints']:
        md.append("### API Endpoints Used\n")
        md.append("```")
        for endpoint in sorted(summary['unique_api_endpoints']):
            md.append(endpoint)
        md.append("```\n")
    
    # Database Models
    if summary['unique_db_models']:
        md.append("### Database Models\n")
        md.append("```")
        for model in sorted(summary['unique_db_models']):
            md.append(model)
        md.append("```\n")
    
    # High-impact files (most depended upon)
    if result['reverse_dependencies']:
        md.append("### High-Impact Files\n")
        md.append("*Files that many other files depend on:*\n")
        sorted_deps = sorted(
            result['reverse_dependencies'].items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )[:10]
        
        if sorted_deps:
            md.append("| File | Depended by |")
            md.append("|------|-------------|")
            for file_path, dependents in sorted_deps:
                if len(dependents) > 1:
                    md.append(f"| `{file_path}` | {len(dependents)} files |")
        md.append("")
    
    return "\n".join(md)


def main():
    debug_log(f"MAIN called: argv={sys.argv}")
    
    parser = argparse.ArgumentParser(
        description="Scan project files for dependencies."
    )
    parser.add_argument("path", nargs="?", default=".", help="Project root path")
    parser.add_argument("--output", choices=["json", "markdown"], default="json", 
                       help="Output format")
    parser.add_argument("--max-files", type=int, default=500,
                       help="Maximum files to scan")
    parser.add_argument("--save", action="store_true",
                       help="Save to project data directory")
    parser.add_argument("--silent", action="store_true",
                       help="Suppress terminal output")
    
    args = parser.parse_args()
    
    try:
        result = scan_project(args.path, max_files=args.max_files)
        debug_log(f"Scan completed: {result['summary']['total_files']} files")
        
        if args.output == "markdown":
            output = format_markdown(result)
        else:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        
        if args.save:
            # Save to project data directory
            PROJECTS_DIR = Path.home() / ".claude" / "data" / "projects"
            project_name = Path(result["project_root"]).name
            safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
            project_dir = PROJECTS_DIR / safe_name
            project_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = project_dir / "dependency-report.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            if not args.silent:
                print(f"[OK] Dependency scan completed.")
                print(f"Report saved to: {output_file}")
                print(f"Files scanned: {result['summary']['total_files']}")
        else:
            if not args.silent:
                print(output)
        
        debug_log("DEPENDENCY_SCANNER completed successfully")
        
    except Exception as e:
        debug_log(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        debug_log(f"TRACEBACK: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
