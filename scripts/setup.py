#!/usr/bin/env python3
"""
Maestro Setup - Cross-platform installer with interactive TUI.

Usage:
    python setup.py              # Interactive mode
    python setup.py --quick      # Quick install (no prompts)
    python setup.py --uninstall  # Remove installation
    python setup.py --verify     # Verify installation
"""

import os
import sys
import shutil
import platform
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Check for Rich library
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.prompt import Confirm, Prompt
    from rich.tree import Tree
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Initialize console
console = Console() if RICH_AVAILABLE else None


def print_msg(msg: str, style: str = ""):
    """Print message with optional styling."""
    if RICH_AVAILABLE and console:
        console.print(msg, style=style)
    else:
        print(msg)


def print_error(msg: str):
    """Print error message."""
    print_msg(f"[red]Error:[/red] {msg}" if RICH_AVAILABLE else f"Error: {msg}")


def print_success(msg: str):
    """Print success message."""
    print_msg(f"[green]{msg}[/green]" if RICH_AVAILABLE else msg)


def print_warning(msg: str):
    """Print warning message."""
    print_msg(f"[yellow]Warning:[/yellow] {msg}" if RICH_AVAILABLE else f"Warning: {msg}")


def get_claude_dir() -> Path:
    """Get the .claude directory path based on OS."""
    if platform.system() == "Windows":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return Path(base) / ".claude"


def get_settings_source(repo_dir: Path) -> Path:
    """Get the appropriate settings file based on OS."""
    if platform.system() == "Windows":
        return repo_dir / "settings.example.windows.json"
    else:
        return repo_dir / "settings.example.unix.json"


def get_all_scripts() -> List[str]:
    """Get list of all script files to install."""
    return [
        "session_hooks.py",
        "explorer_helper.py",
        "dependency_scanner.py",
        "auto_preview.py",
        "parallel_orchestrator.py",
        "session_manager.py",
    ]


def show_banner():
    """Show welcome banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   🎼  M A E S T R O                                          ║
    ║                                                               ║
    ║   AI Development Orchestrator for Claude Code                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """

    if RICH_AVAILABLE and console:
        console.print(Panel.fit(
            "[bold cyan]🎼 MAESTRO[/bold cyan]\n\n"
            "[dim]AI Development Orchestrator for Claude Code[/dim]\n\n"
            f"Platform: [green]{platform.system()}[/green] ({platform.machine()})",
            border_style="cyan"
        ))
    else:
        print(banner)
        print(f"Platform: {platform.system()} ({platform.machine()})")


