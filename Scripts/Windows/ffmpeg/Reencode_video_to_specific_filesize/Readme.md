# Reencode Video to specific Filesize
This script will reencode a Video with the best possible quality to a specific file size
What this will do is checking the input video duration, then calculating the bitrate out of it, pipe that to ffmpeg and dump the finished video wherever you specify.

Usecases are:
- shrinking a video down to 50MB for example to fit for websites or applications that have a upload limit like Discord


Keep in mind that this will reencode the video to VP9 to improve image quality at smaller file sizes, this means that you will definitely find someone on a phone or wherever who does not see the video embeded inside discord, you could however change that to x264 but with the definite issue of image quality being much worse depending how long your videos typically are since longer videos mean less bitrate which equals to less overall quality. ffmpeg is very powerful so check the commands if you need something more specific for your usecases [here](https://ffmpeg.org/documentation.html)

This Script also comes with some optimizations, these are optional but active by default, just delete the code block out of the script if you feel like they are unnecessary to you.

Instructions on how to set it up are written inside the powershell script.
The .bat file is just a batch to link to your desktop so you can easily double click it without needing to open the CLI for it all the time, it is best you have a dedicated folder for it anyway since this runs ffmpeg in double pass which will create logs files.

If necessary you can set the CPU priority class OS wide for ffmpeg to low, that way your OS wont hitch if it uses up all your precious CPU performance. Encoding performance should be impacted rather minimal as far as i have been testing at least.

This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip