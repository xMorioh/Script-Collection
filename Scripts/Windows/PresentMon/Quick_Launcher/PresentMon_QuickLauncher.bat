@echo off
set /p pName="Enter Process Name: "
set exePath=C:\Program Files\Intel\PresentMon\PresentMonConsoleApplication
for /f "skip=1" %%a in ('forfiles /P "%exePath%" /M PresentMon*.exe') do set exeFile=%%a
Start "[PresentMon] Watching Process: %pName%" "%exePath%\%exeFile%" --process_name "%pName%" --terminate_on_proc_exit --exclude_dropped