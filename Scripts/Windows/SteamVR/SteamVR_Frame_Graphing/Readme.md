# SteamVR CSV Graph plotting
With these Python Scripts you can plot Graphs of your SteamVR VRFrames.csv file.
<br>
Within SteamVR you can save the FrameTiming of your VR session onto disc which results in a VRFrames.csv file being saved in "YourSteamInstallationFolder\Steam\logs"

What these scripts aim for is to provide a visualization of the SteamVR advanced frame timing graph but offline for post visualization.
<br>
If you want to learn more about the data itself and how to read it then you can read more about it [here](https://developer.valvesoftware.com/wiki/SteamVR/Frame_Timing)


Usecases are:
- visualizing various aspects of your VR session performance caption

Python 3+ is required, then run the scripts in powershell or cmd like `python C:\folder\SteamVR_Graph_CPU_GPU.py` or `python C:\folder\SteamVR_Graph_FrameTimes.py`.

## Before you begin
The scripts use SteamVR's default Log directory as default source for the csv file to handle, if you want to change this behavior then open the script and change `Input_filePath` as well as `Output_filePath` to your liking.

These scripts will create svg files based on the data inside the csv file and name it according to the last modification date on the VRFrames.csv file itself.
