@echo off
setlocal

set "DASHBOARD_ROOT=%~dp0"
set "SCRIPT_PATH=%DASHBOARD_ROOT%execution_dashboard_resources\generate_execution_dashboard.ps1"
set "OUTPUT_PATH=%DASHBOARD_ROOT%execution_dashboard_resources\execution_items_kanban.html"
set "WORKSPACE_ROOT=%DASHBOARD_ROOT%.."

powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%" -WorkspaceRoot "%WORKSPACE_ROOT%" -OutputHtmlPath "%OUTPUT_PATH%"
if errorlevel 1 exit /b %errorlevel%

start "" "%OUTPUT_PATH%"