def show_features():
    """Show features table."""
    if not RICH_AVAILABLE:
        print("\nFeatures:")
        print("  - 15 Specialized Agents")
        print("  - 40+ Skills & Patterns")
        print("  - Token Usage Tracking")
        print("  - Error Learning System")
        print("  - Smart Commit Messages")
        return

    table = Table(title="What Gets Installed", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Count", justify="right", style="green")

    table.add_row("Scripts", "Automation hooks & utilities", "8")
    table.add_row("Agents", "Specialized AI personas", "17")
    table.add_row("Skills", "Knowledge resources & patterns", "40")
    table.add_row("Commands", "Slash commands for Claude", "9")
    table.add_row("Templates", "Project scaffolds", "12")

    console.print(table)


def show_what_will_be_installed(repo_dir: Path, claude_dir: Path):
    """Show installation preview."""
    if not RICH_AVAILABLE:
        print(f"\nInstallation Preview:")
        print(f"  From: {repo_dir}")
        print(f"  To:   {claude_dir}")
        return

    tree = Tree(f"[bold]📁 {claude_dir}[/bold]")

    scripts = tree.add("📂 scripts/")
    for script in get_all_scripts():
        scripts.add(f"📄 {script}")

    data = tree.add("📂 data/")
    data.add("📂 projects/")
    data.add("📂 reports/")

    tree.add("📄 settings.json")

    console.print("\n[bold]Installation Preview:[/bold]")
    console.print(tree)


def setup_scripts(repo_dir: Path, claude_dir: Path, progress=None) -> Dict[str, bool]:
    """Copy scripts to ~/.claude/scripts/"""
    scripts_src = repo_dir / "scripts"
    scripts_dst = claude_dir / "scripts"
    scripts_dst.mkdir(parents=True, exist_ok=True)

    results = {}
    scripts = get_all_scripts()

    for i, script in enumerate(scripts):
        src = scripts_src / script
        dst = scripts_dst / script

        if src.exists():
            shutil.copy2(src, dst)
            results[script] = True
        else:
            results[script] = False

        if progress:
            progress.update(progress.task_ids[0], advance=1)

    return results


def setup_settings(repo_dir: Path, claude_dir: Path) -> bool:
    """Copy the appropriate settings file."""
    src = get_settings_source(repo_dir)
    dst = claude_dir / "settings.json"

    # Backup existing
    if dst.exists():
        backup = claude_dir / "settings.json.backup"
        shutil.copy2(dst, backup)
        print_warning(f"Backed up existing settings to: settings.json.backup")

    if src.exists():
        shutil.copy2(src, dst)
        return True

    return False


def setup_data_dir(claude_dir: Path) -> None:
    """Create data directory structure."""
    data_dir = claude_dir / "data"
    subdirs = ["projects", "reports"]

    for subdir in subdirs:
        (data_dir / subdir).mkdir(parents=True, exist_ok=True)


def verify_installation(claude_dir: Path) -> Dict[str, Any]:
    """Verify installation status."""
    results = {
        "scripts": {},
        "settings": False,
        "data_dir": False,
        "overall": False
    }

    scripts_dir = claude_dir / "scripts"
    for script in get_all_scripts():
        results["scripts"][script] = (scripts_dir / script).exists()

    results["settings"] = (claude_dir / "settings.json").exists()
    results["data_dir"] = (claude_dir / "data").exists()
    results["overall"] = (
        all(results["scripts"].values()) and
        results["settings"] and
        results["data_dir"]
    )

    return results


def show_verification(results: Dict[str, Any]):
    """Display verification results."""
    if not RICH_AVAILABLE:
        print("\nVerification Results:")
        print(f"  Settings: {'OK' if results['settings'] else 'MISSING'}")
        print(f"  Data Dir: {'OK' if results['data_dir'] else 'MISSING'}")
        print(f"  Scripts:")
        for script, ok in results["scripts"].items():
            print(f"    {script}: {'OK' if ok else 'MISSING'}")
        return

    table = Table(title="Installation Verification", show_header=True)
    table.add_column("Component", style="cyan")
    table.add_column("Status", justify="center")

    # Settings
    status = "[green]✓ OK[/green]" if results["settings"] else "[red]✗ Missing[/red]"
    table.add_row("settings.json", status)

    # Data dir
    status = "[green]✓ OK[/green]" if results["data_dir"] else "[red]✗ Missing[/red]"
    table.add_row("data/", status)

    # Scripts
    for script, ok in results["scripts"].items():
        status = "[green]✓ OK[/green]" if ok else "[red]✗ Missing[/red]"
        table.add_row(f"scripts/{script}", status)

    console.print(table)

    if results["overall"]:
        console.print("\n[bold green]✓ Installation verified successfully![/bold green]")
    else:
        console.print("\n[bold red]✗ Some components are missing. Run setup again.[/bold red]")


def uninstall(claude_dir: Path) -> None:
    """Remove Maestro installation."""
    scripts_dir = claude_dir / "scripts"
    settings_file = claude_dir / "settings.json"

    if scripts_dir.exists():
        shutil.rmtree(scripts_dir)
        print_success("Removed scripts directory")

    if settings_file.exists():
        settings_file.unlink()
        print_success("Removed settings.json")

    print_warning("Data directory preserved at: ~/.claude/data/")


def run_interactive_setup(repo_dir: Path, claude_dir: Path):
    """Run interactive setup with prompts."""
    show_banner()
    print()
    show_features()
    print()
    show_what_will_be_installed(repo_dir, claude_dir)
    print()

    # Confirm installation
    if RICH_AVAILABLE:
        proceed = Confirm.ask("Proceed with installation?", default=True)
    else:
        response = input("Proceed with installation? [Y/n]: ").strip().lower()
        proceed = response in ("", "y", "yes")

    if not proceed:
        print_msg("Installation cancelled.")
        return

    print()

    # Install with progress
    if RICH_AVAILABLE:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("Installing scripts...", total=len(get_all_scripts()))
            results = setup_scripts(repo_dir, claude_dir, progress)

        print()

        # Show results
        failed = [s for s, ok in results.items() if not ok]
        if failed:
            print_warning(f"Some scripts not found: {', '.join(failed)}")
        else:
            print_success("All scripts installed successfully!")

    else:
        print("Installing scripts...")
        results = setup_scripts(repo_dir, claude_dir)
        for script, ok in results.items():
            status = "OK" if ok else "MISSING"
            print(f"  {script}: {status}")

    # Settings
    print_msg("\nInstalling settings...")
    if setup_settings(repo_dir, claude_dir):
        print_success("Settings installed!")
    else:
        print_error("Failed to install settings!")
        return

    # Data directories
    print_msg("\nCreating data directories...")
    setup_data_dir(claude_dir)
    print_success("Data directories created!")

    # Final message
    print()
    if RICH_AVAILABLE:
        console.print(Panel(
            "[bold green]Installation Complete![/bold green]\n\n"
            "[dim]Next steps:[/dim]\n"
            "  1. Restart Claude Code CLI\n"
            "  2. Run [cyan]claude --debug[/cyan] to verify hooks\n"
            "  3. Run [cyan]make verify[/cyan] to check installation",
            title="Success",
            border_style="green"
        ))
    else:
        print("=" * 50)
        print("Installation Complete!")
        print()
        print("Next steps:")
        print("  1. Restart Claude Code CLI")
        print("  2. Run 'claude --debug' to verify hooks")
        print("  3. Run 'make verify' to check installation")
        print("=" * 50)


def run_quick_setup(repo_dir: Path, claude_dir: Path):
    """Run quick setup without prompts."""
    print_msg("Running quick installation...")
    print()

    setup_scripts(repo_dir, claude_dir)
    print_success("Scripts installed")

    setup_settings(repo_dir, claude_dir)
    print_success("Settings installed")

    setup_data_dir(claude_dir)
    print_success("Data directories created")

    print()
    print_success("Installation complete!")


def main():
    parser = argparse.ArgumentParser(description="Maestro Setup")
    parser.add_argument("--quick", "-q", action="store_true", help="Quick install without prompts")
    parser.add_argument("--uninstall", "-u", action="store_true", help="Uninstall Maestro")
    parser.add_argument("--verify", "-v", action="store_true", help="Verify installation")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode (default)")
    args = parser.parse_args()

    # Detect repo directory
    script_path = Path(__file__).resolve()
    repo_dir = script_path.parent.parent

    if not (repo_dir / "agents").exists():
        print_error(f"Could not find repo root at {repo_dir}")
        sys.exit(1)

    claude_dir = get_claude_dir()

    if args.uninstall:
        print_msg("Uninstalling Maestro...")
        uninstall(claude_dir)
        return

    if args.verify:
        show_banner()
        print()
        results = verify_installation(claude_dir)
        show_verification(results)
        sys.exit(0 if results["overall"] else 1)

    if args.quick:
        run_quick_setup(repo_dir, claude_dir)
    else:
        run_interactive_setup(repo_dir, claude_dir)


if __name__ == "__main__":
    main()
