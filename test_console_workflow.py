#!/usr/bin/env python3
"""
MetaNode SDK Console Workflow Test

This script tests the console-based workflow for all MetaNode SDK components,
ensuring that everything works properly without UI dependencies.
"""

import os
import sys
import json
import time
import subprocess
import logging
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode-test")

# Rich console for pretty output
console = Console()

class TestRunner:
    """Test runner for MetaNode SDK console workflow"""
    
    def __init__(self):
        """Initialize test runner"""
        self.test_wallet_id = None
        self.test_deployment_id = None
        self.test_cluster_id = None
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run_command(self, command, input_text=None, expected_output=None, description=None):
        """Run a command and check if expected output is in the result"""
        if description:
            console.print(f"[yellow]Test:[/] {description}")
        
        console.print(f"[dim]$ {' '.join(command)}[/]")
        
        # Handle input text properly - if it's already bytes don't encode it again
        input_data = None
        if input_text is not None:
            if isinstance(input_text, bytes):
                input_data = input_text
            else:
                input_data = input_text.encode()
        
        result = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True
        )
        
        # Check if command succeeded
        if result.returncode != 0:
            console.print(f"[red]✗[/] Command failed with exit code {result.returncode}")
            console.print(f"[red]Error:[/] {result.stderr}")
            self.tests_failed += 1
            return False, result
        
        # Check if expected output is in the result
        if expected_output and expected_output not in result.stdout:
            console.print(f"[red]✗[/] Expected output not found: '{expected_output}'")
            self.tests_failed += 1
            return False, result
        
        # Test passed
        if description:
            console.print(f"[green]✓[/] Test passed: {description}")
        self.tests_passed += 1
        return True, result
    
    def setup(self):
        """Setup test environment"""
        console.print(Panel.fit(
            "[bold blue]MetaNode SDK Console Workflow Test[/]\n"
            "Testing all components function properly without UI dependencies",
            title="Test Suite",
            subtitle="v1.0.0-beta"
        ))
        
        # Create test directories
        os.makedirs(os.path.expanduser("~/.metanode/test"), exist_ok=True)
        
        # Check if SDK is installed
        try:
            # Try to import metanode to check installation
            import metanode
            console.print(f"[green]✓[/] MetaNode SDK v{metanode.__version__} found")
        except ImportError:
            console.print("[yellow]MetaNode SDK not found, attempting to install...[/]")
            
            # Try to install SDK
            success, _ = self.run_command(
                ["pip3", "install", "-e", "."],
                expected_output=None,
                description="Install MetaNode SDK"
            )
            
            if not success:
                console.print("[bold red]Cannot continue without MetaNode SDK[/]")
                return False
        
        return True
    
    def test_wallet_cli(self):
        """Test wallet CLI functionality"""
        console.print("\n[bold blue]Testing Wallet CLI[/]")
        
        # Create wallet
        password = "test123\ntest123\n"
        success, result = self.run_command(
            ["python3", "-m", "metanode.wallet.cli", "create"],
            input_text=password,
            expected_output="Wallet created successfully",
            description="Create wallet"
        )
        
        if not success:
            return False
        
        # Extract wallet ID
        for line in result.stdout.split("\n"):
            if "Wallet ID:" in line:
                self.test_wallet_id = line.split(": ")[1].strip()
                break
        
        if not self.test_wallet_id:
            console.print("[red]✗[/] Could not extract wallet ID")
            self.tests_failed += 1
            return False
        
        console.print(f"[green]Created test wallet: {self.test_wallet_id}[/]")
        
        # List wallets
        success, _ = self.run_command(
            ["python3", "-m", "metanode.wallet.cli", "list"],
            expected_output=self.test_wallet_id,
            description="List wallets"
        )
        
        # Load wallet
        success, _ = self.run_command(
            ["python3", "-m", "metanode.wallet.cli", "load", self.test_wallet_id],
            input_text="test123\n",
            expected_output="Wallet loaded successfully",
            description="Load wallet"
        )
        
        # Check balance
        success, _ = self.run_command(
            ["python3", "-m", "metanode.wallet.cli", "balance"],
            expected_output="Current Balance:",
            description="Check wallet balance"
        )
        
        return True
    
    def test_mining_console(self):
        """Test mining console functionality"""
        console.print("\n[bold blue]Testing Mining Console[/]")
        
        # Start mining in the background
        mining_process = subprocess.Popen(
            ["python3", "-m", "metanode.mining.console", "start", 
             "--compute", "0.5", "--storage", "1.0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        
        # Wait a moment to ensure mining starts
        time.sleep(2)
        
        # Check if process is running
        if mining_process.poll() is not None:
            console.print("[red]✗[/] Mining process failed to start")
            self.tests_failed += 1
            return False
        
        console.print("[green]✓[/] Mining process started")
        self.tests_passed += 1
        
        # Check mining stats
        success, _ = self.run_command(
            ["python3", "-m", "metanode.mining.console", "stats"],
            expected_output="MetaNode Mining Statistics",
            description="Check mining statistics"
        )
        
        # Mine a block manually
        success, _ = self.run_command(
            ["python3", "-m", "metanode.mining.console", "mine"],
            expected_output=None,  # Don't check output as it might vary
            description="Mine a block manually"
        )
        
        # Terminate mining process
        try:
            mining_process.terminate()
            mining_process.wait(timeout=5)
            console.print("[green]✓[/] Mining process terminated")
            self.tests_passed += 1
        except subprocess.TimeoutExpired:
            mining_process.kill()
            console.print("[yellow]Mining process killed")
        
        return True
    
    def test_application_deployment(self):
        """Test application deployment functionality"""
        console.print("\n[bold blue]Testing Application Deployment[/]")
        
        # Create test config directory
        config_dir = os.path.expanduser("~/.metanode/apps")
        os.makedirs(config_dir, exist_ok=True)
        
        # Create test config file
        config_path = os.path.join(config_dir, "test_app.json")
        
        config = {
            "name": "TestApp",
            "version": "1.0.0",
            "description": "Test application for MetaNode SDK",
            "author": "MetaNode Test Suite",
            "resources": {
                "compute": 0.5,
                "memory": "128Mi",
                "storage": "10Mi"
            },
            "federated": {
                "algorithm": "secure-aggregation",
                "min_peers": 2,
                "timeout": 30
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
                    "METANODE_ENV": "test",
                    "LOG_LEVEL": "debug"
                }
            }
        }
        
        # Save config to file
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        console.print(f"[green]✓[/] Created test app config: {config_path}")
        self.tests_passed += 1
        
        # Deploy application
        success, result = self.run_command(
            ["python3", "-m", "metanode.cli", "deploy", config_path],
            expected_output="deployed successfully",
            description="Deploy test application"
        )
        
        if not success:
            return False
        
        # Extract deployment ID
        for line in result.stdout.split("\n"):
            if "Deployment ID:" in line:
                self.test_deployment_id = line.split(": ")[1].strip()
                break
        
        if not self.test_deployment_id:
            console.print("[red]✗[/] Could not extract deployment ID")
            self.tests_failed += 1
            return False
        
        console.print(f"[green]Created test deployment: {self.test_deployment_id}[/]")
        
        # Check deployment status
        success, _ = self.run_command(
            ["python3", "-m", "metanode.cli", "status", self.test_deployment_id],
            expected_output=self.test_deployment_id,
            description="Check deployment status"
        )
        
        # Check mainnet status
        success, _ = self.run_command(
            ["python3", "-m", "metanode.cli", "mainnet-status"],
            expected_output="MetaNode Mainnet Status",
            description="Check mainnet status"
        )
        
        return True
    
    def test_cloud_management(self):
        """Test cloud management functionality"""
        console.print("\n[bold blue]Testing Cloud Management[/]")
        
        # Create cloud config directory
        cloud_dir = os.path.expanduser("~/.metanode/cloud")
        os.makedirs(cloud_dir, exist_ok=True)
        
        # Create a test cluster
        cluster_name = f"test-cluster-{int(time.time())}"
        success, result = self.run_command(
            ["python3", "-m", "metanode.cloud.cli", "create",
             "--name", cluster_name,
             "--provider", "aws",
             "--region", "us-east-1",
             "--nodes", "2",
             "--node-type", "t3.medium"],
            input_text="y\n",  # Confirm creation
            expected_output="Cluster created successfully",
            description="Create test cluster"
        )
        
        if not success:
            return False
        
        # Extract cluster ID
        for line in result.stdout.split("\n"):
            if "Cluster ID:" in line:
                self.test_cluster_id = line.split(": ")[1].strip()
                break
        
        if not self.test_cluster_id:
            console.print("[red]✗[/] Could not extract cluster ID")
            self.tests_failed += 1
            return False
        
        console.print(f"[green]Created test cluster: {self.test_cluster_id}[/]")
        
        # List clusters
        success, _ = self.run_command(
            ["python3", "-m", "metanode.cloud.cli", "list"],
            expected_output=cluster_name,
            description="List clusters"
        )
        
        # Check cluster status
        success, _ = self.run_command(
            ["python3", "-m", "metanode.cloud.cli", "status", self.test_cluster_id],
            expected_output=cluster_name,
            description="Check cluster status"
        )
        
        # Scale cluster
        success, _ = self.run_command(
            ["python3", "-m", "metanode.cloud.cli", "scale", self.test_cluster_id, "--nodes", "3"],
            input_text="y\n",  # Confirm scaling
            expected_output="Scaling cluster",
            description="Scale cluster"
        )
        
        # Delete cluster
        success, _ = self.run_command(
            ["python3", "-m", "metanode.cloud.cli", "delete", self.test_cluster_id],
            input_text="y\n",  # Confirm deletion
            expected_output="deleted successfully",
            description="Delete cluster"
        )
        
        return True
    
    def test_sdk_integration(self):
        """Test SDK integration with all components"""
        console.print("\n[bold blue]Testing SDK Integration[/]")
        
        # Test metanode CLI version command
        success, _ = self.run_command(
            ["python3", "metanode_sdk.py", "version"],
            expected_output="MetaNode SDK",
            description="Check SDK version"
        )
        
        # Test main CLI with no arguments (should show help)
        success, _ = self.run_command(
            ["python3", "metanode_sdk.py"],
            expected_output="Welcome to MetaNode SDK",
            description="Check main CLI help"
        )
        
        return True
    
    def run_tests(self):
        """Run all tests"""
        if not self.setup():
            return False
        
        tests = [
            self.test_wallet_cli,
            self.test_mining_console,
            self.test_application_deployment,
            self.test_cloud_management,
            self.test_sdk_integration
        ]
        
        with Progress() as progress:
            task = progress.add_task("[green]Running tests...", total=len(tests))
            
            for test_func in tests:
                test_name = test_func.__name__.replace("test_", "").replace("_", " ").title()
                progress.update(task, description=f"[green]Testing {test_name}...")
                
                try:
                    test_func()
                except Exception as e:
                    console.print(f"[red]✗[/] Test {test_name} failed with exception: {e}")
                    self.tests_failed += 1
                
                progress.update(task, advance=1)
        
        # Display test results
        console.print(Panel.fit(
            f"[bold green]Tests passed:[/] {self.tests_passed}\n"
            f"[bold red]Tests failed:[/] {self.tests_failed}\n"
            f"[bold]Total tests:[/] {self.tests_passed + self.tests_failed}",
            title="Test Results",
            border_style="green" if self.tests_failed == 0 else "red"
        ))
        
        return self.tests_failed == 0

if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_tests()
    sys.exit(0 if success else 1)
