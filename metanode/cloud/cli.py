#!/usr/bin/env python3
"""
MetaNode Cloud CLI

Console-based cloud deployment tools for MetaNode mainnet infrastructure.
Supports provisioning, scaling, and managing cloud resources without UI dependencies.
"""

import os
import sys
import yaml
import json
import uuid
import typer
import logging
import subprocess
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("metanode.cloud")

# Create Typer app
app = typer.Typer(help="MetaNode Cloud - Deploy and Manage Infrastructure")

# Rich console for pretty output
console = Console()

# Configuration paths
CONFIG_DIR = os.path.expanduser("~/.metanode/cloud")
TEMPLATES_DIR = os.path.join(CONFIG_DIR, "templates")
CLUSTERS_DIR = os.path.join(CONFIG_DIR, "clusters")

# Ensure directories exist
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(CLUSTERS_DIR, exist_ok=True)

class CloudManager:
    """Manages cloud deployments for MetaNode infrastructure"""
    
    def __init__(self, config_dir: str = CONFIG_DIR):
        """Initialize cloud manager"""
        self.config_dir = config_dir
        self.clusters_file = os.path.join(self.config_dir, "clusters.json")
        self.clusters = self._load_clusters()
    
    def _load_clusters(self) -> Dict:
        """Load clusters data"""
        if os.path.exists(self.clusters_file):
            try:
                with open(self.clusters_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading clusters: {e}")
        
        # Initialize with empty data
        return {
            "clusters": [],
            "last_updated": 0
        }
    
    def _save_clusters(self) -> None:
        """Save clusters data"""
        try:
            with open(self.clusters_file, 'w') as f:
                json.dump(self.clusters, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving clusters: {e}")
    
    def create_cluster(self, name: str, cloud_provider: str, region: str, 
                      node_count: int, node_type: str) -> Dict:
        """Create a new cluster"""
        # Check if cluster name already exists
        for cluster in self.clusters["clusters"]:
            if cluster["name"] == name:
                raise ValueError(f"Cluster with name '{name}' already exists")
        
        # Generate cluster ID
        cluster_id = f"cluster_{uuid.uuid4().hex[:8]}"
        
        # Create cluster definition
        cluster = {
            "id": cluster_id,
            "name": name,
            "cloud_provider": cloud_provider,
            "region": region,
            "node_count": node_count,
            "node_type": node_type,
            "status": "creating",
            "created_at": subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ']).decode().strip(),
            "ipfs_gateway": f"https://ipfs-{cluster_id}.metanode.network",
            "api_endpoint": f"https://api-{cluster_id}.metanode.network"
        }
        
        # Add to clusters list
        self.clusters["clusters"].append(cluster)
        self.clusters["last_updated"] = subprocess.check_output(['date', '+%s']).decode().strip()
        self._save_clusters()
        
        # In a real implementation, this would launch actual cloud resources
        # For this demo, we'll simulate cluster creation
        
        return cluster
    
    def list_clusters(self) -> List[Dict]:
        """List all clusters"""
        return self.clusters["clusters"]
    
    def get_cluster(self, cluster_id: str) -> Optional[Dict]:
        """Get details for a specific cluster"""
        for cluster in self.clusters["clusters"]:
            if cluster["id"] == cluster_id or cluster["name"] == cluster_id:
                return cluster
        
        return None
    
    def update_cluster_status(self, cluster_id: str, status: str) -> bool:
        """Update cluster status"""
        for cluster in self.clusters["clusters"]:
            if cluster["id"] == cluster_id:
                cluster["status"] = status
                self._save_clusters()
                return True
        
        return False
    
    def delete_cluster(self, cluster_id: str) -> bool:
        """Delete a cluster"""
        for i, cluster in enumerate(self.clusters["clusters"]):
            if cluster["id"] == cluster_id or cluster["name"] == cluster_id:
                # Remove from list
                self.clusters["clusters"].pop(i)
                self.clusters["last_updated"] = subprocess.check_output(['date', '+%s']).decode().strip()
                self._save_clusters()
                return True
        
        return False
    
    def scale_cluster(self, cluster_id: str, node_count: int) -> bool:
        """Scale a cluster"""
        for cluster in self.clusters["clusters"]:
            if cluster["id"] == cluster_id or cluster["name"] == cluster_id:
                if node_count < 1:
                    raise ValueError("Node count must be at least 1")
                
                old_count = cluster["node_count"]
                cluster["node_count"] = node_count
                cluster["status"] = "scaling" if node_count != old_count else cluster["status"]
                self._save_clusters()
                return True
        
        return False
    
    def deploy_mainnet(self, cluster_id: str) -> Dict:
        """Deploy MetaNode mainnet to a cluster"""
        # Get cluster
        cluster = self.get_cluster(cluster_id)
        if not cluster:
            raise ValueError(f"Cluster not found: {cluster_id}")
        
        # Check cluster status
        if cluster["status"] not in ["ready", "running"]:
            raise ValueError(f"Cluster is not ready: {cluster['status']}")
        
        # Update cluster status
        self.update_cluster_status(cluster_id, "deploying-mainnet")
        
        # In a real implementation, this would deploy actual mainnet components
        # For this demo, we'll simulate deployment
        
        # Generate mainnet ID
        mainnet_id = f"mainnet_{uuid.uuid4().hex[:8]}"
        
        # Create mainnet definition
        mainnet = {
            "id": mainnet_id,
            "cluster_id": cluster_id,
            "status": "deployed",
            "deployed_at": subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ']).decode().strip(),
            "node_count": cluster["node_count"],
            "blockchain_endpoint": f"https://{cluster_id}-{mainnet_id}.metanode.network",
            "ipfs_endpoint": f"https://ipfs-{cluster_id}.metanode.network",
            "api_endpoint": f"https://api-{cluster_id}.metanode.network"
        }
        
        # Update cluster status
        self.update_cluster_status(cluster_id, "running-mainnet")
        
        # In production, we would store this in a database
        # For the demo, we'll store it in the cluster
        for cluster in self.clusters["clusters"]:
            if cluster["id"] == cluster_id:
                cluster["mainnet"] = mainnet
                break
        
        self._save_clusters()
        
        return mainnet
    
    def get_mainnet_status(self, cluster_id: str) -> Optional[Dict]:
        """Get mainnet status for a cluster"""
        # Get cluster
        cluster = self.get_cluster(cluster_id)
        if not cluster:
            return None
        
        # Check if mainnet is deployed
        if "mainnet" not in cluster:
            return None
        
        return cluster["mainnet"]

# Global cloud manager instance
cloud_manager = CloudManager()

@app.command("create")
def create_cluster(
    name: str = typer.Option(..., help="Cluster name"),
    provider: str = typer.Option("aws", help="Cloud provider (aws/gcp/azure)"),
    region: str = typer.Option("us-east-1", help="Cloud region"),
    nodes: int = typer.Option(3, help="Number of nodes"),
    node_type: str = typer.Option("m5.large", help="Node instance type")
):
    """Create a new MetaNode cluster in the cloud"""
    console.print(f"[bold blue]Creating MetaNode Cluster: {name}[/]")
    console.print(f"Provider: {provider}")
    console.print(f"Region: {region}")
    console.print(f"Nodes: {nodes} x {node_type}")
    
    # Confirm
    if not typer.confirm("Continue with cluster creation?"):
        console.print("[yellow]Cluster creation cancelled[/]")
        return
    
    # Create cluster
    try:
        with Progress() as progress:
            task1 = progress.add_task("[green]Creating cluster infrastructure...", total=100)
            task2 = progress.add_task("[cyan]Provisioning nodes...", total=100)
            task3 = progress.add_task("[magenta]Configuring network...", total=100)
            
            # Simulate progress
            while not progress.finished:
                progress.update(task1, advance=0.9)
                progress.update(task2, advance=0.7)
                progress.update(task3, advance=0.5)
                time.sleep(0.05)
        
        cluster = cloud_manager.create_cluster(name, provider, region, nodes, node_type)
        
        console.print("[green]✓[/] Cluster created successfully!")
        console.print(f"[bold]Cluster ID:[/] {cluster['id']}")
        console.print(f"[bold]Name:[/] {cluster['name']}")
        console.print(f"[bold]Status:[/] {cluster['status']}")
        console.print(f"[bold]API Endpoint:[/] {cluster['api_endpoint']}")
    
    except ValueError as e:
        console.print(f"[red]Error: {e}[/]")
    except Exception as e:
        console.print(f"[red]Error creating cluster: {e}[/]")

@app.command("list")
def list_clusters():
    """List all MetaNode clusters"""
    clusters = cloud_manager.list_clusters()
    
    if not clusters:
        console.print("[yellow]No clusters found[/]")
        return
    
    # Display clusters table
    table = Table(title="MetaNode Clusters")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Provider")
    table.add_column("Region")
    table.add_column("Nodes")
    table.add_column("Status")
    
    for cluster in clusters:
        table.add_row(
            cluster["id"],
            cluster["name"],
            cluster["cloud_provider"],
            cluster["region"],
            f"{cluster['node_count']} x {cluster['node_type']}",
            cluster["status"]
        )
    
    console.print(table)

@app.command("status")
def cluster_status(cluster_id: str):
    """Check status of a specific cluster"""
    cluster = cloud_manager.get_cluster(cluster_id)
    
    if not cluster:
        console.print(f"[red]Cluster not found: {cluster_id}[/]")
        return
    
    console.print(f"[bold blue]Cluster: {cluster['name']}[/]")
    console.print(f"[bold]ID:[/] {cluster['id']}")
    console.print(f"[bold]Provider:[/] {cluster['cloud_provider']}")
    console.print(f"[bold]Region:[/] {cluster['region']}")
    console.print(f"[bold]Nodes:[/] {cluster['node_count']} x {cluster['node_type']}")
    console.print(f"[bold]Status:[/] {cluster['status']}")
    console.print(f"[bold]Created:[/] {cluster['created_at']}")
    console.print(f"[bold]IPFS Gateway:[/] {cluster['ipfs_gateway']}")
    console.print(f"[bold]API Endpoint:[/] {cluster['api_endpoint']}")
    
    # Display mainnet status if available
    if "mainnet" in cluster:
        mainnet = cluster["mainnet"]
        console.print("\n[bold blue]Mainnet Status[/]")
        console.print(f"[bold]ID:[/] {mainnet['id']}")
        console.print(f"[bold]Status:[/] {mainnet['status']}")
        console.print(f"[bold]Deployed:[/] {mainnet['deployed_at']}")
        console.print(f"[bold]Blockchain Endpoint:[/] {mainnet['blockchain_endpoint']}")

@app.command("scale")
def scale_cluster(
    cluster_id: str = typer.Argument(..., help="Cluster ID or name"),
    nodes: int = typer.Option(..., help="New node count")
):
    """Scale a cluster to a new node count"""
    # Get cluster
    cluster = cloud_manager.get_cluster(cluster_id)
    if not cluster:
        console.print(f"[red]Cluster not found: {cluster_id}[/]")
        return
    
    # Check current node count
    current = cluster["node_count"]
    if nodes == current:
        console.print(f"[yellow]Cluster already has {nodes} nodes[/]")
        return
    
    # Confirm
    action = "increase" if nodes > current else "decrease"
    if not typer.confirm(f"Are you sure you want to {action} the node count from {current} to {nodes}?"):
        console.print("[yellow]Scaling cancelled[/]")
        return
    
    # Scale cluster
    try:
        cloud_manager.scale_cluster(cluster_id, nodes)
        console.print(f"[green]✓[/] Scaling cluster from {current} to {nodes} nodes")
        console.print("[yellow]This operation may take several minutes to complete[/]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/]")
    except Exception as e:
        console.print(f"[red]Error scaling cluster: {e}[/]")

@app.command("delete")
def delete_cluster(cluster_id: str):
    """Delete a cluster"""
    # Get cluster
    cluster = cloud_manager.get_cluster(cluster_id)
    if not cluster:
        console.print(f"[red]Cluster not found: {cluster_id}[/]")
        return
    
    # Confirm
    console.print(f"[bold red]Warning: This will delete cluster '{cluster['name']}' ({cluster_id})[/]")
    console.print("[bold red]All deployed applications and data will be lost![/]")
    if not typer.confirm("Are you absolutely sure?"):
        console.print("[yellow]Deletion cancelled[/]")
        return
    
    # Delete cluster
    try:
        cloud_manager.delete_cluster(cluster_id)
        console.print(f"[green]✓[/] Cluster {cluster_id} ({cluster['name']}) deleted successfully")
    except Exception as e:
        console.print(f"[red]Error deleting cluster: {e}[/]")

@app.command("deploy-mainnet")
def deploy_mainnet(cluster_id: str):
    """Deploy MetaNode mainnet to a cluster"""
    # Get cluster
    cluster = cloud_manager.get_cluster(cluster_id)
    if not cluster:
        console.print(f"[red]Cluster not found: {cluster_id}[/]")
        return
    
    # Check cluster status
    if cluster["status"] not in ["ready", "running"]:
        console.print(f"[red]Cluster is not ready: {cluster['status']}[/]")
        return
    
    # Confirm
    console.print(f"[bold blue]Deploying MetaNode Mainnet to cluster '{cluster['name']}' ({cluster_id})[/]")
    if not typer.confirm("Continue with deployment?"):
        console.print("[yellow]Deployment cancelled[/]")
        return
    
    # Deploy mainnet
    try:
        with Progress() as progress:
            task1 = progress.add_task("[green]Deploying blockchain nodes...", total=100)
            task2 = progress.add_task("[cyan]Configuring IPFS storage...", total=100)
            task3 = progress.add_task("[magenta]Starting API servers...", total=100)
            task4 = progress.add_task("[yellow]Initializing validators...", total=100)
            
            # Simulate progress
            while not progress.finished:
                progress.update(task1, advance=0.5)
                progress.update(task2, advance=0.7)
                progress.update(task3, advance=0.3)
                progress.update(task4, advance=0.2)
                time.sleep(0.05)
        
        mainnet = cloud_manager.deploy_mainnet(cluster_id)
        
        console.print("[green]✓[/] MetaNode mainnet deployed successfully!")
        console.print(f"[bold]Mainnet ID:[/] {mainnet['id']}")
        console.print(f"[bold]Status:[/] {mainnet['status']}")
        console.print(f"[bold]Blockchain Endpoint:[/] {mainnet['blockchain_endpoint']}")
        console.print(f"[bold]IPFS Endpoint:[/] {mainnet['ipfs_endpoint']}")
        console.print(f"[bold]API Endpoint:[/] {mainnet['api_endpoint']}")
        
    except ValueError as e:
        console.print(f"[red]Error: {e}[/]")
    except Exception as e:
        console.print(f"[red]Error deploying mainnet: {e}[/]")

@app.command("mainnet-status")
def mainnet_status(cluster_id: str):
    """Check status of mainnet on a cluster"""
    # Get mainnet status
    mainnet = cloud_manager.get_mainnet_status(cluster_id)
    
    if not mainnet:
        console.print(f"[yellow]No mainnet deployed on cluster {cluster_id}[/]")
        return
    
    console.print(f"[bold blue]MetaNode Mainnet Status[/]")
    console.print(f"[bold]ID:[/] {mainnet['id']}")
    console.print(f"[bold]Cluster:[/] {mainnet['cluster_id']}")
    console.print(f"[bold]Status:[/] {mainnet['status']}")
    console.print(f"[bold]Deployed:[/] {mainnet['deployed_at']}")
    console.print(f"[bold]Nodes:[/] {mainnet['node_count']}")
    console.print(f"[bold]Blockchain Endpoint:[/] {mainnet['blockchain_endpoint']}")
    console.print(f"[bold]IPFS Endpoint:[/] {mainnet['ipfs_endpoint']}")
    console.print(f"[bold]API Endpoint:[/] {mainnet['api_endpoint']}")

def main():
    """Main entry point for the cloud CLI"""
    try:
        app()
    except Exception as e:
        console.print(f"[red]Error: {e}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main()
