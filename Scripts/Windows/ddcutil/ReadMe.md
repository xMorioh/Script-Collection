# Automate Monitor Brightness based on Daytime
This script utilizes [winddcutil](https://github.com/scottaxcell/winddcutil) to set a monitors brightness, the script in combination will set the brightness on a given Monitor to something you can specify according to your liking and it can also gradualy change brightness at given time intervals.

Usecases are:
- Automatically change Monitor Brightness depending on Daytime, for example, 100% Brightness from Morning to Sunset and then gradualy lower the brightness from Sunset to Evening.

This script requires you to download or compile [winddcutil](https://github.com/scottaxcell/winddcutil) and the path to it to be defined inside the script as well as your daytimes.

To actually make this automated you need to register a Scheduled Task in Windows, you may use the example in this very folder to import it in your Task Scheduler.
To make the Scheduled Task work you need to make sure that:
- First of all the Scheduled Task needs to run under your user, it does not require Admin rights and it will fail to run if you try to run it as SYSTEM User.
- And Secondly the Path to the RunHidden Visual Basic script needs to be defined in it and the Path to the AutomatedMonitorBrightness.ps1 script

With all of this out of the way, enjoy an automated Monitor Brightness change :)
