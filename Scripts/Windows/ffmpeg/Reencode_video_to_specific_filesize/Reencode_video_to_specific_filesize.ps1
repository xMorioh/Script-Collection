param (

#-----Dependencies-----
# This Script requires ffmpeg as well as ffprobe, both can be found here: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
[string]$ffmpegPath = "$PSScriptRoot\ffmpeg.exe",
[string]$ffprobePath = "$PSScriptRoot\ffprobe.exe",

#-----User Settings-----
[string]$inputVideo = "A:\input.*", #No need to specify the file extension
[string]$outputPath = "A:\output.mp4",
[int]$targetVideoSize_megabytes = 50,
[string]$encoder = "libvpx-vp9" #Choose your prefered Encoder Library, for example x264=libx264, VP9=libvpx-vp9, AV1=libsvtav1

)

#-----Script internals-----
$inputVideo = Get-ChildItem -Path $inputVideo #search for file extension via input name

$probedFileDuration = Invoke-Expression "&'$ffprobePath' -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"

[string]$probedFileVideoFPS = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
$probedFileVideoFPSConverted = [Data.DataTable]::New().Compute($probedFileVideoFPS, $null)
$OutputFPS = $probedFileVideoFPSConverted

#Try to get Video Stream bitrate, catch if containers like MKV are in use which do not support stream metadata embedding
#To mitigate streamless container size overflow of the final size, we subtract 10% here which worked best so far.
try {
[float]$probedFileVideoBitrate = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
}
catch {
[float]$probedFileVideoBitrate = Invoke-Expression "&'$ffprobePath' -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
$targetVideoSize_megabytes = ($targetVideoSize_megabytes * 0.9)
}
[float]$probedFileVideoBitrate_kbit = $probedFileVideoBitrate * 0.001

#Try to get Audio Stream bitrate, catch if containers like MKV are in use which do not support stream metadata embedding
#If Stream could not be found then Audio is embedded in the Video Stream or not present at all
try {
[float]$probedFileAudioBitrate = Invoke-Expression "&'$ffprobePath' -v error -select_streams a -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
}
catch {
[float]$probedFileAudioBitrate = 0
}
[float]$AudioSize_megabytes = (($probedFileAudioBitrate * $probedFileDuration) / 8388608)

[float]$targetFileSize_kbit =  (($targetVideoSize_megabytes - $AudioSize_megabytes - 1) * 8192)
[float]$OutputBitrate_kbit = $targetFileSize_kbit / $probedFileDuration

Write-Host "-----DEBUGGING START-----"
Write-Host
if ($probedFileAudioBitrate -eq 0) {
Write-Host "Audio is embedded in the Video Bitrate due to a format being used that does not support stream based metadata embedding"
}
Write-Host
Write-Host "probedFileDuration                    :" $probedFileDuration
Write-Host "probedFileVideoBitrate                :" $probedFileVideoBitrate
Write-Host "probedFileVideoBitrate_kbit           :" $probedFileVideoBitrate_kbit
Write-Host "probedFileAudioBitrate                :" $probedFileAudioBitrate
Write-Host "AudioSize_megabytes                   :" $AudioSize_megabytes
Write-Host "targetFileSize_kbit                   :" $targetFileSize_kbit
Write-Host "OutputFPS          before Optimization:" $OutputFPS
Write-Host "OutputBitrate_kbit before Optimization:" $OutputBitrate_kbit

#-----Optimizations-----
#Limit kbit to the original videos kbit if it's lower than our calculation since wizards do not actually exist and the gain would be too small if any.
    if ($OutputBitrate_kbit -gt $probedFileVideoBitrate_kbit) {
        $OutputBitrate_kbit = $probedFileVideoBitrate_kbit
    }

#Check if the Framerate is above 60fps, if so we limit it by halfing the fps since most monitors only support up to 60fps, 61 because fps can be 60.000001 or something like that.
#This way can focus more of our Bitrate to each individual frame, leaving us with a better image quality overall.
    if ($OutputFPS -gt 61) {
        $OutputFPS = $OutputFPS / 2
    }

#--Check if we can use libx264 instead to save on encoding time if the exact same quality can be achieved in our targetVideoSize, we do not change $OutputBitrate_kbit here we still use target max kbit.
    [int]$probedFileVideoWidth = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=width -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
    [int]$probedFileVideoHeight = Invoke-Expression "&'$ffprobePath' -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 '$inputVideo'"
    [int]$probedFileVideoPixels = ($probedFileVideoWidth * $probedFileVideoHeight)

    $probedFileVideoFPSMultiplier = $OutputFPS / 30
    #Info: 0.00125 = ((((Baseline kbit (500kbit) / 1280*720 assuming the 500Kkbit are good for a 30fps video at that resolution) * 2) + 10%) to get a base quality number meaning kbit for each pixel per second @30fps
    #*2 + 10% = x2 is for the x264 codec uplift since VP9/AV1 has around 50% better quality compared and then just 10% on top for good measure + rounding up, $probedFileVideoFPSMultiplier right below here is for 30fps to 60fps when 500kbit look good at 30fps.
    $x264Check_kbit = (0.00125 * $probedFileVideoFPSMultiplier) * $probedFileVideoPixels
    $x264Check_megabytes = (((($x264Check_kbit * $probedFileDuration) / 8192) + 1) + $AudioSize_megabytes)
    if ($x264Check_megabytes -lt $targetVideoSize_megabytes) {
        $encoder = "libx264"
    }
#--Check end

#Limit kbit for user set encoder, this way we can get away with a much lower filesize in some scenarios, we only do this if the encoder is not x264 as x264 benefits much more from more Bitrate, hence the elseif
    elseif ($OutputBitrate_kbit -gt 10000) {
        $OutputBitrate_kbit = 10000
	}
#-----------------------

Write-Host "OutputFPS          after Optimization :" $OutputFPS
Write-Host "OutputBitrate_kbit after Optimization :" $OutputBitrate_kbit
Write-Host "-----DEBUGGING END-----"

Invoke-Expression "
$ffmpegPath -i '$inputVideo' -c:v $encoder -b:v $($OutputBitrate_kbit)k -vf fps=$OutputFPS -pass 1 -an -row-mt 1 -f null NUL
$ffmpegPath -i '$inputVideo' -c:v $encoder -b:v $($OutputBitrate_kbit)k -vf fps=$OutputFPS -pass 2 -c:a copy -row-mt 1 '$outputPath'
"
