#!/usr/bin/env python3
"""
MetaNode Simple Example Application

This example demonstrates how to create a simple federated application
using the MetaNode SDK. It shows wallet creation, resource allocation,
deployment, and result retrieval through the console-based CLI.
"""

import os
import sys
import json
import time
import logging
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode-example")

# Rich console for pretty output
console = Console()

# Application name
APP_NAME = "MetaNode Federated Calculator"

def check_sdk_installed():
    """Check if MetaNode SDK is installed"""
    console.print("[yellow]Checking MetaNode SDK installation...[/]")
    
    try:
        # Try to import metanode
        import metanode
        console.print(f"[green]✓[/] MetaNode SDK v{metanode.__version__} found")
        return True
    except ImportError:
        console.print("[red]✗[/] MetaNode SDK not found")
        console.print("\n[bold yellow]Installing MetaNode SDK from current directory...[/]")
        
        # Try to install SDK
        result = subprocess.run(
            ["pip", "install", "-e", "."],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print("[green]✓[/] MetaNode SDK installed successfully")
            return True
        else:
            console.print(f"[red]✗[/] Failed to install MetaNode SDK: {result.stderr}")
            return False

def create_wallet():
    """Create a MetaNode wallet for the application"""
    console.print("\n[bold blue]Creating MetaNode Wallet[/]")
    
    # Generate wallet password
    password = "example123"  # In production, use a secure password
    
    # Create wallet directory
    wallet_dir = os.path.expanduser("~/.metanode/wallets")
    os.makedirs(wallet_dir, exist_ok=True)
    
    # Check if example wallet already exists
    example_wallet = next((f for f in os.listdir(wallet_dir) 
                          if f.startswith("wallet_example")), None)
    
    if example_wallet:
        wallet_id = example_wallet.split(".")[0]
        console.print(f"[green]✓[/] Using existing wallet: {wallet_id}")
        return wallet_id
    
    # Create wallet using metanode CLI
    console.print("[yellow]Creating new wallet for the example...[/]")
    
    result = subprocess.run(
        ["python", "-m", "metanode.wallet.cli", "create"],
        input=f"{password}\n{password}\n",
        capture_output=True,
        text=True
    )
    
    if "Wallet created successfully" in result.stdout:
        # Extract wallet ID from output
        wallet_id = next((line.split(": ")[1] for line in result.stdout.split("\n") 
                         if "Wallet ID:" in line), None)
        
        if wallet_id:
            console.print(f"[green]✓[/] Wallet created: {wallet_id}")
            
            # Rename wallet file to make it easier to find
            old_path = os.path.join(wallet_dir, f"{wallet_id}.json")
            new_path = os.path.join(wallet_dir, f"wallet_example.json")
            
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                console.print("[green]✓[/] Wallet saved as example wallet")
            
            return wallet_id
    
    console.print("[red]✗[/] Failed to create wallet")
    return None

def start_mining():
    """Start mining to earn tokens and contribute resources"""
    console.print("\n[bold blue]Starting Mining Console[/]")
    
    # Create mining data directory
    mining_dir = os.path.expanduser("~/.metanode/mining")
    os.makedirs(mining_dir, exist_ok=True)
    
    console.print("[yellow]Starting mining process (non-blocking)...[/]")
    
    # Start mining in the background with minimal resources
    mining_process = subprocess.Popen(
        ["python", "-m", "metanode.mining.console", "start", 
         "--compute", "0.5", "--storage", "1.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )
    
    # Wait a moment to allow mining to start
    time.sleep(2)
    
    # Check if mining process is running
    if mining_process.poll() is None:
        console.print("[green]✓[/] Mining started successfully")
        return mining_process
    else:
        console.print("[red]✗[/] Failed to start mining")
        return None

def create_app_config():
    """Create a configuration for the sample application"""
    console.print("\n[bold blue]Creating Application Configuration[/]")
    
    # Create app config directory
    config_dir = os.path.expanduser("~/.metanode/apps")
    os.makedirs(config_dir, exist_ok=True)
    
    # Create example config file
    config_path = os.path.join(config_dir, "calculator_app.json")
    
    config = {
        "name": APP_NAME,
        "version": "1.0.0",
        "description": "A simple federated calculator application",
        "author": "MetaNode Example",
        "resources": {
            "compute": 1.0,
            "memory": "256Mi",
            "storage": "50Mi"
        },
        "federated": {
            "algorithm": "secure-aggregation",
            "min_peers": 3,
            "timeout": 60
        },
        "security": {
            "use_zk_proofs": True,
            "encrypt_data": True,
            "verify_computation": True
        },
        "runtime": {
            "image": "metanode/federated-py:1.0",
            "entrypoint": "python main.py",
            "environment": {
                "METANODE_ENV": "production",
                "LOG_LEVEL": "info"
            }
        }
    }
    
    # Save config to file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    console.print(f"[green]✓[/] Created application config: {config_path}")
    return config_path

def deploy_application(config_path):
    """Deploy the application to the MetaNode network"""
    console.print("\n[bold blue]Deploying Application[/]")
    
    console.print("[yellow]Deploying to MetaNode mainnet...[/]")
    
    # Use metanode CLI to deploy the app
    result = subprocess.run(
        ["python", "-m", "metanode.cli", "deploy", config_path],
        capture_output=True,
        text=True
    )
    
    if "deployed successfully" in result.stdout:
        # Extract deployment ID from output
        deployment_id = next((line.split(": ")[1] for line in result.stdout.split("\n") 
                             if "Deployment ID:" in line), None)
        
        if deployment_id:
            console.print(f"[green]✓[/] Application deployed: {deployment_id}")
            return deployment_id
    
    console.print("[red]✗[/] Failed to deploy application")
    return None

def check_deployment_status(deployment_id):
    """Check the status of the deployed application"""
    console.print("\n[bold blue]Checking Deployment Status[/]")
    
    # Use metanode CLI to check deployment status
    result = subprocess.run(
        ["python", "-m", "metanode.cli", "status", deployment_id],
        capture_output=True,
        text=True
    )
    
    if deployment_id in result.stdout:
        console.print("[green]✓[/] Deployment is active")
        
        # Display information from output
        status_lines = [line for line in result.stdout.split("\n") if ":" in line]
        
        table = Table(title="Deployment Status")
        table.add_column("Property")
        table.add_column("Value")
        
        for line in status_lines:
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    table.add_row(key, value)
        
        console.print(table)
        return True
    
    console.print("[red]✗[/] Deployment not found or inactive")
    return False

def run_calculation():
    """Simulate running a calculation on the deployed application"""
    console.print("\n[bold blue]Running Calculation[/]")
    
    # Simulate a federated calculation
    console.print("[yellow]Submitting calculation to federated nodes...[/]")
    
    # In a real implementation, this would use the actual SDK APIs
    # For this example, we'll simulate the operation
    
    operations = [
        {"op": "add", "x": 5, "y": 10},
        {"op": "multiply", "x": 7, "y": 8},
        {"op": "divide", "x": 100, "y": 4}
    ]
    
    # Display calculation table
    table = Table(title=f"{APP_NAME} - Calculations")
    table.add_column("Operation")
    table.add_column("Values")
    table.add_column("Result")
    table.add_column("Proof")
    
    for op in operations:
        operation = op["op"]
        x, y = op["x"], op["y"]
        
        # Calculate result
        if operation == "add":
            result = x + y
        elif operation == "subtract":
            result = x - y
        elif operation == "multiply":
            result = x * y
        elif operation == "divide":
            result = x / y if y != 0 else "Error: Division by zero"
        else:
            result = "Error: Unknown operation"
        
        # Generate simulated proof ID
        proof_id = f"zk_{operation}_{x}_{y}_{hash(str(result)) % 10000:04d}"
        
        table.add_row(
            operation,
            f"{x}, {y}",
            str(result),
            proof_id
        )
    
    console.print(table)
    
    # In a real implementation, this would receive real verified results
    return {
        "operations": len(operations),
        "successful": len(operations),
        "results": [
            {"operation": "add", "result": 15, "verified": True},
            {"operation": "multiply", "result": 56, "verified": True},
            {"operation": "divide", "result": 25, "verified": True}
        ]
    }

def stop_mining(mining_process):
    """Stop the mining process"""
    console.print("\n[bold blue]Stopping Mining[/]")
    
    if mining_process and mining_process.poll() is None:
        console.print("[yellow]Stopping mining process...[/]")
        
        # Send Ctrl+C to the process
        mining_process.terminate()
        
        # Wait for process to terminate
        try:
            mining_process.wait(timeout=5)
            console.print("[green]✓[/] Mining stopped successfully")
        except subprocess.TimeoutExpired:
            console.print("[yellow]Mining process not responding, forcing termination...")
            mining_process.kill()
            console.print("[green]✓[/] Mining terminated")
    else:
        console.print("[yellow]Mining process was not running")

def main():
    """Main function to run the example"""
    console.print(Panel.fit(
        "[bold blue]MetaNode SDK Example Application[/]\n"
        "This example demonstrates a simple federated computing application",
        title="Welcome",
        subtitle="v1.0.0-beta"
    ))
    
    # Check SDK installation
    if not check_sdk_installed():
        console.print("[bold red]Cannot continue without MetaNode SDK[/]")
        return
    
    # Create wallet
    wallet_id = create_wallet()
    if not wallet_id:
        console.print("[bold red]Cannot continue without wallet[/]")
        return
    
    # Start mining
    mining_process = start_mining()
    
    try:
        # Create app config
        config_path = create_app_config()
        
        # Deploy application
        deployment_id = deploy_application(config_path)
        if not deployment_id:
            console.print("[bold red]Deployment failed, cannot continue[/]")
            return
        
        # Check deployment status
        check_deployment_status(deployment_id)
        
        # Run calculation
        results = run_calculation()
        
        # Display final summary
        console.print("\n[bold green]Example completed successfully![/]")
        console.print(Panel.fit(
            f"[bold]Application[/]: {APP_NAME}\n"
            f"[bold]Wallet[/]: {wallet_id}\n"
            f"[bold]Deployment[/]: {deployment_id}\n"
            f"[bold]Operations[/]: {results['operations']}\n"
            f"[bold]Successful[/]: {results['successful']}\n",
            title="Summary",
            border_style="green"
        ))
        
    finally:
        # Always stop mining when done
        if mining_process:
            stop_mining(mining_process)

if __name__ == "__main__":
    main()
