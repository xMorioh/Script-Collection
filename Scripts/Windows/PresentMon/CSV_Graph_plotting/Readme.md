# CSV Graph plotting
With this Python Script you can plot a Graph of your PresentMon CSV Output
<br>
This script is multiprocessed so it will look at a given folder and check any csv inside the source folder has already been plotted and if not then it will simultaneously plot svg's for all of the csv files at the same time.

The script does some conversion to overlay Animation Error data on top of the plotted CPUBusy data to visualize Animation Error better and more compact.
<br>
**Animation Error in this graph works by looking at the divergence of CPUBusy and the Animation Error value**, the Animation Error value should either over or undershoot slightly for every record, this indicates a Display and or CPU delta on that recorded frame aka. a Animation Error, in an ideal world the Animation Error line should exactly match the CPUBusy line aka. no animation Error present at all.
<br>
Keep in mind that overlaying the Animation Error data on top of the CPUBusy data will slightly scew the Animation Error data visualized inside the graph, you can look at the Lowest/Highest/Median values to get a summarized ground thuth of the values or comment out the block inside the script for it to visualize Animation Error on the 0 point.

Usecases are:
- visualizing various aspects of your game performance caption

You will need to download the PresentMon Application from [this](https://github.com/GameTechDev/PresentMon) Github repository to make use of this script here.

Python 3+ is required, then run the script in powershell or cmd like `python C:\folder\PresentMon_Graph.py` given that you have csv files from PresentMon captured with version 2.3.1 or newer in the directory where your csv files are saved in.

## Before you begin
Regardless of anything, first you should change the `Input_filePath` and `Output_filePath` Variables inside the script to define the Input and Output Paths of your files.


Another requirement is that you execute the PresentMon application with the `--date_time` Parameter so that the csv Column `CPUStartDateTime` is populated with Date and Time values, the script does some conversion on that Column to calculate the Time axis correctly, if you don't do this then you may get wrong data outputs or even errors, also keep in mind that this is CPU-Time, not the time as on your clock or watch, PresentMon does not offer nor should it offer that. But if you'd like you can just use the Quick_Launcher option that i provide in this Github repo which will take care of that for you.
