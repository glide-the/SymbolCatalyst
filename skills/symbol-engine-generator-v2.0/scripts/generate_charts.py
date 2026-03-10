#!/usr/bin/env python3
"""
Chart generation for Symbol Engine Generator.

Generates Mermaid diagrams for:
- Symbol Graph (nodes = symbols, edges = relations)
- Power Chain (linked motion nodes)
- Fantasy Knot Structure (repetition patterns)
- Runtime Loop (10-stage flow)

Usage:
    python generate_charts.py --type symbol_graph --input data.json --output symbol_graph.mmd
    python generate_charts.py --type power_chain --input data.json --output power_chain.mmd
    python generate_charts.py --type fantasy_knots --input data.json --output fantasy_knots.mmd
    python generate_charts.py --type runtime_loop --output runtime_loop.mmd
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


def generate_symbol_graph(data: Dict[str, Any]) -> str:
    """Generate Mermaid graph for symbol relationships."""
    symbols = data.get("symbols", [])
    fantasy_knots = data.get("fantasy_knots", [])

    lines = ["graph TD"]
    lines.append("  classDef high_tension fill:#f96,stroke:#333,stroke-width:2px")
    lines.append("  classDef high_clarity fill:#6f9,stroke:#333,stroke-width:2px")
    lines.append("  classDef silenced fill:#999,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5")

    # Add symbol nodes
    for sym in symbols:
        sid = sym["id"]
        label = sym.get("label", sid)
        valence = sym.get("valence", {})
        tension = valence.get("tension", 0)
        clarity = valence.get("clarity", 0)

        lines.append(f'  {sid}["{label}"]')
        if tension > 0.5:
            lines.append(f"  {sid}:::high_tension")
        elif clarity > 0.5:
            lines.append(f"  {sid}:::high_clarity")

    # Add fantasy knot connections
    for knot in fantasy_knots:
        linked = knot.get("repetition_pattern", {}).get("linked_symbols", [])
        knot_id = knot["id"]
        force = knot.get("force_index", 0)
        lines.append(f'  {knot_id}{{{{{knot_id}: force={force:.1f}}}}}')
        for sym_id in linked:
            lines.append(f"  {sym_id} --> {knot_id}")

    return "\n".join(lines)


def generate_power_chain(data: Dict[str, Any]) -> str:
    """Generate Mermaid graph for power chain motion."""
    chains = data.get("power_chains", [])
    lines = ["graph LR"]
    lines.append("  classDef active fill:#f9f,stroke:#333,stroke-width:3px")
    lines.append("  classDef low fill:#ddd,stroke:#999,stroke-width:1px")

    for chain in chains:
        chain_id = chain["id"]
        links = chain.get("motion_links", [])
        carriers = chain.get("active_carriers", [])

        for i, link in enumerate(links):
            node_id = f"{chain_id}_n{link['position']}"
            label = link["label"]
            intensity = link.get("intensity", 0)
            lines.append(f'  {node_id}["{label}<br/>i={intensity:.1f}"]')
            if intensity > 0.5:
                lines.append(f"  {node_id}:::active")
            else:
                lines.append(f"  {node_id}:::low")

            if i > 0:
                prev_id = f"{chain_id}_n{links[i-1]['position']}"
                lines.append(f"  {prev_id} --> {node_id}")

        # Show active carriers
        for j, carrier in enumerate(carriers):
            carrier_id = f"{chain_id}_c{j}"
            lines.append(f'  {carrier_id}(("{carrier}"))')
            last_node = f"{chain_id}_n{links[-1]['position']}" if links else chain_id
            lines.append(f"  {last_node} -.-> {carrier_id}")

    return "\n".join(lines)


def generate_fantasy_knots(data: Dict[str, Any]) -> str:
    """Generate Mermaid graph for fantasy knot structures."""
    knots = data.get("fantasy_knots", [])
    lines = ["graph TD"]
    lines.append("  classDef knot fill:#fcf,stroke:#c6c,stroke-width:2px")
    lines.append("  classDef filter fill:#ffc,stroke:#cc0,stroke-width:1px")

    for knot in knots:
        kid = knot["id"]
        pattern = knot.get("repetition_pattern", {})
        ptype = pattern.get("type", "unknown")
        freq = pattern.get("frequency", 0)
        force = knot.get("force_index", 0)

        lines.append(f'  {kid}{{"{kid}<br/>{ptype}<br/>freq={freq}, force={force:.1f}"}}')
        lines.append(f"  {kid}:::knot")

        # Show exclusivity filters
        for i, filt in enumerate(knot.get("exclusivity_filters", [])):
            fid = f"{kid}_f{i}"
            ftype = filt.get("filter_type", "unknown")
            lines.append(f'  {fid}["{ftype}"]')
            lines.append(f"  {fid}:::filter")
            lines.append(f"  {kid} --> {fid}")

            # Show excluded symbols
            for exc in filt.get("excluded_set", []):
                lines.append(f'  {fid} -.->|excludes| {exc}')

        # Show linked symbols
        for sym_id in pattern.get("linked_symbols", []):
            lines.append(f"  {sym_id} --> {kid}")

    return "\n".join(lines)


def generate_runtime_loop() -> str:
    """Generate Mermaid graph for the 10-stage runtime loop."""
    return """graph TD
  S1["Stage 1: 感受场进入<br/>Field Ingestion"]
  S2["Stage 2: 切片化<br/>Slicing"]
  S3["Stage 3: 凝固<br/>Freezing"]
  S4["Stage 4: 结构筛选<br/>Exclusivity Filtering"]
  S5["Stage 5: 符号化与秩序化<br/>Symbolization & Ordering"]
  S6["Stage 6: 命题生成<br/>Proposition Generation"]
  S7["Stage 7: 追问驱动<br/>Interrogation Driver"]
  S8["Stage 8: 巫术检测<br/>Witchcraft Detector"]
  S9["Stage 9: 权力链改写<br/>Power Rewrite"]
  S10["Stage 10: 输出封装<br/>Packaging"]

  S1 -->|fantasy_candidates| S2
  S2 -->|raw_symbols| S3
  S3 -->|frozen_symbols| S4
  S4 -->|exclusivity_filters| S5
  S5 -->|symbol_graph + knots| S6
  S6 -->|propositions| S7
  S7 -->|alternatives + feedback| S8
  S8 -->|scores + dispositions| S9
  S9 -->|rewritten_props + log| S10
  S10 -->|O1-O5| OUT["Output:<br/>O1 Symbol Graph<br/>O2 Rule Deck<br/>O3 Rewrite Log<br/>O4 Silence Report<br/>O5 Interrogation Seeds"]

  S8 -->|silence| SIL["Silence Report"]
  S7 -->|closed_warning| S8
  S10 -.->|next iteration| S1

  classDef stage fill:#e8f0fe,stroke:#4285f4,stroke-width:2px
  classDef output fill:#e6f4ea,stroke:#34a853,stroke-width:2px
  classDef warning fill:#fce8e6,stroke:#ea4335,stroke-width:1px

  class S1,S2,S3,S4,S5,S6,S7,S8,S9,S10 stage
  class OUT output
  class SIL warning"""


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid diagrams for Symbol Engine")
    parser.add_argument("--type", required=True,
                        choices=["symbol_graph", "power_chain", "fantasy_knots", "runtime_loop"],
                        help="Type of diagram to generate")
    parser.add_argument("--input", type=str, help="Path to JSON data file (not needed for runtime_loop)")
    parser.add_argument("--output", type=str, required=True, help="Output Mermaid file path (.mmd)")
    args = parser.parse_args()

    if args.type == "runtime_loop":
        mermaid_code = generate_runtime_loop()
    else:
        if not args.input:
            print("Error: --input required for this diagram type")
            return

        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}")
            return

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        generators = {
            "symbol_graph": generate_symbol_graph,
            "power_chain": generate_power_chain,
            "fantasy_knots": generate_fantasy_knots,
        }
        mermaid_code = generators[args.type](data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    print(f"Generated: {output_path}")
    print(f"Lines: {len(mermaid_code.splitlines())}")


if __name__ == "__main__":
    main()
