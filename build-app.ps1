# Get the directory of the script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "Building app DUT-test"
pyinstaller --name=DUT-test --onefile --windowed "$ScriptDir\main_GUI.py"

$srcImgPath = Join-Path -Path $ScriptDir -ChildPath "images\GUI"
$dstImgPath = Join-Path -Path $ScriptDir -ChildPath "dist\images"

Write-Host "Downloading images from '$srcImgPath' -> '$dstImgPath'"
Copy-Item -Recurse -Force $srcImgPath $dstImgPath

Read-Host -Prompt "Press Enter to exit"
