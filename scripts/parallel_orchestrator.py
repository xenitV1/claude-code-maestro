#!/usr/bin/env python3
"""
Parallel Agent Orchestrator v2.0 - Enhanced multi-agent coordination.

Features:
- Streaming progress UI with Rich
- Retry/fallback logic for failed agents
- Agent message sharing (basic communication)
- Real-time status updates

Usage:
    python scripts/parallel_orchestrator.py "Your task..." --agents 3
    python scripts/parallel_orchestrator.py "Your task..." --agents 5 --test
    python scripts/parallel_orchestrator.py "Your task..." --agents 3 --retries 2
"""

import os
import json
import sys
import uuid
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# Check for Rich
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Debug logging
DEBUG_LOG = Path.home() / ".claude" / "data" / "hook_debug.log"

def debug_log(message: str):
    """Write debug log."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] parallel_orchestrator.py: {message}\n")
    except Exception as e:
        sys.stderr.write(f"DEBUG_LOG_ERROR: {e}\n")

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
ORCHESTRATOR_STATE_FILE = DATA_DIR / "orchestrator-state.json"

# Console
console = Console() if RICH_AVAILABLE else None


class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class AgentMessage:
    """Message shared between agents."""
    from_agent: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    msg_type: str = "info"  # info, warning, finding, suggestion


class MessageBoard:
    """Shared message board for agent communication."""

    def __init__(self):
        self.messages: List[AgentMessage] = []
        self._lock = threading.Lock()

    def post(self, from_agent: str, content: str, msg_type: str = "info"):
        """Post a message to the board."""
        with self._lock:
            msg = AgentMessage(from_agent, content, msg_type=msg_type)
            self.messages.append(msg)
            debug_log(f"MessageBoard: {from_agent} posted: {content[:50]}...")

    def get_messages(self, since: Optional[str] = None) -> List[AgentMessage]:
        """Get messages, optionally since a timestamp."""
        with self._lock:
            if since:
                return [m for m in self.messages if m.timestamp > since]
            return list(self.messages)

    def get_findings(self) -> List[AgentMessage]:
        """Get all findings from agents."""
        with self._lock:
            return [m for m in self.messages if m.msg_type == "finding"]


class AgentTask:
    def __init__(self, agent_id: str, prompt: str, name: str = "",
                 message_board: Optional[MessageBoard] = None,
                 max_retries: int = 2):
        self.agent_id = agent_id
        self.prompt = prompt
        self.name = name or f"Agent-{agent_id[:4]}"
        self.status = AgentStatus.PENDING
        self.result = ""
        self.error = ""
        self.started_at = None
        self.ended_at = None
        self.attempt = 0
        self.max_retries = max_retries
        self.message_board = message_board
        self.progress_callback: Optional[Callable] = None

    def post_message(self, content: str, msg_type: str = "info"):
        """Post a message to the shared board."""
        if self.message_board:
            self.message_board.post(self.name, content, msg_type)

    def execute(self, test_mode: bool = False) -> 'AgentTask':
        """Execute the agent task with retry logic."""
        debug_log(f"AgentTask.execute: {self.name}, test_mode={test_mode}")

        while self.attempt <= self.max_retries:
            self.attempt += 1
            self.status = AgentStatus.RUNNING if self.attempt == 1 else AgentStatus.RETRYING
            self.started_at = datetime.now().isoformat()

            try:
                if test_mode:
                    result = self._mock_execute()
                else:
                    result = self._real_execute()

                if result:
                    self.status = AgentStatus.COMPLETED
                    self.post_message(f"Completed analysis", "info")

                    # Extract and share findings
                    if "issue" in self.result.lower() or "problem" in self.result.lower():
                        self.post_message(f"Found potential issues", "finding")

                    break
                else:
                    if self.attempt <= self.max_retries:
                        debug_log(f"Retrying {self.name}: attempt {self.attempt + 1}")
                        self.post_message(f"Retrying (attempt {self.attempt + 1})", "warning")
                        time.sleep(1)  # Brief pause before retry
                    else:
                        self.status = AgentStatus.FAILED
                        self.post_message(f"Failed after {self.max_retries} retries", "warning")

            except Exception as e:
                self.error = str(e)
                debug_log(f"Agent {self.name} exception: {type(e).__name__}: {e}")

                if self.attempt <= self.max_retries:
                    time.sleep(1)
                else:
                    self.status = AgentStatus.FAILED

        self.ended_at = datetime.now().isoformat()

        if self.progress_callback:
            self.progress_callback(self)

        return self

    def _mock_execute(self) -> bool:
        """Mock execution for testing."""
        import random
        sleep_time = random.uniform(1, 3)
        debug_log(f"Mock execution: {self.name}, sleep={sleep_time:.2f}s")

        # Simulate progress updates
        for i in range(5):
            time.sleep(sleep_time / 5)
            if self.progress_callback:
                self.progress_callback(self, progress=i * 20)

        # Simulate occasional failures for retry testing
        if random.random() < 0.1 and self.attempt == 1:  # 10% fail first attempt
            self.error = "Simulated failure"
            return False

        self.result = f"MOCK RESULT for {self.name}: Analyzed '{self.prompt[:30]}...' - Found 3 potential improvements."
        return True

    def _real_execute(self) -> bool:
        """Real execution using Claude Code CLI."""
        debug_log(f"Real execution: claude --print {self.prompt[:50]}...")

        try:
            process = subprocess.Popen(
                ["claude", "--print", self.prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )

            stdout, stderr = process.communicate(timeout=300)  # 5 min timeout
            debug_log(f"Process finished: {self.name}, returncode={process.returncode}")

            self.result = stdout
            if process.returncode != 0:
                self.error = stderr
                debug_log(f"Agent {self.name} failed: {stderr[:100]}")
                return False

            debug_log(f"Agent {self.name} completed successfully")
            return True

        except subprocess.TimeoutExpired:
            process.kill()
            self.error = "Execution timed out (5 min)"
            return False
        except Exception as e:
            self.error = str(e)
            return False


class Orchestrator:
    def __init__(self, main_prompt: str, agent_count: int = 3,
                 test_mode: bool = False, max_retries: int = 2):
        self.main_prompt = main_prompt
        self.agent_count = agent_count
        self.test_mode = test_mode
        self.max_retries = max_retries
        self.session_id = str(uuid.uuid4())
        self.tasks: List[AgentTask] = []
        self.message_board = MessageBoard()
        self.start_time = None
        debug_log(f"Orchestrator.__init__: session={self.session_id[:8]}, agents={agent_count}")

    def ensure_dirs(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def initialize_tasks(self):
        """Create agent tasks with different perspectives."""
        debug_log(f"initialize_tasks: creating {self.agent_count} tasks")

        agent_map = [
            {"perspective": "Security & Architecture", "agent": "security-auditor", "emoji": "🔒"},
            {"perspective": "Backend & API", "agent": "backend-specialist", "emoji": "⚙️"},
            {"perspective": "Frontend & UX", "agent": "frontend-specialist", "emoji": "🎨"},
            {"perspective": "Testing & QA", "agent": "test-engineer", "emoji": "🧪"},
            {"perspective": "DevOps & Performance", "agent": "devops-engineer", "emoji": "🚀"},
        ]

        for i in range(self.agent_count):
            map_item = agent_map[i % len(agent_map)]
            perspective = map_item["perspective"]
            agent_name = map_item["agent"]
            emoji = map_item["emoji"]

            sub_prompt = f"As {agent_name}, analyze from {perspective} perspective: {self.main_prompt}"

            agent_id = str(uuid.uuid4())
            task = AgentTask(
                agent_id,
                sub_prompt,
                f"{emoji} {agent_name}",
                message_board=self.message_board,
                max_retries=self.max_retries
            )
            self.tasks.append(task)
            debug_log(f"Task created: {agent_name}")

    def save_state(self):
        """Save current orchestration state."""
        state = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "main_prompt": self.main_prompt,
            "tasks": [
                {
                    "id": t.agent_id,
                    "name": t.name,
                    "status": t.status.value,
                    "attempt": t.attempt,
                    "started_at": t.started_at,
                    "ended_at": t.ended_at,
                    "result_snippet": t.result[:200] if t.result else "",
                    "error": t.error
                } for t in self.tasks
            ],
            "messages": [
                {
                    "from": m.from_agent,
                    "content": m.content,
                    "type": m.msg_type,
                    "timestamp": m.timestamp
                } for m in self.message_board.messages
            ]
        }
        ORCHESTRATOR_STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    def _generate_status_table(self):
        """Generate a status table for Rich display."""
        table = Table(title="Agent Status", show_header=True, header_style="bold cyan")
        table.add_column("Agent", style="white")
        table.add_column("Status", justify="center")
        table.add_column("Attempt", justify="center")
        table.add_column("Time", justify="right")

        for task in self.tasks:
            status_style = {
                AgentStatus.PENDING: "[dim]⏳ Pending[/dim]",
                AgentStatus.RUNNING: "[yellow]🔄 Running[/yellow]",
                AgentStatus.COMPLETED: "[green]✅ Done[/green]",
                AgentStatus.FAILED: "[red]❌ Failed[/red]",
                AgentStatus.RETRYING: "[orange1]🔁 Retrying[/orange1]",
            }.get(task.status, task.status.value)

            elapsed = ""
            if task.started_at:
                start = datetime.fromisoformat(task.started_at)
                if task.ended_at:
                    end = datetime.fromisoformat(task.ended_at)
                    elapsed = f"{(end - start).seconds}s"
                else:
                    elapsed = f"{(datetime.now() - start).seconds}s..."

            table.add_row(task.name, status_style, str(task.attempt), elapsed)

        return table

    def run(self):
        """Run orchestration with streaming progress."""
        debug_log("Orchestrator.run: starting")
        self.ensure_dirs()
        self.initialize_tasks()
        self.start_time = datetime.now()

        mode_str = " (TEST MODE)" if self.test_mode else ""

        if RICH_AVAILABLE and console:
            self._run_with_rich_ui(mode_str)
        else:
            self._run_simple(mode_str)

        self.synthesize()

    def _run_with_rich_ui(self, mode_str: str):
        """Run with Rich progress UI."""
        console.print(Panel(
            f"[bold cyan]Orchestrator Session[/bold cyan]\n"
            f"ID: {self.session_id[:8]}{mode_str}\n"
            f"Agents: {self.agent_count}",
            title="🎼 Maestro",
            border_style="cyan"
        ))

        with Live(self._generate_status_table(), refresh_per_second=2, console=console) as live:
            def update_display(task: AgentTask, progress: int = 100):
                live.update(self._generate_status_table())
                self.save_state()

            # Set callbacks
            for task in self.tasks:
                task.progress_callback = update_display

            with ThreadPoolExecutor(max_workers=self.agent_count) as executor:
                futures = {executor.submit(task.execute, self.test_mode): task for task in self.tasks}

                for future in as_completed(futures):
                    task = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        console.print(f"[red]Error in {task.name}: {e}[/red]")

                    live.update(self._generate_status_table())

        # Final status
        completed = sum(1 for t in self.tasks if t.status == AgentStatus.COMPLETED)
        failed = sum(1 for t in self.tasks if t.status == AgentStatus.FAILED)

        console.print(f"\n[bold]Results:[/bold] {completed}/{self.agent_count} completed, {failed} failed")

    def _run_simple(self, mode_str: str):
        """Run without Rich UI."""
        print(f"\n🎼 Maestro Orchestrator{mode_str}")
        print(f"Session: {self.session_id[:8]}")
        print(f"Spawning {self.agent_count} agents...\n")

        with ThreadPoolExecutor(max_workers=self.agent_count) as executor:
            futures = {executor.submit(task.execute, self.test_mode): task for task in self.tasks}

            for future in as_completed(futures):
                task = futures[future]
                try:
                    task = future.result()
                    status = "✅" if task.status == AgentStatus.COMPLETED else "❌"
                    print(f"{status} {task.name}: {task.status.value}")
                except Exception as e:
                    print(f"❌ {task.name}: error - {e}")

                self.save_state()

    def synthesize(self):
        """Create synthesis report with all agent findings."""
        debug_log("Synthesis: starting")

        elapsed = datetime.now() - self.start_time if self.start_time else None
        elapsed_str = str(elapsed).split('.')[0] if elapsed else "unknown"

        # Build report
        report_lines = [
            "# Parallel Agents Synthesis Report",
            "",
            f"**Session ID**: `{self.session_id}`",
            f"**Objective**: {self.main_prompt}",
            f"**Duration**: {elapsed_str}",
            f"**Agents**: {self.agent_count}",
            "",
            "---",
            "",
            "## Agent Results",
            ""
        ]

        for task in self.tasks:
            status_emoji = "✅" if task.status == AgentStatus.COMPLETED else "❌"
            report_lines.extend([
                f"### {task.name} {status_emoji}",
                "",
                f"- **Status**: {task.status.value}",
                f"- **Attempts**: {task.attempt}",
                "",
                "**Output:**",
                "```",
                task.result[:1000] if task.result else "(no output)",
                "```",
                ""
            ])

            if task.error:
                report_lines.extend([
                    "**Error:**",
                    f"```",
                    task.error[:500],
                    "```",
                    ""
                ])

            report_lines.append("---\n")

        # Add shared messages/findings
        findings = self.message_board.get_findings()
        if findings:
            report_lines.extend([
                "## Shared Findings",
                "",
            ])
            for f in findings:
                report_lines.append(f"- **{f.from_agent}**: {f.content}")
            report_lines.append("")

        # Save report
        reports_dir = DATA_DIR / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"synthesis_{self.session_id[:8]}.md"
        report_file.write_text("\n".join(report_lines), encoding="utf-8")

        if RICH_AVAILABLE and console:
            console.print(Panel(
                f"Report saved to:\n[cyan]{report_file}[/cyan]",
                title="✨ Synthesis Complete",
                border_style="green"
            ))
        else:
            print(f"\n✨ Report saved: {report_file}")

        debug_log(f"Synthesis report saved: {report_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Parallel Agent Orchestrator")
    parser.add_argument("prompt", help="Main task/prompt for agents")
    parser.add_argument("--agents", "-a", type=int, default=3, help="Number of agents (default: 3)")
    parser.add_argument("--retries", "-r", type=int, default=2, help="Max retries per agent (default: 2)")
    parser.add_argument("--test", "-t", action="store_true", help="Test mode with mock execution")

    args = parser.parse_args()

    debug_log(f"MAIN: prompt={args.prompt[:50]}..., agents={args.agents}, test={args.test}")

    try:
        orchestrator = Orchestrator(
            args.prompt,
            args.agents,
            test_mode=args.test,
            max_retries=args.retries
        )
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Orchestration cancelled by user")
    except Exception as e:
        debug_log(f"ORCHESTRATOR ERROR: {type(e).__name__}: {e}")
        import traceback
        debug_log(f"TRACEBACK: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
