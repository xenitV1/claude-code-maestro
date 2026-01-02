import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def print_header(text):
    print(f"\n{'='*20} {text} {'='*20}")

def lint_check(file_path):
    path = Path(file_path).absolute()
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    ext = path.suffix.lower()
    project_root = path.parent
    # Try to find project root (where .git or package.json/pyproject.toml exists)
    for parent in path.parents:
        if (parent / ".git").exists() or (parent / "package.json").exists() or (parent / "pyproject.toml").exists():
            project_root = parent
            break

    print(f"🚀 Maestro Quality Audit V2")
    print(f"📁 Target: {file_path}")
    print(f"🏠 Project Root: {project_root}")
    
    results = {"errors": 0, "warnings": 0, "security_issues": 0}

    if ext in ['.ts', '.tsx', '.js', '.jsx']:
        print_header("JAVASCRIPT / TYPESCRIPT")
        
        # ESLint
        print("⚡ Analyzing code style (ESLint)...")
        code, out, err = run_command(f"npx eslint \"{path}\" --fix", cwd=project_root)
        if code != 0:
            print(f"❌ Style/Syntax Issues:\n{out}{err}")
            results["errors"] += 1
        else:
            print("✅ Style is clean.")
            
        # TypeScript
        if ext in ['.ts', '.tsx']:
            print("⚡ Checking types (TSC)...")
            code, out, err = run_command("npx tsc --noEmit", cwd=project_root)
            if code != 0:
                print(f"❌ Type Errors:\n{out}")
                results["errors"] += 1
            else:
                print("✅ Types are valid.")

        # Security
        print("⚡ Scanning for vulnerabilities (NPM Audit)...")
        code, out, err = run_command("npm audit --audit-level=high", cwd=project_root)
        if code != 0:
            print(f"⚠️ Security Warnings:\n{out}")
            results["security_issues"] += 1

    elif ext == '.py':
        print_header("PYTHON")
        
        # Ruff (Fast & Comprehensive)
        print("⚡ Analyzing code style & logic (Ruff)...")
        code, out, err = run_command(f"ruff check \"{path}\" --fix", cwd=project_root)
        if code != 0:
            print(f"❌ Issues found by Ruff:\n{out}{err}")
            results["errors"] += 1
        else:
            print("✅ Ruff passed.")
            
        # Security (Bandit)
        print("⚡ Scanning for security flaws (Bandit)...")
        code, out, err = run_command(f"bandit -r \"{path}\" -ll", cwd=project_root)
        if code != 0:
            print(f"🛡️ Security Issues:\n{out}")
            results["security_issues"] += 1
        else:
            print("✅ Security scan passed.")

        # Types (MyPy)
        print("⚡ Checking types (MyPy)...")
        code, out, err = run_command(f"mypy \"{path}\" --ignore-missing-imports", cwd=project_root)
        if code != 0:
            print(f"❌ Type Errors:\n{out}")
            results["errors"] += 1
        else:
            print("✅ MyPy passed.")

    # Final Report
    print_header("FINAL AUDIT REPORT")
    if results["errors"] == 0 and results["security_issues"] == 0:
        print("🌟 PERFECT: Code meets all Maestro quality standards.")
    else:
        print(f"⚠️ TOTAL ISSUES: {results['errors'] + results['security_issues']}")
        print(f"   - Logic/Style: {results['errors']}")
        print(f"   - Security: {results['security_issues']}")
        print("\n💡 Action: Fix the issues above before proceeding.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/lint_check.py <file_path>")
        sys.exit(1)
    
    lint_check(sys.argv[1])
