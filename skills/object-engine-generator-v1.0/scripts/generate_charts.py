#!/usr/bin/env python3
"""
Chart generation script for Symbol Engine Generator.

Generates:
- State flow diagrams (Mermaid → PNG)
- Task DAG charts
- Data visualization plots

Usage:
    python generate_charts.py --type state_flow --input data.json --output state_flow.png
    python generate_charts.py --type task_dag --input data.json --output task_dag.png
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


def generate_mermaid_state_flow(state_data: Dict[str, Any]) -> str:
    """Generate Mermaid graph for state transitions."""
    current = state_data.get("current", "initial")
    transitions = state_data.get("transitions", [])

    mermaid_lines = ["graph TD"]

    # Add state nodes
    states = set()
    states.add(current)
    for t in transitions:
        states.add(t["from"])
        states.add(t["to"])

    for state in sorted(states):
        if state == current:
            mermaid_lines.append(f'  {state}[{state}]:::current')
        else:
            mermaid_lines.append(f'  {state}[{state}]')

    # Add transitions
    for t in transitions:
        trigger = t.get("trigger", "")
        condition = t.get("condition", "")
        label = f"|{trigger}" + (f" & {condition}" if condition else "")
        mermaid_lines.append(f'  {t["from"]} -->{label} {t["to"]}')

    # Add styling
    mermaid_lines.append("\n  classDef current fill:#f9f,stroke:#333,stroke-width:4px")

    return "\n".join(mermaid_lines)


def generate_mermaid_task_dag(tasks_data: Dict[str, Any]) -> str:
    """Generate Mermaid graph for task dependencies."""
    main_task = tasks_data.get("main_task", {})
    parallel_tasks = tasks_data.get("parallel_tasks", [])

    mermaid_lines = ["graph TD"]

    # Add main task
    main_name = main_task.get("name", "main")
    main_status = main_task.get("status", "pending")
    mermaid_lines.append(f'  {main_name}[{main_name}]:::main')

    # Add parallel tasks
    for task in parallel_tasks:
        task_name = task.get("name", "unknown")
        task_status = task.get("status", "pending")
        deps = task.get("dependencies", [])

        # Style based on status
        style_class = {
            "completed": "done",
            "running": "active",
            "pending": "pending",
            "failed": "failed"
        }.get(task_status, "pending")

        mermaid_lines.append(f'  {task_name}[{task_name}]:::{style_class}')

        # Add dependencies
        for dep in deps:
            mermaid_lines.append(f'  {dep} --> {task_name}')

        # Connect to main task if no dependencies
        if not deps:
            mermaid_lines.append(f'  {main_name} --> {task_name}')

    # Add styling
    mermaid_lines.extend([
        "\n  classDef main fill:#ff9,stroke:#333,stroke-width:2px",
        "  classDef done fill:#9f9,stroke:#333,stroke-width:2px",
        "  classDef active fill:#99f,stroke:#333,stroke-width:2px",
        "  classDef pending fill:#fff,stroke:#333,stroke-width:1px,stroke-dasharray: 5",
        "  classDef failed fill:#f99,stroke:#333,stroke-width:2px"
    ])

    return "\n".join(mermaid_lines)


def save_mermaid_file(mermaid_code: str, output_path: Path):
    """Save Mermaid code to .mmd file."""
    mermaid_path = output_path.with_suffix(".mmd")
    mermaid_path.write_text(mermaid_code, encoding="utf-8")
    print(f"✓ Mermaid file saved: {mermaid_path}")


def generate_png_from_mermaid(mermaid_code: str, output_path: Path):
    """Generate PNG from Mermaid code.

    Requires: https://github.com/mermaid-js/mermaid-cli
    Install: npm install -g @mermaid-js/mermaid-cli

    Fallback: If mmdc not available, save as .mmd file only.
    """
    try:
        import subprocess

        # Save temporary .mmd file
        temp_mmd = output_path.with_suffix(".mmd")
        temp_mmd.write_text(mermaid_code, encoding="utf-8")

        # Run mmdc command
        subprocess.run(
            ["mmdc", "-i", str(temp_mmd), "-o", str(output_path)],
            check=True,
            capture_output=True
        )

        print(f"✓ PNG chart generated: {output_path}")

    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: Save Mermaid text only
        save_mermaid_file(mermaid_code, output_path)
        print(f"⚠ mmdc not available. Mermaid text saved to: {output_path.with_suffix('.mmd')}")


def generate_symbol_table_chart(symbol_table: Dict[str, Any], output_path: Path):
    """Generate visualization for symbol table using matplotlib."""

    try:
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
        import matplotlib

        # Set font for Chinese characters
        matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei"]
        matplotlib.rcParams["axes.unicode_minus"] = False

        symbols = symbol_table.get("symbols", [])

        # Count symbols by type
        type_counts = {}
        for sym in symbols:
            sym_type = sym.get("type", "unknown")
            type_counts[sym_type] = type_counts.get(sym_type, 0) + 1

        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 6))
        types = list(type_counts.keys())
        counts = list(type_counts.values())

        ax.pie(counts, labels=types, autopct="%1.1f%%", startangle=90)
        ax.set_title("Symbol Distribution by Type")

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"✓ Symbol table chart generated: {output_path}")

    except ImportError:
        print(f"⚠ matplotlib not available. Skipping symbol table chart.")
    except Exception as e:
        print(f"⚠ Failed to generate symbol table chart: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate charts for Symbol Engine")
    parser.add_argument("--type", required=True, choices=["state_flow", "task_dag", "symbol_table"])
    parser.add_argument("--input", required=True, type=Path, help="Path to JSON data file")
    parser.add_argument("--output", required=True, type=Path, help="Path to output chart file")

    args = parser.parse_args()

    # Load JSON data
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Generate chart based on type
    if args.type == "state_flow":
        mermaid_code = generate_mermaid_state_flow(data.get("state", {}))
        generate_png_from_mermaid(mermaid_code, args.output)

    elif args.type == "task_dag":
        mermaid_code = generate_mermaid_task_dag(data.get("tasks", {}))
        generate_png_from_mermaid(mermaid_code, args.output)

    elif args.type == "symbol_table":
        generate_symbol_table_chart(data.get("symbol_table", {}), args.output)


if __name__ == "__main__":
    main()
