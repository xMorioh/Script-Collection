param (

#-----Dependencies-----
# This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
[string]$ffmpegPath = "$PSScriptRoot\ffmpeg.exe",
[string]$ffprobePath = "$PSScriptRoot\ffprobe.exe",

#-----User Settings-----
[string]$inputVideo = "A:\input.*", #No need to specify the file extension
[string]$outputPath = "A:\output.gif"

)

#-----Script internals-----
$inputVideo = Get-ChildItem -Path $inputVideo #search for file extension via input name

#-----Optimizations-----
[int]$probedFileVideoWidth = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
[int]$probedFileVideoHeight = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
[string]$probedFileVideoFPS = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"

[string]$probedFileVideoWidthOptimized = $probedFileVideoWidth / 2
[string]$probedFileVideoHeightOptimized = $probedFileVideoHeight / 2
[string]$probedFileVideoFPSOptimized = [Data.DataTable]::New().Compute($probedFileVideoFPS, $null) / 2
#-----------------------

Write-Host "-----DEBUGGING START-----"
Write-Host "probedFileVideoWidth          :" $probedFileVideoWidth
Write-Host "probedFileVideoWidthOptimized :" $probedFileVideoWidthOptimized
Write-Host "probedFileVideoHeight         :" $probedFileVideoHeight
Write-Host "probedFileVideoHeightOptimized:" $probedFileVideoHeightOptimized
Write-Host "probedFileVideoFPS            :" $probedFileVideoFPS
Write-Host "probedFileVideoFPSOptimized   :" $probedFileVideoFPSOptimized
Write-Host "-----DEBUGGING END-----"

[string]$palette = """$PSScriptRoot\palette.png"""
$filters="fps=""$probedFileVideoFPSOptimized"",scale=""$probedFileVideoWidthOptimized"":""$probedFileVideoHeightOptimized"":flags=lanczos"

Invoke-Expression "
$ffmpegPath -v warning -i '$inputVideo' -vf '$filters,palettegen' -y $palette
$ffmpegPath -v warning -i '$inputVideo' -i $palette -lavfi '$filters [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=3' -y '$outputPath'
"