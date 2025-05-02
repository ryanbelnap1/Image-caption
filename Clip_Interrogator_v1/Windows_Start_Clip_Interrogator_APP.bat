@echo off
REM Change the path below to the directory containing your virtual environment
set VENV_PATH=venv

REM Activate the virtual environment
call %VENV_PATH%\Scripts\activate.bat

:choose_option
REM Ask user to choose between normal and low VRAM mode
echo Choose an option:
echo 1. Normal mode
echo 2. Low VRAM mode
set /p CHOICE="Enter 1 or 2: "

REM Execute the Python script based on the user's choice
if "%CHOICE%"=="1" (
    python Clip_Interrogator.py
) else if "%CHOICE%"=="2" (
    python Clip_Interrogator.py --lowvram
) else (
    echo Invalid choice. Please enter 1 or 2.
    goto choose_option
)

pause