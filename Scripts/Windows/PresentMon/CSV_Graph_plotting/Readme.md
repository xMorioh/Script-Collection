# CSV Graph plotting
With this Python Script you can plot a Graph of your PresentMon CSV Output

Usecases are:
- visualizing various aspects of your game performance caption

You will need to download the PresentMon Application from [this](https://github.com/GameTechDev/PresentMon) Github repository to make use of this script here.

The Python Script does not come with any dependencies, you just need to download Python 3+ and install it and then run the script in powershell or cmd as `python C:\folder\PresentMon_Graph.py` given that you have csv files from PresentMon present in that directory.

## Before you begin
You should change the `Input_filePath` and `Output_filePath` Variables inside the script to define the Input and Output Paths of your files. Another requirement is that you execute the PresentMon application with the `--date_time` Parameter so that the csv Column `CPUStartDateTime` is populated with Date and Time values, the script does some conversion on that Column to calculate the Time axis correctly, if you don't do this then you may get wrong data outputs or even errors.