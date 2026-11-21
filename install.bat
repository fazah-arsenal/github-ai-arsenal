@echo off
setlocal enabledelayedexpansion
title FAZAH AI Arsenal Auto-Installer v6.5

echo =========================================================================
echo       FAZAH AI ARSENAL v6.5 - AUTOMATIC ONE-CLICK INSTALLER
echo =========================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not found in PATH!
    echo [*] Attempting to auto-install Python via winget...
    winget install Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo [X] Please download and install Python 3 from https://www.python.org/downloads/
        echo     (Be sure to check "Add python.exe to PATH" during installation)
        pause
        exit /b 1
    )
)

echo [*] Bootstrapping pip and setuptools...
python -m pip install --upgrade pip setuptools --quiet

echo [*] Installing latest FAZAH AI Arsenal from GitHub...
python -m pip install -U "https://github.com/fazah-arsenal/github-ai-arsenal/archive/refs/heads/main.zip"

echo [*] Fixing Windows User PATH for pip and fazah...
python -m scripts.gh_arsenal install-reqs

echo [*] Auto-linking MCP clients (Antigravity, Cursor, Claude, Windsurf)...
python -m scripts.gh_arsenal link

echo.
echo =========================================================================
echo [OK] INSTALLATION COMPLETE! LAUNCHING FAZAH AI ARSENAL CONSOLE...
echo =========================================================================
echo.
python -m scripts.gh_arsenal console
