#!/usr/bin/env python3
"""
Auto Preview - Automatic build and preview pipeline
Port control, process management, health check.

Usage: python auto_preview.py [command] [args]

Commands:
    start       - Start preview server
    stop        - Stop preview server
    restart     - Restart server
    status      - Server status
    check       - Health check
    port        - Find available port
"""

import json
import sys
import subprocess
import socket
import time
import os
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
PREVIEW_FILE = DATA_DIR / "preview-status.json"

# Default ports
DEFAULT_PORTS = [3000, 3001, 3002, 4000, 5000, 8000, 8080]


def ensure_data_dir():
    """Create data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def is_port_in_use(port: int) -> bool:
    """Check if port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def find_available_port(preferred: int = 3000) -> int:
    """Find available port."""
    if not is_port_in_use(preferred):
        return preferred
    
    for port in DEFAULT_PORTS:
        if not is_port_in_use(port):
            return port
    
    # Find random port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def load_preview_status() -> dict:
    """Load preview status."""
    if PREVIEW_FILE.exists():
        return json.loads(PREVIEW_FILE.read_text(encoding="utf-8"))
    return {}


def save_preview_status(status: dict):
    """Save preview status."""
    ensure_data_dir()
    PREVIEW_FILE.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def check_health(port: int, timeout: int = 5) -> Tuple[bool, str]:
    """Perform health check."""
    import urllib.request
    import urllib.error
    
    url = f"http://localhost:{port}"
    
    try:
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                return True, "OK"
            return False, f"HTTP {response.status}"
    except urllib.error.URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)


def detect_project_type(project_path: str) -> Optional[str]:
    """Detect project type."""
    path = Path(project_path)
    
    package_json = path / "package.json"
    if package_json.exists():
        try:
            pkg = json.loads(package_json.read_text())
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            if "next" in deps:
                return "nextjs"
            elif "vite" in deps:
                return "vite"
            elif "react-scripts" in deps:
                return "cra"
            elif "express" in deps:
                return "express"
            else:
                return "node"
        except:
            return "node"
    
    if (path / "requirements.txt").exists() or (path / "pyproject.toml").exists():
        return "python"
    
    if (path / "Cargo.toml").exists():
        return "rust"
    
    return None


def get_start_command(project_type: str) -> str:
    """Start command based on project type."""
    commands = {
        "nextjs": "npm run dev",
        "vite": "npm run dev",
        "cra": "npm start",
        "express": "npm run dev",
        "node": "npm start",
        "python": "python -m http.server 3000"
    }
    return commands.get(project_type, "npm run dev")


def start_preview(project_path: str, port: int = 3000) -> dict:
    """Start preview server."""
    project_path = Path(project_path).resolve()
    
    if not project_path.exists():
        return {"success": False, "error": f"Project not found: {project_path}"}
    
    # Port control
    if is_port_in_use(port):
        new_port = find_available_port(port)
        print(f"[!] Port {port} in use, {new_port} will be used.")
        port = new_port
    
    # Detect project type
    project_type = detect_project_type(str(project_path))
    if not project_type:
        return {"success": False, "error": "Project type could not be detected"}
    
    start_cmd = get_start_command(project_type)
    
    # Environment variables
    env = os.environ.copy()
    env["PORT"] = str(port)
    
    print(f"[START] Starting preview...")
    print(f"   Project: {project_path}")
    print(f"   Type: {project_type}")
    print(f"   Port: {port}")
    print(f"   Command: {start_cmd}")
    
    try:
        # shell=True required on Windows
        process = subprocess.Popen(
            start_cmd,
            shell=True,
            cwd=str(project_path),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        # Save status
        status = {
            "pid": process.pid,
            "port": port,
            "project_path": str(project_path),
            "project_type": project_type,
            "started_at": datetime.now().isoformat(),
            "url": f"http://localhost:{port}"
        }
        save_preview_status(status)
        
        # Wait a few seconds and health check
        time.sleep(3)
        
        health_ok, health_msg = check_health(port)
        if health_ok:
            print(f"\n[OK] Preview ready!")
            print(f"   URL: http://localhost:{port}")
        else:
            print(f"\n[...] Starting server... (health check: {health_msg})")
            print(f"   URL: http://localhost:{port}")
        
        return {
            "success": True,
            "pid": process.pid,
            "port": port,
            "url": f"http://localhost:{port}"
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def stop_preview() -> dict:
    """Stop preview server."""
    status = load_preview_status()
    
    if not status or "pid" not in status:
        return {"success": False, "error": "No running preview"}
    
    pid = status["pid"]
    
    try:
        if os.name == 'nt':
            subprocess.run(f"taskkill /F /PID {pid} /T", shell=True, capture_output=True)
        else:
            os.kill(pid, 9)
        
        # Clear status
        save_preview_status({})
        
        print(f"[OK] Preview stopped (PID: {pid})")
        return {"success": True, "stopped_pid": pid}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_status() -> dict:
    """Show preview status."""
    status = load_preview_status()
    
    if not status:
        print("[X] No running preview")
        return {"running": False}
    
    port = status.get("port", 3000)
    health_ok, health_msg = check_health(port)
    
    print("\n=== Preview Status ===\n")
    print(f"[URL] {status.get('url', 'N/A')}")
    print(f"[PROJECT] {status.get('project_path', 'N/A')}")
    print(f"[TYPE] {status.get('project_type', 'N/A')}")
    print(f"[PID] {status.get('pid', 'N/A')}")
    print(f"[STARTED] {status.get('started_at', 'N/A')}")
    print(f"[HEALTH] {'OK' if health_ok else health_msg}")
    
    return {
        "running": True,
        "healthy": health_ok,
        **status
    }


def main():
    """Main function - CLI operations."""
    if len(sys.argv) < 2:
        get_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        project_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
        start_preview(project_path, port)
    
    elif command == "stop":
        stop_preview()
    
    elif command == "restart":
        status = load_preview_status()
        if status:
            project_path = status.get("project_path", os.getcwd())
            port = status.get("port", 3000)
            stop_preview()
            time.sleep(1)
            start_preview(project_path, port)
        else:
            print("[X] No preview to restart")
    
    elif command == "status":
        get_status()
    
    elif command == "check":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
        ok, msg = check_health(port)
        print(f"Health check (port {port}): {'[OK]' if ok else f'[X] {msg}'}")
    
    elif command == "port":
        preferred = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
        available = find_available_port(preferred)
        print(f"Available port: {available}")
    
    elif command == "json":
        status = load_preview_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
