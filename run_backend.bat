@echo off
TITLE EduTrack Pro - Django Backend Server
cd /d "%~dp0backend"

echo ===================================================
echo   EduTrack Pro - Student Management System
echo   Starting Django REST Backend Server...
echo ===================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in your PATH!
    echo Please install Python 3.10+ or add python.exe to your PATH environment variable.
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -m pip install -q -r requirements.txt

echo [2/3] Applying database migrations...
python manage.py migrate

if not exist db.sqlite3 (
    echo [2.5/3] Seeding initial database records...
    python seed_data.py
)

echo [3/3] Launching server on http://127.0.0.1:8000/api/ ...
python manage.py runserver 127.0.0.1:8000

pause
