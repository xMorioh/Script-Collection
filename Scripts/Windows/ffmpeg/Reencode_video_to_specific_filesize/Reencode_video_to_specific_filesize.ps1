#-----Dependencies-----
# This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
$ffmpegPath = "$PSScriptRoot\ffmpeg.exe"
$ffprobePath = "$PSScriptRoot\ffprobe.exe"

#-----User Settings-----
$inputVideo = """A:\input.mp4"""
$outputPath = """A:\output.webm""" #only .webm is allowed due to VP9 encoding which discord supposedly only accepts in webm format
$targetVideoMegabytes = 50

#-----Script internals-----
$fileSizeInBits =  ($targetVideoMegabytes - 1) * 8388.608
$probedFileDuration = Invoke-Expression "&'$ffprobePath' -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $inputVideo"
$bitrate = ($fileSizeInBits / $probedFileDuration)
Invoke-Expression "
$ffmpegPath -i $inputVideo -c:v libvpx-vp9 -b:v $($bitrate)k -pass 1 -an -f null NUL
$ffmpegPath -i $inputVideo -c:v libvpx-vp9 -b:v $($bitrate)k -pass 2 -c:a libopus -row-mt 1 $outputPath
"