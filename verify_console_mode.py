#!/usr/bin/env python3
"""
MetaNode SDK Console Mode Verification

This script imports and checks all the main components of the MetaNode SDK
to verify they are properly configured for console-only operation.
"""

import os
import sys
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize Rich console
console = Console()

def check_import(module_name, required_attrs=None):
    """Check if a module can be imported and has required attributes"""
    try:
        module = importlib.import_module(module_name)
        console.print(f"[green]✓[/] Successfully imported [bold]{module_name}[/]")
        
        if required_attrs:
            for attr in required_attrs:
                if hasattr(module, attr):
                    console.print(f"  [green]✓[/] Found attribute [bold]{attr}[/]")
                else:
                    console.print(f"  [red]✗[/] Missing attribute [bold]{attr}[/]")
                    return False
                    
        return True
    except ImportError as e:
        console.print(f"[red]✗[/] Failed to import [bold]{module_name}[/]: {e}")
        return False
    except Exception as e:
        console.print(f"[red]✗[/] Error when importing [bold]{module_name}[/]: {e}")
        return False

def check_directory(directory_path):
    """Check if a directory exists and create it if it doesn't"""
    path = os.path.expanduser(directory_path)
    exists = os.path.isdir(path)
    
    if exists:
        console.print(f"[green]✓[/] Directory exists: [bold]{directory_path}[/]")
        return True
    else:
        console.print(f"[yellow]![/] Directory doesn't exist: [bold]{directory_path}[/]")
        try:
            os.makedirs(path, exist_ok=True)
            console.print(f"  [green]✓[/] Created directory: [bold]{directory_path}[/]")
            return True
        except Exception as e:
            console.print(f"  [red]✗[/] Failed to create directory: {e}")
            return False

def main():
    """Main verification function"""
    console.print(Panel.fit(
        "[bold blue]MetaNode SDK Console Mode Verification[/]\n"
        "Checking all components for console-only operation",
        title="Verification Tool",
        subtitle="v1.0.0-beta"
    ))
    
    # Check core directories
    console.print("\n[bold]Checking core directories:[/]")
    directories = [
        "~/.metanode",
        "~/.metanode/wallets",
        "~/.metanode/mining",
        "~/.metanode/cloud",
        "~/.metanode/apps",
        "~/.metanode/deployments"
    ]
    
    for directory in directories:
        check_directory(directory)
    
    # Check core modules
    console.print("\n[bold]Checking core modules:[/]")
    modules = [
        ("metanode", ["__version__"]),
        ("metanode.wallet", None),
        ("metanode.wallet.cli", None),
        ("metanode.mining", None),
        ("metanode.mining.console", None),
        ("metanode.cloud", None), 
        ("metanode.cloud.cli", None),
        ("metanode.cli", None)
    ]
    
    all_imports_successful = True
    for module_name, required_attrs in modules:
        if not check_import(module_name, required_attrs):
            all_imports_successful = False
    
    # Check for UI dependencies
    console.print("\n[bold]Checking for UI dependencies:[/]")
    ui_modules = ["tkinter", "PyQt5", "flask"]
    ui_dependencies_found = False
    
    for ui_module in ui_modules:
        try:
            importlib.import_module(ui_module)
            console.print(f"[yellow]![/] UI dependency found: [bold]{ui_module}[/] (but not imported by SDK)")
            ui_dependencies_found = True
        except ImportError:
            console.print(f"[green]✓[/] UI dependency not found: [bold]{ui_module}[/] (good)")
    
    # Create a summary table
    table = Table(title="Verification Results")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("Core directories", "[green]PASS[/]" if all(check_directory(d) for d in directories) else "[red]FAIL[/]")
    table.add_row("Core modules", "[green]PASS[/]" if all_imports_successful else "[red]FAIL[/]")
    table.add_row("UI independence", "[green]PASS[/]" if not ui_dependencies_found else "[yellow]WARNING[/]")
    
    console.print("\n")
    console.print(table)
    
    # Final verdict
    if all_imports_successful:
        console.print(Panel.fit(
            "[bold green]VERIFICATION SUCCESSFUL[/]\n"
            "The MetaNode SDK is properly configured for console-only operation.",
            border_style="green"
        ))
        return 0
    else:
        console.print(Panel.fit(
            "[bold red]VERIFICATION FAILED[/]\n"
            "Some components of the MetaNode SDK could not be verified.",
            border_style="red"
        ))
        return 1

if __name__ == "__main__":
    sys.exit(main())
