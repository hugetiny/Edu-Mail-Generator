@echo off
echo EDU MAIL GENERATOR - Windows Launcher
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if setup has been run
if not exist "config.json" (
    echo.
    echo Configuration not found. Running setup...
    python setup_modern.py
    if errorlevel 1 (
        echo Setup failed!
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found
    echo Please copy .env.example to .env and configure your email
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        echo Cancelled by user
        pause
        exit /b 0
    )
)

REM Run the generator
echo.
echo Starting Edu Mail Generator...
echo.
python edu_mail_generator.py

echo.
echo Generator finished. Check generated_accounts.txt for results.
pause
