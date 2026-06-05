@echo off
title Image Combiner — Build
cd /d "%~dp0"

echo ============================================
echo   Image Combiner — Windows Build
echo ============================================
echo.

:: ── Check Python ─────────────────────────────
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Install Python 3.10+ and check "Add Python to PATH".
    pause
    exit /b 1
)

:: ── Install dependencies ─────────────────────
echo [2/3] Installing dependencies...
pip install pyinstaller pillow >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    echo Try running manually: pip install pyinstaller pillow
    pause
    exit /b 1
)

:: ── Build ────────────────────────────────────
echo [3/3] Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.png ^
    --name=ImageCombiner ^
    --add-data "icon.png;." ^
    --noconfirm ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed. See the output above for details.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   BUILD SUCCESSFUL!
echo   Output: dist\ImageCombiner.exe
echo ============================================
echo.
pause
