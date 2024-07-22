if "%~1"=="" goto SkriptInput
else goto DragDropInput

:DragDropInput
for %%A in (%*) do powershell -ex bypass -file ".\Reencode_Video_to_specific_filesize.ps1" -inputVideo %%A -outputPath "%%~dpA%%~nA_reencoded.mp4"
exit

:SkriptInput
powershell -ex bypass -file ".\Reencode_Video_to_specific_filesize.ps1"
exit