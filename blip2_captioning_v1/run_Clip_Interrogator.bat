@echo off
REM Change the path below to the directory containing your virtual environment
set VENV_PATH=venv

REM Activate the virtual environment
call %VENV_PATH%\Scripts\activate.bat

REM Initialize options
set OPTIONS=

:menu
cls
echo.
echo Select Options:
echo    1. Start without any special options
echo    2. Start As Low VRAM
echo    3. Start As Gradio Live Share
echo    4. Start with both Low VRAM and Gradio Live Share

echo.
set /p choice=Enter your choice (1-4): 

if "%choice%"=="2" set OPTIONS=--lowvram
if "%choice%"=="3" set OPTIONS=--share
if "%choice%"=="4" set OPTIONS=--lowvram --share
if "%choice%"=="1" set OPTIONS=

REM Execute the Python script with selected options
python Clip_Interrogator.py %OPTIONS%

pause
