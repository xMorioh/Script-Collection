if "%~1"=="" goto SkriptInput
else goto DragDropInput

:DragDropInput
for %%A in (%*) do powershell -ex bypass -file ".\Convert_Video_to_gif.ps1" -inputVideo %%A -outputPath "%%~dpA%%~nA_reencoded.gif"
exit

:SkriptInput
powershell -ex bypass -file ".\Convert_Video_to_gif.ps1"
exit