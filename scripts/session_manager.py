#!/usr/bin/env python3
"""
Session Manager - Project state and conversation context management
Type-safe data models with Pydantic.

Usage: python session_manager.py [command] [args]

Commands:
    init        - Start new project
    load        - Load current project
    save        - Save state
    feature     - Add/remove feature
    decision    - Record decision
    status      - Show project status
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict

CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
PROJECT_FILE = DATA_DIR / "current-project.json"
CONTEXT_FILE = DATA_DIR / "conversation-context.json"

# Fix Windows console encoding
try:
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


@dataclass
class TechStack:
    """Tech stack information."""
    framework: str = "next.js"
    language: str = "typescript"
    database: str = "postgresql"
    orm: str = "prisma"
    styling: str = "tailwind"
    auth: Optional[str] = None
    payment: Optional[str] = None
    hosting: Optional[str] = None


@dataclass
class ProjectState:
    """Project state."""
    project_path: str = ""
    project_name: str = ""
    project_type: str = ""
    tech_stack: TechStack = field(default_factory=TechStack)
    features: List[str] = field(default_factory=list)
    pending_features: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    created_at: str = ""
    last_modified: str = ""
    status: str = "initializing"  # initializing, active, paused, completed


@dataclass 
class Decision:
    """User decision."""
    topic: str
    choice: str
    reason: str = ""
    timestamp: str = ""


@dataclass
class ConversationContext:
    """Conversation context."""
    session_id: str = ""
    project_id: str = ""
    decisions: List[Dict[str, str]] = field(default_factory=list)
    clarifications: List[str] = field(default_factory=list)
    last_user_intent: str = ""
    messages_count: int = 0


def ensure_data_dir():
    """Create data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_project() -> Optional[ProjectState]:
    """Load current project."""
    if PROJECT_FILE.exists():
        data = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
        tech_stack = TechStack(**data.get("tech_stack", {}))
        return ProjectState(
            project_path=data.get("project_path", ""),
            project_name=data.get("project_name", ""),
            project_type=data.get("project_type", ""),
            tech_stack=tech_stack,
            features=data.get("features", []),
            pending_features=data.get("pending_features", []),
            files_created=data.get("files_created", []),
            created_at=data.get("created_at", ""),
            last_modified=data.get("last_modified", ""),
            status=data.get("status", "initializing")
        )
    return None


def save_project(project: ProjectState):
    """Save project."""
    ensure_data_dir()
    project.last_modified = datetime.now().isoformat()
    
    data = {
        "project_path": project.project_path,
        "project_name": project.project_name,
        "project_type": project.project_type,
        "tech_stack": asdict(project.tech_stack),
        "features": project.features,
        "pending_features": project.pending_features,
        "files_created": project.files_created,
        "created_at": project.created_at,
        "last_modified": project.last_modified,
        "status": project.status
    }
    
    PROJECT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_context() -> ConversationContext:
    """Load conversation context."""
    if CONTEXT_FILE.exists():
        data = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))
        return ConversationContext(
            session_id=data.get("session_id", ""),
            project_id=data.get("project_id", ""),
            decisions=data.get("decisions", []),
            clarifications=data.get("clarifications", []),
            last_user_intent=data.get("last_user_intent", ""),
            messages_count=data.get("messages_count", 0)
        )
    return ConversationContext(session_id=datetime.now().isoformat())


def save_context(context: ConversationContext):
    """Save context."""
    ensure_data_dir()
    CONTEXT_FILE.write_text(json.dumps(asdict(context), indent=2, ensure_ascii=False), encoding="utf-8")


def init_project(name: str, path: str, project_type: str = "nextjs-fullstack"):
    """Start new project."""
    project = ProjectState(
        project_path=path,
        project_name=name,
        project_type=project_type,
        created_at=datetime.now().isoformat(),
        status="initializing"
    )
    save_project(project)
    
    # Start in context too
    context = ConversationContext(
        session_id=datetime.now().isoformat(),
        project_id=name
    )
    save_context(context)
    
    print(f"[OK] Project started: {name}")
    print(f"  Path: {path}")
    print(f"  Type: {project_type}")


