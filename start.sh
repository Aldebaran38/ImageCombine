#!/bin/bash
# Move to the script's directory
cd "$(dirname "$0")"

echo "Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in your system PATH."
    echo "Please install Python 3.10+ and try again."
    exit 1
fi

PYTHON_CMD="python3"

echo "Checking dependencies..."
if ! $PYTHON_CMD -c "import PIL" &> /dev/null; then
    echo "Dependencies not found. Installing requirements..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies automatically."
        echo "Please try running: pip3 install -r requirements.txt manually."
        exit 1
    fi
fi

echo "Launching Image Combiner..."
$PYTHON_CMD main.py
