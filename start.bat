@echo off
title Image Combiner
cd /d "%~dp0"

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to your system PATH.
    echo Please install Python 3.10+ and ensure the option "Add Python to PATH" is checked.
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found. Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies automatically.
        echo Please try running: pip install -r requirements.txt manually.
        pause
        exit /b 1
    )
)

echo Launching Image Combiner...
python main.py
if errorlevel 1 (
    echo [ERROR] Application exited with an error code.
    pause
)
