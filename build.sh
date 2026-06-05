#!/bin/bash
# Image Combiner — Linux Build
cd "$(dirname "$0")"

echo "============================================"
echo "  Image Combiner — Linux Build"
echo "============================================"
echo

# ── Check Python ─────────────────────────────
echo "[1/3] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Install Python 3.10+ and try again."
    exit 1
fi

PYTHON_CMD="python3"

# ── Install dependencies ─────────────────────
echo "[2/3] Installing dependencies..."
$PYTHON_CMD -m pip install pyinstaller pillow > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    echo "Try running manually: pip3 install pyinstaller pillow"
    exit 1
fi

# ── Build ────────────────────────────────────
echo "[3/3] Building executable..."
$PYTHON_CMD -m PyInstaller \
    --onefile \
    --windowed \
    --name=ImageCombiner \
    --add-data "icon.png:." \
    --noconfirm \
    --clean \
    main.py

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Build failed. See the output above for details."
    exit 1
fi

echo
echo "============================================"
echo "  BUILD SUCCESSFUL!"
echo "  Output: dist/ImageCombiner"
echo "============================================"
echo
