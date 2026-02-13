<#
.SYNOPSIS
    This script changes Monitor brightness based on system time using winddcutil.
.DESCRIPTION
    This script checks the current system time and performs one of two actions based on the time interval.
    - Between 08:00 and 17:00, it sets brightness to 100.
    - Between 17:00 and 18:30, it performs a linear interpolation between 100 and a standard brightness value (47).
    - Outside these intervals, it sets brightness to the standard value (47).
#>

# Define time ranges in minutes since midnight for better readability and flexibility
$startTimeActionA =  8 * 60 + 0   # 08:00
$endTimeActionA =   17 * 60 + 0   # 17:00
$startTimeActionB = 17 * 60 + 0   # 17:00
$endTimeActionB =   18 * 60 + 30  # 18:30

$standardBrightnessValue = 47
$winddcutil = "C:\Users\Morioh\AppData\Local\Morioh\MonitorManager\dependencies\winddcutil.exe"

# Get current time in minutes since midnight
$currentTimeInMinutes = [math]::Round((Get-Date).TimeOfDay.TotalMinutes)

# Make sure we don't interfere with Brightness 0 because of Monitor Manager Application (if in use)
$getMonitorBrightness = & $winddcutil getvcp 2 0x10
if (($getMonitorBrightness -ne "VCP 0x10 0") -and ($null -ne $getMonitorBrightness) -and ($getMonitorBrightness -ne "")) {
  # Action A: (At Morning)
  if ($currentTimeInMinutes -ge $startTimeActionA -and $currentTimeInMinutes -lt $endTimeActionA) {
    & $winddcutil setvcp 2 0x10 100
  }

  # Action B: (At Sunset)
  elseif ($currentTimeInMinutes -ge $startTimeActionB -and $currentTimeInMinutes -lt $endTimeActionB) {
    # Calculate normalized Action B time within the range (0 to 1)
    $t = ($currentTimeInMinutes - $startTimeActionB) / ($endTimeActionB - $startTimeActionB)

    # Linear interpolation between start and end brightness values
    $startBrightness = 100
    $endBrightness = $standardBrightnessValue
    $lerp = [math]::Round($startBrightness + $t * ($endBrightness - $startBrightness))

    & $winddcutil setvcp 2 0x10 $lerp
  }

  # Default action: set to standard brightness
  else {
    if ($getMonitorBrightness -ne "VCP 0x10 $standardBrightnessValue") {
      & $winddcutil setvcp 2 0x10 $standardBrightnessValue
    }
  }
}
