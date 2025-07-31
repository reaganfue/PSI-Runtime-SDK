#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PSI Runtime SDK Command Line Interface

Enterprise CLI tool for managing PSI Runtime SDK operations.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from psi_runtime_sdk.config import get_config
from psi_runtime_sdk.logging import setup_logging, get_logger
from psi_runtime_sdk.monitoring import health_checker, get_health_status
from psi_runtime_sdk.security import generate_api_key, create_user_token

console = Console()


@click.group()
@click.option('--config-file', help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(config_file: Optional[str], verbose: bool):
    """PSI Runtime SDK Enterprise CLI Tool"""
    if verbose:
        setup_logging()
    
    if config_file:
        console.print(f"Using config file: {config_file}")


@cli.group()
def health():
    """Health check and monitoring commands"""
    pass


@health.command()
def check():
    """Run comprehensive health check"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Running health checks...", total=None)
        
        try:
            health_data = asyncio.run(get_health_status())
            progress.remove_task(task)
            
            # Display results
            table = Table(title="System Health Status")
            table.add_column("Component", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Message", style="white")
            table.add_column("Duration (ms)", style="yellow")
            
            overall_status = health_data['status']
            console.print(f"\n[bold]Overall Status: [{overall_status.upper()}]{overall_status}[/{overall_status.upper()}][/bold]\n")
            
            for check in health_data['checks']:
                status_color = {
                    'healthy': 'green',
                    'degraded': 'yellow', 
                    'unhealthy': 'red',
                    'unknown': 'gray'
                }.get(check['status'], 'white')
                
                table.add_row(
                    check['name'],
                    f"[{status_color}]{check['status']}[/{status_color}]",
                    check['message'],
                    f"{check['duration_ms']:.2f}"
                )
            
            console.print(table)
            
            # System metrics
            if 'system_metrics' in health_data:
                metrics = health_data['system_metrics']
                console.print(f"\n[bold]System Metrics:[/bold]")
                console.print(f"CPU Usage: {metrics.get('cpu_usage_percent', 'N/A')}%")
                console.print(f"Memory Usage: {metrics.get('memory_usage_percent', 'N/A')}%")
                console.print(f"Disk Usage: {metrics.get('disk_usage_percent', 'N/A')}%")
                console.print(f"Uptime: {health_data.get('uptime_seconds', 0):.2f} seconds")
            
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Health check failed: {e}[/red]")
            sys.exit(1)


@cli.group()
def security():
    """Security and authentication commands"""
    pass


@security.command()
@click.option('--description', help='Description for the API key')
def generate_key(description: Optional[str]):
    """Generate a new API key"""
    try:
        key = generate_api_key(description or "CLI generated key")
        console.print(f"[green]Generated API key:[/green] {key}")
        console.print("[yellow]Store this key securely - it cannot be retrieved again![/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to generate API key: {e}[/red]")
        sys.exit(1)


@security.command()
@click.option('--user-id', required=True, help='User ID for the token')
@click.option('--claims', help='Additional claims as JSON string')
def generate_token(user_id: str, claims: Optional[str]):
    """Generate a JWT token for a user"""
    try:
        additional_claims = {}
        if claims:
            additional_claims = json.loads(claims)
        
        token = create_user_token(user_id, additional_claims)
        console.print(f"[green]Generated JWT token for user '{user_id}':[/green]")
        console.print(token)
    except Exception as e:
        console.print(f"[red]Failed to generate token: {e}[/red]")
        sys.exit(1)


@cli.group()
def analysis():
    """AI analysis commands"""
    pass


@analysis.command()
@click.argument('query')
@click.option('--mode', type=click.Choice(['basic', 'quantum', 'semantic', 'comprehensive']), 
              default='comprehensive', help='Analysis mode')
@click.option('--output', type=click.Choice(['json', 'table']), default='table', 
              help='Output format')
def run(query: str, mode: str, output: str):
    """Run AI analysis on input text"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Running {mode} analysis...", total=None)
        
        try:
            if mode == 'basic':
                from psi_runtime_sdk.logic_core import BasicResponseLogic
                engine = BasicResponseLogic()
                result = engine.run(query, {})
            
            elif mode == 'quantum':
                from psi_runtime_sdk.quantum_engine import QuantumAnalyzer
                analyzer = QuantumAnalyzer()
                result = analyzer.comprehensive_analysis(query)
            
            elif mode == 'semantic':
                from psi_runtime_sdk.psi_field import SemanticFieldEngine, DataParser
                engine = SemanticFieldEngine()
                semantic_input = DataParser.parse(query)
                unlocked_keys = engine.psi_engine.unlock_knowledge(semantic_input)
                result = {"unlocked_keys": unlocked_keys}
            
            elif mode == 'comprehensive':
                # Run all analyses
                from psi_runtime_sdk.logic_core import BasicResponseLogic
                from psi_runtime_sdk.quantum_engine import QuantumAnalyzer
                from psi_runtime_sdk.psi_field import SemanticFieldEngine, DataParser
                
                basic_engine = BasicResponseLogic()
                quantum_analyzer = QuantumAnalyzer()
                semantic_engine = SemanticFieldEngine()
                
                basic_result = basic_engine.run(query, {})
                quantum_result = quantum_analyzer.comprehensive_analysis(query)
                semantic_input = DataParser.parse(query)
                semantic_result = semantic_engine.psi_engine.unlock_knowledge(semantic_input)
                
                result = {
                    "basic_analysis": basic_result,
                    "quantum_analysis": quantum_result,
                    "semantic_analysis": {"unlocked_keys": semantic_result}
                }
            
            progress.remove_task(task)
            
            if output == 'json':
                console.print(json.dumps(result, indent=2, default=str))
            else:
                console.print(f"\n[bold]{mode.title()} Analysis Results:[/bold]")
                console.print(f"Query: {query}\n")
                
                if isinstance(result, dict):
                    for key, value in result.items():
                        console.print(f"[cyan]{key}:[/cyan] {value}")
                else:
                    console.print(str(result))
        
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Analysis failed: {e}[/red]")
            sys.exit(1)


@cli.group()
def config():
    """Configuration management commands"""
    pass


@config.command()
def show():
    """Show current configuration"""
    config_obj = get_config()
    
    table = Table(title="PSI Runtime SDK Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Environment", config_obj.environment)
    table.add_row("Debug", str(config_obj.debug))
    table.add_row("Version", config_obj.version)
    table.add_row("API Host", config_obj.api.host)
    table.add_row("API Port", str(config_obj.api.port))
    table.add_row("API Workers", str(config_obj.api.workers))
    table.add_row("Docs Enabled", str(config_obj.api.docs_enabled))
    table.add_row("Metrics Enabled", str(config_obj.monitoring.metrics_enabled))
    table.add_row("Database URL", config_obj.database.url)
    table.add_row("Log Level", config_obj.logging.level)
    
    console.print(table)


@config.command()
def validate():
    """Validate current configuration"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Validating configuration...", total=None)
        
        try:
            config_obj = get_config()
            progress.remove_task(task)
            
            console.print("[green]✓ Configuration is valid[/green]")
            console.print(f"Environment: {config_obj.environment}")
            console.print(f"Version: {config_obj.version}")
            
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[red]Configuration validation failed: {e}[/red]")
            sys.exit(1)


@cli.command()
def version():
    """Show version information"""
    config_obj = get_config()
    console.print(f"PSI Runtime SDK v{config_obj.version}")
    console.print(f"Environment: {config_obj.environment}")
    console.print("Enterprise Edition")


if __name__ == '__main__':
    cli()