@echo off
set "SCRIPT_DIR=%~dp0"

echo Building app DUT-test
pyinstaller --name=DUT-test --onefile --windowed "%SCRIPT_DIR%main_GUI.py"

set "src_img_path=%SCRIPT_DIR%images\GUI"
set "dst_img_path=%SCRIPT_DIR%dist\images"

echo Downloading images from '%src_img_path%' -> '%dst_img_path%'
xcopy /E /I /Y "%src_img_path%" "%dst_img_path%"

pause
