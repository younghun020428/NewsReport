@echo off
setlocal
:: Move to the directory where the batch file is located
cd /d "%~dp0"

:: Locate py launcher using environment variable (handles Korean usernames automatically)
set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Launcher\py.exe"
if not exist "%PY_EXE%" set "PY_EXE=py"

echo Running News Curation Pipeline...
"%PY_EXE%" "scripts\00_main_pipeline.py"

if %ERRORLEVEL% neq 0 (
    echo [ERROR] Pipeline execution failed.
    pause
)
