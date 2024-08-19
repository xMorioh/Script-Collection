# Convert Video to GIF
This script will convert a Video to a gif format.
What this will do is checking the input video, then optimizing some of it's values for the gif, pipe that to ffmpeg and dump the finished gif wherever you specify.

Usecases are:
- converting a video to a gif when necessary, if video files are possible to use then make sure to check out my other script "Reencode_video_to_specific_filesize"

The GIF format is extremely old by now and that shows, compared to video files with temporal optimizations the gif format severely lacks in quality but is insdead supported by almost if not all devices. Also if you need it, ffmpeg is very powerful so check the commands if you need something more specific for your usecases [here](https://ffmpeg.org/documentation.html)

This Script comes with some optimizations, these are optional but active by default, just delete the code block out of the script if you feel like they are unnecessary to you but they are strongly recommended to be left in or maybe just tweaked by the User if necessary, they keep the file size as low as possible without destroying the final image quality.

Instructions on how to set it up are written inside the powershell script.
The .bat file is just a batch to link to your desktop so you can easily double click it without needing to open the CLI for it all the time or to drag and drop a bunch of files onto it to convert a batch of videos in one go, it is best you have a dedicated folder for this script anyway since this runs ffmpeg in double pass which will create a color palette in png format for each run.

If necessary you can set the CPU priority class OS wide for ffmpeg to low, that way your OS wont hitch if ffmpeg uses up all your precious CPU performance. Encoding performance should be impacted rather minimal from this as far as i have been testing at least.

This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
Just extract both ffmpeg and ffprobe into the same folder where the .ps1 script lies the script will automatically find them this way.

Optionally: The Script has some parameters you can pass in CLI with arguments like so:
```
powershell -ex bypass -file "C:\Users\$env:USERNAME\Script-Collection\Scripts\Windows\ffmpeg\Convert_video_to_gif\Convert_Video_to_gif.ps1",
-ffmpegPath "$PSScriptRoot\ffmpeg.exe",
-ffprobePath "$PSScriptRoot\ffprobe.exe",
-inputVideo "A:\input.*",
-outputPath "A:\output.gif"
```