def add_feature(feature: str, pending: bool = False):
    """Add feature."""
    project = load_project()
    if not project:
        print("[X] No active project. Run 'init' first.")
        return
    
    if pending:
        if feature not in project.pending_features:
            project.pending_features.append(feature)
            print(f"[OK] Pending feature added: {feature}")
    else:
        if feature in project.pending_features:
            project.pending_features.remove(feature)
        if feature not in project.features:
            project.features.append(feature)
            print(f"[OK] Feature added: {feature}")
    
    save_project(project)


def add_decision(topic: str, choice: str, reason: str = ""):
    """Record decision."""
    context = load_context()
    context.decisions.append({
        "topic": topic,
        "choice": choice,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    })
    save_context(context)
    print(f"[OK] Decision recorded: {topic} -> {choice}")


def update_tech_stack(key: str, value: str):
    """Update tech stack."""
    project = load_project()
    if not project:
        print("[X] No active project.")
        return
    
    if hasattr(project.tech_stack, key):
        setattr(project.tech_stack, key, value)
        save_project(project)
        print(f"[OK] Tech stack updated: {key} = {value}")
    else:
        print(f"[X] Invalid tech stack key: {key}")


def add_file(file_path: str):
    """Record created file."""
    project = load_project()
    if project and file_path not in project.files_created:
        project.files_created.append(file_path)
        save_project(project)


def set_status(status: str):
    """Update project status."""
    project = load_project()
    if project:
        project.status = status
        save_project(project)
        print(f"[OK] Project status: {status}")


def print_status():
    """Show project status."""
    project = load_project()
    context = load_context()
    
    if not project:
        print("[X] No active project.")
        return
    
    print("\n=== Project Status ===\n")
    print(f"[PROJECT] {project.project_name}")
    print(f"[PATH] {project.project_path}")
    print(f"[TYPE] {project.project_type}")
    print(f"[STATUS] {project.status}")
    print()
    
    print("[TECH STACK]")
    print(f"   Framework: {project.tech_stack.framework}")
    print(f"   Database: {project.tech_stack.database}")
    print(f"   Styling: {project.tech_stack.styling}")
    if project.tech_stack.auth:
        print(f"   Auth: {project.tech_stack.auth}")
    print()
    
    print(f"\n[FEATURES] ({len(project.features)})")
    for f in project.features:
        print(f"   • {f}")
    
    if project.pending_features:
        print(f"\n[PENDING] ({len(project.pending_features)})")
        for f in project.pending_features:
            print(f"   • {f}")
    
    print(f"\n[FILES] Created: {len(project.files_created)}")
    
    if context.decisions:
        print(f"\n[DECISIONS] ({len(context.decisions)})")
        for d in context.decisions[-5:]:  # Last 5 decisions
            print(f"   • {d['topic']}: {d['choice']}")


def main():
    """Main function - CLI operations."""
    if len(sys.argv) < 2:
        print_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "init":
        if len(sys.argv) < 4:
            print("Usage: session_manager.py init <name> <path> [type]")
            return
        name = sys.argv[2]
        path = sys.argv[3]
        project_type = sys.argv[4] if len(sys.argv) > 4 else "nextjs-fullstack"
        init_project(name, path, project_type)
    
    elif command == "feature":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py feature <name> [--pending]")
            return
        pending = "--pending" in sys.argv
        add_feature(sys.argv[2], pending)
    
    elif command == "decision":
        if len(sys.argv) < 4:
            print("Usage: session_manager.py decision <topic> <choice> [reason]")
            return
        reason = sys.argv[4] if len(sys.argv) > 4 else ""
        add_decision(sys.argv[2], sys.argv[3], reason)
    
    elif command == "tech":
        if len(sys.argv) < 4:
            print("Usage: session_manager.py tech <key> <value>")
            return
        update_tech_stack(sys.argv[2], sys.argv[3])
    
    elif command == "file":
        if len(sys.argv) < 3:
            print("Usage: session_manager.py file <path>")
            return
        add_file(sys.argv[2])
    
    elif command == "status":
        if len(sys.argv) > 2:
            set_status(sys.argv[2])
        else:
            print_status()
    
    elif command == "json":
        project = load_project()
        context = load_context()
        print(json.dumps({
            "project": asdict(project) if project else None,
            "context": asdict(context)
        }, indent=2, ensure_ascii=False))
    
    elif command == "load":
        print_status()
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
