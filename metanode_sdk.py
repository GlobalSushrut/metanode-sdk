#!/usr/bin/env python3
"""
MetaNode SDK - Main Entry Point

A complete console-based blockchain infrastructure SDK for federated
computing. This script provides access to all MetaNode components.
"""

import os
import sys
import typer
import logging
from rich.console import Console
from rich import print
from typing import Optional

# MetaNode components
from metanode.cli import app as cli_app
from metanode.wallet.cli import app as wallet_app
from metanode.mining.console import main as mining_main
from metanode.cloud.cli import app as cloud_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode-sdk")

# Create main app
app = typer.Typer(help="MetaNode SDK - Quantum-Federated Blockchain Infrastructure")
console = Console()

# Add subcommands
app.add_typer(cli_app, name="deploy", help="Deploy and manage applications on MetaNode")
app.add_typer(wallet_app, name="wallet", help="Manage MetaNode wallets and tokens")
app.add_typer(cloud_app, name="cloud", help="Manage cloud infrastructure for MetaNode")

@app.command()
def version():
    """Display version information for the MetaNode SDK"""
    print("[bold blue]MetaNode SDK[/bold blue] v1.0.0-beta")
    print("Quantum-Federated Blockchain Infrastructure")
    print("© 2023 MetaNode Foundation")

@app.command()
def mining():
    """Launch the MetaNode mining console"""
    print("[bold blue]Starting MetaNode Mining Console...[/]")
    mining_main()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Main entry point for the MetaNode SDK"""
    # Show help if no command was provided
    if ctx.invoked_subcommand is None:
        print("\n[bold]Welcome to [blue]MetaNode SDK[/blue] v1.0.0-beta[/bold]")
        print("[italic]The next-generation blockchain infrastructure for federated computing[/italic]\n")
        print("Available components:")
        print("  [bold]deploy[/bold]  - Deploy and manage applications on MetaNode")
        print("  [bold]wallet[/bold]  - Manage MetaNode wallets and tokens")
        print("  [bold]mining[/bold]  - Contribute resources and earn tokens")
        print("  [bold]cloud[/bold]   - Deploy and manage cloud infrastructure")
        print("\nRun [bold]metanode --help[/bold] for more information")

if __name__ == "__main__":
    app()
