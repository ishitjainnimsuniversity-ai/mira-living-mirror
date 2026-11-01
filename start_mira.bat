@echo off
title MIRA - Ultra-Intelligent AI Mirror Companion
color 0D

echo =====================================================================
echo          MIRA - THE ENCHANTED LIVING SMART MIRROR COMPANION
echo =====================================================================
echo.
echo  [+] Initializing MIRA Smart Mirror...
echo  [+] Loading Fairytale Cinematic Gate...
echo  [+] Connecting to Gemini Intelligence Engine...
echo  [+] Opening in your browser at http://localhost:5050
echo.

cd /d "%~dp0"
if exist app.py (
    start http://localhost:5050
    python app.py
) else if exist mira_mirror\app.py (
    cd mira_mirror
    start http://localhost:5050
    python app.py
) else (
    echo [!] Could not locate app.py. Please verify path.
    pause
)
