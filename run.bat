@echo off
cd /d "%~dp0"

set PYTHONPATH=%CD%\src

"%CD%\.venv\Scripts\python.exe" -m shell.main