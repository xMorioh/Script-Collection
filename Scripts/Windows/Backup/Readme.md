# Backup Script
This Script uses Robocopy to Backup your files.
Robocopy as used here is a perfect incremental backup tool if you don't worry about verioncontrol, it's windows inbuilt and easy to use.

Usecases are:
- backing up your C drive files that you need for a drive failure at every boot of your PC
- backing up your projects manually before editing them
- or using it as a third backup when you already have a Backup folder on another drive and you want to backup that folder to an external drive once a week which is why this uses pnputil


For pnputil you need to find the device instance path from the device manager in Windows, it is highly recommended to use this on top of a physical switch like an outlet timer switch.
You can set Tasks in Windows Task scheduler to work with it, use as Action Program:`cmd.exe` Add arguments:`/c start /min C:\locate_your_script_here\Backup.bat ^& exit`

For an overview of Robocopys commands check out Microsofts website [robocopy](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy)