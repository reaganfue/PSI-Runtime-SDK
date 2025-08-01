#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PSI Runtime SDK Command Line Interface - L4 Enhanced

Enterprise CLI tool for managing PSI Runtime SDK operations with L4 meta-cognitive capabilities.
Includes advanced analysis modes, engine status monitoring, and L4 optimization controls.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.json import JSON

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from psi_runtime_sdk.config import get_config
from psi_runtime_sdk.logging import setup_logging, get_logger
from psi_runtime_sdk.monitoring import health_checker, get_health_status
from psi_runtime_sdk.security import generate_api_key, create_user_token

# Import L4 components
try:
    from psi_runtime_sdk import L4IntegratedAnalyzer, QuantumAnalyzer, SemanticFieldEngine, BasicResponseLogic
    L4_AVAILABLE = True
except ImportError:
    L4_AVAILABLE = False

console = Console()


@click.group()
@click.option('--config-file', help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--l4-mode', is_flag=True, help='Enable L4 meta-cognitive mode')
def cli(config_file: Optional[str], verbose: bool, l4_mode: bool):
    """PSI Runtime SDK Enterprise CLI Tool - L4 Enhanced"""
    if verbose:
        setup_logging()
    
    if config_file:
        console.print(f"Using config file: {config_file}")
    
    if l4_mode and L4_AVAILABLE:
        console.print("🧠 L4 Meta-Cognitive Mode Enabled", style="bold green")
    elif l4_mode and not L4_AVAILABLE:
        console.print("❌ L4 Mode requested but not available", style="bold red")


@cli.group()
def health():
    """Health check and monitoring commands"""
    pass


@cli.group()
def analysis():
    """L4 Enhanced Analysis Commands"""
    pass


@cli.group()
def l4():
    """L4 Meta-Cognitive Operations"""
    pass


@analysis.command()
@click.argument('query')
@click.option('--mode', default='integrated', 
              type=click.Choice(['integrated', 'logic', 'quantum', 'field']),
              help='Analysis mode: integrated, logic, quantum, field')
@click.option('--session-id', help='Session ID for context continuity')
@click.option('--format', 'output_format', default='table', help='Output format: table, json, detailed')
@click.option('--save', help='Save results to file')
def run(query: str, mode: str, session_id: Optional[str], output_format: str, save: Optional[str]):
    """Run L4 enhanced analysis on query"""
    if not L4_AVAILABLE:
        console.print("❌ L4 components not available", style="bold red")
        return
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Running {mode} analysis...", total=None)
        
        try:
            # Select analyzer based on mode
            if mode == 'integrated':
                analyzer = L4IntegratedAnalyzer()
                result = analyzer.analyze(query, session_id=session_id)
            elif mode == 'logic':
                analyzer = BasicResponseLogic()
                result = analyzer.run(query)
            elif mode == 'quantum':
                analyzer = QuantumAnalyzer()
                result = analyzer.comprehensive_analysis(query)
            elif mode == 'field':
                analyzer = SemanticFieldEngine()
                result = analyzer.analyze(query, session_id=session_id)
            else:
                raise ValueError(f"Unknown mode: {mode}")
            
            progress.remove_task(task)
            
            # Display results based on format
            if output_format == 'json':
                console.print(JSON(json.dumps(result, indent=2)))
            elif output_format == 'detailed':
                _display_detailed_results(result, mode)
            else:
                _display_table_results(result, mode)
            
            # Save if requested
            if save:
                with open(save, 'w') as f:
                    json.dump(result, f, indent=2)
                console.print(f"Results saved to {save}", style="green")
                
        except Exception as e:
            progress.remove_task(task)
            console.print(f"❌ Analysis failed: {e}", style="bold red")


@l4.command()
@click.option('--engine', help='Specific engine to check: logic, quantum, field, integrated')
def status(engine: Optional[str]):
    """Get L4 system status and optimization metrics"""
    if not L4_AVAILABLE:
        console.print("❌ L4 components not available", style="bold red")
        return
    
    try:
        if engine == 'integrated' or not engine:
            analyzer = L4IntegratedAnalyzer()
            status_data = analyzer.get_l4_status()
            _display_l4_status(status_data, "Integrated Analyzer")
        
        if engine == 'quantum' or not engine:
            analyzer = QuantumAnalyzer()
            status_data = analyzer.get_l4_status()
            _display_l4_status(status_data, "Quantum Engine")
        
        if engine == 'field' or not engine:
            analyzer = SemanticFieldEngine()
            status_data = analyzer.get_l4_status()
            _display_l4_status(status_data, "Semantic Field Engine")
        
        if engine == 'logic' or not engine:
            analyzer = BasicResponseLogic()
            status_data = analyzer.get_status()
            _display_l4_status(status_data, "Logic Core Engine")
            
    except Exception as e:
        console.print(f"❌ Status check failed: {e}", style="bold red")


@l4.command()
@click.argument('query')
@click.option('--iterations', default=5, help='Number of analysis iterations')
@click.option('--compare-engines', is_flag=True, help='Compare all engines')
def benchmark(query: str, iterations: int, compare_engines: bool):
    """Benchmark L4 analysis performance"""
    if not L4_AVAILABLE:
        console.print("❌ L4 components not available", style="bold red")
        return
    
    console.print(f"🔬 Running L4 benchmark with {iterations} iterations", style="bold blue")
    
    results = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        if compare_engines:
            # Test all engines
            engines = [
                ('Integrated', lambda: L4IntegratedAnalyzer().analyze(query)),
                ('Logic', lambda: BasicResponseLogic().run(query)),
                ('Quantum', lambda: QuantumAnalyzer().comprehensive_analysis(query)),
                ('Field', lambda: SemanticFieldEngine().analyze(query))
            ]
        else:
            # Test just integrated
            engines = [('Integrated', lambda: L4IntegratedAnalyzer().analyze(query))]
        
        for engine_name, engine_func in engines:
            task = progress.add_task(f"Benchmarking {engine_name}...", total=iterations)
            
            times = []
            confidences = []
            
            for i in range(iterations):
                try:
                    import time
                    start = time.perf_counter()
                    result = engine_func()
                    end = time.perf_counter()
                    
                    times.append(end - start)
                    confidences.append(result.get('confidence', 0.0))
                    
                    progress.advance(task)
                except Exception as e:
                    console.print(f"❌ {engine_name} iteration {i+1} failed: {e}", style="red")
            
            if times:
                results[engine_name] = {
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'avg_confidence': sum(confidences) / len(confidences),
                    'iterations': len(times)
                }
            
            progress.remove_task(task)
    
    # Display benchmark results
    _display_benchmark_results(results)


def _display_detailed_results(result: Dict, mode: str):
    """Display detailed analysis results"""
    console.print(f"\n[bold blue]🧠 L4 {mode.title()} Analysis Results[/bold blue]")
    
    # Main metrics panel
    metrics_content = []
    if 'confidence' in result:
        metrics_content.append(f"Confidence: {result['confidence']:.4f}")
    if 'integrated_score' in result:
        metrics_content.append(f"Integrated Score: {result['integrated_score']:.4f}")
    if 'l4_meta_score' in result:
        metrics_content.append(f"L4 Meta Score: {result['l4_meta_score']:.4f}")
    if 'cross_engine_harmony' in result:
        metrics_content.append(f"Cross-Engine Harmony: {result['cross_engine_harmony']:.4f}")
    
    if metrics_content:
        console.print(Panel("\n".join(metrics_content), title="Core Metrics", border_style="green"))
    
    # Reasoning path
    if 'reasoning_path' in result:
        path_content = "\n".join(result['reasoning_path'][-5:])  # Last 5 steps
        console.print(Panel(path_content, title="Reasoning Path (Last 5 Steps)", border_style="blue"))
    
    # Optimizations applied
    if 'optimization_applied' in result or 'l4_optimizations_applied' in result:
        opts = result.get('optimization_applied', result.get('l4_optimizations_applied', []))
        opts_content = "\n".join(f"✓ {opt}" for opt in opts)
        console.print(Panel(opts_content, title="L4 Optimizations Applied", border_style="yellow"))


def _display_table_results(result: Dict, mode: str):
    """Display results in table format"""
    table = Table(title=f"L4 {mode.title()} Analysis Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Type", style="yellow")
    
    # Add key metrics
    if 'confidence' in result:
        table.add_row("Confidence", f"{result['confidence']:.4f}", "Core")
    if 'integrated_score' in result:
        table.add_row("Integrated Score", f"{result['integrated_score']:.4f}", "L4")
    if 'l4_meta_score' in result:
        table.add_row("L4 Meta Score", f"{result['l4_meta_score']:.4f}", "Meta-Cognitive")
    if 'cross_engine_harmony' in result:
        table.add_row("Cross-Engine Harmony", f"{result['cross_engine_harmony']:.4f}", "Integration")
    if 'processing_time' in result:
        table.add_row("Processing Time", f"{result['processing_time']:.4f}s", "Performance")
    
    console.print(table)


def _display_l4_status(status_data: Dict, engine_name: str):
    """Display L4 status information"""
    console.print(f"\n[bold blue]🔧 {engine_name} Status[/bold blue]")
    
    # Status panel
    status_content = []
    status_content.append(f"Status: {status_data.get('status', 'unknown')}")
    
    if 'l4_optimization_enabled' in status_data:
        status_content.append(f"L4 Optimization: {'✓ Enabled' if status_data['l4_optimization_enabled'] else '✗ Disabled'}")
    
    if 'l4_features' in status_data:
        features = status_data['l4_features']
        status_content.append(f"L4 Features: {len(features)} active")
    
    console.print(Panel("\n".join(status_content), title="Status", border_style="green"))
    
    # Features panel
    if 'l4_features' in status_data:
        features_content = "\n".join(f"✓ {feature}" for feature in status_data['l4_features'])
        console.print(Panel(features_content, title="L4 Features", border_style="blue"))


def _display_benchmark_results(results: Dict):
    """Display benchmark results"""
    table = Table(title="L4 Performance Benchmark Results")
    table.add_column("Engine", style="cyan")
    table.add_column("Avg Time (s)", style="green")
    table.add_column("Min Time (s)", style="green")  
    table.add_column("Max Time (s)", style="green")
    table.add_column("Avg Confidence", style="yellow")
    table.add_column("Iterations", style="white")
    
    for engine_name, metrics in results.items():
        table.add_row(
            engine_name,
            f"{metrics['avg_time']:.4f}",
            f"{metrics['min_time']:.4f}",
            f"{metrics['max_time']:.4f}",
            f"{metrics['avg_confidence']:.4f}",
            str(metrics['iterations'])
        )
    
    console.print(table)


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


@analysis.command(name="legacy")
@click.argument('query')
@click.option('--mode', type=click.Choice(['basic', 'quantum', 'semantic', 'comprehensive']), 
              default='comprehensive', help='Analysis mode')
@click.option('--output', type=click.Choice(['json', 'table']), default='table', 
              help='Output format')
def legacy_run(query: str, mode: str, output: str):
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