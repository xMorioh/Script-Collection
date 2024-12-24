@echo off
set /p "pName=Enter Process Name: "
set scriptPath=%~dp0
for /f "skip=1" %%a in ('forfiles /M PresentMon*.exe') do set exeFile=%%a
Start "[PresentMon] Watching Process: %pName%" "%scriptPath%%exeFile%" --process_name "%pName%" --terminate_on_proc_exit --date_time --exclude_dropped