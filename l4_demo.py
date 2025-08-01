#!/usr/bin/env python
# coding: utf-8

"""
L4 Meta-Cognitive Demonstration Script

This script demonstrates the L4 (Level 4) meta-cognitive optimization capabilities
of the PSI Runtime SDK, showcasing cross-engine integration, adaptive reasoning,
and meta-cognitive confidence calibration.

Usage:
    python l4_demo.py
"""

import time
from psi_runtime_sdk import L4IntegratedAnalyzer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.json import JSON
import json

console = Console()


def main():
    """Main demonstration function."""
    console.print(Panel.fit(
        "🧠 L4 Meta-Cognitive PSI Runtime SDK Demonstration\n"
        "Advanced cross-engine reasoning with meta-cognitive optimization",
        title="PSI Runtime SDK - L4 Enhanced",
        border_style="blue"
    ))
    
    # Initialize L4 analyzer
    console.print("\n🔧 Initializing L4 Integrated Analyzer...", style="cyan")
    analyzer = L4IntegratedAnalyzer()
    
    # Demo queries showcasing different capabilities
    demo_queries = [
        {
            "title": "Simple Reasoning",
            "query": "What is the future of AI?",
            "description": "Basic reasoning test with L4 enhancements"
        },
        {
            "title": "Complex Meta-Cognitive Analysis", 
            "query": "How can artificial intelligence systems develop meta-cognitive self-awareness while maintaining ethical alignment and avoiding harmful behaviors?",
            "description": "Advanced meta-cognitive reasoning with ethical considerations"
        },
        {
            "title": "Technical Deep Dive",
            "query": "Analyze the quantum mechanical principles behind quantum computing and their implications for cryptographic security in distributed blockchain networks",
            "description": "Technical analysis requiring cross-domain knowledge integration"
        },
        {
            "title": "Philosophical Inquiry",
            "query": "What is the nature of consciousness and how might machine consciousness differ from human consciousness?",
            "description": "Deep philosophical reasoning with semantic field analysis"
        }
    ]
    
    results = []
    
    # Process each demo query
    for i, demo in enumerate(demo_queries, 1):
        console.print(f"\n📋 Demo {i}/4: {demo['title']}", style="bold green")
        console.print(f"Description: {demo['description']}", style="italic")
        console.print(f"Query: {demo['query'][:80]}...", style="white")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running L4 analysis...", total=None)
            
            start_time = time.perf_counter()
            result = analyzer.analyze(demo['query'])
            end_time = time.perf_counter()
            
            progress.remove_task(task)
        
        # Display results
        display_result(result, end_time - start_time, i)
        results.append({
            "demo": demo,
            "result": result,
            "processing_time": end_time - start_time
        })
    
    # Summary analysis
    display_summary(results)
    
    # L4 System Status
    display_l4_status(analyzer)
    
    console.print("\n🎉 L4 Demonstration Complete!", style="bold green")


def display_result(result, processing_time, demo_num):
    """Display individual analysis result."""
    
    # Core metrics table
    table = Table(title=f"Demo {demo_num} - L4 Analysis Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Description", style="white")
    
    table.add_row(
        "Confidence", 
        f"{result['confidence']:.4f}",
        "Overall analysis confidence"
    )
    table.add_row(
        "L4 Meta Score", 
        f"{result['l4_meta_score']:.4f}",
        "Meta-cognitive optimization score"
    )
    table.add_row(
        "Cross-Engine Harmony", 
        f"{result['cross_engine_harmony']:.4f}",
        "Inter-engine agreement level"
    )
    table.add_row(
        "Processing Time", 
        f"{processing_time:.4f}s",
        "Total analysis duration"
    )
    
    console.print(table)
    
    # L4 Optimizations applied
    optimizations = result.get('optimization_applied', [])
    if optimizations:
        opt_text = "\n".join(f"✓ {opt.replace('_', ' ').title()}" for opt in optimizations)
        console.print(Panel(
            opt_text,
            title=f"L4 Optimizations Applied ({len(optimizations)})",
            border_style="yellow"
        ))
    
    # Reasoning path (last 3 steps)
    reasoning_path = result.get('reasoning_path', [])
    if reasoning_path:
        path_text = "\n".join(reasoning_path[-3:])
        console.print(Panel(
            path_text,
            title="Reasoning Path (Final Steps)",
            border_style="blue"
        ))


