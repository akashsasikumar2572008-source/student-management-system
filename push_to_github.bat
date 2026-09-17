@echo off
TITLE Push to GitHub - Student Management System
cd /d "%~dp0"

echo ========================================================
echo   Pushing Student Management System to GitHub
echo   Target: https://github.com/akashsasikumar2572008-source/student-management-system
echo ========================================================

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/
    echo or run in PowerShell: winget install --id Git.Git -e --source winget
    echo.
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
if not exist .git (
    git init
)

echo [2/5] Staging all project files...
git add .

echo [3/5] Creating initial commit...
git commit -m "Initial commit: Complete CRUD Student Management System following SOP guidelines"

echo [4/5] Setting branch to main and linking remote repository...
git branch -M main
git remote remove origin >nul 2>nul
git remote add origin https://github.com/akashsasikumar2572008-source/student-management-system.git

echo [5/5] Pushing to GitHub (Authentication window may appear)...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! Project successfully pushed to GitHub:
    echo   https://github.com/akashsasikumar2572008-source/student-management-system
    echo ========================================================
) else (
    echo.
    echo [NOTE] If your GitHub repo was created with an existing README/license, run:
    echo        git pull origin main --allow-unrelated-histories --no-rebase
    echo        git push -u origin main
)

pause
