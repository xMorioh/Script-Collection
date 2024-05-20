#-----Dependencies-----
# This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
$ffmpegPath = "$PSScriptRoot\ffmpeg.exe"
$ffprobePath = "$PSScriptRoot\ffprobe.exe"

#-----User Settings-----
$inputVideo = "A:\input.*" #No need to specify the file extension
$outputPath = "A:\output.mp4"
$targetVideo_megabytes = 50

#-----Script internals-----
$inputVideo = Get-ChildItem -Path $inputVideo #search for file extension via input name

$probedFileDuration = Invoke-Expression "&'$ffprobePath' -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"

[float]$probedFileVideoBitrate = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
[float]$probedFileVideoBitrate_kbit = $probedFileVideoBitrate * 0.001

[float]$probedFileAudioBitrate = Invoke-Expression "&'$ffprobePath' -v error -select_streams a -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
[float]$AudioSize_megabytes = (($probedFileAudioBitrate * $probedFileDuration) / 8388608)

[float]$targetFileSize_kbit =  (($targetVideo_megabytes - $AudioSize_megabytes - 1) * 8192)
[float]$OutputBitrate_kbit = $targetFileSize_kbit / $probedFileDuration

Write-Host "-----DEBUGGING-----"
Write-Host "probedFileDuration                    :" $probedFileDuration
Write-Host "probedFileVideoBitrate                :" $probedFileVideoBitrate
Write-Host "probedFileVideoBitrate_kbit           :" $probedFileVideoBitrate_kbit
Write-Host "probedFileAudioBitrate                :" $probedFileAudioBitrate
Write-Host "AudioSize_megabytes                   :" $AudioSize_megabytes
Write-Host "targetFileSize_kbit                   :" $targetFileSize_kbit
Write-Host "OutputBitrate_kbit before Optimization:" $OutputBitrate_kbit

#-----Optimizations-----
if ($OutputBitrate_kbit -gt $probedFileVideoBitrate_kbit) {
$OutputBitrate_kbit = $probedFileVideoBitrate_kbit
}
if ($OutputBitrate_kbit -gt 10000) {
$OutputBitrate_kbit = 10000
}
#-----------------------

Write-Host "OutputBitrate_kbit after Optimization :" $OutputBitrate_kbit
Write-Host "-----DEBUGGING END-----"

Invoke-Expression "
$ffmpegPath -i '$inputVideo' -c:v libvpx-vp9 -b:v $($OutputBitrate_kbit)k -pass 1 -an -row-mt 1 -f null NUL
$ffmpegPath -i '$inputVideo' -c:v libvpx-vp9 -b:v $($OutputBitrate_kbit)k -pass 2 -c:a copy -row-mt 1 '$outputPath'
"