@echo off
TITLE EduTrack Pro - Frontend Dashboard
cd /d "%~dp0frontend"

echo ===================================================
echo   EduTrack Pro - Student Management System
echo   Launching Frontend in Default Web Browser...
echo ===================================================

start "" index.html

echo Frontend launched!
timeout /t 3 >nul
exit /b 0
