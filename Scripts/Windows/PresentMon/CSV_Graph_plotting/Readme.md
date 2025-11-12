# CSV Graph plotting
With this Python Script you can plot a Graph of your PresentMon CSV Output
<br>
This script is multiprocessed so it will look at a given folder and check any csv inside the source folder has already been plotted and if not then it will simultaneously plot svg's for all of the csv files at the same time.

The script does some conversion to overlay Animation Error data on top of the plotted FrameTime data to visualize Animation Error better and more compact.
<br>
Animation Error in this graph works by looking at the divergence of this AnimationErrors record and the average FrameTime 12 sample points before that, or better said just look if the Animation Error line shoots drasticly up or down which equals bad, the Animation Error line inside the graph is slightly scewed for the adjustment to overlay it on top of the other data, the level of inaccuracy should be extremely minimal and probably not noticeable from the ground truth, a AnimationError shoot to either upward or downward indicates a Display and or CPU delta **on that recorded frame** not on the next frame as PresentMon describes it in their documentation as this graph pulls the AnimationError values down by -1 to overlay it exactly with the corresponding frame.


Usecases are:
- visualizing various aspects of your game performance caption

You will need to download the PresentMon Application from [this](https://github.com/GameTechDev/PresentMon) Github repository to make use of this script here.

Python 3+ is required, then run the script in powershell or cmd like `python C:\folder\PresentMon_Graph.py` given that you have csv files from PresentMon captured with version 2.3.1 or newer in the directory where your csv files are saved in.

## Before you begin
This script uses PresentMon's default GUI Capture directory as default source for csv files to handle, if you want to change this behavior then open the script and change `Input_filePath` as well as `Output_filePath` to your liking.


Both the GUI version and the CLI version are supported but keep in mind that support might fail due to naming convention or data structure changes by Intel in future releases of PresentMon which requires manual fixing of this script.
