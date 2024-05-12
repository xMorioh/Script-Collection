pnputil /enable-device "USB\VID_0BC2&PID_A0A4\MSFT30NA5K3776"
timeout 5
robocopy "F:\Backups" "S:\Backups\Backups" /MIR /B /E /MT:12 /XO /IT
robocopy "\\192.168.0.200\Your Network Folder" "S:\Your Network Folder" /MIR /B /E /MT:12 /XO /IT
timeout 50
pnputil /disable-device "USB\VID_0BC2&PID_A0A4\MSFT30NA5K3776"