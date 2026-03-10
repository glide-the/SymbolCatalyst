#!/usr/bin/env python3
"""
Asset download script for Symbol Engine Generator.

Downloads abstract visual assets from free API sources (Unsplash, Pexels, Google Fonts).
All assets are non-cultural, abstract/geometric only — enforced by search keywords.

Usage:
    python download_assets.py --type card-backgrounds --limit 5
    python download_assets.py --type card-backgrounds --limit 5 --api-key YOUR_UNSPLASH_KEY
    python download_assets.py --type symbol-icons --source lucide --limit 10
    python download_assets.py --type fonts
    python download_assets.py --type palettes
    python download_assets.py --all --limit 3

Environment variables (optional):
    UNSPLASH_ACCESS_KEY  - Unsplash API access key (for card-backgrounds)
    PEXELS_API_KEY       - Pexels API key (fallback for card-backgrounds)

If no API key is provided, generates placeholder SVG files instead.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Optional


# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
SKILL_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_ROOT / "assets"

# Abstract-only search terms (no cultural symbols)
SEARCH_QUERIES = {
    "card-backgrounds": [
        "abstract gradient texture",
        "dark minimal geometric",
        "abstract fluid art",
        "minimalist pattern dark",
    ],
    "symbol-icons": [
        "circle", "diamond", "hexagon", "triangle",
        "square", "octagon", "pentagon", "star-4",
    ],
}

# Lucide icon CDN base
LUCIDE_CDN = "https://unpkg.com/lucide-static@latest/icons"

# Google Fonts API (no key needed for CSS endpoint)
GOOGLE_FONTS_CSS = "https://fonts.googleapis.com/css2"

FONT_SPECS = {
    "NotoSansSC": {
        "family": "Noto Sans SC",
        "weights": [400, 700],
        "url": "https://fonts.google.com/noto/specimen/Noto+Sans+SC",
    },
    "Inter": {
        "family": "Inter",
        "weights": [400, 600, 700],
        "url": "https://fonts.google.com/specimen/Inter",
    },
    "JetBrainsMono": {
        "family": "JetBrains Mono",
        "weights": [400, 700],
        "url": "https://www.jetbrains.com/lp/mono/",
    },
    "LXGWWenKai": {
        "family": "LXGW WenKai",
        "weights": [400, 700],
        "url": "https://github.com/lxgw/LxgwWenKai",
    },
}

# Valence palette
VALENCE_PALETTE = {
    "tension":    {"primary": "#E63946", "secondary": "#F4845F", "label": "张力"},
    "oppression": {"primary": "#4A0E4E", "secondary": "#3D3D3D", "label": "压迫"},
    "seduction":  {"primary": "#E91E90", "secondary": "#FF69B4", "label": "诱惑"},
    "hesitation": {"primary": "#A8DADC", "secondary": "#B0B0B0", "label": "迟疑"},
    "clarity":    {"primary": "#06D6A0", "secondary": "#1D8A6E", "label": "清明"},
}


# ──────────────────────────────────────────────
# Utility
# ──────────────────────────────────────────────

def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def http_get(url: str, headers: Optional[Dict] = None, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "SymbolEngineGenerator/1.0"
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def http_get_json(url: str, headers: Optional[Dict] = None) -> Any:
    data = http_get(url, headers)
    return json.loads(data.decode("utf-8"))


def write_index(directory: Path, assets: List[Dict]):
    index_path = directory / "index.json"
    existing = []
    if index_path.exists():
        try:
            existing = json.loads(index_path.read_text("utf-8")).get("assets", [])
        except (json.JSONDecodeError, KeyError):
            pass
    existing.extend(assets)
    index_path.write_text(
        json.dumps({"assets": existing}, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  Updated index: {index_path} ({len(existing)} entries)")


# ──────────────────────────────────────────────
# Placeholder SVG generators
# ──────────────────────────────────────────────

def generate_card_placeholder(index: int, query: str, output_dir: Path) -> Dict:
    """Generate a placeholder SVG card background."""
    colors = ["#1a1a2e", "#16213e", "#0f3460", "#2c3333", "#1e1e2e"]
    accents = ["#e94560", "#a855f7", "#06d6a0", "#f4845f", "#a8dadc"]
    bg = colors[index % len(colors)]
    accent = accents[index % len(accents)]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="750" height="1050" viewBox="0 0 750 1050">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#000;stop-opacity:1" />
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="40%" r="60%">
      <stop offset="0%" style="stop-color:{accent};stop-opacity:0.15" />
      <stop offset="100%" style="stop-color:{accent};stop-opacity:0" />
    </radialGradient>
  </defs>
  <rect width="750" height="1050" fill="url(#bg)" />
  <rect width="750" height="1050" fill="url(#glow)" />
  <rect x="30" y="30" width="690" height="990" rx="12" fill="none" stroke="{accent}" stroke-opacity="0.3" stroke-width="1"/>
  <text x="375" y="525" text-anchor="middle" fill="{accent}" font-size="14" opacity="0.5">{query}</text>
</svg>"""

    filename = f"placeholder_{index:02d}.svg"
    (output_dir / filename).write_text(svg, encoding="utf-8")
    print(f"  ✓ Generated: {filename}")
    return {
        "filename": filename,
        "source": "placeholder",
        "source_url": "",
        "license": "generated",
        "usage": "card-background",
        "notes": f"Placeholder SVG — query: {query}",
    }


def generate_icon_placeholder(shape: str, output_dir: Path) -> Dict:
    """Generate a placeholder SVG icon for a symbol node."""
    shapes_svg = {
        "circle": '<circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "diamond": '<polygon points="12,2 22,12 12,22 2,12" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "hexagon": '<polygon points="12,2 21,7 21,17 12,22 3,17 3,7" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "triangle": '<polygon points="12,3 22,21 2,21" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "square": '<rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "octagon": '<polygon points="8,2 16,2 22,8 22,16 16,22 8,22 2,16 2,8" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "pentagon": '<polygon points="12,2 22,9 19,21 5,21 2,9" fill="none" stroke="currentColor" stroke-width="1.5"/>',
        "star-4": '<polygon points="12,2 14,10 22,12 14,14 12,22 10,14 2,12 10,10" fill="none" stroke="currentColor" stroke-width="1.5"/>',
    }
    inner = shapes_svg.get(shape, shapes_svg["circle"])
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="1.5">\n  {inner}\n</svg>'

    filename = f"{shape}.svg"
    (output_dir / filename).write_text(svg, encoding="utf-8")
    print(f"  ✓ Generated: {filename}")
    return {
        "filename": filename,
        "source": "placeholder",
        "source_url": "",
        "license": "generated",
        "usage": "symbol-icon",
        "notes": f"Geometric shape: {shape} — 流动态/凝固态/幻想结 node icon",
    }


# ──────────────────────────────────────────────
# Downloaders
# ──────────────────────────────────────────────

