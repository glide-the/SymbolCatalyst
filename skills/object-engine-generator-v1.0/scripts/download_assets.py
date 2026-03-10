#!/usr/bin/env python3
"""
Download visual assets from Pinterest for Symbol Engine Generator.

Usage:
    python download_assets.py --type card-backgrounds --limit 10
    python download_assets.py --type character-illustrations --limit 10
    python download_assets.py --type world-materials --limit 10
"""

import argparse
import json
import time
from pathlib import Path
from typing import List
import urllib.request
from urllib.parse import quote


# Pinterest search URLs (already URL-encoded)
PINTEREST_URLS = {
    "card-backgrounds": "https://www.pinterest.com/search/pins/?q=塔罗牌&rs=srs&b_id=5478440932586243194&source_id=5478440938896572245&request_params=%7B%227%22%3A%20%225478440938896572245%22%2C%20%228%22%3A%20%225478440932586243194%22%2C%20%221%22%3A%20%22139%22%7D&view_parameter_type=3903&pins_display=3&quick_save_icon=1",
    "character-illustrations": "https://www.pinterest.com/search/pins/?q=人物插图&rs=srs&b_id=5478440932586243195&source_id=5478440938896572245&request_params=%7B%227%22%3A%20%225478440938896572245%22%2C%20%228%22%3A%20%225478440932586243195%22%2C%20%221%22%3A%20%22139%22%7D&view_parameter_type=3903&pins_display=3&quick_save_icon=1",
    "world-materials": "https://www.pinterest.com/search/pins/?q=废土风格素材&rs=srs"
}


def download_image(url: str, output_path: Path, timeout: int = 30) -> bool:
    """Download a single image from URL."""
    try:
        # Create user agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())

        print(f"✓ Downloaded: {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False


def create_placeholder_images(asset_type: str, limit: int, output_dir: Path):
    """Create placeholder SVG images with descriptive content."""

    colors = {
        "card-backgrounds": "#1a1a2e",
        "character-illustrations": "#16213e",
        "world-materials": "#0f3460"
    }

    accent_colors = {
        "card-backgrounds": "#e94560",
        "character-illustrations": "#e94560",
        "world-materials": "#533483"
    }

    base_color = colors.get(asset_type, "#1a1a2e")
    accent = accent_colors.get(asset_type, "#e94560")

    for i in range(limit):
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="600" fill="{base_color}"/>

  <!-- Decorative border -->
  <rect x="20" y="20" width="360" height="560" fill="none" stroke="{accent}" stroke-width="2"/>

  <!-- Corner decorations -->
  <path d="M 20 20 L 60 20 L 20 60 Z" fill="{accent}"/>
  <path d="M 380 20 L 340 20 L 380 60 Z" fill="{accent}"/>
  <path d="M 20 580 L 60 580 L 20 540 Z" fill="{accent}"/>
  <path d="M 380 580 L 340 580 L 380 540 Z" fill="{accent}"/>

  <!-- Center text -->
  <text x="200" y="280" font-family="Arial, sans-serif" font-size="24" fill="{accent}" text-anchor="middle">
    {asset_type.replace('-', ' ').title()}
  </text>
  <text x="200" y="320" font-family="Arial, sans-serif" font-size="16" fill="#ffffff" text-anchor="middle" opacity="0.7">
    Placeholder #{i+1}
  </text>

  <!-- Pattern overlay -->
  <circle cx="100" cy="100" r="3" fill="{accent}" opacity="0.5"/>
  <circle cx="300" cy="100" r="3" fill="{accent}" opacity="0.5"/>
  <circle cx="100" cy="500" r="3" fill="{accent}" opacity="0.5"/>
  <circle cx="300" cy="500" r="3" fill="{accent}" opacity="0.5"/>
</svg>"""

        output_path = output_dir / f"placeholder_{i+1:03d}.svg"
        output_path.write_text(svg_content, encoding="utf-8")

    print(f"✓ Created {limit} placeholder SVGs for {asset_type}")


def create_asset_index(asset_dir: Path, asset_type: str) -> dict:
    """Create an index file listing all assets."""

    image_files = list(asset_dir.glob("*.png")) + list(asset_dir.glob("*.jpg")) + list(asset_dir.glob("*.svg"))

    index = {
        "asset_type": asset_type,
        "total_count": len(image_files),
        "assets": [
            {
                "filename": f.name,
                "path": str(f.relative_to(asset_dir.parent)),
                "type": f.suffix[1:]  # Remove the dot
            }
            for f in sorted(image_files)
        ]
    }

    index_path = asset_dir / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"✓ Created index: {index_path}")
    return index


def main():
    parser = argparse.ArgumentParser(description="Download visual assets from Pinterest")
    parser.add_argument("--type", required=True, choices=["card-backgrounds", "character-illustrations", "world-materials"])
    parser.add_argument("--limit", type=int, default=10, help="Number of images to download")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent.parent / "assets")

    args = parser.parse_args()

    asset_type = args.type
    output_dir = args.output_dir / asset_type
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Preparing assets: {asset_type}")
    print(f"{'='*60}\n")

    # Note: Pinterest requires authentication and uses dynamic JavaScript,
    # so direct scraping is difficult. Instead, we'll create placeholders
    # and provide instructions for manual download.

    print("⚠ Note: Pinterest requires authentication for bulk downloads.")
    print("Creating placeholder assets for now...\n")

    # Create placeholder SVG images
    create_placeholder_images(asset_type, args.limit, output_dir)

    # Create index
    index = create_asset_index(output_dir, asset_type)

    # Save README with manual download instructions
    readme_path = output_dir / "README.md"
    readme_content = f"""# {asset_type.replace('-', ' ').title()}

## Asset Information

- **Total Count**: {index['total_count']}
- **Type**: Visual assets for Symbol Engine Generator

## Manual Download Instructions

To download actual images from Pinterest:

1. Visit: {PINTEREST_URLS.get(asset_type, 'https://www.pinterest.com/')}
2. Click on images you like
3. Right-click → "Save image as..."
4. Save to this directory (replace placeholder files)

## Asset Index

See `index.json` for the complete list of assets.

## Naming Convention

Use descriptive names:
- `card_bg_001_mystic.png` (for card backgrounds)
- `character_trader_001.png` (for character illustrations)
- `world_wasteland_001.png` (for world materials)

## Recommended Image Specs

- **Format**: PNG or SVG (for transparency support)
- **Resolution**: Minimum 800x1200 for cards, 512x512 for characters
- **Style**: Consistent with your game's visual identity
"""

    readme_path.write_text(readme_content, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"✓ Assets prepared: {asset_type}")
    print(f"  Directory: {output_dir}")
    print(f"  Count: {args.limit} placeholder files")
    print(f"\n📝 See {readme_path} for manual download instructions")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
