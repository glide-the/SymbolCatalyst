#!/bin/bash
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