def download_card_backgrounds(limit: int, api_key: Optional[str] = None):
    """Download card backgrounds from Unsplash API or generate placeholders."""
    out_dir = ensure_dir(ASSETS_DIR / "card-backgrounds")
    assets = []

    if api_key:
        print(f"\n📥 Downloading card backgrounds from Unsplash (limit={limit})...")
        headers = {
            "Authorization": f"Client-ID {api_key}",
            "User-Agent": "SymbolEngineGenerator/1.0",
        }
        downloaded = 0
        for query in SEARCH_QUERIES["card-backgrounds"]:
            if downloaded >= limit:
                break
            url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(query)}&per_page={min(limit - downloaded, 5)}&orientation=portrait"
            try:
                data = http_get_json(url, headers)
                for photo in data.get("results", []):
                    if downloaded >= limit:
                        break
                    img_url = photo["urls"]["regular"]
                    photo_id = photo["id"]
                    filename = f"unsplash_{photo_id}.jpg"
                    filepath = out_dir / filename

                    if filepath.exists():
                        print(f"  ⏭ Skipped (exists): {filename}")
                        downloaded += 1
                        continue

                    img_data = http_get(img_url)
                    filepath.write_bytes(img_data)
                    print(f"  ✓ Downloaded: {filename}")
                    assets.append({
                        "filename": filename,
                        "source": "unsplash",
                        "source_url": photo["links"]["html"],
                        "license": "Unsplash License",
                        "usage": "card-background",
                        "notes": f"Query: {query} — {photo.get('description', 'abstract')}",
                    })
                    downloaded += 1
                    time.sleep(0.5)
            except urllib.error.HTTPError as e:
                print(f"  ✗ API error for query '{query}': {e}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
    else:
        print(f"\n🎨 No API key — generating {limit} placeholder card backgrounds...")
        queries = SEARCH_QUERIES["card-backgrounds"]
        for i in range(limit):
            query = queries[i % len(queries)]
            asset = generate_card_placeholder(i, query, out_dir)
            assets.append(asset)

    if assets:
        write_index(out_dir, assets)
    print(f"  Total: {len(assets)} card backgrounds")


def download_symbol_icons(limit: int, source: str = "placeholder"):
    """Download symbol icons from Lucide CDN or generate placeholders."""
    out_dir = ensure_dir(ASSETS_DIR / "symbol-icons")
    assets = []
    shapes = SEARCH_QUERIES["symbol-icons"][:limit]

    if source == "lucide":
        print(f"\n📥 Downloading symbol icons from Lucide CDN (limit={limit})...")
        for shape in shapes:
            filename = f"{shape}.svg"
            url = f"{LUCIDE_CDN}/{shape}.svg"
            filepath = out_dir / filename
            if filepath.exists():
                print(f"  ⏭ Skipped (exists): {filename}")
                continue
            try:
                svg_data = http_get(url)
                filepath.write_bytes(svg_data)
                print(f"  ✓ Downloaded: {filename}")
                assets.append({
                    "filename": filename,
                    "source": "lucide",
                    "source_url": f"https://lucide.dev/icons/{shape}",
                    "license": "ISC",
                    "usage": "symbol-icon",
                    "notes": f"Geometric shape for symbol node visualization",
                })
                time.sleep(0.3)
            except Exception as e:
                print(f"  ✗ Failed {shape}: {e}")
                asset = generate_icon_placeholder(shape, out_dir)
                assets.append(asset)
    else:
        print(f"\n🎨 Generating {len(shapes)} placeholder symbol icons...")
        for shape in shapes:
            asset = generate_icon_placeholder(shape, out_dir)
            assets.append(asset)

    if assets:
        write_index(out_dir, assets)
    print(f"  Total: {len(assets)} symbol icons")


def generate_palettes():
    """Generate valence palette JSON config."""
    out_dir = ensure_dir(ASSETS_DIR / "palettes")
    print("\n🎨 Generating valence palette config...")

    palette_file = out_dir / "valence_palette.json"
    palette_file.write_text(
        json.dumps(VALENCE_PALETTE, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  ✓ Generated: valence_palette.json")

    # Generate CSS variables
    css_lines = [":root {"]
    for dim, colors in VALENCE_PALETTE.items():
        css_lines.append(f"  --valence-{dim}-primary: {colors['primary']};")
        css_lines.append(f"  --valence-{dim}-secondary: {colors['secondary']};")
    css_lines.append("}")
    css_file = out_dir / "valence_palette.css"
    css_file.write_text("\n".join(css_lines), encoding="utf-8")
    print(f"  ✓ Generated: valence_palette.css")

    write_index(out_dir, [
        {"filename": "valence_palette.json", "source": "generated", "license": "n/a",
         "usage": "palette", "notes": "5-dimension valence color mapping"},
        {"filename": "valence_palette.css", "source": "generated", "license": "n/a",
         "usage": "palette", "notes": "CSS custom properties for valence colors"},
    ])


def generate_font_manifest():
    """Generate font manifest with download instructions (fonts are large, not auto-downloaded)."""
    out_dir = ensure_dir(ASSETS_DIR / "fonts")
    print("\n📝 Generating font manifest...")

    manifest = {
        "fonts": FONT_SPECS,
        "instructions": {
            "google_fonts": "Download from Google Fonts: https://fonts.google.com — search by family name",
            "lxgw_wenkai": "Download from GitHub releases: https://github.com/lxgw/LxgwWenKai/releases",
            "jetbrains_mono": "Download from: https://www.jetbrains.com/lp/mono/",
            "note": "Fonts are not auto-downloaded due to size. Use this manifest to fetch manually.",
        },
    }

    manifest_file = out_dir / "font_manifest.json"
    manifest_file.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  ✓ Generated: font_manifest.json")

    # Generate a helper script snippet
    helper = """#!/bin/bash
# Download fonts for Symbol Engine Generator
# Run from the skill root directory

FONT_DIR="assets/fonts"
mkdir -p "$FONT_DIR"

echo "Downloading Inter..."
curl -L -o "$FONT_DIR/Inter.zip" "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"

echo "Downloading JetBrains Mono..."
curl -L -o "$FONT_DIR/JetBrainsMono.zip" "https://github.com/JetBrains/JetBrainsMono/releases/latest/download/JetBrainsMono-2.304.zip"

echo "Downloading LXGW WenKai..."
curl -L -o "$FONT_DIR/LXGWWenKai.zip" "https://github.com/lxgw/LxgwWenKai/releases/latest/download/lxgw-wenkai-v1.501.zip"

echo ""
echo "Noto Sans SC: download manually from https://fonts.google.com/noto/specimen/Noto+Sans+SC"
echo ""
echo "Done. Unzip files in $FONT_DIR as needed."
"""
    helper_file = out_dir / "download_fonts.sh"
    helper_file.write_text(helper, encoding="utf-8")
    os.chmod(helper_file, 0o755)
    print(f"  ✓ Generated: download_fonts.sh")

    write_index(out_dir, [
        {"filename": "font_manifest.json", "source": "generated", "license": "n/a",
         "usage": "font-manifest", "notes": "Font specs and download instructions"},
        {"filename": "download_fonts.sh", "source": "generated", "license": "n/a",
         "usage": "font-downloader", "notes": "Bash script to download font files"},
    ])


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Download/generate visual assets for Symbol Engine Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate placeholders (no API key needed)
  python download_assets.py --type card-backgrounds --limit 5
  python download_assets.py --type symbol-icons --limit 8
  python download_assets.py --type palettes
  python download_assets.py --type fonts

  # Download from APIs
  python download_assets.py --type card-backgrounds --limit 5 --api-key YOUR_KEY
  python download_assets.py --type symbol-icons --source lucide --limit 8

  # Download everything
  python download_assets.py --all --limit 5

Environment:
  UNSPLASH_ACCESS_KEY   Unsplash API key (auto-used if set)
        """,
    )
    parser.add_argument(
        "--type",
        choices=["card-backgrounds", "symbol-icons", "palettes", "fonts"],
        help="Asset type to download/generate",
    )
    parser.add_argument("--all", action="store_true", help="Download/generate all asset types")
    parser.add_argument("--limit", type=int, default=5, help="Max items per type (default: 5)")
    parser.add_argument("--api-key", type=str, help="Unsplash API access key")
    parser.add_argument(
        "--source",
        choices=["placeholder", "lucide"],
        default="placeholder",
        help="Icon source: placeholder (SVG) or lucide (CDN download)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Override output base directory (default: <skill-root>/assets/)",
    )

    args = parser.parse_args()

    if args.output_dir:
        global ASSETS_DIR
        ASSETS_DIR = Path(args.output_dir)

    # Resolve API key from args or env
    api_key = args.api_key or os.environ.get("UNSPLASH_ACCESS_KEY")

    if not args.type and not args.all:
        parser.print_help()
        sys.exit(1)

    print(f"📦 Asset output directory: {ASSETS_DIR}")

    if args.all or args.type == "card-backgrounds":
        download_card_backgrounds(args.limit, api_key)

    if args.all or args.type == "symbol-icons":
        download_symbol_icons(args.limit, args.source)

    if args.all or args.type == "palettes":
        generate_palettes()

    if args.all or args.type == "fonts":
        generate_font_manifest()

    print("\n✅ Done.")


if __name__ == "__main__":
    main()
