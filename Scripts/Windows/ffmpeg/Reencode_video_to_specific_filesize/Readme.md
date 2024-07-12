# Reencode Video to specific Filesize
This script will reencode a Video with the best possible quality to a specific file size
What this will do is checking the input video duration, then calculating the bitrate from the duration and the specified target file size, pipe that to ffmpeg and dump the finished video wherever you specify.

Usecases are:
- shrinking a video down to 50MB for example to make it fit for websites or applications that have a upload limit like Discord.
- reencode a video to a different format to make it be readable by applications or websites that have strict limitations or support for different video formats.


The Format is choosable inside the script and supports every format that ffmpeg supports but keep in mind that by default this script will reencode the given video to VP9 to improve image quality at smaller file sizes, this means that you will definitely find someone on a phone or wherever who does not see the video embeded inside discord for example, you could however change that to x264 but with the definite issue of image quality being worse depending how long your videos typically are since longer videos mean less bitrate which equals to less overall quality. ffmpeg is very powerful so check the commands if you need something more specific for your usecases [here](https://ffmpeg.org/documentation.html) or [here](https://trac.ffmpeg.org/wiki#Encoding)

This Script also comes with some optimizations, these are optional but active by default, just delete the code block out of the script if you feel like they are unnecessary to you.

Instructions on how to set it up are written inside the powershell script.
The .bat file is just a batch to link to your desktop so you can easily double click it without needing to open the CLI for it all the time, it is best you have a dedicated folder for this script anyway since this runs ffmpeg in double pass which will create log files.

If necessary you can set the CPU priority class OS wide for ffmpeg to low, that way your OS wont hitch if ffmpeg uses up all your precious CPU performance. Encoding performance should be impacted rather minimal from this as far as i have been testing at least.

This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
Just extract both ffmpeg and ffprobe into the same folder where the .ps1 script lies the script will automatically find them this way.

A good comparison from x264, x265 and libvpx-vp9 can be found here: https://blogs.gnome.org/rbultje/2015/09/28/vp9-encodingdecoding-performance-vs-hevch-264/

Optionally: The Script has some parameters you can pass in CLI with arguments like so:
```
powershell -ex bypass -file "C:\Users\$env:USERNAME\Script-Collection\Scripts\Windows\ffmpeg\Reencode_video_to_specific_filesize\Reencode_video_to_specific_filesize.ps1",
-ffmpegPath "$PSScriptRoot\ffmpeg.exe",
-ffprobePath "$PSScriptRoot\ffprobe.exe",
-inputVideo "A:\input.*",
-outputPath "A:\output.mp4",
-targetVideoSize_megabytes 100,
-encoder "libvpx-vp9"
```