def display_summary(results):
    """Display summary statistics across all demos."""
    console.print("\n📊 L4 Performance Summary", style="bold blue")
    
    # Calculate averages
    avg_confidence = sum(r['result']['confidence'] for r in results) / len(results)
    avg_l4_score = sum(r['result']['l4_meta_score'] for r in results) / len(results)
    avg_harmony = sum(r['result']['cross_engine_harmony'] for r in results) / len(results)
    avg_time = sum(r['processing_time'] for r in results) / len(results)
    total_optimizations = sum(len(r['result'].get('optimization_applied', [])) for r in results)
    
    summary_table = Table(title="L4 System Performance Metrics")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Average Value", style="green")
    summary_table.add_column("Assessment", style="yellow")
    
    # Confidence assessment
    conf_assessment = "Excellent" if avg_confidence > 0.7 else "Good" if avg_confidence > 0.5 else "Needs Improvement"
    summary_table.add_row("Average Confidence", f"{avg_confidence:.4f}", conf_assessment)
    
    # L4 Meta Score assessment
    l4_assessment = "Excellent" if avg_l4_score > 0.8 else "Good" if avg_l4_score > 0.6 else "Needs Improvement"
    summary_table.add_row("Average L4 Meta Score", f"{avg_l4_score:.4f}", l4_assessment)
    
    # Harmony assessment
    harmony_assessment = "Excellent" if avg_harmony > 0.7 else "Good" if avg_harmony > 0.5 else "Needs Improvement"
    summary_table.add_row("Average Cross-Engine Harmony", f"{avg_harmony:.4f}", harmony_assessment)
    
    # Performance assessment
    perf_assessment = "Excellent" if avg_time < 0.01 else "Good" if avg_time < 0.05 else "Acceptable"
    summary_table.add_row("Average Processing Time", f"{avg_time:.4f}s", perf_assessment)
    
    summary_table.add_row("Total L4 Optimizations", str(total_optimizations), "Applied across all demos")
    
    console.print(summary_table)


def display_l4_status(analyzer):
    """Display L4 system status."""
    console.print("\n🔧 L4 System Status", style="bold blue")
    
    status = analyzer.get_l4_status()
    
    # Engine status table
    engine_table = Table(title="L4 Engine Status")
    engine_table.add_column("Engine", style="cyan")
    engine_table.add_column("Status", style="green")
    engine_table.add_column("L4 Optimized", style="yellow")
    
    engines_info = status.get('engines', {})
    
    for engine_name, engine_status in engines_info.items():
        status_text = engine_status.get('status', 'unknown')
        l4_status = "✅ Yes" if engine_status.get('l4_optimization_enabled', False) else "❌ No"
        engine_table.add_row(engine_name.title(), status_text.title(), l4_status)
    
    console.print(engine_table)
    
    # Integration features
    features = status.get('integration_features', [])
    if features:
        features_text = "\n".join(f"✓ {feature.replace('_', ' ').title()}" for feature in features)
        console.print(Panel(
            features_text,
            title=f"L4 Integration Features ({len(features)})",
            border_style="green"
        ))
    
    # Optimal weights
    weights = status.get('optimal_weights', {})
    if weights:
        weights_text = "\n".join(f"{engine.title()}: {weight:.4f}" for engine, weight in weights.items())
        console.print(Panel(
            weights_text,
            title="Adaptive Engine Weights",
            border_style="blue"
        ))


if __name__ == "__main__":
    main()