# CSV Graph plotting
With this Python Script you can plot a Graph of your PresentMon CSV Output
This script is multiprocessed so it will look at a given folder and check any csv inside the source folder has already been plotted and if not then it will simultaneously plot svg's for all of the csv files at the same time.
The script does some conversion to overlay recorded Animation Error on top of the plot to visualize Animation Error better.

Usecases are:
- visualizing various aspects of your game performance caption

You will need to download the PresentMon Application from [this](https://github.com/GameTechDev/PresentMon) Github repository to make use of this script here.

Python 3+ is required, then run the script in powershell or cmd like `python C:\folder\PresentMon_Graph.py` given that you have csv files from PresentMon captured with version 2.3.1 or newer in that directory.

## Before you begin
You should change the `Input_filePath` and `Output_filePath` Variables inside the script to define the Input and Output Paths of your files.
Another requirement is that you execute the PresentMon application with the `--date_time` Parameter so that the csv Column `CPUStartDateTime` is populated with Date and Time values, the script does some conversion on that Column to calculate the Time axis correctly, if you don't do this then you may get wrong data outputs or even errors, also keep in mind that this is CPU-Time, not the time as on your clock or watch, PresentMon does not offer nor should it offer that. But if you'd like you can just use the Quick_Launcher option that i provide in this Github repo which will take care of that for you.
