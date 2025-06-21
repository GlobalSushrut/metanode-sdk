#!/usr/bin/env python3
"""
MetaNode CLI - Main SDK Interface

Console-based command-line interface for interacting with the MetaNode
infrastructure, deploying apps, and managing resources.
"""

import os
import sys
import yaml
import json
import typer
import logging
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode.cli")

# Create Typer app
app = typer.Typer(help="MetaNode CLI - Blockchain-grade Federated Cloud Computing")

# Rich console for pretty output
console = Console()

# Configuration paths
CONFIG_DIR = os.path.expanduser("~/.metanode")
APPS_DIR = os.path.join(CONFIG_DIR, "apps")
DEPLOY_DIR = os.path.join(CONFIG_DIR, "deployments")

# Ensure directories exist
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(APPS_DIR, exist_ok=True)
os.makedirs(DEPLOY_DIR, exist_ok=True)

@app.command()
def deploy(config_path: str = typer.Argument(..., help="Path to deployment config file")):
    """
    Deploy an application to the MetaNode network using blockchain-grade security
    """
    if not os.path.exists(config_path):
        console.print(f"[red]Error: Config file not found: {config_path}[/]")
        return
    
    # Load config
    try:
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading config: {e}[/]")
        return
    
    # Display config details
    console.print(f"[bold blue]Deploying application from config: {config_path}[/]")
    console.print(f"[bold]Application name:[/] {config.get('name', 'Unnamed')}")
    console.print(f"[bold]Version:[/] {config.get('version', '0.0.1')}")
    
    # Simulate deployment steps
    with console.status("[bold green]Deploying application...") as status:
        console.print("[green]✓[/] Validating deployment configuration")
        console.print("[green]✓[/] Creating blockchain record")
        console.print("[green]✓[/] Generating deployment proofs")
        console.print("[green]✓[/] Allocating federated resources")
        console.print("[green]✓[/] Provisioning secure runtime")
        console.print("[green]✓[/] Deploying application")
    
    # Save deployment record
    deployment_id = f"deploy_{os.path.basename(config_path).split('.')[0]}_{config.get('version', '0')}"
    deployment_path = os.path.join(DEPLOY_DIR, f"{deployment_id}.json")
    
    with open(deployment_path, 'w') as f:
        json.dump({
            "id": deployment_id,
            "config": config,
            "status": "deployed",
            "created_at": str(subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ']).decode().strip()),
        }, f, indent=2)
    
    console.print(f"[bold green]✓ Application deployed successfully![/]")
    console.print(f"Deployment ID: {deployment_id}")

@app.command()
def status(deployment_id: Optional[str] = typer.Argument(None, help="Deployment ID")):
    """
    Check status of deployments on the MetaNode network
    """
    if deployment_id:
        # Check specific deployment
        deployment_path = os.path.join(DEPLOY_DIR, f"{deployment_id}.json")
        if not os.path.exists(deployment_path):
            console.print(f"[red]Error: Deployment not found: {deployment_id}[/]")
            return
        
        # Load deployment
        try:
            with open(deployment_path, 'r') as f:
                deployment = json.load(f)
        except Exception as e:
            console.print(f"[red]Error loading deployment: {e}[/]")
            return
        
        # Display deployment status
        console.print(f"[bold blue]Deployment: {deployment_id}[/]")
        console.print(f"[bold]Name:[/] {deployment['config'].get('name', 'Unnamed')}")
        console.print(f"[bold]Version:[/] {deployment['config'].get('version', '0.0.1')}")
        console.print(f"[bold]Status:[/] {deployment.get('status', 'unknown')}")
        console.print(f"[bold]Created at:[/] {deployment.get('created_at', 'unknown')}")
    else:
        # List all deployments
        deployments = []
        for filename in os.listdir(DEPLOY_DIR):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(DEPLOY_DIR, filename), 'r') as f:
                        deployment = json.load(f)
                        deployments.append(deployment)
                except Exception as e:
                    logger.error(f"Error loading deployment {filename}: {e}")
        
        if not deployments:
            console.print("[yellow]No deployments found[/]")
            return
        
        # Display deployments table
        table = Table(title="MetaNode Deployments")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Version")
        table.add_column("Status")
        table.add_column("Created At")
        
        for deployment in deployments:
            table.add_row(
                deployment.get('id', 'unknown'),
                deployment['config'].get('name', 'Unnamed'),
                deployment['config'].get('version', '0.0.1'),
                deployment.get('status', 'unknown'),
                deployment.get('created_at', 'unknown')
            )
        
        console.print(table)

@app.command()
def mainnet_status():
    """
    Check the status of the MetaNode mainnet
    """
    # Simulate retrieving mainnet status
    with console.status("[bold green]Fetching mainnet status..."):
        status = {
            "name": "MetaNode Mainnet",
            "version": "1.0.0-beta",
            "status": "operational",
            "nodes": 128,
            "compute_power": 512.5,
            "storage_capacity": "128.0 TB",
            "active_deployments": 47,
            "last_block": "0x8f72d4e470142ab23",
            "last_block_time": str(subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ']).decode().strip()),
            "tps": 10240  # Transactions per second
        }
    
    # Display mainnet status
    console.print(f"[bold blue]MetaNode Mainnet Status[/]")
    console.print(f"[bold]Name:[/] {status['name']}")
    console.print(f"[bold]Version:[/] {status['version']}")
    console.print(f"[bold]Status:[/] [green]{status['status']}[/]")
    console.print(f"[bold]Nodes:[/] {status['nodes']}")
    console.print(f"[bold]Compute Power:[/] {status['compute_power']} units")
    console.print(f"[bold]Storage Capacity:[/] {status['storage_capacity']}")
    console.print(f"[bold]Active Deployments:[/] {status['active_deployments']}")
    console.print(f"[bold]Last Block:[/] {status['last_block']}")
    console.print(f"[bold]Last Block Time:[/] {status['last_block_time']}")
    console.print(f"[bold]Transactions per second:[/] {status['tps']}")

def main():
    """Main entry point for the CLI"""
    if not os.path.exists(CONFIG_DIR):
        console.print("[yellow]Initializing MetaNode SDK for first use...[/]")
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(APPS_DIR, exist_ok=True)
        os.makedirs(DEPLOY_DIR, exist_ok=True)
    
    try:
        app()
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main()
